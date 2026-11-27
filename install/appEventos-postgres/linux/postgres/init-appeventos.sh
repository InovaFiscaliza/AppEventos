#!/usr/bin/env bash
# O entrypoint oficial do PostgreSQL carrega este script no primeiro startup.
(
    cd /opt/appeventos/postgres || exit 1
    docker_process_sql --file 0001_novobd.sql
)
