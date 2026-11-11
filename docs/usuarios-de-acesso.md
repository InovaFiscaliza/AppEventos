# Usuários de acesso

## Cadastrar Usuário

| Campo   | Valor               |
|---------|---------------------|
| Usuário | `Cadastrar Usuário` |
| Senha   | `5000`              |

Uso:

1. Na tela inicial (`/`), escolha **Cadastrar Usuário** no campo *Usuário*.
2. Informe a senha `5000` e clique em **Entrar**.
3. A tela **Início › Cadastro › Novo Usuário** (`/usuarios`) é aberta para incluir usuários.
4. **Sair** encerra a sessão e volta ao login.

Observações:

- O usuário **Cadastrar Usuário** só existe enquanto não houver nenhum usuário cadastrado. Depois do primeiro cadastro, ele some do login e a senha `5000` deixa de ser aceita. A sessão já aberta continua válida até **Sair**.
- Sem essa sessão, `/usuarios` redireciona para o login.
- A senha não fica em texto no código: `app/config.py` guarda só o SHA-256 dela (`SENHA_CADASTRO_SHA256`).
- Para trocar a senha, gere o novo hash com `uv run python -c "import hashlib; print(hashlib.sha256(b'NOVA').hexdigest())"`, atualize a constante e este documento.
- A sessão usa a variável de ambiente `SESSION_SECRET`. Sem ela, a chave é gerada a cada início do servidor e as sessões abertas expiram.
- Os usuários são gravados em `TB_FISCAL` com nome, unidade executante e papéis permitidos (`IC_COORDENACAO`, `IC_ABORDAGEM`, `IC_MONITORACAO`: 0 - Não; 1 - Sim), criados pela migração `local_server/migrations/0002_papeis_fiscal.sql`.
- A unidade é escolhida entre as de `TB_UNIDADE_EXECUTANTE`, populada pela migração 0002 com as 11 Gerências Regionais (GR01 a GR11) e as 16 Unidades Operacionais.
