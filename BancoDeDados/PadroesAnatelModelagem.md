# TIC - Dados: Padrões de Modelagem de Bancos de Dados

**Área:** Administração de Dados  
**Publicado em:** 06/10/26  
**Autor:** Elvis Soriano Rodrigues — Servidor(a)

## 1. Definições gerais

1.1. O SGBD (Sistema Gerenciador de Banco de Dados) deve ser o Microsoft SQL Server 2014. Casos excepcionais devem ser justificados e aprovados pela GIIB (Gerência de Informações e Biblioteca).

1.2. A ferramenta homologada pela Anatel para a elaboração dos modelos de dados é o SAP Power Designer, na versão 16.7 ou superior;

1.3. Os modelos de dados serão construídos apenas em Modelo Físico, seguindo as orientações deste documento.

## 2. Criação de objetos

### 2.1. Orientação para criação de tabelas

2.1.1. As tabelas devem seguir regras de normalização dos dados, buscando alcançar ao menos a terceira forma normal.

2.1.2. Os modelos de dados analíticos (dimensionais) devem seguir o padrão de esquema em estrela. É proibido o uso de modelagem em snow-flake.

2.1.3. As tabelas do tipo stage oriundas de coletas devem refletir o conteúdo da fonte de dados original, sem alterações ou transformações.

2.1.4. As tabelas do tipo stage para tratamento de dados para uso no DW seguem as definições dos demais tipos de tabelas.

2.1.5. Usar obrigatoriamente tabelas de domínio (chave-valor) em vez de check constraints. As colunas de domínio restrito são proibidas, exceto em situações em que os valores possíveis são binários (sim ou não, ligado ou desligado, etc.), como por exemplo o campo IC_PERMITIDO 0 (não), 1 (sim).

2.1.6. O projeto de banco de dados deve garantir que a presença de quaisquer das particularidades a seguir não seja decorrente de falhas de análise:

- Entidade isolada ou solitária;
- Relacionamento paralelo;
- Entidade de “Histórico”;
- Entidade de “LOG”.

2.1.7. Tabelas de Histórico são aquelas que mantém a situação anterior de um registro, guardando informações sobre o responsável pela alteração e o momento em que ocorreu.

2.1.8. Tabelas de Log são aquelas que mantém informações sobre operações realizadas no sistema. Neste caso verificar se existe a possibilidade de utilização de arquivos físicos.

2.1.9. As tabelas temporárias devem ser utilizadas quando os dados a serem armazenados têm uma característica de existência apenas para um processamento específico, sendo descartados a seguir.

2.1.10. As tabelas de Log e Histórico devem preferencialmente, ser preenchidas por meio da aplicação, evitando a utilização de triggers ou procedures para este fim.

2.1.11. O projeto deve evitar a replicação de dados de outro sistema. Caso haja necessidade, é recomendado que se opte pelo uso de dados obtidos através do uso dos serviços corporativos (webservices). Como segunda opção, é possível acessar o dado com o uso de técnicas de ligação entre as bases de dados. Em último caso, a cópia dos dados através de ETL é permitida. No entanto, é expressamente proibida a alteração dos dados fora da sua fonte original.

2.1.12. Em projetos de bases de dados transacionais, as tabelas devem acrescentar sempre que possível, uma coluna que indique a data e hora de criação do registro, para auxiliar na rastreabilidade e auditoria dos dados.

2.1.13. Identificar a existência de dados pessoais sensíveis na criação da tabela, conforme orientado no item 12, para avaliação da GIIB.

2.1.14. Sempre que for identificada a existência de tabelas distintas com muitas propriedades, atributos e relacionamentos em comum, recomenda-se avaliar a possibilidade de generalização, criação de um supertipo, contendo as colunas e relacionamentos comuns.

2.1.15. É obrigatório que todas as tabelas sejam associadas a um proprietário específico, mesmo que dbo. A criação de esquemas ou proprietários que não possuam tabelas associadas não é aceita.

### 2.2. Orientação para criação de colunas

2.2.1. As colunas devem ser as necessárias para atender às necessidades apontadas pela análise do negócio.

2.2.2. As colunas que façam referência a outros sistemas da Anatel devem ser devidamente documentadas apontando a origem completa do dado.

2.2.3. Ao projetar a coluna, avaliar corretamente o seu tipo de dado, tamanho, regras de validação e se este pode assumir valores nulos.

2.2.4. Deve-se evitar a utilização de colunas multivaloradas, garantindo que o conteúdo seja acessível de forma direta e sem necessidade de tratamento ou utilização de regras.

2.2.5. No item 12 há orientações sobre como identificar se a coluna irá armazenar um dado pessoal sensível. Ao projetar o modelo de dados no Power Designer, é preciso classificar o dado armazenado na coluna como “Sensitive”, usando o campo “Personal Data Level” na opção Data Protection. Os dados que fazem relação à identificação, devem ser marcados como “Private (Identifying)”.

2.2.6. Deve-se evitar a utilização de colunas com nomes distintos, porém com a mesma finalidade em tabelas diferentes, buscando a padronização e a consistência dos dados.

Exemplo a ser evitado:

```text
IC_EXCLUIDO e IC_REMOVIDO
Tabela TB_ORGAO
IC_REMOVIDO – Campo que indica se o registro foi excluído
Tabela TB_COLABORADOR
IC_EXCLUIDO – Campo que indica se o registro foi excluído
```

2.2.7. O armazenamento de dados binários deve ser evitada, e tratada somente como exceção. Um exemplo comum é o armazenamento de códigos binários de uso apenas da aplicação para autenticação ou validação de informações, como hash ou chaves de acesso.

### 2.3. Orientação para criação de chaves

#### 2.3.1. Primárias

2.3.1.1. Todas as tabelas precisam obrigatoriamente de uma chave primária. Todas as chaves primárias devem obrigatoriamente possuir ao menos uma coluna.

2.3.1.2. Utilizar preferencialmente um campo com autoincremento para a chave primária.

2.3.1.2.1. Em Tabelas de Domínio (Chave-Valor) com poucos registros (conjunto menor que 30), optar por uma coluna sem o autoincremento como chave primária.

2.3.1.3. Dar preferência ao uso de chaves primárias com apenas um campo, evitando o uso de chaves compostas.

2.3.1.4. Especificamente em tabelas do tipo stage utilizadas no sistema Coleta, será utilizada uma chave primária composta do identificador do arquivo (NU_ARQUIVO) e do número da linha (NU_LINHA). A coluna NU_LINHA deve ser autoincremento (IDENTITY).

#### 2.3.2. Alternativas

2.3.2.1. Quando surgir necessidade deste tipo de identificação de registros, opte por utilizar índices únicos.

#### 2.3.3. Estrangeiras

2.3.3.1. Identificar todas as ligações das quais a tabela é dependente.

### 2.4. Orientação para criação de relacionamentos

2.4.1. Os relacionamentos entre as tabelas devem ser criados de forma a ligar os objetos de negócio, observando a dependência entre eles. Todos devem ser incluídos no modelo de dados, de forma explícita.

2.4.2. Deve-se evitar o surgimento de relacionamento circular entre entidades.

2.4.3. Deve-se evitar relacionamentos “um-para-um”, isso indica que as entidades podem ser unificadas em uma única tabela.

2.4.4. Não são permitidos relacionamentos obrigatórios nos dois sentidos, pois isso pode gerar problemas na inserção e na exclusão de registros.

2.4.5. Se for necessário fazer várias ligações com a mesma tabela de origem, é importante identificar a ligação na chave estrangeira e no nome da coluna, usando um sufixo que indique o propósito da ligação. O item 5.7.1.2 detalha essa definição de forma mais clara.

### 2.5. Orientação para criação de índices

2.5.1. Não são necessários índices para as chaves primárias, criadas automaticamente pelo SGBD.

2.5.2. Criar um índice para cada chave estrangeira.

2.5.3. Identificar os campos mais utilizados pelo negócio para acessar os dados da tabela e criar índices adequados.

2.5.4. Todos os índices devem possuir ao menos uma coluna associada.

### 2.6. Orientação para criação de constraints

2.6.1. A validação de dados para um campo deve ser realizada através de check constraints.

2.6.2. O valor padrão (default) de um campo deve ser documentado através de uma default constraint.

### 2.7. Orientação para criação de views, procedures, triggers e functions

2.7.1. Estão proibidos no projeto a criação de objetos desses tipos. Em situações em que seu uso seja indispensável, é exigida a autorização da GIIB.

2.7.2. A codificação desses objetos é de inteira responsabilidade da equipe de desenvolvimento de sistemas, com suas definições especificamente direcionadas às necessidades do negócio.

## 3. Documentação de objetos

3.1. A documentação é realizada por meio do campo Comment da ferramenta de modelagem de dados.

3.2. A documentação deve ser concisa, não ambígua, escrita em linguagem não técnica e utilizando a língua portuguesa.

3.3. A documentação deve evitar o uso de termos e expressões em idioma estrangeiro. Se necessário, deve-se fornecer as respectivas traduções.

3.4. A documentação deve evitar o uso de tautologia, ou seja, repetir o termo que está sendo descrito.

3.5. A documentação deve descrever o conceito do objeto, não apenas exemplos ou valores possíveis.

3.6. A documentação deve usar a terminologia do negócio, mas também ser compreensível para o leitor leigo ou não especializado.

3.7. A documentação deve explicar o que o objeto é em sua essência e com relação ao negócio. Não se deve copiar definições de fontes externas que não se aplicam ao contexto do negócio.

3.8. A documentação deve explicitar os valores possíveis do objeto, quando aplicável, especificamente no caso de indicadores ou atributos discretos.

3.9. A documentação deve usar o formato “Valor – Descrição” para listar os valores possíveis, separados por ponto e vírgula.

Exemplo:

```text
Coluna IC_ATIVO
Documentação: Indica se o registro está ativo. Valores possíveis: 1 (Sim); 2 (Não).”
Tabela TP_AGENDAMENTO_EVENTO
Documentação: Armazena os tipos de agendamento possíveis para os eventos. Valores possíveis: Recorrente; eventual; etc.
```

3.10. Ao utilizar siglas na documentação, deve-se sempre explicar o seu significado, mesmo que sejam de conhecimento comum da Agência.

3.11. Ao documentar as chaves primárias e estrangeiras, adote a expressão "Chave primária -" seguida do nome da tabela. Essa prática permite identificar de maneira eficaz todos os pontos nos quais a chave é empregada como chave estrangeira.

Exemplo:

```text
Tabela:
TB_EMPREGADO
Chave primária:
ID_EMPREGADO
Documentação: Chave primária - TB_EMPREGADO
```

## 4. Nomeação de objetos

4.1. O nome deve ser descritivo, técnico e preferencialmente em português.

4.1.1. O uso de termos técnicos considerados jargões, como no caso das palavras Link, Upload, Download, site é possível, mas deve ser avaliado junto a GIIB.

4.2. O nome deve ser escrito em letra maiúscula, sem acentuação ou caracteres especiais.

4.3. Deve ser grafado no singular, infinitivo e preferencialmente no gênero masculino.

Exemplo:

```text
Usar preferencialmente IC_BLOQUEADO ao invés de IC_BLOQUEADA.
```

4.4. O nome deve seguir as regras específicas para cada tipo de objeto de banco de dados, conforme o item 5 deste documento.

4.5. Para os objetos que possuem restrição de número de caracteres na nomeação (Tabelas e Colunas), abreviar de forma semelhante todos os demais objetos relacionados, visando dar maior clareza ao modelo de dados.

4.6. O nome em todos os objetos deve ter o mesmo valor nos campos Name, Code e, quando aplicável, Constraint Name ou Default Constraint Name.

## 5. Nomes de objetos

### 5.1. Banco de Dados

5.1.1. A criação do banco de dados é de responsabilidade da GIIB, que deve ser acionada preferencialmente pela GIDS.

5.1.2. O nome deve conter a constante DB, seguido do nome do sistema para o qual o banco está sendo projetado.

Estrutura de nomeação:

```text
DB_XX
XX = Nome do sistema de banco de dados projetado
```

Exemplo:

```text
Sistema Desempenho
Banco de dados DB_DESEMPENHO
```

### 5.2. Modelo de dados

#### 5.2.1. Transacionais

5.2.1.1. O nome deve conter a constante PDM, seguido do nome do banco onde o projeto será implantado.

Estrutura de nomeação:

```text
PDM_XX
XX = Nome do banco de dados projetado
```

Exemplo:

```text
Sistema Auditar
Banco de dados DB_AUDITAR
Modelo de dados PDM_DB_AUDITAR
```

#### 5.2.2. Analíticos

5.2.2.1. Para cada processo de carga do banco de dados analítico, deve-se construir um modelo de dados.

5.2.2.2. O nome deve conter a constante PDM, seguido do nome do processo de carga a que se refere.

5.2.2.3. Cada tabela fato deve ser projetado em um diagrama separado.

Estrutura de nomeação:

```text
PDM_XXX
PDM = Constante de Arquivo de Modelo de Dados
XX = Nome do processo ETL
```

Exemplo:

```text
ETL: EF_EMPRESAS_PPP
Modelo: PDM_EF_EMPRESAS_PPP
Tabelas Fato:
FATO_EF_PPP_SCM
FATO_EF_PPP_SEAC
FATO_EF_PPP_SMP
Diagramas:
EF_PPP_SCM
EF_PPP_SEAC
EF_PPP_SMP
```

### 5.3. Tabelas

5.3.1. Não exceder 32 caracteres no nome, abreviando quando for o caso.

5.3.2. O nome de uma entidade deve ser aquele mais apropriado para denominar uma ocorrência do conjunto.

5.3.3. A estrutura de denominação é composta pela classe da tabela abreviada e pelos termos que completam seu nome, separados por “_” (underscore).

Estrutura de nomeação:

```text
XX_XXXXXXXXXXXXXXXXXXXXXXXXXX
XX = Classe (qualificador)
YY = Termos que completam seu nome
TB_ACESSO
TB_USUARIO
```

5.3.4. Os objetos são nomeados utilizando-se de termos que não causem interpretações dúbias.

Exemplo:

```text
TB_OBJETO_FISCALIZACAO → (Correto)
TB_OBJETO → (Incorreto)
```

5.3.5. Evitar o uso de denominação em língua estrangeira, exceto em casos em que não exista correspondência na língua portuguesa.

Exemplo:

```text
TB_SITUACAO_UNIDADE → (Correto)
TB_STATUS_UNIDADE → (Inadequado)
```

5.3.6. Não é permitida a utilização de vícios de linguagem e jargão fora do contexto.

Exemplo:

```text
TB_PAGAMENTO_FUTURO → (Correto)
TB_PENDURADO → (Incorreto)
```

5.3.7. Não são utilizados nomes ou siglas de unidades/sistemas da Anatel para denominar objetos.

Exemplo:

```text
TB_RESPONSAVEL_UNIDADE → (Correto)
TB_RESPONSAVEL_GIIB → (Incorreto)
```

5.3.8. Preposições, artigos e conjunções irrelevantes para o significado do objeto não são utilizados na denominação dos objetos.

Exemplos:

```text
TB_ORGAO_ORIGEM → (Correto)
TB_ORGAO_SAIDA_COLABORADOR → (Correto)
TB_ORGAO_SAIDA_DO_COLABORADOR → (Incorreto)
```

5.3.9. Numerais devem ser representados por algarismos arábicos.

Exemplo:

```text
STAGE_ACESSO_3_SCM → (Correto)
STAGE_ACESSO_III_SCM → (Incorreto)
STAGE_ACESSO_TRES_SCM → (Incorreto)
```

5.3.10. Ao nomear tabelas transacionais que tratam do mesmo assunto, utilizar nomes semelhantes, com o objetivo de facilitar a organização.

Exemplos:

```text
Assunto: Notas no sistema Desempenho
TB_NOTA
TB_NOTA_PLANO_ENTREGA
TB_NOTA_PLANO_TRABALHO
```

5.3.11. Em modelos de dados analíticos, a regra é adicionar o assunto e, quando for o caso, acrescentar um prefixo para diferenciar de acordo com a tabela fato.

Exemplo de modelagem dimensional do CO_STFC:

```text
FATO_CO_STFC_INVENTARIO
DIM_CO_STFC_INVENTARIO_CONTA_CONTABIL
DIM_CO_STFC_INVENTARIO_MEDIDA_REFERENCIA
DIM_CO_STFC_INVENTARIO_PATRIMONIO
FATO_CO_STFC_RBR
DIM_CO_STFC_RBR_ENTIDADE
DIM_CO_STFC_RBR_ITEM
DIM_CO_STFC_RBR_QUALIFICACAO
DIM_CO_STFC_RBR_REFERENCIA
FATO_CO_STFC_RBT_RSC
DIM_CO_STFC_RBT_RSC_CLAUSULA
DIM_CO_STFC_RBT_RSC_CONTRATO
DIM_CO_STFC_RBT_RSC_EMPRESA
DIM_CO_STFC_RBT_RSC_REG_CARTORIO
DIM_CO_STFC_RBT_RSC_RELACAO_TP
```

### 5.4. Colunas

5.4.1. Não exceder 32 caracteres, abreviando quando for o caso.

5.4.2. A estrutura de denominação para o atributo é composta pela classe abreviada do atributo e pelos termos que completam seu nome, separados por “_” (underscore).

Estrutura de nomeação da coluna:

```text
Termos que completam seu nome
<Classe de valor></classe>_NOME
NO_CONSUMIDOR
NU_ORDENACAO
```

5.4.3. Deve-se utilizar de termos que não causem interpretações dúbias.

Exemplo:

```text
IC_FORMA_PAGAMENTO → (Correto)
IC_FORMA → (Incorreto)
```

5.4.4. Não deve ser utilizada denominação em língua estrangeira, exceto em casos em que não exista correspondência na língua portuguesa.

Exemplo:

```text
IC_SITUACAO_UNIDADE → (Correto)
IC_STATUS_UNIDADE → (Incorreto)
```

5.4.5. Não é permitida a utilização de vícios de linguagem e jargão fora do contexto.

Exemplo:

```text
VR_A_PAGAR → (Correto)
VR_PENDURADO → (Incorreto)
```

5.4.6. Não são utilizados nomes ou siglas de unidades/sistemas da Anatel para denominar objetos.

Exemplo:

```text
NO_RESPONSAVEL_UNIDADE → (Correto)
NO_RESPONSAVEL_GIIB → (Incorreto)
```

5.4.7. A denominação é efetuada utilizando-se de verbos no particípio quando a qualificação do nome se referir a uma ação concluída.

Exemplo:

```text
VR_TRIBUTO_FGTS_RECOLHIDO → (Correto)
VR_TRIBUTO_RECOLHER → (Incorreto)
```

5.4.8. Preposições, artigos e conjunções irrelevantes para o significado do objeto não são utilizados na denominação dos objetos.

Exemplos:

```text
NU_AGENCIA_ORIGEM → (Correto)
VR_A_PAGAR → (Correto)
NU_AGENCIA_DE_ORIGEM → (Incorreto)
```

5.4.9. Numerais devem ser representados por algarismos arábicos.

Exemplo:

```text
PC_3_MULTA_FGTS → (Correto)
PC_III_MULTA_FGTS → (Incorreto)
```

5.4.10. Os sinônimos para um mesmo contexto são evitados.

Exemplo:

```text
HH_TERMINO_JORNADA_TRABALHO → (Incorreto)
HH_FIM_JORNADA_TRABALHO → (Correto)
```

5.4.11. Os nomes devem expressar o significado preciso do seu conteúdo, de modo a não gerar ambiguidades sobre o dado representado.

Exemplo:

```text
Indicação se o empregado é Orgânico ou Terceirizado.
Solução 1: uso de uma tabela de domínio.
Solução 2: uso de um campo ic (IC_EMPREGADO_VINCULO char(1), aceitando apenas os valores ‘O’ – Orgânico e 'T’ – Terceirizado)
Solução 3: uso de um campo IC (IC_EMPREGADO_ORGANICO bit) que vai indicar 1 para orgânico e 0 para não (terceirizado).
```

5.4.12. Campos do tipo BIT só podem ser utilizados quando o dado armazenado indicar Sim ou Não. Preferencialmente os campos devem ser obrigatórios, uma vez que o valor NULL pode indicar uma terceira opção.

Exemplo:

```text
Indicação se o empregado é orgânico.
IC_EMPREGADO_ORGANICO bit, que vai indicar 1 para orgânico e 0 para não.
```

5.4.13. Na criação da tabela deve-se organizar as colunas de maneira lógica. Recomenda-se começar com as colunas da chave primária, seguidas pelas chaves estrangeiras. Na sequência, as colunas relacionadas a aspectos de negócios. Por último, incluem-se as colunas auxiliares, como DH_CARGA, ID_ARQUIVO, DH_EXCLUSAO ou IC_ATIVO. Esta estrutura facilita a compreensão e manutenção das tabelas, contribuindo para uma melhor organização e legibilidade do esquema do banco de dados.

5.4.14. Ao realizar modificações em tabelas existentes, é boa prática criar colunas acrescentando-as ao final, respeitando a ordem original da tabela. O foco principal é manter o modelo de dados alinhado com a estrutura física da tabela.

### 5.5. Constraints

#### 5.5.1. Check

5.5.1.1. O nome da verificação de dados deve indicar claramente o seu escopo, ou seja, se aplicada a colunas específicas ou a toda a tabela. No primeiro caso, a coluna deve ser mencionada no nome. No segundo caso, basta usar o nome da tabela.

Estrutura de nomeação:

```text
CC_XX_YY_99
CC = Identificador de Check Constraint
XX = Nome da tabela
YY = Coluna (Opcional quando for o caso de uma geral para a tabela)
99 = Sequencial da Constraint, iniciando do 01
TB_USUARIO_ACESSO_UNIDADE, campo IC_ACESSO_REMOTO
CC_TB_USUARIO_ACESSO_UNIDADE_IC_ACESSO_REMOTO_01
TB_USUARIO_ACESSO_UNIDADE
CC_TB_USUARIO_ACESSO_UNIDADE_01
```

#### 5.5.2. Default

5.5.2.1. A estrutura de nomeação indica a qual coluna se refere o valor padrão.

Estrutura de nomeação:

```text
DF_XX_YY_99
DF = Identificador de Default Constraint
XX = Nome da tabela
YY = Nome do campo
99 = Sequencial da Constraint, iniciando do 01
TB_USUARIO_ACESSO_UNIDADE, campo IC_ACESSO_RESTRITO
DF_TB_USUARIO_ACESSO_UNIDADE_IC_ACESSO_RESTRITO_01
```

### 5.6. Chave Primária

5.6.1. O nome deve ser grafado com a constante PK, seguido do nome da tabela.

Exemplo:

```text
Tabela: TB_COLETA
Chave Primária PK_TB_COLETA
```

### 5.7. Relacionamentos

#### 5.7.1. Coluna de ligação

5.7.1.1. Identificar na tabela filho o campo de ligação de forma igual à tabela de origem, facilitando assim a identificação da origem do dado.

Exemplo:

```text
Coluna na tabela pai: TB_TIPO_ACAO (ID_TIPO_ACAO)
Coluna na tabela filho: TB_ACAO (ID_TIPO_ACAO)
```

5.7.1.2. Quando houver mais de uma ligação com a mesma tabela de origem, deve-se acrescentar um sufixo que identifique o negócio da ligação. Deve-se observar o limite de 32 caracteres.

Exemplo:

```text
Coluna na tabela pai: TB_MOVIMENTO (ID_MOVIMENTO)
Colunas na tabela filho: TB_OCORRENCIA
ID_MOVIMENTO_FASE_ANALISE
ID_MOVIMENTO_FASE_PREPARACAO
ID_MOVIMENTO_FASE_FINAL
```

5.7.1.3. Quando houver a ligação com uma base de dados externa à estrutura do banco de dados, deve-se indicar no nome da coluna o sistema de origem do dado. A documentação deve especificar corretamente a origem do dado armazenado no campo, informando o schema, a tabela e o campo.

Exemplo do nome da coluna:

```text
Coluna na tabela pai, no banco SITARWEB : Entidade (IdtEntidade)
Coluna na tabela filho: TB_ACAO_FISCALIZACAO (ID_ENTIDADE_SITARWEB)
```

Exemplo da documentação da coluna:

```text
Identificador da entidade fiscalizada no Sitarweb. Refere-se a SITARWEB.DBO.ENTIDADE.IdtEntidade
```

5.7.1.4. Ao estabelecer conexões com a dimensão corporativa DIM_TEMPO em modelos dimensionais, é requerido que a estrutura de nomeação do campo de chave estrangeira incorpore a classe "DT" ao nome do campo.

Exemplo:

```text
Data de referência
ID_DT_REFERENCIA
```

#### 5.7.2. Nome da Constraint Foreign Key

5.7.2.1. Não há restrição do número de caracteres para o nome do objeto de relacionamento entre tabelas.

5.7.2.2. Único entre duas tabelas

Exemplo:

```text
Tabela pai: TB_TIPO_ACAO
Tabela filho: TB_ACAO
FK_TB_ACAO_TB_TIPO_ACAO
```

5.7.2.3. Várias ligações com a mesma tabela

Exemplo:

```text
Tabela pai: TB_MOVIMENTO
Tabela filho: TB_OCORRENCIA
FK_TB_OCORRENCIA_TB_MOVIMENTO_FASE_ANALISE
FK_TB_OCORRENCIA_TB_MOVIMENTO_FASE_PREPARACAO
FK_TB_OCORRENCIA_TB_MOVIMENTO_FASE_FINAL
```

5.7.2.4. Em ligação com sistema externo, não é necessário informar o nome da foreign key, pois a dependência do dado não será criada no banco de dados de forma explícita.

### 5.8. Índices

5.8.1. Os índices devem ser nomeados contendo o sufixo “IX_”, seguido do nome da tabela e um sufixo contendo um sequencial, iniciando do “_01".

Estrutura de nomeação:

```text
IX_XX_99
IX = Identificador de índice
XX = Nome da tabela
99 = Sequencial do índice, iniciando do 01
TB_ACESSO
IX_TB_ACESSO_01
```

### 5.9. Views

5.9.1. Não exceder 32 caracteres no nome, abreviando quando for o caso.

5.9.2. O nome de uma view deve ser aquele mais apropriado para denominar a visualização dos dados.

Estrutura de nomeação:

```text
VW_XX
IX = Identificador de view
XX = Nome da visualização
```

### 5.10. Procedures

5.10.1. O nome de uma procedure deve ser claro para identificar o processo negocial.

Estrutura de nomeação:

```text
SP_XX
SP = Identificador de stored procedure
XX = Nome da procedure
```

### 5.11. Funções

5.11.1. O nome de uma function deve ser claro para identificar o processo negocial.

Estrutura de nomeação:

```text
FN_XX
FN = Identificador de function
XX = Nome da function
```

### 5.12. Triggers

5.12.1. O nome de uma trigger deve ser claro para identificar o processo negocial e a tabela a qual pertence.

Estrutura de nomeação:

```text
TRG_XX_YY_9
TRG = Identificador de trigger
XX = Nome da tabela à qual está vinculada
YY = Nome negocial da trigger
9 = Sequencial, iniciando do 01
```

## 6. Classes de tabelas

### 6.1. Classes transacionais

| Nome | Abreviatura | Descrição |
| --- | --- | --- |
| Tabela | `TB` | Tabelas genéricas, destinadas a armazenar informações do sistema. |
| Histórico | `TH` | Tabelas destinadas a armazenar informações de histórico, espelhando uma outra tabela. |
| Log | `TL` | Tabelas para registro de ações realizadas no sistema. Deve identificar o momento e o responsável pelas alterações. |
| Temporária | `TT` | Tabelas destinadas a armazenar dados de forma temporária |

### 6.2. Classes analíticas

| Nome | Abreviatura | Descrição |
| --- | --- | --- |
| Dimensão | `DIM` | Tabelas destinadas a armazenar as dimensões do modelo de dados analítico. |
| Fato | `FATO` | Tabelas a armazenar os fatos negociais. |
| Stage | `STG` | Tabelas que armazenam dados brutos de outras fontes de dados sem tratamento ou validação negocial. |

## 7. Classes de colunas

Os campos serão classificados de acordo com a natureza dos dados armazenados.
Segue relação das classes de valores.

### 7.1. Classes temporais

| Nome | Abreviatura | Descrição | Tipo (SQL Server) |
| --- | --- | --- | --- |
| Ano | `AA` | Atribuída aos dados de natureza numérica que expressam o ano no calendário civil.<br>Exemplo: `AA_CONTRATO` | `smallint` |
| Dia | `DD` | Atribuída aos dados de natureza numérica que expressam o dia no calendário civil.<br>Exemplo: `DD_VENCIMENTO_PADO` | `tinynt` |
| Data/Hora | `DH` | Atribuída aos dados de que expressam o dia, mês, ano, hora, minuto e segundo.<br>Exemplo: `DH_CRIACAO_REGISTRO` | `datetime` |
| Data | `DT` | Atribuída aos dados que expressam o dia, mês e ano no calendário civil.<br>Exemplo: `DT_CADASTRO_ENTIDADE` | `date` |
| Hora | `HH` | Atribuída aos dados que expressam uma hora em qualquer formato com ou sem precisão de minutos e/ou quaisquer outras frações.<br>Exemplo: `HH_CHAMADA`<br>Importante: A documentação da coluna deve deixar claro qual é o formato e granularidade do conteúdo. | `tinyint`, `float`, `numeric`, `time` |
| Minuto | `MI` | Atribuída a dados de natureza numérica que expressam o minuto.<br>Exemplo: `MI_COLETA` | `tinynt` |
| Mês | `MM` | Atribuída aos dados de natureza numérica que expressam o mês em um calendário civil.<br>Exemplo: `MM_VENCIMENTO` | `tinynt` |

### 7.2. Classes de identificação

| Nome | Nome | Descrição | Tipo (SQL Server) |
| --- | --- | --- | --- |
| Código | `CO` | Identificador unívoco de um objeto, alfanumérico, formado por um ou mais atributos. Podem ser utilizados como chave primária, como no caso do número de CPF ou CNPJ.<br>Exemplos:<br>`CO_DEPENDENTE_EMPREGADO`<br>`CO_CPF`, `CO_CNPJ` | `char`, `varchar`, `nchar`, `nvarchar` |
| Indicador | `IC` | Atribuída aos dados de natureza binária (sim ou não, ligado ou desligado, etc.)<br>Exemplo:<br>`IC_EMPREGADO_ATIVO` | `bit` |
| Identificador | `ID` | Atribuída aos dados identificadores de registros. Comumente é parte da chave primária ou chave estrangeira. Pode ser auto incremental.<br>Exemplo:<br>`ID_ENTIDADE` | `int` ou `bigint` |
| Sigla | `SG` | Atribuída aos dados de natureza alfabética ou alfanumérica que expressam a forma sintética de um conteúdo extenso através da redução de palavras ou expressões a letras ou sílabas iniciais.<br>Exemplo: `SG_UF` | `char` ou `varchar` |

### 7.3. Classes de Texto

| Nome | Nome | Descrição | Tipo (SQL Server) |
| --- | --- | --- | --- |
| Descrição | `DE` | Atribuída aos dados cujo conteúdo discursivo e resumido, com até 1.000 caracteres, descreve algo associado ao objeto.<br>Exemplo: `DE_SITUACAO_CONTRATO` | `varchar`, `nvarchar`, `text` |
| Endereço | `ED` | Atribuída aos dados de natureza textual utilizado para designar qualquer tipo de endereço. Na documentação, explicar a natureza do endereço.<br>Exemplos: `ED_ENTIDADE`, `ED_EMAIL`, `ED_SITE` | `varchar`, `nvarchar` |
| Nome | `NO` | Atribuída aos dados de natureza alfabética ou alfanumérica cujo conteúdo expressa uma denominação por extenso, e composta de palavras, abreviaturas ou ambas.<br>Exemplo: `NO_EMPREGADO` | `varchar`, `nvarchar` |
| Texto | `TX` | Atribuída aos dados cujo conteúdo, livre e em forma discursiva, se utiliza, em geral, para registrar ou documentar algo associado ao objeto de dado. Atribuído a dados que possam ultrapassar os 1.000 caracteres<br>Exemplo: `TX_ADITIVO_CONTRATO` | `varchar`, `nvarchar`, `text` |

### 7.4. Classes Numéricas

| Nome | Nome | Descrição | Tipo (SQL Server) |
| --- | --- | --- | --- |
| Número | `NU` | Atribuída aos dados de natureza numérica cuja identificação se faz por valores absolutos, e que não se enquadram nas demais categorias de identificação.<br>Exemplo: `NU_VERSAO` | `int`, `smallint`, `bigint` |
| Percentual | `PC` | Atribuída aos dados de natureza numérica que expressam uma parte de uma quantidade de 100 (cem) unidades.<br>Exemplo: `PC_INADIMPLENCIA` | `decimal` |
| Quantidade | `QT` | Atribuída aos dados de natureza numérica que determinam um conjunto de coisas e pessoas consideradas como equivalentes e suscetíveis de aumento e diminuição. Ao nomeá-los devem ser relacionados a uma unidade de medida para expressar a real grandeza.<br>Exemplo: `QT_EQUIPAMENTO_UNIDADE` | `int`, `bigint` |
| Valor | `VR` | Atribuída aos dados de natureza numérica que expressam uma importância monetária. ou grandezas de caráter decimal.<br>Exemplos: `VR_SALARIO` e `VR_NIVEL_SINAL` | `decimal` |

### 7.5. Classes Binárias

| Nome | Nome | Descrição | Tipo (SQL Server) |
| --- | --- | --- | --- |
| Binário | `BI` | Atribuída a dados binários armazenados no banco de dados.<br>Exemplos: `BI_IMAGEM`, `BI_HASH_USUARIO` | `binary`, `varbinary`, `varbinary(max)` |

### 7.6. Classes Especializadas

| Nome | Nome | Descrição | Tipo (SQL Server) |
| --- | --- | --- | --- |
| Geometria | `GE` | Atribuída aos dados de natureza espacial geométrico que representam objetos geométricos.<br>Exemplo: `GE_POLIGONO` | `geometry` |
| Geografia | `GF` | Atribuída aos dados de natureza espacial geográfico que representam informações sobre o local físico e a forma de objetos geométricos.<br>Exemplo: `GF_MUNICIPIO` | `geography` |
| XML | `XL` | Atribuída aos dados de natureza textual, estruturada no padrão XML.<br>Exemplo: `XL_RETORNO_API` | `xml` |

#### 7.6.1. Considerações sobre os campos espaciais (Geometria e Geografia)

7.6.2. Ao nomear campos destinados à representação de dados espaciais, é necessário que este reflita claramente o tipo de informação espacial armazenada. Utilize "PONTO" para dados do tipo ponto, "LINHA" para representar linhas e multilinhas, e "POLIGONO" para polígonos e multipolígonos.

7.6.3. Evite o uso de coleções de geometrias diversas.

7.6.4. Na eventualidade de existirem múltiplos campos geométricos na mesma tabela, é recomendado adicionar um sufixo explicativo para elucidar o propósito de cada um. Exemplos incluem:

```text
GE_PONTO
GF_LINHA
GE_POLIGONO_EXTERNO
GE_POLIGONO_INTERNO
```

7.6.5. Caso haja dados separados de latitude e longitude, sempre deverá ser criado um campo de geometria unindo os dois.

7.6.6. Se for necessário, pode ser armazenada a geometria em texto WKT, mas ela não prescinde da existência do campo de geometria binário.

7.6.7. Todo campo de geometria deve ter um índice espacial associado.

### 7.7. As seguintes combinações de classes NÃO serão aceitas:

| Classe | Código |
| --- | --- |
| `AA` | `AA_ANO` |
| `CO` | `CO_CODIGO` |
| `DD` | `DD_DIA` |
| `DE` | `DE_DESCRICAO` |
| `DH` | `DH_DATA_HORA` |
| `DT` | `DT_DATA` |
| `ED` | `ED_ENDERECO` |
| `GE` | `GE_GEOMETRIA` |
| `GE` | `GF_GEOGRAFIA` |
| `HH` | `HH_HORA` |
| `IC` | `IC_INDICADOR` |
| `ID` | `ID_IDENTIFICADOR` |
| `MM` | `MM_MES` |
| `NO` | `NO_NOME` |
| `NU` | `NU_NUMERO` |
| `PC` | `PC_PERCENTUAL` |
| `QT` | `QT_QUANTIDADE` |
| `SG` | `SG_SIGLA` |
| `TX` | `TX_TEXTO` |
| `VR` | `VR_VALOR` |

## 8. Guia rápido de nomes

| Objeto | Padrão | Composição |
| --- | --- | --- |
| Chave primária | `PK_TT` | PK = Constante<br>TT – Nome da tabela |
| Check Constraint | `CC_XX_YY_99` | CC = Identificador de Check Constraint<br>XX = Nome da tabela<br>YY = Coluna (Opcional quando for o caso de uma geral para a tabela)<br>99 = Sequencial da Constrant, iniciando do 01 |
| Coluna | `CC_XX` | CC = Classe de Valor<br>XX = Nome da coluna<br>32 Caracteres no máximo |
| Default Constraint | `DF_XX_YY_99` | DF = Identificador de Default Constraint<br>XX = Nome da tabela<br>YY = Nome do campo<br>99 = Sequencial da Constrant, iniciando do 01 |
| Function | `FN_XX` | FN = Constante<br>XX = Nome da function |
| Índice | `IX_TT_99` | IX = Constante<br>TT = Nome da Tabela<br>99 = Sequencial, iniciando do 01 |
| Modelo de dados | `PDM_XXX` | PDM = Constante de Modelo<br>XXX = Banco de dados (transacionais) ou Tabela Fato (analíticos) |
| Relacionamento | `FK_TF_TP_XX` | FK = Constante<br>TF = Tabela Filho<br>TP = Tabela Pai<br>XX – Qualificador da relação |
| Stored Procedure | `SP_XX` | SP = Constante<br>XX = Nome da procedure |
| Tabela | `CC_XX` | CC = Classe de tabela<br>XX = Nome da tabela<br>32 Caracteres no máximo |
| Trigger | `TRG_XX_YY_9` | TRG = Constante<br>XX = Nome da tabela<br>YY = Nome negocial da trigger<br>9 = Sequencial, iniciando do 1 |
| View | `VW_XX` | IX = Identificador de view<br>XX = Nome da visualização |

## 9. Critérios de aprovação do Modelo de dados

9.1. Avaliação automatizada através do script “validador.vbs”, acessível no GIT abaixo:

<https://git.anatel.gov.br/ad_modelagem_de_banco/validador-vb>

9.1.1. A utilização do script pode ser realizada pelo próprio analista, garantindo que a validação do modelo de dados será realizada levando-se em conta o negócio

9.2. Verificação da existência de documentação obrigatória.

9.2.1. Verificação da adequação do nome dos objetos de banco de dados à estrutura de nomeação descrita no item 3 deste documento.

9.2.2. Verificação da existência dos objetos obrigatórios para as tabelas, como chaves primárias, chaves estrangeiras, índices e constraints.

9.3. Validação qualitativa, realizada pela GIIB:

9.3.1. Análise dos nomes dos objetos de banco de dados com as informações negociais, sempre visando dar maior clareza ao dado armazenado.

9.3.2. Análise da documentação existente nos objetos de banco de dados, tendo em vista os objetivos descritos no item 4 deste documento.

9.4. Caso o modelo de dados não atenda a quaisquer os itens, não será aceito pela GIIB e será retornado para as devidas correções.

## 10. Bancos de dados mais utilizados

| Banco de dados | SGBD | Descrição |
| --- | --- | --- |
| `CORPORATIVO` | SQL Server | Dados corporativos da Anatel |
| `DB_COLETADEDADOS` | SQL Server | Banco de dados do sistema de coleta de dados |
| `DB_COLETADEDADOS_STAGE` | SQL Server | Banco de dados para a área de stage das coletas de dados |
| `DB_DW_ANATEL` | SQL Server | Banco de dados analítico da Anatel |
| `DB_DW_ANATEL_STAGE` | SQL Server | Área de stage para tratamento dos dados analíticos |
| `prod_SEI` | MySQL | Banco de dados do SEI |
| `SARH` | SQL Server | Banco de dados com a organização funcional (Unidades, Colaboradores, etc.) da Anatel |
| `SITARWEB` | SQL Server | Banco de dados do sistema SitarWeb |

## 11. Boas práticas de Modelagem

### 11.1. Geral

11.1.1. É considerada boa prática a inclusão do campo DH_CRIACAO ou DH_CARGA em todas as tabelas, preferencialmente com o valor padrão da data atual do sistema.

### 11.2. Modelos Analíticos

11.2.1. Em projetos onde os dados são obtidos através do sistema Coleta, é obrigatório o uso da coluna de identificação do arquivo (ID_ARQUIVO). Em projetos onde os dados são obtidos de sistemas legados, o campo pode aceitar valores nulos

11.2.2. Em todos os projetos dimensionais, é obrigatória a presença da coluna DH_CARGA na tabela FATO e Dimensões.

### 11.3. Outsystems

11.3.1. Quando o projeto de dados necessitar de deleção lógica dos dados, utilizar a coluna DH_EXCLUSAO.

11.3.2. Se for o caso do uso de um indicador pra registros ativos, utilizar a coluna IC_ATIVO.

11.3.3. Sempre que possível, inclua o ID do usuário do Outsystems nas tabelas para identificar o usuário que realizou a inserção do registro.

## 12. Dados pessoais sensíveis

12.1. A Lei Geral de Proteção de Dados (LGPD) trata de dados pessoais.

12.2. Ela também define o conceito de dados pessoais sensíveis.

12.3. No serviço público, a existência de dados pessoais não implica necessariamente em restrição, que é definida pelo artigo 31 da Lei de Acesso à Informação (LAI), que estabelece que apenas dados pessoais sensíveis devem ser restritos por natureza.

12.4. Apenas os dados classificados como sensíveis pela LGPD devem ser tratados como restritos.

art. 5º, inciso II, da LGPD:

> Art. 5º Para os fins desta Lei, considera-se:
>
> II - dado pessoal sensível: dado pessoal sobre

- origem racial ou étnica;
- convicção religiosa;
- opinião política;
- filiação a sindicato ou a organização de caráter religioso, filosófico ou político;
- referente à saúde ou à vida sexual; e
- dado genético ou biométrico, quando vinculado a uma pessoa natural.
