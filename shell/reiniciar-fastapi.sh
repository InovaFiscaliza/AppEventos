#!/usr/bin/env bash
set -Eeuo pipefail

state_dir=/run/appeventos-fastapi
pid_file="$state_dir/uvicorn.pids"

if [[ ! -r "$pid_file" ]]; then
    entrypoint=/usr/local/bin/appeventos-entrypoint.sh
    if [[ -r "$entrypoint" ]] && ! grep -q 'uvicorn-supervisor.sh' "$entrypoint"; then
        printf 'O contêiner usa o entrypoint antigo. No host do Podman, instale o entrypoint atualizado e reinicie o contêiner uma vez.\n' >&2
    else
        printf 'O supervisor do FastAPI ainda não está ativo. Execute dentro do contêiner após ele iniciar com o entrypoint atualizado.\n' >&2
    fi
    exit 1
fi

exec 9>"$state_dir/restart.lock"
if ! flock -n 9; then
    printf 'Já há um reinício do FastAPI em andamento.\n' >&2
    exit 1
fi

read -r supervisor_pid previous_pid < "$pid_file"
if [[ ! "$supervisor_pid" =~ ^[1-9][0-9]*$ || ! "$previous_pid" =~ ^[1-9][0-9]*$ ]] ||
    ! kill -USR1 "$supervisor_pid"; then
    printf 'Não foi possível sinalizar o supervisor do FastAPI.\n' >&2
    exit 1
fi

deadline=$((SECONDS + 30))
while (( SECONDS < deadline )); do
    if [[ -r "$pid_file" ]] &&
        read -r current_supervisor current_pid < "$pid_file" &&
        [[ "$current_supervisor" == "$supervisor_pid" && "$current_pid" != "$previous_pid" ]] &&
        curl -fsS --max-time 1 http://127.0.0.1/health >/dev/null 2>&1; then
        printf 'FastAPI reiniciado. PID anterior: %s. PID atual: %s. /health OK.\n' \
            "$previous_pid" "$current_pid"
        exit 0
    fi
    sleep 0.25
done

printf 'O FastAPI não confirmou o reinício em 30 segundos. Confira os logs do contêiner.\n' >&2
exit 1
