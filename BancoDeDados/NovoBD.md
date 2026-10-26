# Projeto do Banco de Dados

## Referência Normativa

Os padrões de modelagem deste projeto são os definidos em [PadroesAnatelModelagem.md](PadroesAnatelModelagem.md). Esse documento prevalece sobre [auditoria-schema.md](auditoria-schema.md), que permanece como referência auxiliar de correspondência com a estrutura anterior, não como norma.

### Nomenclatura e Regras Gerais

- Nomes em português, no singular, em caixa alta e sem acentos. Tabelas e colunas devem ter até 32 caracteres.
- Classes transacionais: `TB_` para tabelas genéricas, inclusive associativas; `TH_` para históricos; `TL_` para registros de operações; `TT_` para tabelas temporárias. O prefixo `BRIDGE_` da auditoria não integra o padrão normativo.
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

- Substituir os nomes associativos `BRIDGE_` por nomes `TB_`, atualizando referências e definindo suas chaves e índices.
- Detalhar os domínios dos seletores, especialmente a situação da emissão, e substituir descrições provisórias por referências quando aplicável.
- Completar a documentação de chaves, índices, tipos físicos, valores padrão, criação dos registros e classificação de dados pessoais.
- Definir o armazenamento externo dos anexos, mantendo no banco os metadados necessários, salvo exceção justificada.

O item 1 da norma exige Microsoft SQL Server 2014, modelo físico e SAP Power Designer 16.7 ou superior, com aprovação da Gerência de Informações e Biblioteca (GIIB) para exceções de banco. As instruções atuais do projeto mencionam PostgreSQL. Essa divergência precisa ser resolvida antes de definir o modelo físico ou gerar scripts; este documento não autoriza troca de tecnologia nem presume aprovação de exceção. Views, procedimentos, funções e gatilhos também dependem da autorização prevista na norma.

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
| Validação de latitude | `CC_TB_ESTACAO_VR_LATITUDE_01` | `VR_LATITUDE` entre -90 e 90. |
| Validação de longitude | `CC_TB_ESTACAO_VR_LONGITUDE_01` | `VR_LONGITUDE` entre -180 e 180. |

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

## Tabela `TB_EMISSAO`

Armazena os registros de emissões de radiofrequência apresentados na janela **Inserir emissão**. O nome acompanha a terminologia da tela; a referência de auditoria denomina essa entidade `TB_OCORRENCIA`. Nesta proposta, utilizam-se `TB_EMISSAO` e `ID_EMISSAO`, preservando os padrões de nomenclatura, sem criar duas entidades para o mesmo registro.

| Campo | Tipo lógico | Obrigatório | Descrição |
| --- | --- | --- | --- |
| `ID_EMISSAO` | Inteiro | Sim | Chave primária da emissão, gerada automaticamente. |
| `ID_EVENTO` | Inteiro | Sim | Chave estrangeira para `TB_EVENTO.ID_EVENTO`. Obtida do contexto do evento, embora não apareça no recorte da tela. |
| `DT_EMISSAO` | Data | Sim | Data da emissão informada no formulário. |
| `HH_EMISSAO` | Hora | Sim | Hora da emissão informada no formulário. |
| `DE_LOCAL_REGIAO` | Texto curto | Não | Local ou região da emissão. |
| `DE_ORIGEM_CAPTURA` | Texto curto | Sim | Opção selecionada em Captura realizada por. As opções e sua representação definitiva precisam ser confirmadas. |
| `ID_ESTACAO` | Inteiro | Condicional | Chave estrangeira para `TB_ESTACAO.ID_ESTACAO`, quando a captura estiver vinculada a uma estação. |
| `VR_FREQUENCIA_MHZ` | Decimal | Sim | Frequência central da emissão, em MHz. |
| `VR_LARGURA_KHZ` | Decimal | Sim | Largura de banda ocupada, em kHz, selecionada no formulário. |
| `DE_FAIXA` | Texto curto | Sim | Faixa relacionada selecionada no formulário. |
| `DE_IDENTIFICACAO` | Texto curto | Sim | Identificação selecionada para a emissão. |
| `DE_INTERFERENTE` | Texto curto | Sim | Resposta ao campo Interferente?. Mantida como texto até confirmar todas as opções do seletor. |
| `IC_UTE` | Booleano | Sim | Indica se a emissão corresponde a um usuário temporário de espectro. Tipo proposto caso o seletor UTE? contenha apenas sim e não. |
| `TX_OBSERVACAO` | Texto longo | Sim | Conteúdo do campo Entidade Resp./Contato/Observações, preservado como um único campo conforme a tela. |
| `CO_SITUACAO` | Texto curto | Sim | Código da situação da emissão, conforme os estados descritos abaixo. |

O campo Fiscal é obrigatório na tela e possui um botão `+`. A proposta admite vários fiscais participantes, armazenados no relacionamento abaixo, e não como nomes ou listas de identificadores em `TB_EMISSAO`.

### Relacionamentos

| Objeto proposto | Cardinalidade | Dados e regras |
| --- | --- | --- |
| `TB_EVENTO` | Um evento para muitas emissões | Cada emissão pertence a um evento, por `ID_EVENTO`. |
| `TB_ESTACAO` | Uma estação para muitas emissões | Vínculo opcional ou condicional por `ID_ESTACAO`; a estação deve pertencer ao mesmo evento da emissão. |
| `BRIDGE_EMISSAO_FISCAL` | Muitos para muitos entre emissões e fiscais | Colunas `ID_EMISSAO` e `ID_FISCAL`, referenciando `TB_EMISSAO` e `TB_FISCAL`. Cada par deve ser único; deve existir ao menos um fiscal por emissão. |
| `TB_EMISSAO_IMAGEM` | Uma emissão para muitas imagens | Cada imagem possui identificador próprio e referência `ID_EMISSAO`. Nome do arquivo, tipo, tamanho e forma de armazenamento serão detalhados no projeto de anexos. A inclusão de imagens é opcional. |

### Chaves

| Objeto | Nome | Definição |
| --- | --- | --- |
| Chave primária | `PK_TB_EMISSAO` | Coluna `ID_EMISSAO`. |
| Chave estrangeira de evento | `FK_TB_EMISSAO_TB_EVENTO` | `ID_EVENTO` referenciando `TB_EVENTO.ID_EVENTO`. |
| Chave estrangeira de estação | `FK_TB_EMISSAO_TB_ESTACAO` | `ID_ESTACAO` referenciando `TB_ESTACAO.ID_ESTACAO`. |

### Situação da Emissão

- Os estados funcionais são `Pendente`, `Concluída Pelo Fiscal` e `Concluída Pelo Coordenador`. Os códigos armazenados em `CO_SITUACAO` ainda serão definidos.
- A mensagem da tela informa que emissões pendentes e concluídas pelo fiscal serão submetidas à inspeção da coordenação.
- As permissões e transições entre estados devem ser definidas antes da implementação; a imagem não permite concluir quais opções cada perfil pode selecionar.

### Regras de Consistência e Frequência

- Os campos obrigatórios não podem ser nulos; textos obrigatórios não podem conter apenas espaços.
- Frequência e largura de banda devem ser armazenadas como decimais, não como ponto flutuante. A frequência deve ser positiva; os valores permitidos para a largura dependem das opções do seletor.
- A entrada de frequência deve aceitar ponto ou vírgula decimal e ser normalizada antes da comparação e da gravação. A referência utiliza três casas decimais para frequência em MHz e largura em kHz; essa precisão deve ser confirmada para o novo sistema.
- Toda frequência incluída ou alterada deve ser consultada no banco durante o preenchimento e novamente no salvamento, inclusive nos fluxos offline/API ao processar a gravação. Na edição, desconsiderar o próprio registro.
- Verificar conflitos com equipamentos, emissões e demais cadastros aplicáveis, usando a precisão normalizada e considerando sobreposição entre frequência central e largura de banda, com conversão de MHz e kHz para uma unidade comum.
- Os alertas devem identificar a entidade conflitante, seu tipo, etiqueta e local quando disponíveis. São informativos e não devem impedir a conclusão do cadastro por conflito de frequência.
- Inclusões, edições, exclusões, mudanças de situação e alterações nos vínculos de fiscais e imagens devem gerar auditoria com origem, registro, usuário e valores anteriores e novos aplicáveis. A consulta de auditoria deve permitir exibir essas ações; sua estrutura será detalhada separadamente.
- Antes de registrar diferenças na auditoria, normalizar valores nulos, vazios e equivalentes, evitando alterações fictícias.

### Pontos a Confirmar

- Opções dos seletores Captura realizada por, Faixa relacionada, Identificação, Interferente? e UTE?, incluindo eventuais respostas além de sim e não.
- Quais seletores terão tabelas de domínio próprias, substituindo as descrições por chaves estrangeiras.
- Como a seleção da origem da captura determina o vínculo com uma estação.
- Se os fiscais selecionáveis devem estar vinculados previamente ao evento e se haverá distinção entre fiscal participante e autor do cadastro.
- Se entidade responsável e contato devem ser separados de observações em campos próprios.
- Campos condicionais de UTE, limites de tamanho, valores padrão, fuso horário e precisão dos valores numéricos.

## Tabela `TB_FISCAL`

Armazena o cadastro global dos fiscais apresentado na janela **Fiscais cadastrados**, com nome, unidade Anatel e papéis permitidos. O mesmo fiscal pode participar de vários eventos sem duplicação de seu cadastro.

A tela não apresenta asteriscos de obrigatoriedade. As indicações abaixo são propostas de consistência a confirmar, e os tipos permanecem lógicos.

| Campo | Tipo lógico | Obrigatório proposto | Descrição |
| --- | --- | --- | --- |
| `ID_FISCAL` | Inteiro | Sim | Chave primária do fiscal, gerada automaticamente. |
| `NO_FISCAL` | Texto curto | Sim | Nome do fiscal. Corresponde ao campo Nome. |
| `SG_UNIDADE_EXECUTANTE` | Texto curto | Sim | Chave estrangeira para `TB_UNIDADE_EXECUTANTE.SG_UNIDADE_EXECUTANTE`. Corresponde à GR ou UO selecionada em Local Anatel. |
| `IC_COORDENACAO` | Booleano | Sim | Indica se o fiscal pode exercer o papel de Coordenação. |
| `IC_ABORDAGEM` | Booleano | Sim | Indica se o fiscal pode exercer o papel de Abordagem. |
| `IC_MONITORACAO` | Booleano | Sim | Indica se o fiscal pode exercer o papel de Monitoração. |

Nesta proposta, os três papéis fixos da tela são representados por indicadores independentes, em vez da coleção `CO_PAPEIS` existente na referência de auditoria. A nomenclatura segue os prefixos da referência, mas a forma de armazenamento é uma proposta para o novo sistema. Indicador desmarcado corresponde a falso, não a valor nulo.

### Relacionamentos

| Objeto | Cardinalidade | Dados e regras |
| --- | --- | --- |
| `TB_UNIDADE_EXECUTANTE` | Uma unidade para muitos fiscais | Cada fiscal referencia uma unidade por `SG_UNIDADE_EXECUTANTE`. A descrição exibida em Local Anatel vem do cadastro da unidade, sem duplicação em `TB_FISCAL`. |
| `BRIDGE_EVENTO_FISCAL` | Muitos para muitos entre eventos e fiscais | Reutiliza `ID_EVENTO` e `ID_FISCAL`, com os indicadores das funções exercidas naquele evento. |
| `BRIDGE_EMISSAO_FISCAL` | Muitos para muitos entre emissões e fiscais | Reutiliza `ID_EMISSAO` e `ID_FISCAL` para identificar os participantes da emissão. |

### Papéis Permitidos e Funções no Evento

- Em `TB_FISCAL`, os indicadores representam os papéis que o fiscal pode exercer de forma geral.
- Em `BRIDGE_EVENTO_FISCAL`, os indicadores representam as funções selecionadas para um evento específico. Participar de um evento não altera automaticamente as permissões globais do fiscal.
- Como regra proposta, uma função somente pode ser atribuída no evento se o respectivo papel estiver permitido no cadastro do fiscal.
- A coluna Função no evento exibida na lista deve ser obtida do vínculo com o evento em contexto, se esse for seu significado funcional. Como a janela também apresenta os rótulos Lista global de fiscais e Papéis permitidos, essa interpretação precisa ser confirmada.

### Chaves e Regras de Consistência

| Objeto | Nome | Definição |
| --- | --- | --- |
| Chave primária | `PK_TB_FISCAL` | Coluna `ID_FISCAL`. |
| Chave estrangeira de unidade | `FK_TB_FISCAL_TB_UNIDADE_EXECUTANTE` | `SG_UNIDADE_EXECUTANTE` referenciando a chave de mesmo nome em `TB_UNIDADE_EXECUTANTE`. |

- O nome não deve conter apenas espaços. Não se propõe unicidade por nome, pois podem existir homônimos.
- A unidade selecionada deve existir em seu cadastro de referência.
- A ação Excluir não deve apagar em cascata participações, emissões ou outros registros históricos. O tratamento de fiscais já vinculados depende da política de exclusão ou desativação a definir.
- Inclusão, edição, exclusão ou desativação do fiscal e alterações de unidade, papéis e vínculos devem gerar auditoria com origem, registro, usuário, campo e valores anteriores e novos aplicáveis. A consulta de auditoria deve permitir exibir essas ações; sua estrutura será detalhada separadamente.
- A auditoria deve normalizar valores nulos, vazios e equivalentes antes de registrar diferenças.

### Pontos a Confirmar

- Obrigatoriedade de nome e unidade, tamanho dos campos e necessidade de selecionar pelo menos um papel.
- Valores padrão dos indicadores de papéis e possibilidade de novos papéis além dos três exibidos.
- Se Função no evento apresenta as atribuições do evento em contexto ou apenas os papéis globais permitidos.
- Necessidade de matrícula ou outro identificador institucional para distinguir fiscais homônimos.
- Política de exclusão ou desativação e tratamento de vínculos existentes quando uma permissão global for retirada.

## Tabela `TB_INCIDENTE`

Armazena os incidentes identificados durante a fiscalização, conforme a janela **Registrar incidente**, incluindo bloqueadores de sinal (BSR), também conhecidos como bloqueadores intencionais ou jammers, e estações rádio-base falsas (ERB Fake). A lista completa de tipos ainda deve ser confirmada.

Os tipos abaixo são lógicos. O vínculo com o evento e a data e hora de criação são dados de contexto e rastreabilidade, não campos apresentados no recorte da tela.

| Campo | Tipo lógico | Obrigatório | Descrição |
| --- | --- | --- | --- |
| `ID_INCIDENTE` | Inteiro | Sim | Chave primária - TB_INCIDENTE. Identificador gerado automaticamente. |
| `ID_EVENTO` | Inteiro | Sim | Chave primária - TB_EVENTO. Identifica o evento em cujo contexto o incidente foi registrado. |
| `CO_TIPO_INCIDENTE` | Código textual | Sim | Chave primária - TB_TIPO_INCIDENTE. Classifica o incidente conforme o seletor Tipo. |
| `CO_SITUACAO` | Código textual | Sim | Chave primária - TB_SITUACAO. Representa o estado de tratamento escolhido em Status. |
| `DE_LOCAL` | Texto curto | Sim | Descrição do local onde o incidente foi identificado. |
| `VR_LATITUDE` | Decimal | Não | Latitude do incidente em graus decimais, entre -90 e 90. |
| `VR_LONGITUDE` | Decimal | Não | Longitude do incidente em graus decimais, entre -180 e 180. |
| `GE_PONTO` | Geometria de ponto | Condicional | Posição formada pelas coordenadas, conforme o item 7.6.5 da norma. Deve existir quando o par de coordenadas estiver informado. |
| `TX_OBSERVACAO` | Texto longo | Sim | Informações descritivas sobre o incidente e as circunstâncias observadas. |
| `DH_CRIACAO` | Data e hora | Sim | Momento de criação do registro, preenchido automaticamente pela aplicação. Não representa necessariamente o momento em que o incidente ocorreu. |

### Domínios

- `TB_TIPO_INCIDENTE` terá a chave `CO_TIPO_INCIDENTE` e a descrição `DE_TIPO_INCIDENTE`. A opção visível na tela é Bloqueador de sinal (BSR); os demais valores e códigos devem ser confirmados. Para um domínio com menos de 30 registros, não utilizar autoincremento na chave.
- `TB_SITUACAO` terá a chave `CO_SITUACAO` e a descrição `DE_SITUACAO`, compartilhando os estados funcionais com as emissões: Pendente; Concluída Pelo Fiscal; Concluída Pelo Coordenador. Os códigos ainda serão definidos.
- Os códigos devem ser validados por chaves estrangeiras, não por listas em colunas nem por restrições `CHECK` enumerando opções.
- O compartilhamento de `TB_SITUACAO` exige adequar posteriormente a referência `CO_SITUACAO` de `TB_EMISSAO`, ainda descrita de forma preliminar.

### Relacionamentos

| Objeto proposto | Cardinalidade | Dados e regras |
| --- | --- | --- |
| `TB_EVENTO` | Um evento para muitos incidentes | Cada incidente pertence a um evento por `ID_EVENTO`. |
| `TB_TIPO_INCIDENTE` | Um tipo para muitos incidentes | Cada incidente possui um tipo por `CO_TIPO_INCIDENTE`. |
| `TB_SITUACAO` | Uma situação para muitos incidentes | Cada incidente possui uma situação atual por `CO_SITUACAO`. |
| `TB_INCIDENTE_FISCAL` | Muitos para muitos entre incidentes e fiscais | Chave simples `ID_INCIDENTE_FISCAL`, gerada automaticamente, e referências `ID_INCIDENTE` e `ID_FISCAL`. Criar índice único para o par incidente/fiscal. Deve existir ao menos um participante, conforme o campo Fiscal obrigatório e seu botão `+`. |
| `TB_INCIDENTE_IMAGEM` | Um incidente para muitas imagens | Cada foto possui identificador próprio `ID_INCIDENTE_IMAGEM` e referência `ID_INCIDENTE`. Armazenar metadados e referência ao arquivo externo; o conteúdo binário no banco depende de exceção justificada. Fotos são opcionais. |

### Chaves, Índices e Validações

| Objeto | Nome | Definição |
| --- | --- | --- |
| Chave primária | `PK_TB_INCIDENTE` | Coluna `ID_INCIDENTE`. |
| Chave estrangeira de evento | `FK_TB_INCIDENTE_TB_EVENTO` | `ID_EVENTO` referenciando `TB_EVENTO.ID_EVENTO`. |
| Chave estrangeira de tipo | `FK_TB_INCIDENTE_TB_TIPO_INCIDENTE` | `CO_TIPO_INCIDENTE` referenciando a chave de mesmo nome em `TB_TIPO_INCIDENTE`. |
| Chave estrangeira de situação | `FK_TB_INCIDENTE_TB_SITUACAO` | `CO_SITUACAO` referenciando a chave de mesmo nome em `TB_SITUACAO`. |
| Índice de evento | `IX_TB_INCIDENTE_01` | Coluna `ID_EVENTO`. |
| Índice de tipo | `IX_TB_INCIDENTE_02` | Coluna `CO_TIPO_INCIDENTE`. |
| Índice de situação | `IX_TB_INCIDENTE_03` | Coluna `CO_SITUACAO`. |
| Índice espacial | `IX_TB_INCIDENTE_04` | Campo `GE_PONTO`. Implementação dependente do banco escolhido. |
| Validação de latitude | `CC_TB_INCIDENTE_VR_LATITUDE_01` | Quando informada, latitude entre -90 e 90. |
| Validação de longitude | `CC_TB_INCIDENTE_VR_LONGITUDE_01` | Quando informada, longitude entre -180 e 180. |

As associativas e tabelas dependentes também deverão possuir suas chaves estrangeiras e índices por referência no detalhamento físico.

### Regras de Consistência, Fotos e Auditoria

- Tipo, local, observações e situação são obrigatórios na tela. Textos obrigatórios não podem conter apenas espaços. O vínculo com ao menos um fiscal deve ser validado junto à gravação do incidente.
- Latitude e longitude não são obrigatórias na tela. Como proposta, quando houver localização por coordenadas, exigir o par completo e manter `GE_PONTO` consistente com seus valores; confirmar essa regra antes da implementação.
- O botão `+` de Local sugere um controle auxiliar, mas não comprova a existência de cadastro próprio. Caso seja confirmado, substituir `DE_LOCAL` por uma referência ao cadastro de locais.
- A tela apresenta Pendente como seleção inicial. Confirmar se isso deve ser um valor padrão persistente; nesse caso, documentar a restrição `DF_TB_INCIDENTE_CO_SITUACAO_01` com o código correspondente.
- A conclusão pelo fiscal e a conclusão pelo coordenador são estados distintos; as permissões e transições devem ser detalhadas sem presumir que todos os perfis possam selecionar todos os estados.
- Fotos devem receber nomes no formato `NomeEvento_Classificacao_ID_Registro_Data_Hora_Sequencia.extensao`, preservando a extensão original e substituindo caracteres inválidos por `_`. A exclusão de uma foto exige confirmação, auditoria própria e não pode excluir o incidente nem outras fotos.
- Inclusões, edições, exclusões, mudanças de situação e alterações nos vínculos de fiscais e fotos devem registrar auditoria com origem, registro afetado, usuário, campo e valores anteriores e novos aplicáveis. Preencher a auditoria pela aplicação e garantir sua exibição na consulta; sua estrutura será detalhada separadamente.
- Normalizar valores nulos, vazios e equivalentes antes de comparar alterações para auditoria, evitando registros de diferenças fictícias.

### Pontos a Confirmar

- Lista completa e códigos dos tipos de incidente, códigos das situações e seleção inicial persistente.
- Se os fiscais participantes devem estar previamente vinculados ao evento e como identificar separadamente o autor do cadastro.
- Existência de cadastro próprio de locais, tamanho dos textos e precisão das coordenadas.
- Sistema de referência espacial, ordem das coordenadas e regras de atualização do ponto geométrico.
- Limites, formatos e armazenamento dos arquivos, política de exclusão ou desativação e estrutura de auditoria.

## Tabela `TB_TESTE_ETIQUETAGEM`

Armazena o teste e a etiquetagem de um equipamento ou conjunto de equipamentos iguais, conforme a janela **Teste e etiquetagem**. Cada teste pertence a um evento e pode possuir várias frequências, adicionadas individualmente pelo botão `+` ao lado de Frequências. As frequências são registros dependentes, descritos na tabela `TB_TESTE_ETIQUETAGEM_FREQUENCIA`, e não uma coluna multivalorada do teste.

Os tipos são lógicos. As obrigatoriedades sem indicação explícita na imagem e as regras de geração de etiquetas permanecem propostas a confirmar. Os campos do formulário são mantidos como dados do teste nesta etapa; avaliar um cadastro próprio da entidade se ela for reutilizada entre testes.

| Campo | Tipo lógico | Obrigatório | Descrição |
| --- | --- | --- | --- |
| `ID_TESTE_ETIQUETAGEM` | Inteiro | Sim | Chave primária - TB_TESTE_ETIQUETAGEM. Identificador gerado automaticamente. |
| `ID_EVENTO` | Inteiro | Sim | Chave primária - TB_EVENTO. Evento do teste, obtido do contexto da aplicação. |
| `CO_PERFIL` | Código textual | Sim, proposto | Chave primária - TB_PERFIL_ENTIDADE. Opção escolhida entre Pessoa Física, Pessoa Jurídica e Estrangeiro. |
| `CO_LICENCA` | Código textual | Sim, proposto | Chave primária - TB_LICENCA. Enquadramento selecionado entre usuário temporário de espectro (UTE), Outorgado, Não Outorgado e Radiação Restrita. |
| `CO_TIPO_EQUIPAMENTO` | Código textual | Sim | Chave primária - TB_TIPO_EQUIPAMENTO. Tipo escolhido no seletor Tipo do equipamento. |
| `CO_PERMISSAO` | Código textual | Sim, proposto | Chave primária - TB_PERMISSAO_ETIQUETA. Opção escolhida em Status da etiqueta. |
| `CO_CPF_CNPJ` | Texto curto | Não na tela; validar condição | Cadastro de Pessoas Físicas (CPF) ou Cadastro Nacional da Pessoa Jurídica (CNPJ), conforme o perfil selecionado. Armazenar como texto, preservando zeros iniciais. |
| `NO_ENTIDADE` | Texto curto | Sim | Nome da pessoa ou entidade à qual se refere o equipamento testado. |
| `NO_RESPONSAVEL_CONTATO` | Texto curto | Não | Nome do responsável informado para contato. |
| `CO_TELEFONE` | Texto curto | Não | Telefone de contato, incluindo código de país e de área quando informados. Não armazenar como número inteiro. |
| `ED_EMAIL` | Texto curto | Não | Endereço de correio eletrônico para contato. |
| `DE_LOCAL` | Texto curto | Sim | Local do evento ao qual o teste e a permissão se referem. Confirmar se o campo identifica uma localidade cadastrada. |
| `IC_EQUIPAMENTO_HOMOLOGADO` | Booleano | Sim, proposto | Informa se o equipamento é homologado. Valores: 0 - Não; 1 - Sim. Corresponde à caixa Equipamento homologado. |
| `QT_EQUIPAMENTO` | Inteiro | Sim | Quantidade de equipamentos iguais sendo etiquetados. A tela apresenta inicialmente 1. |
| `TX_OBSERVACAO` | Texto longo | Não | Observações e características complementares do equipamento. |
| `DH_CRIACAO` | Data e hora | Sim | Momento de criação do teste, preenchido automaticamente pela aplicação. |

O número inicial da etiqueta e o número final exibidos no formulário serão representados pelos registros individuais de `TB_TESTE_ETIQUETAGEM_ETIQUETA`, conforme a proposta abaixo. Não confundir a permissão da etiqueta com os estados de tratamento de emissões e incidentes.

### Tabela `TB_TESTE_ETIQUETAGEM_FREQUENCIA`

Armazena cada frequência adicionada no popup **Adicionar frequência**, com sua banda e faixa. Um teste possui uma ou mais linhas nesta tabela; cada linha pertence a um único teste. Duas frequências adicionadas pelo botão `+` geram dois registros dependentes, e não duas colunas no teste.

| Campo | Tipo lógico | Obrigatório | Descrição |
| --- | --- | --- | --- |
| `ID_TESTE_ETIQUETAGEM_FREQUENCIA` | Inteiro | Sim | Chave primária - TB_TESTE_ETIQUETAGEM_FREQUENCIA. Identificador gerado automaticamente. |
| `ID_TESTE_ETIQUETAGEM` | Inteiro | Sim | Chave primária - TB_TESTE_ETIQUETAGEM. Identifica o teste ao qual a frequência pertence. |
| `CO_BANDA` | Código textual | Sim, proposto | Chave primária - TB_BANDA. Banda selecionada para esta frequência; confirmar a unidade e os valores do seletor. |
| `CO_FAIXA` | Código textual | Sim, proposto | Chave primária - TB_FAIXA. Faixa selecionada para esta frequência. |
| `VR_FREQUENCIA_MHZ` | Decimal | Sim | Frequência central informada no popup, em megahertz (MHz). |
| `DH_CRIACAO` | Data e hora | Sim | Momento de inclusão da frequência no teste, preenchido pela aplicação. |

A banda pertence a cada frequência, não ao teste inteiro. Se o seletor Banda representar a largura de banda ocupada, `TB_BANDA` deverá disponibilizar seu valor decimal e unidade, por exemplo `VR_LARGURA_KHZ` em quilohertz (kHz), após confirmação. Não duplicar no registro dependente um valor já determinado exclusivamente pelo código da banda.

### Domínios e Relacionamentos Complementares

| Objeto proposto | Finalidade e dados |
| --- | --- |
| `TB_PERFIL_ENTIDADE` | Domínio com chave `CO_PERFIL` e descrição `DE_PERFIL`. Representa as três opções de perfil exibidas. |
| `TB_LICENCA` | Domínio com chave `CO_LICENCA` e descrição `DE_LICENCA`. Representa os quatro enquadramentos exibidos, não um número de licença individual. |
| `TB_TIPO_EQUIPAMENTO` | Domínio com chave `CO_TIPO_EQUIPAMENTO` e descrição `DE_TIPO_EQUIPAMENTO`. Opções a confirmar. |
| `TB_PERMISSAO_ETIQUETA` | Domínio com chave `CO_PERMISSAO` e descrição `DE_PERMISSAO`. Opções visíveis: Permitido em um local; Permitido em todos; Não permitido. Confirmar a redação e o alcance de todos os locais. |
| `TB_BANDA` | Domínio com chave `CO_BANDA` e descrição `DE_BANDA`, além da largura e unidade caso esse seja o significado do seletor. Uma banda pode ser referenciada por várias frequências de testes. |
| `TB_FAIXA` | Domínio com chave `CO_FAIXA` e descrição `DE_FAIXA`. Uma faixa pode ser referenciada por várias frequências de testes. |
| `TB_TESTE_ETIQUETAGEM_ETIQUETA` | Registros individuais das etiquetas de um teste. Proposta: chave simples `ID_TESTE_ETIQUETAGEM_ETIQUETA`, referência `ID_TESTE_ETIQUETAGEM` e código textual `CO_ETIQUETA`, preservando zeros iniciais. A quantidade e o intervalo apresentados no formulário orientam a geração, cuja regra ainda deve ser confirmada. |
| `TB_TESTE_ETIQUETAGEM_IMAGEM` | Fotos opcionais do equipamento. Chave `ID_TESTE_ETIQUETAGEM_IMAGEM`, referência `ID_TESTE_ETIQUETAGEM`, metadados e endereço do arquivo externo. Evitar conteúdo binário no banco, salvo exceção justificada. |

Os domínios devem ter códigos e descrições documentados e chaves sem autoincremento quando tiverem menos de 30 registros. Valores não binários são referências a tabelas de domínio, não listas em campos de texto nem enumerações em restrições `CHECK`.

### Chaves e Índices

- Chave primária do teste: `PK_TB_TESTE_ETIQUETAGEM`, em `ID_TESTE_ETIQUETAGEM`.
- Chave primária da frequência: `PK_TB_TESTE_ETIQUETAGEM_FREQUENCIA`, em `ID_TESTE_ETIQUETAGEM_FREQUENCIA`.
- Vínculo da frequência com o teste: `FK_TB_TESTE_ETIQUETAGEM_FREQUENCIA_TB_TESTE_ETIQUETAGEM`, com índice `IX_TB_TESTE_ETIQUETAGEM_FREQUENCIA_01` em `ID_TESTE_ETIQUETAGEM`.
- Vínculo com a banda: `FK_TB_TESTE_ETIQUETAGEM_FREQUENCIA_TB_BANDA`, com índice `IX_TB_TESTE_ETIQUETAGEM_FREQUENCIA_02` em `CO_BANDA`.
- Vínculo com a faixa: `FK_TB_TESTE_ETIQUETAGEM_FREQUENCIA_TB_FAIXA`, com índice `IX_TB_TESTE_ETIQUETAGEM_FREQUENCIA_03` em `CO_FAIXA`.
- Em `TB_TESTE_ETIQUETAGEM`, criar uma chave estrangeira para cada referência: evento, perfil, licença, tipo de equipamento e permissão, usando `FK_<FILHA>_<PAI>`; criar seus índices `IX_TB_TESTE_ETIQUETAGEM_01` a `IX_TB_TESTE_ETIQUETAGEM_05`, respectivamente.
- Etiquetas e imagens devem possuir chave primária própria, chave estrangeira para o teste e índice dessa referência. Definir o escopo da unicidade de `CO_ETIQUETA` antes de criar seu índice único.
- Confirmar se a combinação teste, frequência normalizada, banda e faixa deve ser única antes de definir um índice único adicional.

### Regras de Consistência e Etiquetagem

- O teste deve possuir ao menos uma frequência ao ser concluído, conforme o campo Frequências obrigatório. A gravação do teste e de seus registros dependentes deve ser transacional.
- O botão `+` abre o popup para incluir uma frequência com seus próprios valores de banda e faixa. A edição ou remoção de uma linha não pode alterar ou remover as demais frequências do teste.
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

- Registrar inclusão, edição e exclusão do teste, de cada frequência, etiqueta e foto com origem, registro afetado, usuário, campo e valores anteriores e novos aplicáveis. Manter o vínculo com o teste para permitir consulta conjunta dessas alterações.
- Preencher a auditoria pela aplicação, normalizar valores equivalentes antes de registrar diferenças e garantir que a consulta de auditoria consiga exibir as novas operações. A estrutura será detalhada separadamente.
- Confirmar os códigos dos domínios, a unidade e obrigatoriedade de Banda e Faixa no popup, o vínculo entre faixa e banda e os limites dos campos.
- Definir a representação da localidade, o alcance das permissões, o controle da numeração e a política de reserva de etiquetas para evitar duplicação em gravações simultâneas.
- Confirmar se a classificação Estrangeiro é exclusiva das opções Pessoa Física e Pessoa Jurídica ou se a nacionalidade deve ser modelada separadamente.
- Definir se a entidade e seus contatos serão cadastros reutilizáveis ou dados históricos específicos do teste, e como identificar o fiscal autor, não exibido no recorte da tela.
