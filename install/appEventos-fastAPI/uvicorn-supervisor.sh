#!/usr/bin/env bash
set -Eeuo pipefail

state_dir=/run/appeventos-fastapi
mkdir -p "$state_dir"

worker_pid=
restart_requested=0

cleanup() {
    rm -f "$state_dir/uvicorn.pids" "$state_dir/uvicorn.pids.tmp"
    if [[ -n "$worker_pid" ]]; then
        kill -TERM "$worker_pid" 2>/dev/null || true
        wait "$worker_pid" 2>/dev/null || true
    fi
}

request_restart() {
    restart_requested=1
    if [[ -n "$worker_pid" ]]; then
        kill -TERM "$worker_pid" 2>/dev/null || true
    fi
}

trap cleanup EXIT
trap 'exit 0' TERM INT
trap request_restart USR1

while true; do
    restart_requested=0
    "$@" &
    worker_pid=$!
    printf '%s %s\n' "$BASHPID" "$worker_pid" > "$state_dir/uvicorn.pids.tmp"
    mv -f "$state_dir/uvicorn.pids.tmp" "$state_dir/uvicorn.pids"

    status=0
    wait "$worker_pid" || status=$?
    if (( ! restart_requested )); then
        worker_pid=
        exit "$status"
    fi

    # O sinal interrompe wait antes de o Uvicorn concluir o desligamento.
    wait "$worker_pid" 2>/dev/null || true
    worker_pid=
done
