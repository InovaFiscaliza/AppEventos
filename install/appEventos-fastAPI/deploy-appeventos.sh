#!/usr/bin/env bash
set -Eeuo pipefail

if (($#)); then
    case "$1" in
        --help|-h) printf 'Usage: %s\n' "$0"; exit 0 ;;
        *) printf 'ERROR: Unknown option: %s\n' "$1" >&2; exit 2 ;;
    esac
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
container_name="appEventos-fastAPI"
image_name="appeventos-fastapi:debian12"
SSH_PASSWORD="${SSH_PASSWORD:-changeme}"
export SSH_PASSWORD

if [[ ! -d /appEventos ]]; then
    echo "ERROR: Create /appEventos on the Podman host before deploying." >&2
    exit 1
fi
if podman container exists "$container_name"; then
    echo "ERROR: appEventos-fastAPI already exists; no resources were replaced." >&2
    exit 1
fi
podman network inspect podman >/dev/null
podman build --pull=always -t "$image_name" "$script_dir"
podman volume exists appeventos-fastapi-ssh || podman volume create appeventos-fastapi-ssh >/dev/null
podman run -d \
    --name "$container_name" --hostname appeventos-fastapi \
    --restart unless-stopped --network podman \
    -p 9087:22 -p 9088:80 \
    -e SSH_PASSWORD -e "APP_MODULE=${APP_MODULE:-bootstrap:app}" \
    -v /appEventos:/appEventos:z \
    -v appeventos-fastapi-ssh:/var/lib/appeventos-ssh \
    "$image_name"

for ((attempt=1; attempt<=30; attempt++)); do
    if podman exec "$container_name" curl --fail --silent --max-time 2 \
        http://127.0.0.1/health >/dev/null && \
        podman exec "$container_name" /bin/bash -c 'exec 3<>/dev/tcp/127.0.0.1/22'; then
        printf 'appEventos-fastAPI ready. Web: http://127.0.0.1:9088/docs | SSH: port 9087\n'
        exit 0
    fi
    if [[ "$(podman inspect -f '{{.State.Status}}' "$container_name")" != running ]]; then
        break
    fi
    sleep 2
done
echo "ERROR: Runtime did not become ready. Inspect podman logs appEventos-fastAPI; resources were retained." >&2
exit 1
