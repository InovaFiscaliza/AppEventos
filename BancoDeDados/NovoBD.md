# Projeto do Banco de Dados

## Referência Normativa

Os padrões de modelagem deste projeto são os definidos em [PadroesAnatelModelagem.md](PadroesAnatelModelagem.md). Esse documento prevalece sobre [auditoria-schema.md](auditoria-schema.md), que permanece como referência auxiliar de correspondência com a estrutura anterior, não como norma.

### Nomenclatura e Regras Gerais

- Nomes em português, no singular, em caixa alta e sem acentos. Tabelas e colunas devem ter até 32 caracteres.
- Classes transacionais: `TB_` para tabelas genéricas, inclusive associativas; `TH_` para históricos; `TL_` para registros de operações; `TT_` para tabelas temporárias.
- Colunas classificadas conforme o conteúdo, com prefixos como `ID_`, `CO_`, `SG_`, `NO_`, `DE_`, `TX_`, `DT_`, `HH_`, `DH_`, `IC_` e `VR_`.
- Modelagem normalizada ao menos até a terceira forma normal, evitando colunas multivaloradas. Todas as dependências devem aparecer explicitamente no modelo.
- Todas as tabelas devem possuir chave primária, preferencialmente simples e autoincremental. Para pequenos domínios com menos de 30 registros, preferir chave sem autoincremento. Nas associativas, preferir identificador próprio e índice único para o par de referências.
- Valores de domínio não binários devem ser representados por tabelas de domínio e chaves estrangeiras, não por listas restritas em colunas ou por validações `CHECK`. Indicadores binários são permitidos, com valores documentados: 0 - Não; 1 - Sim.
- Validações de dados, como limites de coordenadas, podem usar `CHECK`, com nomes `CC_<TABELA>_<COLUNA>_01`. Valores padrão devem ter restrições documentadas com nomes `DF_<TABELA>_<COLUNA>_01`.
- Chaves primárias usam `PK_<TABELA>`; estrangeiras, `FK_<FILHA>_<PAI>`, com sufixo de finalidade quando houver várias ligações com a mesma origem. As colunas de referência preservam o nome da chave de origem, observadas as regras de papel da norma.
- Criar índice para cada chave estrangeira e para acessos relevantes, com nomes `IX_<TABELA>_01`. A unicidade adicional deve ser implementada por índices únicos.
- Documentar tipos físicos, tamanhos, nulabilidade, valores padrão, proprietário ou esquema e significado dos dados em português. Documentar as chaves com a expressão `Chave primária - <TABELA>`, inclusive nas referências estrangeiras.
- Incluir, sempre que possível, a data e hora de criação dos registros transacionais. Justificar históricos e registros de operações, preferindo preenchê-los pela aplicação. Evitar armazenamento binário no banco.
- Identificar dados pessoais e sensíveis e classificá-los no modelo conforme a norma; o nome do fiscal é um dado pessoal identificador.

### Adequações Pendentes

As seções abaixo são propostas preliminares e ainda não constituem um modelo físico integralmente aderente à norma. Devem ser revisadas para:

- Definir o identificador aceito pela API do eFiscaliza e concluir o detalhamento dos domínios de classificação da emissão e da etiquetagem.
- Detalhar os domínios dos seletores, especialmente a situação da emissão, e substituir descrições provisórias por referências quando aplicável.
- Completar a documentação de chaves, índices, tipos físicos, valores padrão, criação dos registros e classificação de dados pessoais.
- Definir o armazenamento dos anexos. A reunião registrou que o sistema atual usa BLOB, mas não decidiu se esse modelo será mantido; não assumir armazenamento externo nem binário sem decisão e justificativa.
- Definir como a auditoria identificará o responsável pelas operações: o modelo não prevê uma tabela de usuários, e `TB_FISCAL` representa o cadastro funcional de fiscais, não uma identidade autenticada.

### Resumo das Principais Tabelas

| Tabela                   | Finalidade resumida                                                                                   |
| ------------------------ | ----------------------------------------------------------------------------------------------------- |
| `TB_EVENTO`            | Cadastro dos eventos, período, localização, ação de fiscalização e coordenação responsável. |
| `TB_ESTACAO`           | Estações de monitoração vinculadas a um evento, com modelo, local e coordenadas.                  |
| `TB_EMISSAO`           | Emissões de radiofrequência registradas no evento, com frequência, origem da captura e situação. |
| `TB_INCIDENTE`         | Incidentes de fiscalização, como BSR e ERB Fake, com situação, local e observações.             |
| `TB_TICKET`            | Acompanhamento de emissões e incidentes, com situação e prioridade.                                |
| `TB_TESTE_ETIQUETAGEM` | Testes de equipamentos, entidade vinculada, permissões e etiquetas.                                  |
| `TB_ENTIDADE`          | Cadastro reutilizável de entidades, perfil, identificação e contatos usados nos testes.            |
| `TL_TICKET`            | Histórico de operações, relatos e mudanças de estado de cada ticket.                              |

| Tabela de apoio                                   | Finalidade resumida                                                                                                           |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `TB_FISCAL`                                     | Cadastro funcional de fiscais, com identificador, nome e unidade; não representa usuários autenticados.                     |
| `TB_UNIDADE_EXECUTANTE`                         | Cadastro de unidades referenciadas por fiscais e eventos.                                                                     |
| `TB_MUNICIPIO`                                  | Referência de município e UF usada na localização do evento; sua definição não está detalhada neste documento.        |
| `TB_EVENTO_UNIDADE_EXECUTANTE`                  | Associação de eventos com uma ou mais unidades executantes.                                                                 |
| `TB_EVENTO_FISCAL`                              | Associação de fiscais a eventos e às funções exercidas em cada evento.                                                   |
| `TB_EMISSAO_FISCAL`                             | Associação dos fiscais participantes de cada emissão.                                                                      |
| `TB_EMISSAO_ANEXO`                              | Metadados e referência de cada anexo vinculado a uma emissão.                                                               |
| `TB_TIPO_INCIDENTE`                             | Domínio dos tipos de incidente, como BSR e ERB Fake.                                                                         |
| `TB_SITUACAO`                                   | Domínio compartilhado das situações de emissões e incidentes (`Pendente`, `Relatada` e situação final a confirmar). |
| `TB_INCIDENTE_FISCAL`                           | Associação dos fiscais participantes de cada incidente.                                                                     |
| `TB_INCIDENTE_ANEXO`                            | Metadados e referência de cada anexo vinculado a um incidente.                                                               |
| `TB_TICKET_EMISSAO`                             | Associação entre tickets e emissões.                                                                                       |
| `TB_TICKET_INCIDENTE`                           | Associação entre tickets e incidentes.                                                                                      |
| `TB_TICKET_FISCAL`                              | Associação dos fiscais atribuídos a cada ticket.                                                                           |
| `TB_OPERACAO_TICKET`                            | Domínio proposto para classificar as operações registradas no histórico de tickets.                                       |
| `TB_SITUACAO_TICKET`                            | Domínio próprio de situações e transições dos tickets, distinto do domínio de emissão/incidente.                      |
| Domínio de prioridade do ticket (nome a definir) | Valores de prioridade disponíveis para tickets.                                                                              |
| `TB_TESTE_ETIQUETAGEM_FREQUENCIA`               | Frequências, larguras de banda e classificações registradas em cada teste.                                                 |
| `TB_PERFIL_ENTIDADE`                            | Domínio dos perfis de pessoa física, pessoa jurídica e estrangeiro.                                                        |
| `TB_LICENCA`                                    | Domínio dos enquadramentos de licença apresentados no teste.                                                                |
| `TB_TIPO_EQUIPAMENTO`                           | Domínio dos tipos de equipamento etiquetados.                                                                                |
| `TB_PERMISSAO_ETIQUETA`                         | Domínio das permissões associadas à etiqueta.                                                                              |
| `TB_BANDA`                                      | Domínio opcional para largura de banda, caso a representação final seja por código.                                       |
| `TB_SERVICO_TECNOLOGIA`                         | Domínio proposto para a classificação de emissão hoje chamada “Faixa”; nome e conteúdo a confirmar.                    |
| `TB_CLASSIFICACAO_TESTE`                        | Domínio proposto para a classificação própria da etiquetagem, distinto do domínio de emissão.                           |
| `TB_TESTE_ETIQUETAGEM_ETIQUETA`                 | Uma linha por etiqueta vinculada ao teste.                                                                                    |
| `TB_TESTE_ETIQUETAGEM_ANEXO`                    | Metadados e referência de cada anexo do equipamento testado.                                                                 |

Os nomes dos domínios de classificação da emissão e da etiquetagem são propostas semânticas e ainda precisam de validação. Também permanecem pendentes o contrato da API do eFiscaliza, a estrutura final do histórico de tickets, o armazenamento de anexos, o tratamento da divergência normativa sobre geometria e a conciliação entre a simplificação de auditoria discutida na reunião e os requisitos institucionais de rastreabilidade.

O item 1 da norma exige Microsoft SQL Server 2014, modelo físico e SAP Power Designer 16.7 ou superior, com aprovação da Gerência de Informações e Biblioteca (GIIB) para exceções de banco. As instruções atuais do projeto mencionam PostgreSQL. Essa divergência precisa ser resolvida antes de definir o modelo físico ou gerar scripts; este documento não autoriza troca de tecnologia nem presume aprovação de exceção. Views, procedimentos, funções e gatilhos também dependem da autorização prevista na norma.

## Tabela `TB_EVENTO`

Armazena os dados do evento apresentados na janela **Gerenciar Eventos**. Esta proposta utiliza tipos lógicos; os tipos específicos serão definidos após a escolha do banco de dados.

| Campo                     | Tipo lógico | Descrição                                                                                              |
| ------------------------- | ------------ | -------------------------------------------------------------------------------------------------------- |
| `ID_EVENTO`             | Inteiro      | Chave primária do evento, gerada automaticamente.                                                       |
| `NO_EVENTO`             | Texto curto  | Nome do evento. Obrigatório, conforme indicado na tela.                                                 |
| `VR_LATITUDE`           | Decimal      | Latitude do local do evento, entre -90 e 90.                                                             |
| `VR_LONGITUDE`          | Decimal      | Longitude do local do evento, entre -180 e 180.                                                          |
| `CO_MUNICIPIO_IBGE`     | Inteiro      | Chave estrangeira para `TB_MUNICIPIO.CO_MUNICIPIO_IBGE`, identificando a cidade selecionada.           |
| `CO_ACAO_FISCALIZACAO`  | Inteiro      | Identificador estável da ação de fiscalização no eFiscaliza, validado pela API.                     |
| `TX_ACAO_FISCALIZACAO`  | Texto longo  | Texto da ação retornado pela API; pode ser sugerido na interface, sem substituir a observação local. |
| `ID_FISCAL_RESPONSAVEL` | Inteiro      | Chave estrangeira para `TB_FISCAL.ID_FISCAL`, no papel de coordenador responsável.                    |
| `DT_INICIO`             | Data         | Início do período de realização.                                                                     |
| `DT_FIM`         | Data         | Fim do período de realização.                                                                         |
| `IC_TESTE_ETIQUETAGEM`  | Booleano     | Indica se o evento possui teste de etiquetagem: sim ou não.                                             |
| `TX_OBSERVACAO`         | Texto longo  | Observações sobre o evento.                                                                            |

### Localização

- A tela apresenta os seletores de UF e cidade, sendo a cidade habilitada após a seleção da UF.
- Nesta proposta, a UF é obtida de `TB_MUNICIPIO.SG_UF` pelo vínculo `CO_MUNICIPIO_IBGE`, sem duplicá-la na tabela `TB_EVENTO`.
- Deve ser confirmado se será permitido cadastrar um evento informando apenas a UF, sem cidade. Nesse caso, a modelagem da localização precisará contemplar essa possibilidade.

### Relacionamentos Exibidos na Tela

As listas permitem selecionar várias unidades executantes e vários fiscais. Esses vínculos não devem ser armazenados como listas de identificadores em uma coluna de `TB_EVENTO`.

| Relacionamento proposto          | Cardinalidade                               | Dados do vínculo                                                                                                                                                          |
| -------------------------------- | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TB_EVENTO_UNIDADE_EXECUTANTE` | Muitos para muitos entre eventos e unidades | `ID_EVENTO` e `SG_UNIDADE_EXECUTANTE`, referenciando as chaves de `TB_EVENTO` e `TB_UNIDADE_EXECUTANTE`. Cada par deve ser único.                                 |
| `TB_EVENTO_FISCAL`             | Muitos para muitos entre eventos e fiscais  | `ID_EVENTO`, `ID_FISCAL` e os indicadores `IC_COORDENACAO`, `IC_ABORDAGEM`, `IC_MONITORACAO` e `IC_TESTE_ETIQUETAGEM`. Cada par evento/fiscal deve ser único. |

Os indicadores de atuação pertencem à participação do fiscal no evento, não ao cadastro geral do fiscal. A tela permite marcar mais de um indicador para o mesmo participante.

### Regras de Consistência

- Quando ambas as datas forem informadas, `DT_FIM_EVENTO` não pode ser anterior a `DT_INICIO_EVENTO`.
- A cidade selecionada deve pertencer à UF escolhida.
- O coordenador responsável deve ser um fiscal participante do evento com o indicador `IC_COORDENACAO` marcado, conforme o filtro apresentado na tela.
- O identificador da ação deve ser validado na API do eFiscaliza. A API demonstrada requer autenticação HTTP; confirmar contrato, ambiente e validação de unidade/situação antes de implementar. O texto retornado pode ser apresentado como sugestão, distinguindo-o da observação própria do evento.
- As referências a cidades, unidades e fiscais dependem das respectivas tabelas de cadastro, ainda a serem projetadas.

### Pontos a Confirmar

- Obrigatoriedade dos campos além do nome, limites de tamanho e valores padrão.
- Nome definitivo dos campos de ação, identificador exato aceito pela API e regras de validação da unidade e da situação.
- Se `DT_INICIO_EVENTO` e `DT_FIM_EVENTO` devem perder o sufixo `_EVENTO`; o alcance da renomeação não ficou definido na reunião.
- Se será obrigatório selecionar ao menos uma unidade executante, um fiscal ou um coordenador responsável.
- Precisão das coordenadas geográficas e possibilidade de informar apenas uma delas.

## Tabela `TB_ESTACAO`

Armazena as estações de monitoração cadastradas pela janela **Cadastro de Estações**, vinculadas ao evento selecionado. Os tipos abaixo são lógicos, seguindo o mesmo nível de definição de `TB_EVENTO`.

| Campo                     | Tipo lógico      | Obrigatório | Descrição                                                                          |
| ------------------------- | ----------------- | ------------ | ------------------------------------------------------------------------------------ |
| `ID_ESTACAO`            | Inteiro           | Sim          | Chave primária da estação, gerada automaticamente.                                |
| `ID_EVENTO`             | Inteiro           | Sim          | Chave estrangeira para `TB_EVENTO.ID_EVENTO`. Corresponde ao seletor Evento.       |
| `NO_ESTACAO`            | Texto curto       | Sim          | Identificação da estação informada no formulário.                               |
| `DE_MODELO_EQUIPAMENTO` | Texto curto       | Sim          | Modelo do equipamento escolhido no seletor Modelo.                                   |
| `DE_LOCAL`              | Texto curto       | Sim          | Local de instalação ou operação da estação.                                    |
| `VR_LATITUDE`           | Decimal (6 casas) | Sim          | Latitude da estação em graus decimais, entre -90 e 90, com seis casas decimais.    |
| `VR_LONGITUDE`          | Decimal (6 casas) | Sim          | Longitude da estação em graus decimais, entre -180 e 180, com seis casas decimais. |

### Relacionamento com Evento

- Um evento pode possuir várias estações; cada registro de `TB_ESTACAO` pertence a um único evento.
- `ID_EVENTO` deve referenciar um evento existente.
- As coordenadas representam a posição da estação e não precisam ser iguais às coordenadas do evento.
- O cadastro permanece vinculado diretamente ao evento nesta etapa. A relação N:N e a integração com RFusion foram discutidas como possíveis evoluções, mas não foram aprovadas para esta revisão; coordenadas de RFusion não devem ser presumidas como posição atual de estação móvel.

### Chaves e Restrições

| Objeto                   | Nome                              | Definição                                                            |
| ------------------------ | --------------------------------- | ---------------------------------------------------------------------- |
| Chave primária          | `PK_TB_ESTACAO`                 | Coluna `ID_ESTACAO`.                                                 |
| Chave estrangeira        | `FK_TB_ESTACAO_TB_EVENTO`       | Coluna `ID_EVENTO` referenciando `TB_EVENTO.ID_EVENTO`.            |
| Validação de latitude  | `CC_TB_ESTACAO_VR_LATITUDE_01`  | `VR_LATITUDE` entre -90 e 90, armazenada com seis casas decimais.    |
| Validação de longitude | `CC_TB_ESTACAO_VR_LONGITUDE_01` | `VR_LONGITUDE` entre -180 e 180, armazenada com seis casas decimais. |

### Regras de Consistência

- Os campos indicados como obrigatórios na tela não podem receber valor nulo. Campos textuais também não podem conter apenas espaços.
- O cadastro da estação não deve alterar os dados do evento vinculado.
- A inclusão, edição e eventual exclusão da estação devem gerar auditoria, identificando registro, usuário, origem e valores anteriores e novos aplicáveis. A estrutura de auditoria será detalhada separadamente.

### Pontos a Confirmar

- Se a identificação da estação deve ser única dentro de cada evento.
- Se o modelo será armazenado como descrição ou como chave estrangeira para um cadastro próprio de modelos de equipamento.
- Se o campo Local e o botão `+` correspondem a um cadastro próprio de locais; nessa hipótese, substituir a descrição por uma referência ao cadastro a ser definido.
- Limites de tamanho dos campos textuais.
- A evolução futura para cadastro global de estação e vínculo N:N, caso surja uma identificação confiável do equipamento.
- Se haverá desativação da estação, em vez de exclusão, para preservar os vínculos com registros operacionais.

## Tabela `TB_EMISSAO`

Armazena os registros de emissões de radiofrequência apresentados na janela **Inserir emissão**. O nome acompanha a terminologia da tela; a referência de auditoria denomina essa entidade `TB_OCORRENCIA`. Nesta proposta, utilizam-se `TB_EMISSAO` e `ID_EMISSAO`, preservando os padrões de nomenclatura, sem criar duas entidades para o mesmo registro.

| Campo                     | Tipo lógico    | Obrigatório | Descrição                                                                                                                           |
| ------------------------- | --------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| `ID_EMISSAO`            | Inteiro         | Sim          | Chave primária da emissão, gerada automaticamente.                                                                                  |
| `ID_EVENTO`             | Inteiro         | Sim          | Chave estrangeira para `TB_EVENTO.ID_EVENTO`. Obtida do contexto do evento, embora não apareça no recorte da tela.                |
| `DH_EMISSAO`            | Data e hora     | Sim          | Data e hora da emissão em um único valor; fuso horário a definir.                                                                  |
| `DE_LOCAL_REGIAO`       | Texto curto     | Não         | Local ou região da emissão.                                                                                                         |
| `DE_ORIGEM_CAPTURA`     | Texto curto     | Sim          | Opção selecionada em Captura realizada por. As opções e sua representação definitiva precisam ser confirmadas.                  |
| `ID_ESTACAO`            | Inteiro         | Condicional  | Chave estrangeira para `TB_ESTACAO.ID_ESTACAO`, quando a captura estiver vinculada a uma estação.                                 |
| `VR_FREQUENCIA_MHZ`     | Decimal         | Sim          | Frequência central da emissão, em MHz.                                                                                              |
| `VR_LARGURA_KHZ`        | Decimal         | Sim          | Largura de banda ocupada, em kHz, selecionada no formulário.                                                                         |
| `CO_SERVICO_TECNOLOGIA` | Código textual | Sim          | Classificação de serviço, aplicação ou tecnologia selecionada; tabela e nome finais a confirmar.                                 |
| `DE_IDENTIFICACAO`      | Texto curto     | Sim          | Identificação selecionada para a emissão.                                                                                          |
| `IC_INTERFERENTE`       | Booleano        | Sim          | Indica se a emissão é interferente. Valores: 0 - Não; 1 - Sim.                                                                     |
| `IC_UTE`                | Booleano        | Sim          | Indica se a emissão corresponde a um usuário temporário de espectro. Tipo proposto caso o seletor UTE? contenha apenas sim e não. |
| `TX_OBSERVACAO`         | Texto longo     | Sim          | Conteúdo do campo Entidade Resp./Contato/Observações, preservado como um único campo conforme a tela.                             |
| `CO_SITUACAO`           | Texto curto     | Sim          | Código da situação da emissão, conforme os estados descritos abaixo.                                                              |

O campo Fiscal é obrigatório na tela e possui um botão `+`. A proposta admite vários fiscais participantes, armazenados no relacionamento abaixo, e não como nomes ou listas de identificadores em `TB_EMISSAO`.

### Relacionamentos

| Objeto proposto           | Cardinalidade                                     | Dados e regras                                                                                                                                                      |
| ------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TB_EVENTO`             | Um evento para muitas emissões                   | Cada emissão pertence a um evento, por `ID_EVENTO`.                                                                                                              |
| `TB_ESTACAO`            | Uma estação para muitas emissões               | Vínculo opcional ou condicional por `ID_ESTACAO`; a estação deve pertencer ao mesmo evento da emissão.                                                        |
| `TB_SERVICO_TECNOLOGIA` | Um valor de classificação para muitas emissões | `CO_SERVICO_TECNOLOGIA` referencia o domínio proposto de serviço, aplicação ou tecnologia; nome e códigos a confirmar.                                       |
| `TB_SITUACAO`           | Uma situação para muitas emissões              | `CO_SITUACAO` referencia o domínio compartilhado com incidentes; os rótulos e códigos finais ainda precisam de confirmação.                                  |
| `TB_EMISSAO_FISCAL`     | Muitos para muitos entre emissões e fiscais      | Colunas `ID_EMISSAO` e `ID_FISCAL`, referenciando `TB_EMISSAO` e `TB_FISCAL`. Cada par deve ser único; deve existir ao menos um fiscal por emissão.       |
| `TB_EMISSAO_ANEXO`      | Uma emissão para muitos anexos                   | Cada anexo possui identificador próprio e referência `ID_EMISSAO`. Nome, tipo, tamanho e armazenamento serão definidos separadamente. A inclusão é opcional. |

### Chaves

| Objeto                               | Nome                                    | Definição                                                                          |
| ------------------------------------ | --------------------------------------- | ------------------------------------------------------------------------------------ |
| Chave primária                      | `PK_TB_EMISSAO`                       | Coluna `ID_EMISSAO`.                                                               |
| Chave estrangeira de evento          | `FK_TB_EMISSAO_TB_EVENTO`             | `ID_EVENTO` referenciando `TB_EVENTO.ID_EVENTO`.                                 |
| Chave estrangeira de estação       | `FK_TB_EMISSAO_TB_ESTACAO`            | `ID_ESTACAO` referenciando `TB_ESTACAO.ID_ESTACAO`.                              |
| Chave estrangeira de classificação | `FK_TB_EMISSAO_TB_SERVICO_TECNOLOGIA` | `CO_SERVICO_TECNOLOGIA` referenciando o domínio proposto; confirmar o nome final. |
| Chave estrangeira de situação      | `FK_TB_EMISSAO_TB_SITUACAO`           | `CO_SITUACAO` referenciando `TB_SITUACAO.CO_SITUACAO`.                           |

### Situação da Emissão

- Os estados funcionais propostos são `Pendente`, `Relatada` e `Conferida` ou `Aprovada`. A escolha entre os dois últimos nomes e os códigos armazenados em `CO_SITUACAO` ainda será confirmada.
- A mensagem da tela informa que emissões pendentes e relatadas serão submetidas à inspeção da coordenação.
- As permissões e transições entre estados devem ser definidas antes da implementação; a imagem não permite concluir quais opções cada perfil pode selecionar.

### Regras de Consistência e Frequência

- Os campos obrigatórios não podem ser nulos; textos obrigatórios não podem conter apenas espaços.
- Frequência e largura de banda devem ser armazenadas como decimais, não como ponto flutuante. A frequência deve ser positiva; os valores permitidos para a largura dependem das opções do seletor.
- A entrada de frequência deve aceitar ponto ou vírgula decimal e ser normalizada antes da comparação e da gravação. A referência utiliza três casas decimais para frequência em MHz e largura em kHz; essa precisão deve ser confirmada para o novo sistema.
- Toda frequência incluída ou alterada deve ser consultada no banco durante o preenchimento e novamente no salvamento, inclusive nos fluxos offline/API ao processar a gravação. Na edição, desconsiderar o próprio registro.
- Verificar conflitos com equipamentos, emissões e demais cadastros aplicáveis, usando a precisão normalizada e considerando sobreposição entre frequência central e largura de banda, com conversão de MHz e kHz para uma unidade comum.
- Os alertas devem identificar a entidade conflitante, seu tipo, etiqueta e local quando disponíveis. São informativos e não devem impedir a conclusão do cadastro por conflito de frequência.
- Inclusões, edições, exclusões, mudanças de situação e alterações nos vínculos de fiscais e anexos devem gerar auditoria com origem, registro, usuário e valores anteriores e novos aplicáveis. A consulta de auditoria deve permitir exibir essas ações; sua estrutura será detalhada separadamente.
- Antes de registrar diferenças na auditoria, normalizar valores nulos, vazios e equivalentes, evitando alterações fictícias.

### Pontos a Confirmar

- Opções dos seletores Captura realizada por, serviço/aplicação/tecnologia, Identificação e UTE?.
- Nome, códigos e conteúdo do domínio de serviço/aplicação/tecnologia; a tela demonstrou FM, SMA, SMM, SLP, TV, SMP, SARC, GNSS, Satélite, Radiação Restrita e Outros, mas a lista não foi aprovada como domínio final. Não confundir esse domínio com a classificação própria da etiquetagem.
- Como a seleção da origem da captura determina o vínculo com uma estação.
- Se os fiscais selecionáveis devem estar vinculados previamente ao evento e se haverá distinção entre fiscal participante e autor do cadastro.
- Se entidade responsável e contato devem ser separados de observações em campos próprios.
- Campos condicionais de UTE, limites de tamanho, valores padrão, fuso horário e precisão dos valores numéricos.

## Tabela `TB_FISCAL`

Armazena o cadastro global dos fiscais apresentado na janela **Fiscais cadastrados**, somente com identificador, nome e unidade Anatel. O mesmo fiscal pode participar de vários eventos sem duplicação de seu cadastro; suas funções são definidas em cada vínculo com evento.

A tela não apresenta asteriscos de obrigatoriedade. As indicações abaixo são propostas de consistência a confirmar, e os tipos permanecem lógicos.

| Campo                                                                                                                                                                        | Tipo lógico | Obrigatório proposto | Descrição                                                                                                                  |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ | --------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `ID_FISCAL`                                                                                                                                                                | Inteiro      | Sim                   | Chave primária do fiscal, gerada automaticamente.                                                                           |
| `NO_FISCAL`                                                                                                                                                                | Texto curto  | Sim                   | Nome do fiscal. Corresponde ao campo Nome.                                                                                   |
| `SG_UNIDADE_EXECUTANTE`                                                                                                                                                    | Texto curto  | Sim                   | Chave estrangeira para `TB_UNIDADE_EXECUTANTE.SG_UNIDADE_EXECUTANTE`. Corresponde à GR ou UO selecionada em Local Anatel. |
| `TB_FISCAL` contém somente o identificador, o nome e a unidade do fiscal. Os papéis são definidos por evento no vínculo `TB_EVENTO_FISCAL`, não no cadastro global. |              |                       |                                                                                                                              |

### Relacionamentos

| Objeto                    | Cardinalidade                                | Dados e regras                                                                                                                                                         |
| ------------------------- | -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TB_UNIDADE_EXECUTANTE` | Uma unidade para muitos fiscais              | Cada fiscal referencia uma unidade por `SG_UNIDADE_EXECUTANTE`. A descrição exibida em Local Anatel vem do cadastro da unidade, sem duplicação em `TB_FISCAL`. |
| `TB_EVENTO_FISCAL`      | Muitos para muitos entre eventos e fiscais   | Reutiliza `ID_EVENTO` e `ID_FISCAL`, com os indicadores das funções exercidas naquele evento.                                                                    |
| `TB_EMISSAO_FISCAL`     | Muitos para muitos entre emissões e fiscais | Reutiliza `ID_EMISSAO` e `ID_FISCAL` para identificar os participantes da emissão.                                                                                |

### Funções no Evento

- Em `TB_EVENTO_FISCAL`, `IC_COORDENACAO`, `IC_ABORDAGEM`, `IC_MONITORACAO` e `IC_TESTE_ETIQUETAGEM` representam as funções selecionadas para cada evento. Um fiscal pode exercer funções diferentes em eventos diferentes.
- Os indicadores do vínculo começam como falso (0); o usuário marca os papéis aplicáveis. Mais de um papel pode ser atribuído ao mesmo fiscal no mesmo evento.
- A coluna Função no evento deve refletir os indicadores do vínculo `TB_EVENTO_FISCAL` para o evento em contexto; confirmar apenas a apresentação dessa coluna na lista global de fiscais.

### Chaves e Regras de Consistência

| Objeto                       | Nome                                   | Definição                                                                                 |
| ---------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------- |
| Chave primária              | `PK_TB_FISCAL`                       | Coluna `ID_FISCAL`.                                                                       |
| Chave estrangeira de unidade | `FK_TB_FISCAL_TB_UNIDADE_EXECUTANTE` | `SG_UNIDADE_EXECUTANTE` referenciando a chave de mesmo nome em `TB_UNIDADE_EXECUTANTE`. |

- O nome não deve conter apenas espaços. Não se propõe unicidade por nome, pois podem existir homônimos.
- A unidade selecionada deve existir em seu cadastro de referência.
- A ação Excluir não deve apagar em cascata participações, emissões ou outros registros históricos. O tratamento de fiscais já vinculados depende da política de exclusão ou desativação a definir.
- Inclusão, edição, exclusão ou desativação do fiscal e alterações de unidade, papéis e vínculos devem gerar auditoria com origem, registro, usuário, campo e valores anteriores e novos aplicáveis. A consulta de auditoria deve permitir exibir essas ações; sua estrutura será detalhada separadamente.
- A auditoria deve normalizar valores nulos, vazios e equivalentes antes de registrar diferenças.

### Pontos a Confirmar

- Obrigatoriedade de nome e unidade, tamanho dos campos e possibilidade de novos papéis além dos quatro atribuídos por evento.
- Necessidade de matrícula ou outro identificador institucional para distinguir fiscais homônimos.
- Política de exclusão ou desativação e tratamento de vínculos existentes quando um fiscal deixar de participar de eventos.

## Tabela `TB_INCIDENTE`

Armazena os incidentes identificados durante a fiscalização, conforme a janela **Registrar incidente**, incluindo bloqueadores de sinal (BSR), também conhecidos como bloqueadores intencionais ou jammers, e estações rádio-base falsas (ERB Fake). A lista completa de tipos ainda deve ser confirmada.

Os tipos abaixo são lógicos. O vínculo com o evento e a data e hora de criação são dados de contexto e rastreabilidade, não campos apresentados no recorte da tela.

| Campo                 | Tipo lógico    | Obrigatório | Descrição                                                                                                                                          |
| --------------------- | --------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ID_INCIDENTE`      | Inteiro         | Sim          | Chave primária - TB_INCIDENTE. Identificador gerado automaticamente.                                                                                |
| `ID_EVENTO`         | Inteiro         | Sim          | Chave estrangeira - TB_EVENTO. Identifica o evento em cujo contexto o incidente foi registrado.                                                      |
| `CO_TIPO_INCIDENTE` | Código textual | Sim          | Chave estrangeira - TB_TIPO_INCIDENTE. Classifica o incidente conforme o seletor Tipo.                                                               |
| `CO_SITUACAO`       | Código textual | Sim          | Chave estrangeira - TB_SITUACAO. Representa o estado de tratamento escolhido em Status.                                                              |
| `DE_LOCAL`          | Texto curto     | Sim          | Descrição do local onde o incidente foi identificado.                                                                                              |
| `VR_LATITUDE`       | Decimal         | Não         | Latitude do incidente em graus decimais, entre -90 e 90.                                                                                             |
| `VR_LONGITUDE`      | Decimal         | Não         | Longitude do incidente em graus decimais, entre -180 e 180.                                                                                          |
| `TX_OBSERVACAO`     | Texto longo     | Sim          | Informações descritivas sobre o incidente e as circunstâncias observadas.                                                                         |
| `DH_CRIACAO`        | Data e hora     | Sim          | Momento de criação do registro, preenchido automaticamente pela aplicação. Não representa necessariamente o momento em que o incidente ocorreu. |

### Domínios

- `TB_TIPO_INCIDENTE` terá a chave `CO_TIPO_INCIDENTE` e a descrição `DE_TIPO_INCIDENTE`. A opção visível na tela é Bloqueador de sinal (BSR); os demais valores e códigos devem ser confirmados. Para um domínio com menos de 30 registros, não utilizar autoincremento na chave.
- `TB_SITUACAO` terá a chave `CO_SITUACAO` e a descrição `DE_SITUACAO`, compartilhando com as emissões os estados `Pendente`, `Relatada` e `Conferida` ou `Aprovada`. A escolha do estado final e os códigos ainda serão definidos.
- Os códigos devem ser validados por chaves estrangeiras, não por listas em colunas nem por restrições `CHECK` enumerando opções.
- O compartilhamento de `TB_SITUACAO` aplica-se somente a emissões e incidentes; tickets terão domínio próprio.

### Relacionamentos

| Objeto proposto         | Cardinalidade                                 | Dados e regras                                                                                                                                                                                                                                                    |
| ----------------------- | --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TB_EVENTO`           | Um evento para muitos incidentes              | Cada incidente pertence a um evento por `ID_EVENTO`.                                                                                                                                                                                                            |
| `TB_TIPO_INCIDENTE`   | Um tipo para muitos incidentes                | Cada incidente possui um tipo por `CO_TIPO_INCIDENTE`.                                                                                                                                                                                                          |
| `TB_SITUACAO`         | Uma situação para muitos incidentes         | Cada incidente possui uma situação atual por `CO_SITUACAO`.                                                                                                                                                                                                   |
| `TB_INCIDENTE_FISCAL` | Muitos para muitos entre incidentes e fiscais | Chave simples `ID_INCIDENTE_FISCAL`, gerada automaticamente, e referências `ID_INCIDENTE` e `ID_FISCAL`. Criar índice único para o par incidente/fiscal. Deve existir ao menos um participante, conforme o campo Fiscal obrigatório e seu botão `+`. |
| `TB_INCIDENTE_ANEXO`  | Um incidente para muitos anexos               | Cada anexo possui identificador próprio `ID_INCIDENTE_ANEXO` e referência `ID_INCIDENTE`. Metadados e forma de armazenamento serão definidos separadamente. Fotos/anexos são opcionais.                                                                   |

### Chaves, Índices e Validações

| Objeto                          | Nome                                  | Definição                                                                         |
| ------------------------------- | ------------------------------------- | ----------------------------------------------------------------------------------- |
| Chave primária                 | `PK_TB_INCIDENTE`                   | Coluna `ID_INCIDENTE`.                                                            |
| Chave estrangeira de evento     | `FK_TB_INCIDENTE_TB_EVENTO`         | `ID_EVENTO` referenciando `TB_EVENTO.ID_EVENTO`.                                |
| Chave estrangeira de tipo       | `FK_TB_INCIDENTE_TB_TIPO_INCIDENTE` | `CO_TIPO_INCIDENTE` referenciando a chave de mesmo nome em `TB_TIPO_INCIDENTE`. |
| Chave estrangeira de situação | `FK_TB_INCIDENTE_TB_SITUACAO`       | `CO_SITUACAO` referenciando a chave de mesmo nome em `TB_SITUACAO`.             |
| Índice de evento               | `IX_TB_INCIDENTE_01`                | Coluna `ID_EVENTO`, mantida por ser chave estrangeira da tabela filha.            |
| Índice de tipo                 | `IX_TB_INCIDENTE_02`                | Coluna `CO_TIPO_INCIDENTE`.                                                       |
| Índice de situação           | `IX_TB_INCIDENTE_03`                | Coluna `CO_SITUACAO`.                                                             |
| Validação de latitude         | `CC_TB_INCIDENTE_VR_LATITUDE_01`    | Quando informada, latitude entre -90 e 90.                                          |
| Validação de longitude        | `CC_TB_INCIDENTE_VR_LONGITUDE_01`   | Quando informada, longitude entre -180 e 180.                                       |

As associativas e tabelas dependentes também deverão possuir suas chaves estrangeiras e índices por referência no detalhamento físico.

### Regras de Consistência, Anexos e Auditoria

- Tipo, local, observações e situação são obrigatórios na tela. Textos obrigatórios não podem conter apenas espaços. O vínculo com ao menos um fiscal deve ser validado junto à gravação do incidente.
- Latitude e longitude não são obrigatórias na tela. Quando informadas, devem respeitar os limites de graus decimais; confirmar se o par completo é obrigatório.
- A reunião orientou não incluir `GE_PONTO` nem índice espacial. Isso diverge dos itens 7.6.5 e 7.6.7 da referência normativa, que exigem geometria quando há latitude/longitude separadas e índice espacial. A decisão normativa precisa ser resolvida antes do modelo físico.
- O botão `+` de Local sugere um controle auxiliar, mas não comprova a existência de cadastro próprio. Caso seja confirmado, substituir `DE_LOCAL` por uma referência ao cadastro de locais.
- A tela apresenta Pendente como seleção inicial. Confirmar se isso deve ser um valor padrão persistente; nesse caso, documentar a restrição `DF_TB_INCIDENTE_CO_SITUACAO_01` com o código correspondente.
- Os estados `Relatada` e `Conferida` ou `Aprovada` representam etapas distintas; confirmar o nome final e detalhar permissões e transições sem presumir que todos os perfis possam selecionar todos os estados.
- Fotos devem receber nomes no formato `NomeEvento_Classificacao_ID_Registro_Data_Hora_Sequencia.extensao`, preservando a extensão original e substituindo caracteres inválidos por `_`. A exclusão de uma foto exige confirmação, auditoria própria e não pode excluir o incidente nem outras fotos.
- Inclusões, edições, exclusões, mudanças de situação e alterações nos vínculos de fiscais e anexos devem registrar auditoria com origem, registro afetado, usuário, campo e valores anteriores e novos aplicáveis. Preencher a auditoria pela aplicação e garantir sua exibição na consulta; sua estrutura será detalhada separadamente.
- Normalizar valores nulos, vazios e equivalentes antes de comparar alterações para auditoria, evitando registros de diferenças fictícias.

### Pontos a Confirmar

- Lista completa e códigos dos tipos de incidente, códigos das situações e seleção inicial persistente.
- Se os fiscais participantes devem estar previamente vinculados ao evento e como identificar separadamente o autor do cadastro.
- Existência de cadastro próprio de locais, tamanho dos textos e precisão das coordenadas.
- Resolução formal da divergência entre a retirada de geometria/índice espacial acordada na reunião e os itens 7.6.5 e 7.6.7 da norma.
- Formatos e armazenamento dos anexos, política de exclusão ou desativação e estrutura de auditoria.

## Tabela `TB_TICKET`

Armazena tickets de acompanhamento de emissões e incidentes. Cada ticket pertence a um evento e pode estar associado a zero, uma ou várias emissões e, independentemente, a zero, um ou vários incidentes. Um mesmo ticket pode ter associações dos dois tipos; não é obrigatório vinculá-lo a pelo menos um registro.

Os vínculos são mantidos em tabelas associativas, evitando uma coluna de emissão ou incidente no ticket e permitindo múltiplas referências sem valores nulos. Cada emissão ou incidente também pode estar associado a vários tickets, conforme a proposta NxN.

| Campo             | Tipo lógico    | Obrigatório | Descrição                                                                                                                           |
| ----------------- | --------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| `ID_TICKET`     | Inteiro         | Sim          | Chave primária - TB_TICKET. Identificador gerado automaticamente.                                                                    |
| `ID_EVENTO`     | Inteiro         | Sim          | Chave estrangeira para `TB_EVENTO.ID_EVENTO`. Evento ao qual o ticket pertence.                                                     |
| `CO_SITUACAO`   | Código textual | Sim          | Situação atual do ticket. Referencia domínio próprio, distinto de `TB_SITUACAO`; valores e transições precisam ser definidos. |
| `CO_PRIORIDADE` | Código textual | Sim          | Prioridade do ticket. Deve referenciar domínio próprio; valores e códigos precisam ser confirmados.                                |
| `TX_OBSERVACAO` | Texto longo     | Não         | Observações informadas na criação ou no acompanhamento do ticket.                                                                 |
| `DH_CRIACAO`    | Data e hora     | Sim          | Momento de criação do ticket, preenchido automaticamente pela aplicação.                                                          |

### Tabelas Associativas

| Tabela                  | Campos e regras                                                                                                                                                                                                                                                        |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TB_TICKET_EMISSAO`   | `ID_TICKET_EMISSAO` como chave primária; `ID_TICKET` referenciando `TB_TICKET.ID_TICKET`; `ID_EMISSAO` referenciando `TB_EMISSAO.ID_EMISSAO`. Criar índice único para o par `ID_TICKET`/`ID_EMISSAO`.                                                 |
| `TB_TICKET_INCIDENTE` | `ID_TICKET_INCIDENTE` como chave primária; `ID_TICKET` referenciando `TB_TICKET.ID_TICKET`; `ID_INCIDENTE` referenciando `TB_INCIDENTE.ID_INCIDENTE`. Criar índice único para o par `ID_TICKET`/`ID_INCIDENTE`.                                       |
| `TB_TICKET_FISCAL`    | `ID_TICKET_FISCAL` como chave primária; `ID_TICKET` referenciando `TB_TICKET.ID_TICKET`; `ID_FISCAL` referenciando `TB_FISCAL.ID_FISCAL`. Criar índice único para o par `ID_TICKET`/`ID_FISCAL`; confirmar se ao menos um fiscal deve ser atribuído. |

### Histórico de Operações do Ticket

Cada ticket pode possuir várias linhas em `TL_TICKET`. O nome e os campos abaixo são uma proposta técnica, ainda sujeita à validação normativa e à definição da identidade autenticada do responsável.

| Campo                      | Tipo lógico    | Obrigatório | Descrição                                                                                                                                 |
| -------------------------- | --------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `ID_MOVIMENTACAO_TICKET` | Inteiro         | Sim          | Chave primária da movimentação, gerada automaticamente.                                                                                  |
| `ID_TICKET`              | Inteiro         | Sim          | Chave estrangeira para `TB_TICKET.ID_TICKET`.                                                                                             |
| `DH_OPERACAO`            | Data e hora     | Sim          | Momento em que a operação ocorreu.                                                                                                        |
| `CO_OPERACAO`            | Código textual | Sim          | Operação classificada por domínio próprio `TB_OPERACAO_TICKET`; inclui criação, edição, relato, devolução e mudança de estado. |
| `CO_RESPONSAVEL`         | Texto curto     | A definir    | Identificador do responsável autenticado; origem e tipo dependem do mecanismo de identidade do sistema.                                    |
| `NO_CAMPO`               | Texto curto     | Não         | Campo alterado, quando aplicável.                                                                                                          |
| `TX_VALOR_ANTERIOR`      | Texto longo     | Não         | Valor anterior do campo, quando aplicável.                                                                                                 |
| `TX_VALOR_NOVO`          | Texto longo     | Não         | Novo valor do campo, quando aplicável.                                                                                                     |
| `TX_CONTEUDO`            | Texto longo     | Não         | Relato, motivo de devolução ou providência correspondente à operação.                                                                 |

O histórico é 1:N e não sobrescreve movimentações anteriores. `DH_CRIACAO` permanece em `TB_TICKET`; cada atualização e ocorrência tem seu próprio `DH_OPERACAO`.

### Relacionamentos, Chaves e Índices

- Um evento pode possuir vários tickets; cada ticket pertence a um evento por `ID_EVENTO`.
- Um ticket pode estar associado a zero ou várias emissões por `TB_TICKET_EMISSAO`; uma emissão pode estar associada a zero ou vários tickets.
- Um ticket pode estar associado a zero ou vários incidentes por `TB_TICKET_INCIDENTE`; um incidente pode estar associado a zero ou vários tickets.
- As associações com emissões e incidentes são independentes. A inclusão de um tipo não exige nem impede a inclusão do outro.
- As emissões e os incidentes associados devem pertencer ao mesmo evento do ticket. Validar essa consistência no salvamento, inclusive quando os vínculos forem alterados.
- `ID_EVENTO` deve ter chave estrangeira `FK_TB_TICKET_TB_EVENTO` e índice. Não há vínculo direto com fiscal em `TB_TICKET`; os fiscais atribuídos ficam em `TB_TICKET_FISCAL`.
- Cada tabela associativa deve possuir chaves estrangeiras para suas duas entidades e índices para consulta por cada referência, além do índice único do par.
- `CO_SITUACAO` deve referenciar `TB_SITUACAO_TICKET.CO_SITUACAO`; `CO_PRIORIDADE` deve referenciar domínio próprio de prioridade. Ambos são distintos do domínio compartilhado por emissões e incidentes. Definir códigos, valores iniciais e transições antes do modelo físico.
- `TL_TICKET.ID_TICKET` deve referenciar `TB_TICKET`; criar índice para a FK. `CO_OPERACAO` deve referenciar `TB_OPERACAO_TICKET`.

### Regras de Consistência e Auditoria

- A ausência de vínculos com emissões e incidentes é válida; não exigir uma associação mínima para concluir ou salvar o ticket.
- Ao devolver um ticket relatado, exigir motivo e registrar uma nova movimentação em `TL_TICKET`, incluindo o estado anterior, o responsável e o motivo. Relatos e providências posteriores também geram novas movimentações, sem substituir registros anteriores.
- Criação, edição, mudança de estado, devolução e mudanças nos vínculos de emissões, incidentes e fiscais devem ser reconstruíveis a partir de `TL_TICKET`, com momento, responsável, operação e conteúdo/valores pertinentes.
- Alterações nos vínculos não podem excluir os registros de emissão ou incidente associados, nem outros vínculos do ticket.
- A consulta de auditoria deve exibir corretamente o histórico do ticket e de suas associações; normalizar valores nulos, vazios e equivalentes antes de registrar diferenças.

### Pontos a Confirmar

- Valores e códigos dos domínios de situação, prioridade e operação, incluindo transições entre coordenação e fiscal.
- Tipo e origem do identificador do responsável autenticado e confirmação do nome final e campos de `TL_TICKET`.
- Se a atribuição de pelo menos um fiscal será obrigatória e se um ticket pode ser criado sem emissão e sem incidente, além de permanecer sem vínculos posteriormente.
- Como garantir, no banco e na aplicação, que emissão e incidente associados pertençam ao evento do ticket.

## Tabela `TB_ENTIDADE`

Cadastro reutilizável de entidades vinculadas a testes de etiquetagem. O identificador próprio não depende de CPF ou CNPJ, que podem não existir ou não se aplicar a uma entidade estrangeira. O perfil é associado à entidade, e não ao teste.

| Campo                       | Tipo lógico    | Obrigatório | Descrição                                                                                 |
| --------------------------- | --------------- | ------------ | ------------------------------------------------------------------------------------------- |
| `ID_ENTIDADE`             | Inteiro         | Sim          | Chave primária da entidade, gerada automaticamente.                                        |
| `CO_PERFIL`               | Código textual | Sim          | Chave estrangeira para `TB_PERFIL_ENTIDADE.CO_PERFIL`.                                    |
| `NO_ENTIDADE`             | Texto curto     | Sim          | Nome da pessoa ou entidade.                                                                 |
| `CO_CPF_CNPJ`             | Texto curto     | Condicional  | CPF ou CNPJ quando aplicável; armazenar como texto e permitir ausência conforme o perfil. |
| `NO_RESPONSAVEL_CONTATO`  | Texto curto     | Não         | Nome do responsável ou contato principal, quando informado.                                |
| `CO_TELEFONE`             | Texto curto     | Não         | Telefone, preservando código de país e de área.                                          |
| `ED_EMAIL`                | Texto curto     | Não         | Endereço de correio eletrônico.                                                           |
| `TX_INFORMACAO_ADICIONAL` | Texto longo     | Não         | Informações complementares e outros contatos.                                             |
| `DH_CRIACAO`              | Data e hora     | Sim          | Momento de criação do cadastro, preenchido pela aplicação.                              |

O perfil referencia o domínio `TB_PERFIL_ENTIDADE`. A consulta deve permitir localizar por CPF/CNPJ ou nome e selecionar uma entidade existente ou cadastrar uma nova. A regra de unicidade e a política para preservar contatos antigos quando o cadastro mudar ainda precisam ser definidas.

`ID_ENTIDADE` é a chave primária de `TB_ENTIDADE`. `CO_PERFIL` referencia `TB_PERFIL_ENTIDADE.CO_PERFIL` por `FK_TB_ENTIDADE_TB_PERFIL_ENTIDADE`, com índice para a chave estrangeira. Nome, CPF/CNPJ e contatos podem conter dados pessoais e devem ser classificados conforme a norma.

Inclusões, alterações e desativações do cadastro devem ser auditadas conforme a política institucional. A reunião não definiu se testes antigos devem exibir os contatos atuais da entidade, um retrato dos dados no momento do teste ou ambos; essa política permanece pendente.

## Tabela `TB_TESTE_ETIQUETAGEM`

Armazena o teste e a etiquetagem de um equipamento ou conjunto de equipamentos iguais, conforme a janela **Teste e etiquetagem**. Cada teste pertence a um evento e pode possuir várias frequências, adicionadas individualmente pelo botão `+` ao lado de Frequências. As frequências são registros dependentes, descritos na tabela `TB_TESTE_ETIQUETAGEM_FREQUENCIA`, e não uma coluna multivalorada do teste.

Os tipos são lógicos. As obrigatoriedades sem indicação explícita na imagem e as regras de geração de etiquetas permanecem propostas a confirmar. Os dados cadastrais da entidade ficam em `TB_ENTIDADE`; o teste mantém somente o vínculo `ID_ENTIDADE`.

| Campo                         | Tipo lógico    | Obrigatório  | Descrição                                                                                                                             |
| ----------------------------- | --------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `ID_TESTE_ETIQUETAGEM`      | Inteiro         | Sim           | Chave primária - TB_TESTE_ETIQUETAGEM. Identificador gerado automaticamente.                                                           |
| `ID_EVENTO`                 | Inteiro         | Sim           | Chave estrangeira para `TB_EVENTO.ID_EVENTO`. Evento do teste, obtido do contexto da aplicação.                                     |
| `ID_ENTIDADE`               | Inteiro         | Sim           | Chave estrangeira para `TB_ENTIDADE.ID_ENTIDADE`. Entidade responsável pelo equipamento testado.                                     |
| `CO_LICENCA`                | Código textual | Sim, proposto | Chave estrangeira para `TB_LICENCA.CO_LICENCA`. Enquadramento selecionado entre UTE, Outorgado, Não Outorgado e Radiação Restrita. |
| `CO_TIPO_EQUIPAMENTO`       | Código textual | Sim           | Chave estrangeira para `TB_TIPO_EQUIPAMENTO.CO_TIPO_EQUIPAMENTO`. Tipo escolhido no seletor Tipo do equipamento.                      |
| `CO_PERMISSAO`              | Código textual | Sim, proposto | Chave estrangeira para `TB_PERMISSAO_ETIQUETA.CO_PERMISSAO`. Opção escolhida em Status da etiqueta.                                 |
| `DE_LOCAL`                  | Texto curto     | Sim           | Local do evento ao qual o teste e a permissão se referem. Confirmar se o campo identifica uma localidade cadastrada.                   |
| `IC_EQUIPAMENTO_HOMOLOGADO` | Booleano        | Sim, proposto | Informa se o equipamento é homologado. Valores: 0 - Não; 1 - Sim. Corresponde à caixa Equipamento homologado.                        |
| `QT_EQUIPAMENTO`            | Inteiro         | Sim           | Quantidade de equipamentos iguais sendo etiquetados. A tela apresenta inicialmente 1.                                                   |
| `TX_OBSERVACAO`             | Texto longo     | Não          | Observações e características complementares do equipamento.                                                                         |
| `DH_CRIACAO`                | Data e hora     | Sim           | Momento de criação do teste, preenchido automaticamente pela aplicação.                                                             |

O número inicial da etiqueta e o número final exibidos no formulário serão representados pelos registros individuais de `TB_TESTE_ETIQUETAGEM_ETIQUETA`, conforme a proposta abaixo. Não confundir a permissão da etiqueta com os estados de tratamento de emissões e incidentes.

### Tabela `TB_TESTE_ETIQUETAGEM_FREQUENCIA`

Armazena cada frequência adicionada no popup **Adicionar frequência**, com sua largura de banda e classificação própria da etiquetagem. Um teste possui uma ou mais linhas nesta tabela; cada linha pertence a um único teste. Duas frequências adicionadas pelo botão `+` geram dois registros dependentes, e não duas colunas no teste.

| Campo                               | Tipo lógico               | Obrigatório   | Descrição                                                                                                                                    |
| ----------------------------------- | -------------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `ID_TESTE_ETIQUETAGEM_FREQUENCIA` | Inteiro                    | Sim            | Chave primária - TB_TESTE_ETIQUETAGEM_FREQUENCIA. Identificador gerado automaticamente.                                                       |
| `ID_TESTE_ETIQUETAGEM`            | Inteiro                    | Sim            | Chave estrangeira - TB_TESTE_ETIQUETAGEM. Identifica o teste ao qual a frequência pertence.                                                   |
| `VR_LARGURA_KHZ` ou `CO_BANDA`  | Decimal ou código textual | Sim, a definir | Escolher uma única representação: valor decimal em kHz, alinhado a `TB_EMISSAO.VR_LARGURA_KHZ`, ou código estrangeiro para `TB_BANDA`. |
| `CO_CLASSIFICACAO`                | Código textual            | Sim, proposto  | Chave estrangeira para `TB_CLASSIFICACAO_TESTE`; domínio específico da etiquetagem.                                                        |
| `VR_FREQUENCIA_MHZ`               | Decimal                    | Sim            | Frequência central informada no popup, em megahertz (MHz).                                                                                    |
| `DH_CRIACAO`                      | Data e hora                | Sim            | Momento de inclusão da frequência no teste, preenchido pela aplicação.                                                                     |

A largura de banda pertence a cada frequência, não ao teste inteiro, e deve ser representada de forma consistente com `TB_EMISSAO.VR_LARGURA_KHZ`. A reunião não definiu se o seletor será um valor decimal em kHz ou um código referenciado; confirmar a representação antes do modelo físico e não manter duas representações divergentes.

### Domínios e Relacionamentos Complementares

| Objeto proposto                   | Finalidade e dados                                                                                                                                                                                                                                                                                                                 |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TB_PERFIL_ENTIDADE`            | Domínio com chave `CO_PERFIL` e descrição `DE_PERFIL`. Representa as três opções de perfil exibidas.                                                                                                                                                                                                                     |
| `TB_LICENCA`                    | Domínio com chave `CO_LICENCA` e descrição `DE_LICENCA`. Representa os quatro enquadramentos exibidos, não um número de licença individual.                                                                                                                                                                              |
| `TB_TIPO_EQUIPAMENTO`           | Domínio com chave `CO_TIPO_EQUIPAMENTO` e descrição `DE_TIPO_EQUIPAMENTO`. Opções a confirmar.                                                                                                                                                                                                                            |
| `TB_PERMISSAO_ETIQUETA`         | Domínio com chave `CO_PERMISSAO` e descrição `DE_PERMISSAO`. Opções visíveis: Permitido em um local; Permitido em todos; Não permitido. Confirmar a redação e o alcance de todos os locais.                                                                                                                           |
| `TB_BANDA`                      | Representação da largura de banda, caso a opção final seja um código de domínio; alinhar unidade e significado com `VR_LARGURA_KHZ` da emissão.                                                                                                                                                                           |
| `TB_CLASSIFICACAO_TESTE`        | Domínio próprio da classificação da etiquetagem, com código e descrição a definir; não compartilhar automaticamente com a classificação de emissão.                                                                                                                                                                     |
| `TB_TESTE_ETIQUETAGEM_ETIQUETA` | Registros individuais das etiquetas de um teste. Proposta: chave simples `ID_TESTE_ETIQUETAGEM_ETIQUETA`, referência `ID_TESTE_ETIQUETAGEM` e código textual `CO_ETIQUETA`, preservando zeros iniciais. A quantidade e o intervalo apresentados no formulário orientam a geração, cuja regra ainda deve ser confirmada. |
| `TB_TESTE_ETIQUETAGEM_ANEXO`    | Anexos opcionais do equipamento. Chave `ID_TESTE_ETIQUETAGEM_ANEXO`, referência `ID_TESTE_ETIQUETAGEM` e metadados. Formatos e armazenamento ainda precisam de definição.                                                                                                                                                   |

Os domínios devem ter códigos e descrições documentados e chaves sem autoincremento quando tiverem menos de 30 registros. Valores não binários são referências a tabelas de domínio, não listas em campos de texto nem enumerações em restrições `CHECK`.

### Chaves e Índices

- Chave primária do teste: `PK_TB_TESTE_ETIQUETAGEM`, em `ID_TESTE_ETIQUETAGEM`.
- Chave primária da frequência: `PK_TB_TESTE_ETIQUETAGEM_FREQUENCIA`, em `ID_TESTE_ETIQUETAGEM_FREQUENCIA`.
- Vínculo da frequência com o teste: `FK_TB_TESTE_ETIQUETAGEM_FREQUENCIA_TB_TESTE_ETIQUETAGEM`, com índice `IX_TB_TESTE_ETIQUETAGEM_FREQUENCIA_01` em `ID_TESTE_ETIQUETAGEM`.
- Se for escolhido o código de domínio, criar `FK_TB_TESTE_ETIQUETAGEM_FREQUENCIA_TB_BANDA` e índice `IX_TB_TESTE_ETIQUETAGEM_FREQUENCIA_02` em `CO_BANDA`. Se for escolhido o valor decimal, usar `VR_LARGURA_KHZ` sem FK para `TB_BANDA`.
- Vínculo com a classificação: `FK_TB_TESTE_ETIQUETAGEM_FREQUENCIA_TB_CLASSIFICACAO_TESTE`, com índice `IX_TB_TESTE_ETIQUETAGEM_FREQUENCIA_03` em `CO_CLASSIFICACAO`.
- Em `TB_TESTE_ETIQUETAGEM`, criar uma chave estrangeira para cada referência: evento, entidade, licença, tipo de equipamento e permissão, usando `FK_<FILHA>_<PAI>`; criar seus índices `IX_TB_TESTE_ETIQUETAGEM_01` a `IX_TB_TESTE_ETIQUETAGEM_05`, respectivamente. O perfil é referenciado por `TB_ENTIDADE`, não pelo teste.
- Etiquetas e anexos devem possuir chave primária própria, chave estrangeira para o teste e índice dessa referência. Definir o escopo da unicidade de `CO_ETIQUETA` antes de criar seu índice único.
- Confirmar se a combinação teste, frequência normalizada, largura de banda e classificação deve ser única antes de definir um índice único adicional.

### Regras de Consistência e Etiquetagem

- O teste deve possuir ao menos uma frequência ao ser concluído, conforme o campo Frequências obrigatório. A gravação do teste e de seus registros dependentes deve ser transacional.
- O botão `+` abre o popup para incluir uma frequência com sua largura de banda e classificação própria. A edição ou remoção de uma linha não pode alterar ou remover as demais frequências do teste.
- Frequência central deve ser positiva e armazenada como decimal, não ponto flutuante. Aceitar ponto ou vírgula na entrada e normalizar antes de comparar e gravar. Confirmar a precisão; a referência anterior utiliza três casas decimais em MHz.
- `QT_EQUIPAMENTO` deve ser inteiro positivo, validado por `CC_TB_TESTE_ETIQUETAGEM_QT_EQUIPAMENTO_01`. Confirmar o valor padrão 1 e, se adotado, documentar `DF_TB_TESTE_ETIQUETAGEM_QT_EQUIPAMENTO_01`.
- A proposta é emitir uma etiqueta por equipamento. Se confirmada, a quantidade de etiquetas deve coincidir com `QT_EQUIPAMENTO`; confirmar se o número final é calculado, informado ou apenas exibido, e como funciona o intervalo de numeração.
- Validar CPF ou CNPJ quando informado, conforme o perfil aplicável, sem exigir documento brasileiro de estrangeiro por presunção. A obrigatoriedade por perfil e o uso de outro documento ainda precisam ser definidos.
- Nome, documento e contatos podem identificar pessoas naturais e devem ser classificados conforme a norma. Documentar a origem completa de dados obtidos de sistemas corporativos e evitar cópias alteráveis fora da fonte original.
- Se as opções de perfil, licença e permissão tiverem valores iniciais persistentes, documentar suas restrições de valor padrão após definir os códigos dos domínios.

### Consulta de Frequências e Alertas

- Consultar o banco para cada frequência incluída ou alterada, durante o preenchimento e novamente no salvamento. Na edição, desconsiderar o próprio registro de frequência, sem ignorar os demais registros do teste.
- Comparar frequência central e banda ocupada com equipamentos e demais cadastros aplicáveis, incluindo as emissões do mesmo evento e localidade, também quando registradas pelos fiscais de campo.
- Usar a precisão normalizada e converter frequência e largura para uma unidade comum ao verificar sobreposição. A definição da localidade e da banda deve permitir essa comparação, não apenas comparação textual de nomes.
- Alertar imediatamente o fiscal, apresentando frequência central, banda e os dados disponíveis da emissão ou cadastro conflitante, incluindo entidade, tipo, etiqueta e local quando existentes.
- O conflito é informativo: não deve impedir inclusão, edição ou conclusão do teste. A consulta de interface não substitui a verificação no backend, inclusive ao processar gravações offline/API.

### Auditoria e Pontos a Confirmar

- Registrar inclusão, edição e exclusão do teste, de cada frequência, etiqueta e anexo com origem, registro afetado, usuário, campo e valores anteriores e novos aplicáveis. Manter o vínculo com o teste para permitir consulta conjunta dessas alterações.
- Preencher a auditoria pela aplicação, normalizar valores equivalentes antes de registrar diferenças e garantir que a consulta de auditoria consiga exibir as novas operações. A estrutura será detalhada separadamente.
- Confirmar se a largura de banda será valor decimal ou referência a domínio, a unidade em kHz, a classificação específica da etiquetagem e os limites dos campos.
- A tela demonstrou SLP/VHF, SLP/UHF, SLP/800 MHz, SLP/2,4 GHz, SLP/3,7 GHz, Radiação Restrita e Outra faixa autorizada pela Anatel; validar valores e intervalos antes de definir o domínio de etiquetagem.
- Definir a representação da localidade, o alcance das permissões, o controle da numeração e a política de reserva de etiquetas para evitar duplicação em gravações simultâneas.
- Confirmar se a classificação Estrangeiro é exclusiva das opções Pessoa Física e Pessoa Jurídica ou se a nacionalidade deve ser modelada separadamente; definir como mudanças nos contatos atuais serão apresentadas ao consultar testes antigos.
- Definir como identificar o fiscal autor do teste, não exibido no recorte da tela.
