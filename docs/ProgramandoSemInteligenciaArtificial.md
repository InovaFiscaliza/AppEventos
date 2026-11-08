# Programando o AppGrandesEventos sem IA

Este guia ajuda você a entender, alterar e testar o projeto por conta própria.
Não é necessário usar assistentes de IA: escreva as alterações no VS Code,
consulte a documentação das ferramentas e confira os resultados no navegador
e nos testes.

Este projeto é um esqueleto de aplicação. A página inicial apresenta uma tela
de login ainda sem autenticação. O campo **Evento** já oferece a opção
**+ Criar Evento**, que grava novos eventos no PostgreSQL. Os demais campos
continuam desabilitados.

## Preparar o ambiente

1. Abra a pasta do projeto no VS Code.
2. No painel **Extensões**, localize GitHub Copilot e GitHub Copilot Chat e,
   se estiverem instaladas, use a opção de desabilitar para este workspace.
   O editor, o terminal e os testes continuam disponíveis.
3. Use o Explorador do VS Code para abrir os arquivos e o terminal integrado
   para executar os comandos deste guia. Execute os comandos na raiz do
   projeto, a pasta que contém `pyproject.toml`.
4. Fora do VS Code, use o atalho **AppEventos - PowerShell** da Área de
   Trabalho: ele abre o PowerShell já na raiz do projeto.

O preenchimento de código do próprio editor e a documentação das linguagens
podem continuar sendo usados sem gerar código por IA.

## Como o projeto funciona

1. O navegador solicita um endereço, como `/`.
2. O FastAPI encontra a rota correspondente em `app/routers/`.
3. A rota escolhe um template em `app/templates/`.
4. O Jinja2 monta a página usando o template e a estrutura de `base.html`.
5. O navegador carrega o HTML, o CSS e o JavaScript em `app/static/`.

Em resumo: Python controla a resposta; HTML define o conteúdo; CSS define a
aparência; JavaScript adiciona comportamentos no navegador. Modificar uma tela
não cria automaticamente banco de dados, autenticação ou regras de negócio.

## Executar

Instale o Python 3.13 ou superior e o [uv](https://docs.astral.sh/uv/).

O cadastro de eventos precisa do PostgreSQL. Na primeira vez, crie o
contêiner com o Podman (os mesmos comandos estão em `comandosbasicos`):

```powershell
podman run -d --name appeventos-postgres -e POSTGRES_USER=appeventos -e POSTGRES_PASSWORD=appPasswd -e POSTGRES_DB=appeventos -p 5433:5432 -v appeventos-pgdata:/var/lib/postgresql/data --restart unless-stopped docker.io/library/postgres:16
```

A aplicação lê o endereço do banco na variável `DATABASE_URL`. Sem ela, usa o
endereço local acima (`app/services/db.py`). Para outro banco:

```powershell
$env:DATABASE_URL = "postgresql+psycopg://usuario:senha@servidor:porta/banco"
```

As tabelas são criadas pelas migrações em `local_server/migrations/`.

Na pasta do projeto, execute:

```powershell
uv sync
uv run uvicorn app.main:app --reload
```

O servidor é iniciado pelo `uvicorn` a partir da raiz, indicando o módulo
`app.main` e o objeto `app`. Não execute `python main.py` dentro de `app/`
nem `uv run main.py`: o arquivo apenas cria a aplicação e o Python não
encontra o pacote `app` fora da raiz.

Abra `http://127.0.0.1:8000`. Para parar o servidor, pressione `Ctrl+C`.
Para executar o teste da página inicial:

```powershell
uv run pytest
```

## Onde alterar

- `app/main.py`: cria a aplicação e registra as rotas e os arquivos estáticos.
- `app/routers/menu.py`: define a rota da página inicial.
- `app/routers/evento.py`: rotas do formulário e da gravação de eventos.
- `app/services/db.py`: conexão com o PostgreSQL (`engine` do SQLAlchemy).
- `app/templates/base.html`: estrutura compartilhada das páginas.
- `app/templates/menu.html`: conteúdo da página inicial.
- `app/templates/evento_novo.html`: formulário de criação de evento.
- `app/static/style.css`: estilos da interface.
- `app/static/app.js`: JavaScript da interface.
- `app/static/rf-fusion/`: local reservado aos recursos visuais originais.
- `tests/`: testes automatizados.
- `local_server/migrations/`: migrações SQL do banco.
- `pyproject.toml`: dependências e configuração do projeto.

Para criar uma nova tela, normalmente você altera:

1. `app/routers/<tela>.py` (novo): rota da tela.
2. `app/main.py`: registro do `router` com `app.include_router(...)`.
3. `app/templates/<tela>.html` (novo): conteúdo da tela.
4. `app/static/style.css` e a versão `?v=` em `base.html`, se houver estilo novo.
5. `app/static/app.js`, se houver comportamento no navegador.
6. `tests/test_<tela>.py` (novo): testes da rota.
7. `local_server/migrations/`, se a tela exigir nova estrutura no banco.

## Ciclo de trabalho

1. Escolha uma mudança pequena e descreva o resultado esperado. Por exemplo:
   "alterar o texto do título da tela de login".
2. Localize o texto no Explorador ou na busca do VS Code (`Ctrl+Shift+F`).
   Leia o trecho e identifique se a mudança pertence ao HTML, CSS, JavaScript
   ou Python.
3. Faça a alteração, salve o arquivo (`Ctrl+S`) e confira a página no
   navegador. Teste também uma janela estreita para verificar o uso no celular.
4. Execute `uv run pytest`. Se alguma verificação falhar, leia a mensagem e
   corrija a causa antes de seguir para a próxima mudança.
5. Revise os arquivos modificados no painel **Controle do Código-Fonte** do
   VS Code ou execute `git status --short` e `git diff`. Arquivos novos ainda
   não adicionados ao Git aparecem no status, mas não no `git diff` comum;
   abra-os no editor para revisá-los.

Comece alterando um texto existente em `app/templates/menu.html`, confira o
resultado em `/` e depois ajuste os testes correspondentes em
`tests/test_menu.py` quando o comportamento esperado mudar. Esse exercício
ajuda a conhecer o fluxo sem precisar criar um módulo inteiro.

## Criar uma tela

Uma tela reúne uma **rota** Python, um **template** HTML e, quando necessário,
regras de **CSS** e código **JavaScript**. O exemplo abaixo mostra como criar
uma página simples chamada "Exemplo". Ele é apenas um guia: não cria arquivos
automaticamente.

### 1. Criar a rota

Abra `app/routers/menu.py` e acrescente ao final do arquivo:

```python
@router.get("/exemplo", response_class=HTMLResponse)
async def exemplo(request: Request) -> HTMLResponse:
	"""Exibe a pagina de exemplo."""
	return templates.TemplateResponse(request=request, name="exemplo.html")
```

O endereço `/exemplo` identifica a página no navegador. O arquivo `menu.py` já
possui os imports, o `router` e `templates` usados pelo exemplo; não é necessário
copiá-los novamente. Ele também já está registrado em `app/main.py`. Ao criar
um arquivo de rotas separado, importe-o e registre seu `router` em
`app/main.py` com `app.include_router(...)`.

### 2. Criar o template

Crie `app/templates/exemplo.html` com este conteúdo:

```html
{% extends "base.html" %}

{% block title %}Exemplo - AppEventos{% endblock %}

{% block content %}
<main class="pagina-exemplo">
	<h1>Minha tela</h1>
	<p>Conteúdo da página.</p>
</main>
{% endblock %}
```

`extends` aproveita a estrutura de `base.html`; os blocos definem o título e o
conteúdo da página. Os trechos `{% ... %}` e `{{ ... }}` são comandos do
Jinja2 e devem ser preservados durante a edição visual.

### 3. Ajustar aparência e comportamento

Acrescente ao final de `app/static/style.css` as regras da página, por exemplo:

```css
.pagina-exemplo {
	max-width: 800px;
	margin: 2rem auto;
	padding: 1rem;
}
```

Depois de alterar o CSS, incremente o número após `?v=` no endereço de
`style.css` em `app/templates/base.html`, para que o navegador receba a versão
atualizada. Comportamentos interativos podem ser acrescentados em
`app/static/app.js`.

O Pinegrow pode ajudar na edição visual de HTML e CSS, mas pode não montar
templates Jinja2 herdados. Confira sempre a página pelo FastAPI. O inspetor do
navegador, acessível com `F12`, permite experimentar estilos; suas alterações
são temporárias e precisam ser reproduzidas no arquivo CSS.

### 4. Visualizar

Na pasta do projeto, inicie o servidor:

```powershell
uv run uvicorn app.main:app --reload
```

Abra `http://127.0.0.1:8000/exemplo` e atualize o navegador depois de alterar o
template ou o CSS. A opção `--reload` reinicia o servidor após alterações no
Python. Se já houver um servidor nessa porta, use a porta dele ou escolha outra
com `--port 8001`.

### 5. Testar

Crie `tests/test_exemplo.py` para verificar a nova rota:

```python
from fastapi.testclient import TestClient

from app.main import app


def test_exemplo_exibe_pagina() -> None:
	response = TestClient(app).get("/exemplo")

	assert response.status_code == 200
	assert "Minha tela" in response.text
```

Execute `uv run pytest` e confira a página também em uma tela de celular.
Quando a página tiver formulários ou dados, acrescente testes para seus
comportamentos e erros. Para uma nova dependência, use `uv add nome`.

## Exemplo real: Criar Evento

O cadastro de eventos segue os mesmos passos de uma tela, acrescentando um
formulário e a gravação no banco.

### Dependências

```powershell
uv add sqlalchemy "psycopg[binary]" python-multipart
```

`sqlalchemy` executa os comandos SQL, `psycopg` conecta ao PostgreSQL e
`python-multipart` permite ao FastAPI ler formulários HTML.

### Fluxo

1. Em `menu.html`, o campo **Evento** tem a opção `+ Criar Evento` com o
   atributo `data-url`, gerado por `url_for('novo_evento')`.
2. Em `app.js`, o evento `change` do campo lê o `data-url` da opção escolhida
   e leva o navegador até `/eventos/novo`.
3. Em `evento.py`, a rota `GET /eventos/novo` exibe `evento_novo.html`.
4. O formulário envia `nome`, `data_inicio` e `data_fim` por `POST` para a
   mesma rota, que:
   - remove espaços do nome e converte as datas; campo de data vazio vira
     `None` (a função `converter_data`);
   - valida o nome obrigatório e se o fim não é anterior ao início. Em caso de
     erro, devolve o formulário com status 400, a mensagem e os valores
     digitados;
   - grava com `INSERT INTO TB_EVENTO` usando `text()` e parâmetros nomeados
     (`:nome`), nunca concatenando valores no SQL;
   - redireciona para `/` com status 303.
5. `style.css` ganhou `.form-erro`, o link de `.form-actions` e o botão
   habilitado; a versão do CSS em `base.html` passou para `v=5`.

As datas chegam como texto (`str`) porque um campo `date` vazio envia `""`,
que o FastAPI rejeitaria com erro 422 se o parâmetro fosse do tipo `date`.

### Testes sem banco

`tests/test_evento.py` substitui o `engine` real por uma classe falsa com
`monkeypatch.setattr(evento, "engine", ...)`. Assim os testes conferem os
valores enviados ao banco sem precisar do PostgreSQL em execução. Os testes
cobrem a opção no menu, o formulário, a gravação válida e os dados inválidos.

### Pendências

- Auditoria da criação: falta uma nova migração (`0002_...sql`) com a tabela
  de log de eventos; não edite a `0001_novobd.sql`.
- O campo **Evento** ainda não lista os eventos gravados; isso exige um
  `SELECT ID_EVENTO, NO_EVENTO FROM TB_EVENTO` na rota `menu`.

## Entender e corrigir erros

- **A página não abre:** confira se o servidor está em execução, se o endereço
  e a porta estão corretos e leia as mensagens no terminal do servidor.
- **`ModuleNotFoundError: No module named 'app'`:** o servidor foi iniciado
  fora da raiz. Volte com `cd ..` e use `uv run uvicorn app.main:app --reload`.
- **`Failed to spawn: main.py`:** `uv run` recebeu um arquivo inexistente na
  raiz. Use o comando do `uvicorn` acima.
- **Erro ao salvar evento:** confira se o contêiner do PostgreSQL está ativo
  (`podman ps`), se `DATABASE_URL` aponta para ele e se as migrações foram
  aplicadas.
- **A rota retorna 404:** verifique o endereço no navegador, o `@router.get`
  e se o `router` do arquivo foi registrado em `app/main.py`.
- **O template não é encontrado:** confira o nome passado a
  `TemplateResponse` e o caminho e a grafia do arquivo em `app/templates/`.
- **O estilo não mudou:** salve o CSS, incremente sua versão em `base.html`
  e atualize a página. No inspetor (`F12`), confira se a regra é aplicada ao
  elemento e se outra regra a substitui.
- **Um teste falhou:** leia o nome do teste, a primeira mensagem de erro e a
  linha indicada. Execute apenas esse arquivo, por exemplo
  `uv run pytest tests/test_menu.py -q`, corrija o problema e execute
  `uv run pytest` novamente.

Faça uma alteração por vez e repita a verificação. Evite apagar dados ou
arquivos para tentar corrigir erros sem antes entender suas consequências.

## Antes de trabalhar com dados

O login atual é apenas visual. Não habilite o envio de senhas como se houvesse
autenticação pronta. Ao implementar acesso, consulte a documentação de
segurança do FastAPI, use conexões protegidas e armazenamento seguro de senhas,
sem registrar senhas ou informações sensíveis em logs ou testes.

Para operações de inclusão, edição e exclusão, defina validação e
tratamento de erros no backend e planeje a auditoria das alterações, como no
cadastro de eventos. Mudanças
no banco devem preservar os dados existentes e seguir as orientações de
migração do projeto; não execute o esquema legado de implantação para atualizar
um banco existente.

## Fontes de consulta

- [Tutorial de Python](https://docs.python.org/pt-br/3/tutorial/): linguagem,
  funções, módulos e tratamento de erros.
- [Documentação do FastAPI](https://fastapi.tiangolo.com/): rotas, respostas,
  formulários, templates e segurança.
- [Documentação do Jinja2](https://jinja.palletsprojects.com/): templates,
  herança e variáveis.
- [MDN Web Docs](https://developer.mozilla.org/pt-BR/): HTML, CSS, JavaScript e
  ferramentas do navegador.
- [Documentação do pytest](https://docs.pytest.org/): criação e execução de
  testes.
- [Documentação do Git](https://git-scm.com/doc): histórico e revisão de
  alterações.

- [Documentação do SQLAlchemy](https://docs.sqlalchemy.org/): conexões e
  execução de SQL com `text()`.

Os recursos RF.Fusion não foram fornecidos. A conexão com PostgreSQL é usada
apenas no cadastro de eventos; autenticação e funcionamento offline não estão
implementados.
