# Projeto do Banco de Dados

## Padrão de Nomenclatura

A nomenclatura segue [auditoria-schema.md](auditoria-schema.md): tabelas no singular e em caixa alta, prefixo `TB_` para entidades, `TL_` para logs e `BRIDGE_` para relacionamentos muitos para muitos. Colunas usam caixa alta e prefixos conforme seu conteúdo, como `ID_`, `CO_`, `SG_`, `NO_`, `DE_`, `TX_`, `DT_`, `IC_` e `VR_`.

Tabelas e colunas devem ter até 32 caracteres. Chaves estrangeiras preservam o nome da chave de origem, com sufixo de papel quando necessário. A referência é utilizada para nomenclatura; diferenças de modelagem permanecem propostas a confirmar, sem reprodução automática da estrutura legada.

## Tabela `TB_EVENTO`

Armazena os dados do evento apresentados na janela **Gerenciar Eventos**. Esta proposta utiliza tipos lógicos; os tipos específicos serão definidos após a escolha do banco de dados.

| Campo | Tipo lógico | Descrição |
| --- | --- | --- |
| `ID_EVENTO` | Inteiro | Chave primária do evento, gerada automaticamente. |
| `NO_EVENTO` | Texto curto | Nome do evento. Obrigatório, conforme indicado na tela. |
| `VR_LATITUDE` | Decimal | Latitude do local do evento, entre -90 e 90. |
| `VR_LONGITUDE` | Decimal | Longitude do local do evento, entre -180 e 180. |
| `CO_MUNICIPIO_IBGE` | Inteiro | Chave estrangeira para `TB_MUNICIPIO.CO_MUNICIPIO_IBGE`, identificando a cidade selecionada. |
| `DE_ACAO_FISCALIZACAO` | Texto curto | Ação de fiscalização informada para o evento. |
| `CO_PROCESSO_SEI` | Texto curto | Identificador do processo SEI. Deve ser textual para preservar zeros e formatação. |
| `ID_FISCAL_RESPONSAVEL` | Inteiro | Chave estrangeira para `TB_FISCAL.ID_FISCAL`, no papel de coordenador responsável. |
| `DT_INICIO_EVENTO` | Data | Início do período de realização. |
| `DT_FIM_EVENTO` | Data | Fim do período de realização. |
| `IC_TESTE_ETIQUETAGEM` | Booleano | Indica se o evento possui teste de etiquetagem: sim ou não. |
| `TX_OBSERVACAO` | Texto longo | Observações sobre o evento. |

### Localização

- A tela apresenta os seletores de UF e cidade, sendo a cidade habilitada após a seleção da UF.
- Nesta proposta, a UF é obtida de `TB_MUNICIPIO.SG_UF` pelo vínculo `CO_MUNICIPIO_IBGE`, sem duplicá-la na tabela `TB_EVENTO`.
- Deve ser confirmado se será permitido cadastrar um evento informando apenas a UF, sem cidade. Nesse caso, a modelagem da localização precisará contemplar essa possibilidade.

### Relacionamentos Exibidos na Tela

As listas permitem selecionar várias unidades executantes e vários fiscais. Esses vínculos não devem ser armazenados como listas de identificadores em uma coluna de `TB_EVENTO`.

| Relacionamento proposto | Cardinalidade | Dados do vínculo |
| --- | --- | --- |
| `BRIDGE_EVENTO_UNIDADE_EXECUTANTE` | Muitos para muitos entre eventos e unidades | `ID_EVENTO` e `SG_UNIDADE_EXECUTANTE`, referenciando as chaves de `TB_EVENTO` e `TB_UNIDADE_EXECUTANTE`. Cada par deve ser único. |
| `BRIDGE_EVENTO_FISCAL` | Muitos para muitos entre eventos e fiscais | `ID_EVENTO`, `ID_FISCAL` e os indicadores booleanos `IC_COORDENACAO`, `IC_ABORDAGEM` e `IC_MONITORACAO`. Cada par evento/fiscal deve ser único. |

Os indicadores de atuação pertencem à participação do fiscal no evento, não ao cadastro geral do fiscal. A tela permite marcar mais de um indicador para o mesmo participante.

### Regras de Consistência

- Quando ambas as datas forem informadas, `DT_FIM_EVENTO` não pode ser anterior a `DT_INICIO_EVENTO`.
- A cidade selecionada deve pertencer à UF escolhida.
- O coordenador responsável deve ser um fiscal participante do evento com o indicador `IC_COORDENACAO` marcado, conforme o filtro apresentado na tela.
- As referências a cidades, unidades e fiscais dependem das respectivas tabelas de cadastro, ainda a serem projetadas.

### Pontos a Confirmar

- Obrigatoriedade dos campos além do nome, limites de tamanho e valores padrão.
- Se a ação de fiscalização será texto livre ou uma referência a um cadastro próprio.
- Se o processo SEI deve ser único por evento ou pode ser compartilhado entre eventos.
- Se será obrigatório selecionar ao menos uma unidade executante, um fiscal ou um coordenador responsável.
- Precisão das coordenadas geográficas e possibilidade de informar apenas uma delas.

## Tabela `TB_ESTACAO`

Armazena as estações de monitoração cadastradas pela janela **Cadastro de Estações**, vinculadas ao evento selecionado. Os tipos abaixo são lógicos, seguindo o mesmo nível de definição de `TB_EVENTO`.

| Campo | Tipo lógico | Obrigatório | Descrição |
| --- | --- | --- | --- |
| `ID_ESTACAO` | Inteiro | Sim | Chave primária da estação, gerada automaticamente. |
| `ID_EVENTO` | Inteiro | Sim | Chave estrangeira para `TB_EVENTO.ID_EVENTO`. Corresponde ao seletor Evento. |
| `NO_ESTACAO` | Texto curto | Sim | Identificação da estação informada no formulário. |
| `DE_MODELO_EQUIPAMENTO` | Texto curto | Sim | Modelo do equipamento escolhido no seletor Modelo. |
| `DE_LOCAL` | Texto curto | Sim | Local de instalação ou operação da estação. |
| `VR_LATITUDE` | Decimal | Sim | Latitude da estação em graus decimais, entre -90 e 90. |
| `VR_LONGITUDE` | Decimal | Sim | Longitude da estação em graus decimais, entre -180 e 180. |

### Relacionamento com Evento

- Um evento pode possuir várias estações; cada registro de `TB_ESTACAO` pertence a um único evento.
- `ID_EVENTO` deve referenciar um evento existente.
- As coordenadas representam a posição da estação e não precisam ser iguais às coordenadas do evento.

### Chaves e Restrições

| Objeto | Nome | Definição |
| --- | --- | --- |
| Chave primária | `PK_TB_ESTACAO` | Coluna `ID_ESTACAO`. |
| Chave estrangeira | `FK_TB_ESTACAO_TB_EVENTO` | Coluna `ID_EVENTO` referenciando `TB_EVENTO.ID_EVENTO`. |
| Validação de latitude | `CC_ESTACAO_LATITUDE` | `VR_LATITUDE` entre -90 e 90. |
| Validação de longitude | `CC_ESTACAO_LONGITUDE` | `VR_LONGITUDE` entre -180 e 180. |

### Regras de Consistência

- Os campos indicados como obrigatórios na tela não podem receber valor nulo. Campos textuais também não podem conter apenas espaços.
- O cadastro da estação não deve alterar os dados do evento vinculado.
- A inclusão, edição e eventual exclusão da estação devem gerar auditoria, identificando registro, usuário, origem e valores anteriores e novos aplicáveis. A estrutura de auditoria será detalhada separadamente.

### Pontos a Confirmar

- Se a identificação da estação deve ser única dentro de cada evento.
- Se o modelo será armazenado como descrição ou como chave estrangeira para um cadastro próprio de modelos de equipamento.
- Se o campo Local e o botão `+` correspondem a um cadastro próprio de locais; nessa hipótese, substituir a descrição por uma referência ao cadastro a ser definido.
- Limites de tamanho dos campos textuais e precisão das coordenadas.
- Se uma mesma estação física poderá participar de vários eventos, exigindo separar seu cadastro permanente do vínculo com cada evento.
- Se haverá desativação da estação, em vez de exclusão, para preservar os vínculos com registros operacionais.
