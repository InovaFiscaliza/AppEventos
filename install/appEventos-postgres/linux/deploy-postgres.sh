#!/usr/bin/env bash
set -Eeuo pipefail

if (($#)); then
    case "$1" in
        --help|-h) printf 'Usage: %s\n' "$0"; exit 0 ;;
        *) printf 'ERROR: Unknown option: %s\n' "$1" >&2; exit 2 ;;
    esac
fi

projectRoot="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
postgresSources="$(cd "${projectRoot}/../../../local_server/postgres" && pwd)"
if [[ ! -d /appEventos ]]; then
    echo "ERROR: Create /appEventos on the Podman host before deploying." >&2
    exit 1
fi

POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-changeme}"
SSH_PASSWORD="${SSH_PASSWORD:-changeme}"
PGADMIN_DEFAULT_PASSWORD="${PGADMIN_DEFAULT_PASSWORD:-changeme}"
PGADMIN_SSH_PASSWORD="${PGADMIN_SSH_PASSWORD:-changeme}"
PGADMIN_DEFAULT_EMAIL="${PGADMIN_DEFAULT_EMAIL:-admin@anatel.gov.br}"
export POSTGRES_PASSWORD SSH_PASSWORD PGADMIN_DEFAULT_EMAIL PGADMIN_DEFAULT_PASSWORD PGADMIN_SSH_PASSWORD

podName="appeventos-postgres-pod"
containerName="appeventos-postgres"
pgadminContainer="appeventos-pgadmin"
imageName="appeventos-postgres:17-alpine"
pgadminImage="appeventos-pgadmin:9.18"
infraImage="registry.k8s.io/pause:3.10"

if podman pod exists "$podName" || podman container exists "$containerName" || \
    podman container exists "$pgadminContainer" || podman container exists appeventos-postgres-infra; then
    echo "ERROR: appEventos pod or containers already exist; no resources were replaced." >&2
    exit 1
fi

podmanInfo="$(podman info --format '{{.Host.Security.Rootless}} {{.Host.CgroupsVersion}} {{range .Host.CgroupControllers}}{{.}} {{end}}')"
read -r rootless cgroupVersion controllers <<< "$podmanInfo"
if [[ "$cgroupVersion" == v1 ]]; then
    if [[ "$rootless" == true ]]; then controllers=""; else controllers="cpu memory pids"; fi
fi
resourceArgs=()
if [[ " ${controllers} " == *" cpu "* ]]; then resourceArgs+=(--cpus=1); else echo "WARNING: CPU limit unavailable."; fi
if [[ " ${controllers} " == *" memory "* ]]; then resourceArgs+=(--memory=2g --memory-swap=3g); else echo "WARNING: Memory limit unavailable."; fi
if [[ " ${controllers} " == *" pids "* ]]; then resourceArgs+=(--pids-limit=1024); else echo "WARNING: PID limit unavailable."; fi

podman network inspect podman >/dev/null
podman build --pull=always --build-context "appeventos_sql=$postgresSources" \
    -t "$imageName" "${projectRoot}/postgres"
podman build --pull=always -t "$pgadminImage" "${projectRoot}/pgadmin"
podman pull "$infraImage"
for volumeName in appeventos-postgres-data appeventos-postgres-ssh appeventos-pgadmin-data appeventos-pgadmin-ssh; do
    podman volume exists "$volumeName" || podman volume create "$volumeName" >/dev/null
done

podman pod create --name "$podName" \
    --infra-name appeventos-postgres-infra \
    --infra-image "$infraImage" \
    --infra-command /pause \
    --hostname appeventos-postgres \
    --network podman --ip 10.88.0.36 \
    -p 2228:22 -p 9085:5432 -p 9086:8080 >/dev/null
podman run -d \
    --name "$containerName" --pod "$podName" \
    "${resourceArgs[@]}" \
    -e POSTGRES_DB=postgres -e POSTGRES_PASSWORD -e SSH_PASSWORD \
    -v /appEventos:/appEventos:z \
    -v appeventos-postgres-data:/var/lib/postgresql/data \
    -v appeventos-postgres-ssh:/var/lib/appeventos-ssh \
    "$imageName"

ready=false
for ((attempt=1; attempt<=60; attempt++)); do
    if podman exec "$containerName" pg_isready -h 127.0.0.1 -U postgres -d postgres >/dev/null 2>&1; then
        ready=true
        break
    fi
    if [[ "$(podman inspect -f '{{.State.Status}}' "$containerName")" != running ]]; then
        echo "ERROR: PostgreSQL container stopped; inspect its logs. Resources were retained." >&2
        exit 1
    fi
    sleep 2
done
if [[ "$ready" != true ]]; then
    echo "ERROR: PostgreSQL did not become ready; inspect its logs. Resources were retained." >&2
    exit 1
fi

podman run -d \
    --name "$pgadminContainer" --pod "$podName" \
    -e PGADMIN_DEFAULT_EMAIL -e PGADMIN_DEFAULT_PASSWORD -e PGADMIN_SSH_PASSWORD \
    -e PGADMIN_LISTEN_PORT=8080 \
    -v appeventos-pgadmin-data:/var/lib/pgadmin:U \
    -v appeventos-pgadmin-ssh:/var/lib/appeventos-pgadmin-ssh \
    "$pgadminImage"
printf 'appEventos pod created. PostgreSQL is ready; check pgAdmin logs before connecting.\n'
