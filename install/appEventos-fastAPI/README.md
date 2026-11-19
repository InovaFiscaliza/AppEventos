# Container appEventos FastAPI

Pasta autocontida para transferência ao repositório do appEventos. Segue o
[contrato local](ARCHITECTURE.md) e o [ambiente de execução](ENVIRONMENT.md).

O deploy constrói uma imagem Debian 12 e instala Python 3.11, ambiente virtual,
FastAPI, Uvicorn com extras padrão, suporte a formulários e templates, NGINX e
SSH. Não depende dos arquivos ou da configuração do RF.Fusion.

| Recurso | Configuração |
|---|---|
| Container | `appEventos-fastAPI` |
| Imagem | `appeventos-fastapi:debian12` |
| SSH | `9087:22` |
| HTTP via NGINX | `9088:80` |
| Uvicorn interno | `127.0.0.1:8000` |
| Rede | `podman`, IP atribuído automaticamente |
| Volume compartilhado | `/appEventos:/appEventos:z` |
| Chaves SSH | Volume `appeventos-fastapi-ssh` |

## Deploy

No host proprietário do Podman, prepare `/appEventos` com acesso para o operador
e confirme a disponibilidade das portas e da rede `podman`. Entre nesta pasta:

```bash
./deploy-appeventos.sh
```

O instalador recusa substituir um container existente. O build instala as
dependências da imagem; não instala pacotes no host nem modifica o conteúdo do
volume compartilhado. O diretório é montado com `:z` para compartilhamento
SELinux com o container PostgreSQL do appEventos. Os arquivos da aplicação
permanecem no host; não são servidos diretamente pelo NGINX.

## Acessos

- Documentação interativa: `http://IP_DA_VM:9088/docs`.
- Verificação HTTP: `http://IP_DA_VM:9088/health`.
- SSH: `ssh root@IP_DA_VM -p 9087`.
- Logs: `podman logs -f appEventos-fastAPI`.

A aplicação inicial da imagem responde sem banco de dados. Para executar a
API própria, coloque seu código em `/appEventos` e defina `APP_MODULE=main:app`
no ambiente antes do deploy, para importar `app` de `/appEventos/main.py`.
Mantenha um endpoint `/health` com HTTP 200, usado pelo deploy e pelo healthcheck.
Adicione dependências da aplicação a `requirements.txt` e reconstrua a imagem.
O Python do runtime é `/opt/appeventos/venv/bin/python`.

O container reinicia com `unless-stopped`. A saída de Uvicorn, NGINX ou SSH
encerra o runtime e seus demais processos. Alterações no código montado exigem
reinício; não há recarga automática. Alterações nas dependências, NGINX ou
entrypoint exigem reconstruir a imagem e recriar o container. O deploy preserva
recursos em caso de falha para diagnóstico.

A credencial SSH inicial é `root/changeme`. Para outra senha, forneça
`SSH_PASSWORD` pelo ambiente antes do deploy.
A senha SSH é inicializada na criação do container; alterações feitas por SSH
persistem em reinícios, mas uma recriação usa a senha fornecida no novo deploy.
As chaves de host persistem no volume nomeado. HTTP e a documentação inicial
são publicados sem autenticação; configure acesso e HTTPS conforme o ambiente.
