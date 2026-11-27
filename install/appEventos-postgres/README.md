# PostgreSQL e pgAdmin do appEventos

Instalação própria do appEventos. Usa o SQL e os dados de referência em
`local_server/postgres/`, no repositório AppEventos.
Cria PostgreSQL 17 Alpine com SSH e pgAdmin em containers separados no pod
`appeventos-postgres-pod`.

| Porta do host | Porta do pod | Serviço |
|---|---|---|
| 2228 | 22 | SSH do PostgreSQL |
| 9085 | 5432 | PostgreSQL |
| 9086 | 8080 | pgAdmin HTTP |

O pod usa `--network podman --ip 10.88.0.36`. O SSH do pgAdmin não é publicado.
No primeiro startup com um volume vazio, o PostgreSQL cria `DB_EVENTOS`,
inicializa `SC_EVENTOS` e carrega `TB_MUNICIPIO` do CSV incluído na imagem.
A carga usa os 5.571 registros das 27 UFs da API de Localidades do IBGE,
consultada em 26/11/2026, e roda sem acesso à internet.

## Executar

No host proprietário do Podman, prepare o diretório `/appEventos` com acesso
para o operador e confirme que a rede, o IP e as portas estão disponíveis.
Entre nesta pasta e execute:

```bash
./linux/deploy-postgres.sh
```

As imagens e seus entrypoints ficam em `linux/postgres/` e `linux/pgadmin/`.
O deploy monta `/appEventos` do host em `/appEventos` do container PostgreSQL
com `-v /appEventos:/appEventos:z`. O sufixo `:z` permite compartilhamento com
outros containers em hosts com SELinux. Esse diretório contém os arquivos do
appEventos; os dados do PostgreSQL permanecem no volume nomeado separado.
Não é necessário montar o repositório RF.Fusion nem configurar `.env/runtime.env`.

Os containers são `appeventos-postgres` e `appeventos-pgadmin`. Os volumes
`appeventos-postgres-data`, `appeventos-postgres-ssh`, `appeventos-pgadmin-data`
e `appeventos-pgadmin-ssh` persistem dados, configuração e chaves SSH no
armazenamento do Podman do operador. O instalador recusa pods ou containers
existentes e não remove volumes. Falhas preservam os recursos para diagnóstico.
As credenciais iniciais do banco e do pgAdmin só se aplicam a volumes vazios.
O SSH inicia com `root/changeme`, tanto no PostgreSQL quanto no SSH interno do
pgAdmin. `SSH_PASSWORD` e `PGADMIN_SSH_PASSWORD` permitem sobrescrever essas
senhas no deploy. O banco inicia com `postgres/changeme` e a interface pgAdmin
com `admin@anatel.gov.br/changeme`. Para outros valores, forneça
`POSTGRES_PASSWORD`, `PGADMIN_DEFAULT_EMAIL` e `PGADMIN_DEFAULT_PASSWORD` pelo
ambiente antes do deploy. Não há necessidade de exportar variáveis para usar
os valores iniciais. Esses valores só inicializam volumes vazios e não alteram
senhas de instalações existentes.

Abra `http://IP_DA_VM:9086` e cadastre no pgAdmin o servidor `127.0.0.1`, porta
`5432`, banco de manutenção `postgres` e usuário `postgres`. O SSH do PostgreSQL
usa `root` na porta `2228`. O pgAdmin usa HTTP; restrinja o acesso na rede ou
configure HTTPS antes de exposição externa. As portas seguem a publicação do
Podman nas interfaces do host.

Para verificar a instalação:

```bash
podman ps -a --pod --filter pod=appeventos-postgres-pod
podman logs appeventos-postgres
podman logs appeventos-pgadmin
podman exec -u postgres appeventos-postgres psql -X -U postgres -d template1 -c '\l'
```

## Esquema e carga em volumes existentes

O PostgreSQL executa a inicialização automática apenas em volumes vazios.
Para aplicar o SQL consolidado em um volume que já existe, use os arquivos
do repositório montado no container. A carga preserva registros com códigos
IBGE já cadastrados.

```bash
podman exec -u postgres -w /appEventos/AppEventos/local_server/postgres \
  appeventos-postgres psql -X -U postgres -d postgres -f 0001_novobd.sql
```
