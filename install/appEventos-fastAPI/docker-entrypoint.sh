#!/usr/bin/env bash
set -Eeuo pipefail

install -d -m 700 /var/lib/appeventos-ssh/etc/ssh
ssh-keygen -A -f /var/lib/appeventos-ssh
for key in /var/lib/appeventos-ssh/etc/ssh/ssh_host_*_key; do
    ln -sf "$key" "/etc/ssh/${key##*/}"
    ln -sf "${key}.pub" "/etc/ssh/${key##*/}.pub"
done
if [[ ! -e /etc/ssh/appeventos-password-initialized ]]; then
    printf 'root:%s\n' "${SSH_PASSWORD:?SSH_PASSWORD is required}" | chpasswd
    touch /etc/ssh/appeventos-password-initialized
fi
unset SSH_PASSWORD
nginx -t
/usr/sbin/sshd -t

service_pids=()
cleanup() {
    trap - EXIT
    if ((${#service_pids[@]})); then
        kill -TERM "${service_pids[@]}" 2>/dev/null || true
        wait "${service_pids[@]}" 2>/dev/null || true
    fi
}
trap cleanup EXIT
trap 'exit 0' TERM INT

uvicorn "${APP_MODULE:-bootstrap:app}" --app-dir /appEventos \
    --host 127.0.0.1 --port 8000 --proxy-headers --forwarded-allow-ips 127.0.0.1 &
service_pids+=("$!")
nginx -g 'daemon off;' &
service_pids+=("$!")
/usr/sbin/sshd -D -e -o Port=22 -o PermitRootLogin=yes -o PasswordAuthentication=yes &
service_pids+=("$!")

service_status=0
wait -n "${service_pids[@]}" || service_status=$?
if ((service_status == 0)); then service_status=1; fi
printf 'ERROR: A runtime service exited; stopping appEventos-fastAPI.\n' >&2
exit "$service_status"
