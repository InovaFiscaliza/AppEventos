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
