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
/usr/sbin/sshd -o Port=22 -o PermitRootLogin=yes -o PasswordAuthentication=yes

exec /usr/local/bin/docker-entrypoint.sh "$@"
