#!/usr/bin/env bash
set -Eeuo pipefail

install -d -m 700 /var/lib/appeventos-pgadmin-ssh/etc/ssh
ssh-keygen -A -f /var/lib/appeventos-pgadmin-ssh
for key in /var/lib/appeventos-pgadmin-ssh/etc/ssh/ssh_host_*_key; do
    ln -sf "$key" "/etc/ssh/${key##*/}"
    ln -sf "${key}.pub" "/etc/ssh/${key##*/}.pub"
done
if [[ ! -e /etc/ssh/appeventos-password-initialized ]]; then
    printf 'root:%s\n' "${PGADMIN_SSH_PASSWORD:?PGADMIN_SSH_PASSWORD is required}" | chpasswd
    touch /etc/ssh/appeventos-password-initialized
fi
/usr/sbin/sshd -o Port=2222 -o PermitRootLogin=yes -o PasswordAuthentication=yes

exec /entrypoint.sh "$@"
