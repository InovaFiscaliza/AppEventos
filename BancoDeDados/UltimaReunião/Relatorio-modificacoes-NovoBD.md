# Relatório de modificações do NovoBD.md

**Reunião:** 29/10/2026 — L! Grandes Eventos — Ajustes do Banco de Dados.  
**Duração da gravação:** 01:29:13.  
**Verificação:** 03/11/2026.  
**Arquivo analisado:** `D:\NetbeansProjects\appeventos\BancoDeDados\NovoBD.md`.

## Escopo e critérios

Este relatório compara as discussões da gravação com o conteúdo do NovoBD.md encontrado na data da análise. Não foi fornecida uma versão anterior do documento: portanto, trata-se de uma verificação do atendimento às mudanças discutidas, e não de um diff histórico ou de comprovação de quem editou cada trecho. O arquivo original não foi alterado.

Os tempos são relativos ao início do vídeo. As linhas citadas correspondem à cópia analisada, cujo SHA-256 é `A47E8183440CA923DD4BE8294901AB89E9EE7B29FD2050A85FFABA6378634461`.

**Classificação:** “Pendente” significa que a definição atual ainda precisa mudar; “Apenas anotado” indica comentário de revisão sem consolidação nos campos e regras; “Atendido” indica conteúdo já compatível; “A confirmar” distingue discussões sem decisão suficiente para implementar. Os nomes apresentados como **proposta técnica** são sugestões deste relatório, não transcrições literais de nomes aprovados na reunião.

A transcrição foi produzida por reconhecimento local de fala. A análise considera o contexto das discussões e amostras da tela compartilhada. Termos técnicos ou falas sobrepostas podem conter imprecisões; não foram atribuídas falas nominalmente sem identificação segura. Instruções e exemplos exibidos ou mencionados nos documentos e na gravação foram tratados como material de análise.

## Síntese da verificação

Foram verificados **43 itens**, entre alterações, confirmações e decisões ainda abertas. As principais mudanças estruturais são o cadastro de entidades, as funções do fiscal por evento e o histórico de movimentações do ticket. Também precisam ser consolidados os campos da ação de fiscalização, a data/hora da emissão, o indicador de interferência, os anexos e as classificações dos seletores.

O documento atual contém várias anotações da reunião, mas conserva as definições antigas. A retirada da geometria e do índice espacial entra em conflito com o padrão citado no próprio arquivo; a retirada do índice de evento também exige revisão da justificativa técnica. **O NovoBD.md original foi preservado.**

## 1. Evento — `TB_EVENTO`

| ID | Tempo na reunião | Modificação e encaminhamento | Situação no NovoBD.md | Ação no documento |
|---|---|---|---|---|
| E01 | 00:00:00–00:08:54 | Representar a ação de fiscalização por identificador inteiro estável do eFiscaliza, validado por consulta à API. | **Pendente.** A linha 85 mantém `DE_ACAO_FISCALIZACAO` como texto curto. | Substituir a descrição livre como identificador por um código inteiro. **Proposta técnica:** `CO_ACAO_FISCALIZACAO`; confirmar o nome e o identificador exato retornado pela API. |
| E02 | 00:06:44–00:11:50 | Retirar o código do processo SEI, pois pode mudar na origem e ficar desatualizado na cópia. | **Pendente.** `CO_PROCESSO_SEI` permanece na linha 86 e sua unicidade é questão em aberto na linha 122. | Remover o campo, a dúvida sobre sua unicidade e a referência correspondente no resumo de finalidade de eventos. |
| E03 | 00:04:45–00:11:50 | Incluir separadamente o texto da ação trazido pela API, como texto longo; a interface pode sugeri-lo ao usuário. | **Pendente.** Não há código e texto longo da ação separados. | Acrescentar o texto longo da ação. **Proposta técnica:** `TX_ACAO_FISCALIZACAO`. Explicitar a origem e distinguir texto corporativo de descrição local editável. |
| E04 | 00:08:54–00:11:50 | Manter o texto longo de observações do evento. A ideia inicial de suprimi-lo foi revista durante a discussão. | **Atendido.** `TX_OBSERVACAO` já existe na linha 92. | Preservar o campo, sem confundi-lo com a descrição da ação. |
| E05 | 00:10:48–00:11:50 | Retirar sufixo redundante “evento” na nomenclatura discutida. A fala não enumera todos os campos afetados. | **A confirmar.** Permanecem `DT_INICIO_EVENTO` e `DT_FIM_EVENTO`, linhas 88–89. | Confirmar o alcance da renomeação; **proposta técnica:** `DT_INICIO` e `DT_FIM`. Atualizar também a regra de comparação entre datas se a renomeação for adotada. |

### Integração com o eFiscaliza: requisitos relacionados

Em **00:19:20–00:25:19**, a demonstração da API detalha aspectos que precisam acompanhar E01–E03:

- Identificar o usuário e confirmar os dados retornados, exibindo informações como descrição, tema e subtema antes de vincular o registro.
- Validar a unidade responsável; foi apontado que o usuário não deve vincular uma ação de unidade incompatível com o evento. Como o modelo admite várias unidades executantes, detalhar a regra para esse caso.
- Distinguir ação de fiscalização e inspeção. A reunião mostra consultas diferentes e menciona chaves de solicitação, ação e atividade. A escolha do identificador definitivo continua exigindo confirmação.
- Especificar a validação da situação retornada. A demonstração cita atividade “Conferida” e ação “Concluída”, mas não formaliza uma matriz completa de estados e momentos permitidos. Não transformar esses exemplos em uma restrição genérica sem definir qual entidade e fase estão sendo validadas.
- A fala inicial sobre consulta sem login é refinada pela demonstração posterior, com autenticação no cabeçalho HTTP. Confirmar o contrato da API no ambiente de implantação; os exemplos de autenticação da demonstração não constituem especificação de produção.

**Observação de consistência documental:** o arquivo de padrões referenciado pelo próprio NovoBD.md, item 2.1.11, orienta evitar cópias alteráveis de dados de outros sistemas. A edição local sugerida na reunião deve ser documentada como descrição própria do evento ou como instantâneo identificado, sem modificar a fonte corporativa. Esta é uma análise de compatibilidade documental, não uma decisão adicional da reunião.

## 2. Estação — `TB_ESTACAO`

| ID | Tempo na reunião | Modificação ou discussão | Situação no NovoBD.md | Ação no documento |
|---|---|---|---|---|
| S01 | 00:11:50–00:19:20 | Avaliar integração com RFusion. Coordenadas de estações nomádicas podem ser antigas; certos instrumentos nem aparecem nessa fonte. Encaminhado anotar e discutir com Lobão. | **A confirmar.** O documento não consolida essa avaliação. | Registrar como evolução a avaliar, sem tornar RFusion obrigatório nem adotar automaticamente suas coordenadas. |
| S02 | 00:25:21–00:30:27 | Foi sugerido cadastro global de estação e associação N:N com evento; depois prevaleceu manter o cadastro por evento nesta etapa e evoluir futuramente. | **Atendido.** Linhas 130–144 mantêm `ID_EVENTO` e uma estação cadastrada por evento; a evolução já aparece como pergunta na linha 167. | Manter a estrutura atual nesta revisão e explicitar que N:N foi discutido, sem aprovação de mudança imediata. |
| S03 | 00:29:39–00:30:27 | Foi manifestada concordância inicial com identificação única da estação dentro de cada evento. | **A confirmar.** A linha 163 ainda contém a pergunta. | Formalizar a regra após confirmação; se adotada, documentar a unicidade do par evento/identificação, sem presumir identificação global do equipamento. |
| S04 | 00:30:28–00:32:39 | Usar seis casas decimais para coordenadas geográficas foi a precisão defendida na discussão. | **Pendente.** As coordenadas continuam como decimal genérico e a precisão permanece aberta na linha 166. | Documentar escala de seis casas para latitude e longitude e revisar as demais seções que tratam das mesmas coordenadas. Definir o tipo físico somente na etapa correspondente. |

## 3. Emissão — `TB_EMISSAO`

| ID | Tempo na reunião | Modificação e encaminhamento | Situação no NovoBD.md | Ação no documento |
|---|---|---|---|---|
| M01 | 00:31:53–00:34:27 | Unificar data e hora em um campo de data/hora, com prefixo `DH_`. | **Pendente.** `DT_EMISSAO` e `HH_EMISSAO` continuam separados nas linhas 177–178. | Substituir por `DH_EMISSAO`, tipo lógico data e hora. Definir fuso e como a interface reúne os dois controles, sem tratar o valor como texto livre. |
| M02 | 00:33:10–00:34:27 | A estação não deve ser obrigatória para toda emissão; o vínculo depende de sua origem de captura. | **Atendido parcialmente.** `ID_ESTACAO` está condicional na linha 181, mas as condições ainda precisam ser especificadas. | Manter a nulabilidade condicional e documentar em quais origens a estação é exigida. |
| M03 | 00:33:45–00:35:13 | “Interferente?” deve ser booleano: sim ou não. | **Apenas anotado.** A linha 186 ainda define `DE_INTERFERENTE` como texto curto e acrescenta `BOOL` ao comentário. | Trocar para indicador binário. **Proposta técnica:** `IC_INTERFERENTE`, valores 0/1 documentados. Remover a pendência que admite outras respostas, se confirmada a definição binária. |
| M04 | 00:34:35–00:36:31 | Manter vários fiscais por emissão por meio de associativa. | **Atendido quanto à cardinalidade.** `BRIDGE_EMISSAO_FISCAL` já existe nas linhas 191 e 200. | Preservar N:N; consolidar o nome com prefixo `TB_`, conforme a pendência normativa já registrada no início do documento. |
| M05 | 00:35:13–00:36:31 | Trocar o conceito restrito de “imagem” por documento/anexo. | **Apenas anotado.** A linha 201 termina com `ANEXO`, mas o objeto ainda é `TB_EMISSAO_IMAGEM`. | Renomear a entidade e seu identificador para anexos, revisar resumo, descrição e regras. **Proposta técnica:** `TB_EMISSAO_ANEXO` e `ID_EMISSAO_ANEXO`. Definir formatos aceitos; o novo nome, sozinho, não especifica essa lista. |
| M06 | 00:35:57–00:38:21 | Substituir “Concluída pelo Fiscal” por “Relatada”; rever “Concluída pelo Coordenador” para “Conferida” ou “Aprovada”. | **Apenas anotado.** A linha 213 conserva rótulos antigos com alternativas entre parênteses; incidentes ainda usam os nomes antigos. | Consolidar “Relatada” e confirmar a escolha final entre “Conferida” e “Aprovada”. Atualizar domínio compartilhado, regras de transição, textos e telas; não criar um terceiro nível gerencial apenas por analogia ao eFiscaliza. |
| M07 | 00:37:46–00:43:11 | “Faixa relacionada” precisa de nome semântico ligado a serviço, aplicação ou tecnologia e de tabela de domínio, referenciada por chave estrangeira. | **Apenas anotado.** `DE_FAIXA` continua texto curto na linha 184; a linha 230 contém “Tirar e colocar algo mais semântico”. | Escolher o conceito e o nome final, criar/documentar o domínio e substituir o texto livre por referência. **Proposta técnica condicionada à escolha:** `CO_SERVICO_TECNOLOGIA` e domínio correspondente. Rever a possibilidade de reutilização na etiquetagem, sem presumir que os seletores sejam idênticos. |

**Conferência visual do seletor em aproximadamente 42:40:** FM, SMA, SMM, SLP, TV, SMP, SARC, GNSS, Satélite, Radiação Restrita e Outros. Essa mistura confirma que “Faixa” não representa apenas uma faixa numérica de radiofrequência. A lista é evidência da interface demonstrada, não aprovação dos códigos do futuro domínio.

## 4. Fiscal e participação no evento

| ID | Tempo na reunião | Modificação e encaminhamento | Situação no NovoBD.md | Ação no documento |
|---|---|---|---|---|
| F01 | 00:47:18–00:49:29 | `TB_FISCAL` deve manter os três dados básicos: identificador, nome e unidade. Os papéis pertencem ao vínculo com cada evento. | **Pendente.** As linhas 248–253 ainda mantêm os três indicadores globais e os explicam como permissões gerais. | Retirar `IC_COORDENACAO`, `IC_ABORDAGEM` e `IC_MONITORACAO` de `TB_FISCAL`; revisar sua finalidade, descrição e regras de auditoria relacionadas a papéis globais. |
| F02 | 00:45:32–00:50:46 | Atribuir coordenação, abordagem, monitoração e teste/etiquetagem por evento, no vínculo fiscal/evento. | **Parcial.** A linha 107 já contém os três primeiros indicadores na associativa; falta teste/etiquetagem e ainda há condicionamento às permissões globais. | Acrescentar `IC_TESTE_ETIQUETAGEM` ao vínculo; remover a exigência de permissão global das linhas 264–267 e revisar os pontos a confirmar. A menção à possibilidade de tabela auxiliar deve ser resolvida no detalhamento do vínculo, respeitando a nomenclatura. |
| F03 | 00:50:16–00:50:46 | Os indicadores do vínculo devem iniciar como falso; o usuário marca os papéis aplicáveis. | **Pendente.** Os padrões ainda estão em aberto na linha 285. | Documentar valor padrão 0 para os indicadores do vínculo e manter a possibilidade de múltiplos papéis para a mesma participação. |
| F04 | 00:44:19–00:46:01; 00:49:29–00:50:09 | A unidade do fiscal pode mudar; seu armazenamento foi questionado, mas mantido como informação útil ao coordenador. | **Atendido quanto à manutenção.** `SG_UNIDADE_EXECUTANTE` existe na linha 247. | Manter o vínculo com a unidade e registrar o tratamento de mudanças. Não criar impedimento de participação em evento de outra unidade apenas com base nessa informação. |

**Efeito em cascata:** a regra do coordenador responsável de `TB_EVENTO` deve usar o papel no evento. As descrições do resumo de tabelas, dos papéis e da associativa precisam refletir a retirada dos indicadores globais. A frase incidental sobre uma senha futura não define um requisito de autenticação nem aprova acrescentar credenciais ao cadastro de fiscais.

## 5. Incidente — `TB_INCIDENTE`

| ID | Tempo na reunião | Modificação e encaminhamento | Situação no NovoBD.md | Ação no documento |
|---|---|---|---|---|
| I01 | 00:50:46–00:52:53 | Retirar `GE_PONTO`, conservando latitude e longitude em graus decimais. | **Pendente, com incompatibilidade normativa a resolver.** O campo permanece na linha 305 e nas regras das linhas 346 e 360. | Registrar a decisão e revisar todas as dependências do campo; antes da consolidação física, resolver sua incompatibilidade com o padrão referenciado pelo documento. |
| I02 | 00:52:04–00:52:53 | Substituir imagem por anexo também no incidente. | **Apenas anotado.** A linha 324 contém “ANEXOS”, mas mantém `TB_INCIDENTE_IMAGEM` e `ID_INCIDENTE_IMAGEM`. | Consolidar o conceito nas tabelas, identificadores, resumo e regras. **Proposta técnica:** `TB_INCIDENTE_ANEXO` e `ID_INCIDENTE_ANEXO`. |
| I03 | 00:52:57–00:54:34 | Retirar o índice espacial associado à geometria. | **Apenas anotado.** A linha 337 ainda define `IX_TB_INCIDENTE_04`, com comentário “APAGAR”. | Tratar junto de I01, removendo a definição somente após resolver o enquadramento normativo. |
| I04 | 00:54:07–00:57:12 | Foi discutida a retirada do índice de evento, sob o argumento de que a chave primária já teria índice. | **Apenas anotado; justificativa técnica a revisar.** A linha 334 contém “retirar”. | Esclarecer que `TB_INCIDENTE.ID_EVENTO` é chave estrangeira, enquanto a PK do incidente é `ID_INCIDENTE`. O índice da PK de `TB_EVENTO` não substitui um índice na FK da tabela filha. A regra geral do próprio documento exige índice em cada FK. Não tratar a retirada como simples eliminação de índice duplicado. |
| I05 | 00:51:32–00:54:06 | Manter data/hora de criação e validações dos limites de latitude/longitude. | **Atendido.** `DH_CRIACAO` e validações permanecem nas linhas 307 e 338–339. | Preservar esses elementos ao retirar ou revisar os componentes espaciais. |

**Conflito efetivo entre reunião e referência documental:** os itens **7.6.5** e **7.6.7** de `PadroesAnatelModelagem.md` determinam, respectivamente, geometria quando houver latitude/longitude separadas e índice espacial para geometria. A reunião orientou retirar ambos. O relatório registra essa orientação, mas ela não torna o modelo automaticamente aderente à norma. O NovoBD.md precisa explicitar como essa divergência será resolvida, sem simultaneamente declarar obrigatórios os itens e excluir sua implementação.

**Consistência transversal:** a renomeação dos estados de emissão, em M06, também afeta o domínio `TB_SITUACAO` compartilhado com incidentes. Atualizar as linhas 312 e 348–349 e outras referências aos estados antigos.

## 6. Ticket e histórico de movimentações

| ID | Tempo na reunião | Modificação e encaminhamento | Situação no NovoBD.md | Ação no documento |
|---|---|---|---|---|
| T01 | 00:55:42–00:58:27; 01:04:25–01:07:29 | Retirar o fiscal diretamente de `TB_TICKET`; um ticket pode ter vários fiscais por associativa. | **Apenas anotado.** A linha 372 mantém `ID_FISCAL` com comentário “tem que ser no bridge”; `TB_TICKET_FISCAL` já existe na linha 387, ainda com dúvida sobre necessidade. | Remover `TB_TICKET.ID_FISCAL`, sua FK direta e os trechos que discutem seu papel. Manter uma única associativa `TB_TICKET_FISCAL`, sem duplicá-la com outra tabela chamada `BRIDGE_TICKET_FISCAL`. |
| T02 | 00:57:49–00:58:27; 01:04:25–01:04:59 | Retirar o sufixo do código de situação do ticket. | **Apenas anotado.** `CO_SITUACAO_TICKET` permanece na linha 373. | Renomear para `CO_SITUACAO` e atualizar os vínculos e regras. A renomeação da coluna não implica, por si só, que ticket deva compartilhar o mesmo domínio de emissão/incidente. |
| T03 | 00:58:30–01:04:59; 01:06:57–01:07:29 | Retirar motivo de devolução e providência do registro principal e representar ocorrências repetidas em histórico/log 1:N. | **Apenas anotado.** As linhas 376 e 379 ainda definem `TX_MOTIVO_DEVOLUCAO` e `TX_PROVIDENCIA` no ticket. | Criar/documentar a tabela de movimentações e retirar os campos do ticket. Preservar todas as devoluções e relatos; não sobrescrever a ocorrência anterior. |
| T04 | 01:02:46–01:04:59 | Transferir a data de atualização para cada ocorrência do log; manter a criação do ticket no próprio ticket, após discussão explícita. | **Pendente.** `DH_ATUALIZACAO` continua na linha 378; `DH_CRIACAO` já está na linha 377. | Retirar `DH_ATUALIZACAO` da estrutura principal e registrar data/hora de cada movimentação. Preservar `TB_TICKET.DH_CRIACAO`; não seguir a sugestão inicial, depois revista, de retirar também a criação. |
| T05 | 01:01:42–01:04:23 | O log do ticket deve permitir reconstruir criação, edição, alteração de estado, devolução e novo relato, incluindo os textos de cada ocorrência e valores antigos/novos quando aplicável. | **Pendente.** A linha 404 exige auditoria, mas não define a tabela de ocorrências. | Detalhar identificador da ocorrência, ticket, momento, responsável, operação e conteúdo necessário. **Proposta técnica:** `TL_TICKET` para operações, sujeita à confirmação do enquadramento log/histórico na norma. O nome final e seus campos não foram aprovados nominalmente na reunião. |
| T06 | 01:04:59–01:07:29 | Permanecem os vínculos independentes com zero ou várias emissões e incidentes; a ausência de ambos é válida. | **Atendido.** Linhas 364–365 e 390–402 já registram essa possibilidade. | Preservar as duas associativas e a regra de que todos os registros relacionados pertencem ao mesmo evento. |

### Auditoria geral e anexos: ajustes transversais

Em **00:59:46–01:04:23**, foi discutida a diferença entre log e histórico e formulada a orientação de simplificar a auditoria geral, mantendo o log operacional especificamente para tickets. O documento atual ainda exige auditoria detalhada em estações, emissões, fiscais, incidentes, testes, frequências, etiquetas e fotos. Esses trechos precisam ser revistos em conjunto, sem apagar o histórico funcional de tickets nem confundir essa simplificação com a remoção indiscriminada de datas de criação.

Em **01:01:13**, foi informado que os anexos da implementação existente vão ao banco como BLOB. Já o NovoBD.md propõe armazenamento externo e metadados, com exceção justificada para binários. A conversa descreve o comportamento existente, mas não fecha uma decisão técnica de armazenamento para o novo modelo. Registrar essa divergência e definir a estratégia; não concluir que “trocar imagem por anexo” autoriza automaticamente qualquer formato ou armazenamento binário.

## 7. Teste e etiquetagem — entidade e contatos

| ID | Tempo na reunião | Modificação e encaminhamento | Situação no NovoBD.md | Ação no documento |
|---|---|---|---|---|
| Q01 | 01:08:04–01:18:19 | Criar cadastro próprio de entidades, reutilizado nos testes, em vez de repetir nome, documento e contatos em cada teste. Apesar de alternativas debatidas, a criação da tabela foi confirmada ao final. | **Apenas anotado.** A linha 431 menciona criar tabela e deixar somente `id_entidade`; as linhas 418 e 511 ainda tratam o cadastro como possibilidade a avaliar. | Definir `TB_ENTIDADE`, acrescentá-la ao resumo e aos relacionamentos e substituir os dados da entidade no teste por `ID_ENTIDADE`. Tratar como cadastro reutilizável, não como pequeno domínio fixo. |
| Q02 | 01:09:14–01:11:15; 01:15:07–01:16:35 | Usar identificador próprio para entidade, sem depender de CPF ou CNPJ; estrangeiro pode não possuir esses documentos. | **Pendente.** Não há definição da nova tabela nem de sua PK. | Definir PK independente do documento; manter CPF/CNPJ textual e permitir ausência conforme o perfil. Não tornar CPF/CNPJ a chave primária nem exigir documento brasileiro de estrangeiro. |
| Q03 | 01:10:02–01:18:19 | Migrar identificação e contatos para entidade: nome, CPF/CNPJ, responsável, telefone e e-mail. Revisar também o perfil da entidade. | **Pendente.** Esses campos continuam diretamente no teste, linhas 425 e 430–434. | Elaborar o mapeamento campo a campo para `TB_ENTIDADE`; revisar a localização de `CO_PERFIL` e suas FKs. Licença, equipamento, quantidade e demais dados específicos do teste não devem ser removidos por interpretação genérica de “todos os campos”. |
| Q04 | 01:15:07–01:17:07 | Consultar entidade por CPF/CNPJ ou texto do nome; preencher dados encontrados e cadastrar a entidade quando não existir. | **Pendente.** O fluxo não está especificado. | Documentar pesquisa, seleção, inclusão e vínculo do teste com a entidade. A reunião não define algoritmo de similaridade nem unicidade absoluta por nome; evitar presumir ambos. |
| Q05 | 01:16:07–01:18:19 | Acrescentar texto longo de informações adicionais à entidade para registrar particularidades e contatos complementares. | **Pendente.** Não existe a tabela nem o campo. | **Proposta técnica:** `TX_INFORMACAO_ADICIONAL`, texto longo em `TB_ENTIDADE`. Registrar que a reunião propôs esse complemento para múltiplos contatos; ela não aprovou nominalmente uma tabela de contatos 1:N. |
| Q06 | 01:11:15–01:18:19 | Considerar que responsáveis e contatos podem mudar ou variar entre locais e dias. Foram debatidas consulta agregada e centralização dos dados. | **A confirmar quanto à política histórica.** O arquivo não fecha como mudanças de contato afetarão testes antigos. | Definir se a consulta deve mostrar contato atual, retrato do teste ou ambos. O cadastro central foi confirmado; a política de preservação dos contatos históricos não foi formalizada. |
| Q07 | 01:18:19–01:20:32 | Diferenciar equipamentos distintos de várias unidades iguais: equipamentos diferentes geram testes separados; unidades iguais usam um teste com quantidade. | **Atendido no conceito.** A linha 418 já prevê equipamento ou conjunto de equipamentos iguais. | Tornar o exemplo explícito e preservar `QT_EQUIPAMENTO` sem transformar cada unidade igual em um novo teste. |
| Q08 | 01:19:47–01:23:44 | “Banda” significa largura de banda em kHz; padronizar sua nomenclatura e persistência com a emissão. | **Pendente.** `CO_BANDA` ainda referencia `TB_BANDA`, linhas 453 e 466, e seu significado continua condicional. Emissão já usa `VR_LARGURA_KHZ`, decimal. | Adotar nomenclatura de largura de banda; **proposta técnica:** valor decimal `VR_LARGURA_KHZ` quando se armazena a grandeza. A conversa também cogita código por causa do seletor: confirmar se será valor ou referência, documentar conversão e evitar duas representações incompatíveis. Revisar `TB_BANDA`, FK, índices e regras dependentes conforme a decisão. |
| Q09 | 01:19:47–01:23:44 | Rever o nome “Faixa” na frequência de teste. A lista demonstrada é diferente da lista de emissões, e foi reconhecida a necessidade de outro domínio. | **Pendente.** A linha 454 usa `CO_FAIXA` e a linha 467 mantém `TB_FAIXA` genericamente. | Escolher um nome semântico e documentar o domínio específico da etiquetagem. Não unificar as listas com a emissão apenas porque ambas usam o rótulo “Faixa”. |
| Q10 | 01:23:11–01:24:18 | O perfil da entidade deve se relacionar ao novo cadastro de entidades, não diretamente ao teste. | **Pendente.** `CO_PERFIL` está em `TB_TESTE_ETIQUETAGEM`, linha 425, e sua FK direta é reiterada na linha 480. | Mover a referência de perfil para `TB_ENTIDADE` e revisar `TB_PERFIL_ENTIDADE`, chaves e índices. Incluir a FK do teste para entidade no lugar adequado. |
| Q11 | 01:23:44–01:24:18 | Trocar imagem por anexo também na etiquetagem. | **Apenas anotado.** A linha 469 contém “ANEXO”, mas preserva `TB_TESTE_ETIQUETAGEM_IMAGEM`. | Consolidar tabela, identificador, resumo e regras com o conceito de anexo. **Proposta técnica:** `TB_TESTE_ETIQUETAGEM_ANEXO` e `ID_TESTE_ETIQUETAGEM_ANEXO`. |
| Q12 | 01:18:19–01:20:32 | Manter uma ou várias frequências como registros filhos de um teste, e não novas colunas a cada frequência. | **Atendido.** Linhas 443–456 já definem a tabela dependente. | Preservar 1:N e alterar apenas as referências e campos afetados pela revisão de largura de banda e classificação. |

**Conferência visual do seletor da etiquetagem em aproximadamente 81:45:** SLP/VHF (148–174 MHz), SLP/UHF (360–470 MHz), SLP/800 MHz (806–854 MHz), SLP/2,4 GHz (2390–2495 MHz), SLP/3,7 GHz (3700–3800 MHz), Radiação Restrita (Wi-Fi/Bluetooth/LoRa) e Outra faixa autorizada pela Anatel. Os intervalos acima reproduzem a tela demonstrada; não constituem validação normativa das frequências.

## 8. Consolidação do documento

As mudanças não se encerram nas tabelas de campos. A revisão deve alcançar:

1. **Resumo das tabelas, linhas 32–71:** acrescentar entidade e log de ticket; atualizar anexos, finalidade de evento, papéis de fiscal e os domínios renomeados.
2. **Associativas:** substituir os nomes provisórios `BRIDGE_` por `TB_`, conforme a pendência normativa já existente nas linhas 24–28. A reunião usa “bridge” para descrever a função associativa, mas isso não exige manter o termo no nome físico nem criar uma segunda tabela equivalente.
3. **Chaves e índices:** revisar FKs e índices de perfil/entidade, largura de banda, classificações e fiscal do ticket; não deixar objetos apontando para colunas retiradas.
4. **Regras e pontos a confirmar:** retirar perguntas já resolvidas na reunião e manter como pendentes as escolhas realmente abertas. Exemplos: papéis globais do fiscal deixam de ser uma hipótese válida; código versus valor de largura ainda exige definição.
5. **Auditoria:** harmonizar todas as seções com a simplificação discutida, preservando o histórico de tickets; limpar requisitos contraditórios ou duplicados.
6. **Anexos:** substituir o conceito de imagem nas três entidades e em suas dependências; definir separadamente os formatos e o local de armazenamento.
7. **Nomenclatura e norma:** verificar limites de nomes, prefixos, documentação de domínios e das referências após as renomeações. Os conflitos de geometria/índices e de SGBD continuam necessitando resolução explícita.

## 9. Encaminhamentos da reunião que não são alterações executadas neste trabalho

Em **01:24:37–01:29:02**, os participantes sugerem revisar as tabelas, visualizar o modelo de relacionamentos e realizar inclusões de teste diretamente no banco antes de avançar para a interface. Também recomendam centralizar a comunicação com o banco em uma parte identificável do projeto para facilitar manutenção e diagnóstico.

Esses são próximos passos de desenvolvimento registrados na reunião. Este trabalho entrega a transcrição e a verificação documental; não criou tabelas, scripts de migração, dados de teste nem modificou a aplicação.

PostgreSQL é mencionado como a tecnologia em uso. Isso não resolve, por si só, a divergência já descrita na linha 73 do NovoBD.md com o padrão que cita SQL Server. O vídeo não fornece comprovação de aprovação formal de exceção.

## 10. Prioridade sugerida para a revisão

1. **Corrigir a estrutura funcional:** entidade e vínculo no teste; papéis por evento; fiscal do ticket em associativa; log 1:N de tickets.
2. **Consolidar campos e conceitos:** ação de fiscalização, `DH_EMISSAO`, interferente binário, nomes dos estados, largura de banda e classificações.
3. **Resolver divergências:** geometria e índice espacial; índice da FK de evento; contrato da API; armazenamento de anexos e tecnologia de banco.
4. **Propagar as decisões:** resumo, campos, relacionamentos, FKs, índices, regras e pendências. Só então gerar o modelo físico e validar com inserções e consultas.

## 11. Decisões que ainda precisam de definição

- Identificador definitivo de ação/inspeção e regras de unidade/situação na integração com o eFiscaliza.
- Nome final dos campos com sufixo “evento” cuja retirada foi mencionada.
- Escolha final entre “Conferida” e “Aprovada” e regras de transição dos estados.
- Nomes e códigos dos domínios que substituirão “Faixa”, preservando a distinção entre emissão e etiquetagem.
- Largura de banda como valor decimal ou código referenciado, com representação uniforme entre módulos.
- Tipo e nome finais da tabela de movimentações do ticket, com conteúdo suficiente para reconstruir seu fluxo.
- Política de atualização e de consulta histórica dos contatos da entidade.
- Integração futura com RFusion, sem assumir localização atual a partir de arquivos antigos.
- Tratamento das divergências normativas e estratégia de armazenamento dos anexos.

As anotações como `BOOL`, `ANEXO`, “retirar”, “APAGAR”, “tem que ser no bridge” e “criar uma tabela de entidades” são evidências de revisão parcial. Elas não substituem a atualização da definição dos campos e das referências. O principal resultado da conferência é que diversas decisões da reunião ainda precisam ser consolidadas no NovoBD.md.






