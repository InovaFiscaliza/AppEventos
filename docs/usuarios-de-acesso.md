# Usuários de acesso

## Login do RF.Fusion pelo navegador

A página inicial abre como **Anônimo**. Ao selecionar **Login**, o AppEventos redireciona para `https://fiscalizacao.anatel.gov.br/rffusion/api/users/login_eventos`. A variável `URL_ACESSO_ANATEL` permite alterar esse destino.

Depois de autenticar o usuário, o RF.Fusion envia um formulário no navegador com `method="post"` e `action="http://rhfisnsdsin01:9088/api/usuarios/login-evento"`. O formato é `application/x-www-form-urlencoded`. Envie `NA_USER_EMAIL` e `NA_USER_NAME`. Os campos `NA_DEPARTMENT`, `NA_JOB_TITLE` e `NA_LOCATION` são opcionais.

O AppEventos insere os campos na tabela `SC_EVENTOS.TB_FISCAL` se o e-mail ainda não existir. A comparação de e-mail ignora maiúsculas e minúsculas. O POST devolve `303` para `/` e o nome recebido aparece no cabeçalho por até oito horas, ou até selecionar **Sair**. O formulário alimenta o cadastro básico do protótipo e a exibição do nome. A sessão autenticada usa o perfil fornecido pelo proxy.

## Perfil fornecido pelo proxy

O proxy corporativo autentica o usuário e encaminha o perfil ao AppEventos. A aplicação lê `x-user-profile` nas rotas `/` e `/entrar/anatel`. O JSON inclui `NA_USER_EMAIL`, `NA_USER_NAME`, `NA_DEPARTMENT`, `NA_JOB_TITLE` e `NA_LOCATION`.

Configure `ANATEL_PROXY_TOKEN` com um segredo aleatório compartilhado entre FastAPI e proxy. O proxy deve descartar os cabeçalhos `x-user-profile` e `x-appeventos-proxy-token` enviados pelo navegador. Em requisições autenticadas, ele deve preencher o primeiro com o perfil verificado e o segundo com o token. Encaminhe os cabeçalhos por uma conexão protegida com o backend. Remova o cookie corporativo da requisição ao FastAPI e preserve o cookie da sessão do AppEventos.

Quando recebe o perfil autenticado, o AppEventos localiza o registro pelo e-mail, sem distinção entre maiúsculas e minúsculas, e atualiza o perfil e a data de atualização quando algum campo muda. Cadastros antigos sem e-mail não são associados automaticamente ao perfil corporativo.

**Sair** encerra a sessão do AppEventos. Para voltar a entrar no mesmo navegador, use **Login**. A sessão usa a variável de ambiente `SESSION_SECRET`. Sem ela, a chave é gerada a cada início do servidor e as sessões abertas expiram.
