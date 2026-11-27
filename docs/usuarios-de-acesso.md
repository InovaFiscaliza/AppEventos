# Usuários de acesso

O AppEventos recebe as requisições depois da autenticação de dois fatores no F5. Para identificar o usuário encaminhado pelo RF.Fusion, a aplicação lê `X-User-Name` e `X-User-Email`. Com os dois campos válidos, o AppEventos cadastra ou atualiza o fiscal pelo e-mail, sem distinção de maiúsculas e minúsculas. Acentos enviados em UTF-8 são decodificados na leitura dos cabeçalhos.

Os campos opcionais `X-User-Job-Title`, `X-User-Department`, `X-User-Location` e `X-User-Avatar-Url` atualizam os dados do fiscal. O avatar deve ser uma URL HTTPS sem credenciais, parâmetros ou fragmento.

A sessão do AppEventos guarda o fiscal e a seleção de perfil e evento. A identidade vem dos cabeçalhos de cada requisição. Se ela mudar ou estiver ausente, a seleção anterior é descartada. As permissões são consultadas no PostgreSQL, a partir dos vínculos do fiscal com eventos e dos papéis globais ativos.

A implantação confia na identidade encaminhada pelo RF.Fusion. O serviço deve ficar atrás do gateway autenticado, que sobrescreve os cabeçalhos `X-User-*` vindos do cliente. Acesso direto à porta do backend permite ao cliente informar a própria identidade.

Defina `SESSION_SECRET` no ambiente para preservar a seleção entre reinicializações.
