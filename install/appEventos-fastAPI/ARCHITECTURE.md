# Contrato do container appEventos FastAPI

Esta pasta pertence ao appEventos e fica temporariamente neste repositório.
Deve continuar autocontida para transferência ao repositório próprio, sem
dependências de configuração, serviços ou entrypoints do RF.Fusion.

O container `appEventos-fastAPI` usa Debian 12, Python 3.11 em ambiente virtual,
FastAPI com Uvicorn, NGINX e SSH. O fluxo HTTP é
`cliente -> host:9088 -> NGINX:80 -> Uvicorn:127.0.0.1:8000`.
O SSH é publicado em `9087:22`. A rede é `podman`, com IP atribuído pelo Podman.
O diretório `/appEventos` do host é montado em `/appEventos` com `:z`.

O código da aplicação pertence ao volume. `APP_MODULE` seleciona o import ASGI;
por padrão, uma aplicação mínima da imagem disponibiliza `/`, `/health` e
`/docs`, sem criar arquivos no volume ou conectar ao banco. Dependências Python
são instaladas durante o build e pertencem à imagem, fora do volume compartilhado.

Tini administra o processo inicial. O entrypoint supervisiona Uvicorn, NGINX e
SSH; a saída de qualquer um encerra o container com falha. Os logs HTTP e da
aplicação vão para stdout/stderr. As chaves de host SSH ficam em volume próprio.
A credencial inicial SSH é `root/changeme`; `SSH_PASSWORD` permite sobrescrever
a senha no deploy. O deploy recusa
substituir um container existente e não remove dados.
