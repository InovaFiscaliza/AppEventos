# Transcrição da reunião — 29/10/2026

**Gravação:** L! Grandes Eventos — AjustesBancoDeDados.  
**Duração:** 01:29:13.  
**Idioma:** português.

Transcrição automática produzida localmente, com segunda passagem nos cinco trechos de reconhecimento mais fraco. Os tempos são aproximados e relativos ao início do vídeo. Falantes não foram identificados de forma segura. Pode haver erros em nomes, siglas e falas sobrepostas; esta não é uma transcrição literal certificada. O relatório separado organiza as decisões e verifica seu atendimento no NovoBD.md.


## Evento e integração com eFiscaliza

**[00:00:01–00:00:36]** Aqui na gravação, eu vou colocar aqui a consulta que você faz lá no SKL Server para pegar as informações lá do tabela de inspeção, lá do EFISCALISA. Então, por exemplo, a ação é aquele, é ação tal não sei o que, né? Ele é esse CO inspectividade. O ID

**[00:00:36–00:01:05]** É o número inteiro que aparece lá depois do hashtag. Aí depois você pode... Todo mundo tem acesso, só você abrir lá no... fazer a conexão lá no SQL Server e rodar essa consulta lá que vai dar certo. Você vai ver direitinho o que vem. Mas minha dúvida aí é só entender o que a gente quer exatamente. Porque...

**[00:01:08–00:01:39]** Então, é que o Augusto comentou aí da possibilidade do fiscal digitar o nome errado da ação. Mas, sendo um campo numérico, o mapeamento não vai ter problema, só que você vai ter que dizer qual é o tipo, se é uma sólistação, se é uma ação ou se é uma atividade dispersão.

**[00:01:39–00:02:09]** Então, hoje nos apps, a gente pede a inspeção. No caso aí, eu não sei se o pessoal vai querer que seja a ação. Mas assim, aí você entra um número, e aí vai ter uma validação lá na guia de que aquilo ali tem que ser um número. Entendo o número, você faz a consulta na API e retorna. Aí a minha dúvida é, a gente quer ter essa informação do eFiscaliz aí para mostrar ou não?

**[00:02:11–00:02:40]** Porque, no máximo, o fiscalismo também tem aquela URL padrão. Então, a gente poderia... Sim. Sabe o que André fazendo, por favor. Essa tabela aí é qual que é? Essa tabela do evento. Essa tabela aí vai ser popular quando o cara cadastrar o evento, certo? Isso. Quando o cara cadastrar o evento, vai ser... É um pra um? É uma ação pra cada evento?

**[00:02:41–00:03:13]** Sim. Então, aí eu acho que podia o seguinte, o cara, quando estiver cadastrando o evento, ele coloca o número da ação aí, e aí ele busca lá no EFISCALISA e popula aí a tabela. E ficam campos editáveis, digamos assim, porque essa consulta na API seria um retrato daquele momento, depois o cara muda lá no EFISCALISA e não volta pra cá, né? É, aquele, é. Aí seria uma validação, né? Se existe essa ação de fiscalização, né?

**[00:03:15–00:03:47]** Avalidação, não é popular, não? Você vai informar, para falar, essa ação existe. A descrição é essa aqui. Você pode até olhar a descrição e falar, é a bate, é esse mesmo. Que isso é importante, eu sei que é, a indicação da ação. Eu só estou pensando na utilidade disso. Será que algum dia a gente vai...

**[00:03:48–00:04:15]** Diariamente, o coordenador vai ter como subir um relatório lá para o SEI ou para o fiscaliza. Acho que a primeira coisa que garantimos é a integridade, que o cara não vai fazer um negócio errado. De vez em quando, coloca o número de uma ação, coloca o número da inspeção, lá no escalado, dá uns problemas assim, lembra?

**[00:04:15–00:04:45]** Isso, cara, já colocar o número certo, já validar esse número lá no eFiscaliza melhor. Eu concordo, concordo. Mas tem coisas que são editáveis no eFiscaliza. O código do processo C, por exemplo, é editável. E aí, os apps, hoje em dia, quando gera um relatório, vai subir, ele não está preocupado com essa porra, porque a gente sabe que muda.

**[00:04:45–00:05:14]** Eu colocaria o mínimo possível do eFiscaliza, que é que ele pode trazer só o ID, o ID da ação. Ou deixa sua descrição aí de jeito que está aí. Não, traz o ID, porque o ID não muda. O ID não muda e a partir do ID você monta o link para fazer aquela consulta online. Isso, isso.

**[00:05:14–00:05:42]** Acho que poderia até, e aí já pensando na guia aqui, Markson, quando estiver nessa tela de cadastro, o cara insere lá o id numérico, a API do eFiscaliza retorna pra ele, é isso aqui, irmão, que você quer? E aí ali vai vir um tema, sub tema, descrição, é o cara disse, é isso aí que eu quero. E aí ele já aproveita o campo descrição e já sugere aí, como o campo descrição do evento. E aí o cara obviamente pode editar, mas fica aguardado aí na tabela.

**[00:05:42–00:06:14]** Não o código do processo C, mas o só o ID da ação, a do eFiscaliza. ID inspection, isso. Aí, isso aí. Aí não é nem essa consulta então que eu coloquei no chat ali. O André, depois eu vou, eu tô vendo aqui. Eu vou colocar aqui a consulta que busca a ação. Só pra você ver direitinho a tabela lá que ele pega lá então. Eu acho que pode ser cara, acho que pode ser o...

**[00:06:14–00:06:44]** Eu passo aqui, Max, ao RL do contexto da ação, que ele retorna tudo, da API lá. Não vai fazer via consulta no banco, não, né? É, não. A API entrega. Não precisa, nem tá alogado. Pô, sou de bola. É consulta pública. Não tem souber que tá usando de uma bloqueada, não. Não, mas é consulta sua pública. Se você quiser fazer relato, você precisa tá alogado.

**[00:06:44–00:07:20]** A consulta é pública? A consulta é pública dentro da rede da Anatel, né? Sim. Ah, que bom. É como vai estar no contêiner dentro da rede, né? Eu coloco aqui a URL. Aqui é um pouquinho. Show de bola. Mas aí, beleza, né? Entendeu aí, né, André? Dá pra dar uma simplificada aí, cara. Tirar esse código, processo C, dá pra tirar fora. Eu acho que esse...

**[00:07:20–00:07:51]** Aí você tem que ter um... não é descrição da ação, é um ID ou código da ação de fiscalização e aí você puxa lá da API a observação sobre o evento, já coloca a descrição que vem lá do EFiscaliza e o cara pode editar, né? Se ele quiser. Imagina que seria isso aí. Então tira o mesmo código do processo C? Tira, cara, porque isso muda no C. Ah, entendi.

**[00:07:51–00:08:23]** Então, no final ele pode ser... Pode estar desatualizado no final. Então, beleza. E a descrição da ação vira código, tá? E é um inteiro. Então, tem que abrir mais uma coluna que seria o código, porque ele vai ser consultado a partir dessa lista. Eu acho que você pode ter aí, pensando nos nomes.

**[00:08:23–00:08:54]** Em cima, ao invés de descrição de ação de fiscalização, é código de ação de fiscalização inteiro. Esse do processo C vai embora. O que é esse TX? Significa o que mesmo? É texto, né? Aí poderia ser o último campo, aí poderia ser texto, underline, descrição. Não observação, descrição. É porque descrição tem outra regra, né? Aí é DE, colocar DE alguma coisa.

**[00:08:54–00:09:35]** Então, descrição é vento. Descrição, ação. Então, eu fico de cima também. Então, esse textil de observação vai embora e você só insere em sério um código ação de fiscalização. Mas o observação pode ser importante para o cara narrar alguma outra coisa que aconteceu, algum outro detalhe. Cara, eu fico pensando, você precisa de um campo textual. É esse? É um campo textual longo. Eu não mudaria, só se você quiser assim...

**[00:09:36–00:10:09]** Pode até ser, num caso desse Copa do Mundo, aí nessa descrição, nesse texto curto, cara bota, Salvador. E na observação, ele escreve pra caramba. E aí tem outro evento, Copa do Mundo, descrição Rio de Janeiro e na observação, um texto longo, sei lá. Pode ser, pode ser. Sempre vai ter uma exceção, alguma orientação que venha.

**[00:10:10–00:10:48]** Pode ser, em campo a mais de texto não tem problema não. Eu só acho que se a gente for trazer a descrição da API do EFiscaliza, do código da ação que ele seria, não é texto curto, é texto longo também. Então você tem que mudar a tipologia desse campo. Ah, tá, tá bom. Tirou? Então pelo que eu entendi, se você quiser já mexer nesse MD aí, você bota aí o código, ação de fiscalização,

**[00:10:48–00:11:50]** Enteiro, embaixo, texto, ação e fiscalização, texto longo, segue o resto tudo, e o último tem texto de observação, texto longo também. Isso, acho que seriam os ajustes e tira ali o suffixo do evento também. Vou fazer isso com calma. Ah, tá, eu vou passar o RL aqui. Vou pegar aqui o RL, é um segundo. É caminhando aí, André? Oi. É caminhando aí. Mas tá bem?


## Estações e demonstração da API

**[00:11:50–00:12:31]** Podemos, caminhão? Podemos, né? TBestação, que fechou, né? ou não? A única coisa que eu penso em relação a isso aí, que Lobão lembrou em uma reunião, se seria o caso de a gente criar uma ponte com o refúgio. E aí eu não sei como é que está lá no refúgio. Mas dá pra disponibilizar lá uma peizinha igual...

**[00:12:31–00:13:09]** igual, fiz lá por app analysis, selecionou a estação, a chave da estação ou alguma coisa assim, mas assim, só um ponto que essas estações aí vão ser estações nomáticas, não é isso? Sim. Não, pode ser nomática, nomática ou não? Ou fixa, né? Pode ser fixa, ou pode ser nomática.

**[00:13:09–00:13:41]** Não, tudo bem, é porque o seguinte, se ela for nomádica e ela ainda não tiver subindo arquivos no RFusion, então muito provavelmente a latitude, longitude dela vão ser da última região ali que ela foi monitorada, entendeu? Se eu estou entendendo bem, esta tabela, estação, ela é cadastrada uma vez só, ninguém fica ali atualizando latitude, longitude dela ou fica?

**[00:13:41–00:14:13]** Não, vão ter estações que vão estar no RFusion e outras que acho que não estarão, né? Tem nomádica no RFusion? Tem, o negócio aqui é nomádica, ela fica desligada, entendeu? Então assim, imagina, você cadastrou a estação, mas a estação ainda não foi ligada. Aí quando você pegar essa estação do RFusion, a latitude e longitude vai ser da última região,

**[00:14:13–00:14:43]** e quando entrar no seu banco de dados vai com uma coordenada antiga, isso que eu receio. Ele não vai usar o arquivo da Refusion, ele só vai dizer que ele usou ela para coletar as informações que ele está informando ali na hora. Não, tudo bem, mas o ponto é que do RFusion a gente tem esses dados, latitude, longitude da estação, entendeu?

**[00:14:43–00:15:16]** Mas estão errados, não vou usar o RFusion para isso. Eles estão do último arquivo válido que ele processou. Sim, ele não vai usar, ele vai usar onde ele está na hora. Ele não vai usar o RFusion, ele não pode usar. Então, vamos pensar que seria o nome da estação, sei lá, o nome da estação e o modelo de equipamento.

**[00:15:17–00:15:53]** Tem umas que ele pode usar, tem outras que ele não pode usar, com certeza. Nem todos ele vai usar, com certeza não. As normáticas ele não vai usar tudo. Lá de estúdio no estúdio vai estar diferente e os arquivos não serão... Não vai ser os últimos, ele vai ligar lá na hora, lá vai começar a trabalhar, vai achar lá uma interferência. Muito provavelmente não vai ter subido e não vai estar na RFI.

**[00:15:54–00:16:28]** Não, ele vai subir de noite, isso aí é fado. Muito provavelmente ele vai relatar uma coisa que não subiu ainda para RFI hoje. Se subir, porque está arriscado ele desligar ela. Desligar antes de... É, foi um silóscopo que ele foi lá para a curva, para a curva 3 do autódomo, ele vai desligar e provavelmente não vai lembrar de ligar a noite. Ele vai botar lá o print,

**[00:16:28–00:17:21]** ele vai tirar a foto da tela do silóscop, do espectro e... Pimbo. ele vai botar lá na inissão. provavelmente. isso que eu acho, não? aí tem caso. se for nomática tem muito que consultar na RFusion ou não. o que você acha, Eric? sei lá, tenho dúvidas. de fato, pode ser que seja uma coisa muito fora da caixinha, né? esses da gente foi aí.

**[00:17:23–00:17:55]** Cara, deixa esse ponto anotado, André. Depois dá uma falada com o Lobão, que ele é um cara bom para esses links de informação. Mas do jeito que você está pontuando aí, eu também acho que não mexerei com essa integração. Estação fixa, beleza. Integração válida. Normática provavelmente vai se chamar.

**[00:17:55–00:18:31]** A informação é muito fresquinha. Pão quentinho que não está no RFI. Não é, porque assim, não é trivial você conseguir saber se ela é nomádica ou não. Tem que ver o contexto. Ela não está escancarada assim, é RFI, não é nomádica. Isso aí, o pessoal da rede de monitoração de espectro tem lá no SharePoint, lá anotado e tal. Mas não é fácil.

**[00:18:31–00:19:20]** Entendia. Só com uma iazinha para ficar inferiante. Eu ia dizer, eu aceito um cara de cenomático, eu vou sempre parar de ir. E tocam, né, RFI para, aí o cara troca. Mandei para você aí, André, você puder mostrar o chat, que aí eu te explico rapidinho aí. Vou abrir o chat aqui pelo meu celular. Não quer abrir aí não, pô. Abrei o time. Tem que estar na VPN.

**[00:19:20–00:20:02]** No chat dessa reunião aqui, chat, clica ali em cima. Gente do céu. É só você ir na reunião onde aparece a carinha de todo mundo, chat, pronto aí. Beleza. Agora que eu vi aqui a requisição da API, você precisa injetar ali no header, essa autenticação, HTTP básica, tá? Mas ele só tá validando login.

**[00:20:02–00:20:33]** Então, a senha pode ser um dos textos 456 que vai passar. O que a gente faz hoje? Então, eu queria que você clicar nesses três links aí. Primeiro no debaixo. O debaixo, no debaixo. O último. É. Esse debaixo aí, ele vai te dizer quem você é. Então, clica ali no... para ficar bonitinho ali. Estilo de formatação, clica nisso. Perceba que aí, ó...

**[00:20:33–00:21:10]** useremail, André Rezende, robanatel.gov.br. Então você sabe quem você é. Então esse é o primeiro ponto. Você já sabe seu login. Isso como vai estar rodando lá na VM? A gente vai ter acesso a isso. Segundo ponto, clique agora nos outros links lá. Ele vai pedir seu login senha. Eita porra.

**[00:21:10–00:21:56]** Que medo! A segunda ele costuma ir. Que esquisita essa forma de autenticação. Meu tá assim também, de tapinha agora. Pronto, a IPC, bote aí o seu loquim da Anatel. Deixa eu tentar. Não, não, velho. Bote seu loquim na Anatel. É André Rezende, bote aí. E a 100 é bote 245.6, qualquer coisa. Isso aí você vai ter que injetar no header da autenticação.

**[00:21:56–00:22:25]** E aí, dei um salvar. OK. Clica ali no checkbox. Perceba que nessa requisição aí, da ação, então você vai pedir para o usuário, ele vai te dizer o número, 248-368. Eu estou olhando para o URL ali, tá? Lá em cima. Olhe lá para o URL, pronto. E aí você vai criar essa frase, essa é o endpoint, 24 fermeute, é o que ele te deu. E aí você vai entrar aí, ó.

**[00:22:25–00:22:57]** A descrição vai estar em ação de expressão abaixo mais. Ação de expressão abaixo vai ter uma hora que vai chegar o campo de descrição aí. Pode ir, pode ir, pode ir. Descrição aí. Descrição, expressão, ação já passou. É esse aí de cima, grande. E aí, Value. Perceba que é esse campo aí que eu imagino que você traz pro cara e já coloca como sugerido. Além disso, perceba que tem coisas aí

**[00:22:57–00:23:27]** que vai possibilitar o cara validar se essa é a expressão correta. Então, eu acho que você tem aí a indicação da gerencia no Grandes Eventos, lá a gente diz qual é a unidade. Ele não pode colocar uma ação de outra unidade. Então, vai ter essa validação que você consegue fazer. E tem coisas aí, nomes da temática, sub-tema, todas essas coisas que criam, que aí aparece lá um pop-up, cara, tem certeza que esse aqui é abastalhado? É o cara, sim.

**[00:23:27–00:23:58]** e aí você vincula e traz a descrição, tá? Isso se você for pesquisar pela ação. Eu tenho dúvidas, mas se a gente for pesquisar pela inspeção, aí clica ali no outro, no link do meio ali que eu mandei no chat. Essa, esse é o que a gente usa nos apps. Então o que é aquela outra zorra lá da ação, filtrado. É só informação que o app precisa. Então você tem a descrição de cada

**[00:23:58–00:24:29]** Coisa vinculada à inspeção, então você vai trazer a sólistação, abaixo um pouquinho mais. Então tem a chave sólistação, tem a chave ação, e embaixo tem a chave atividade. Então o campo de descrição estaria aí. Aí você consegue validar também um status, perceba que o status desse cara ia conferida da atividade. A ação está concluída. Então se tiver um status diferente de

**[00:24:29–00:25:19]** em status conferida, os caras não podem relacionar. Então, quando a gente for fazer essa tela na guia lá, essa telinha, a gente cria essas validações para que o cara faça diminuir o erro, né? Sim. Beleza? Mas só isso aí que eu queria te falar da API hoje. Mas aí pode continuar aí. Emissão, fiscal, deixa eu voltar, a gente está na tabela de estação.

**[00:25:21–00:25:59]** Peixão aqui com a tabela de estação, vocês têm alguma coisa? Acho que isso aí pode começar com no bonde depois aí, como o Augusto falou. Mas é muito específico, né? Talvez seja isso aí mesmo, cara. Desculpa, sobe um pouquinho aí. Idê da estação, nome da estação, tá. Essa tabela não seria só um...

**[00:26:00–00:26:39]** A gente não teria uma tabela auxiliar aí para ter o nome, porque eu fico imaginando que uma estação pode se repetir, né? É o UNO estação, não? Pois é, mas ele já está vinculando ao evento. Você pode ter uma estação que vai rodar no Carnaval, e a mesma estação vai rodar na Copa do Mundo, e a mesma estação é o mesmo equipamento, né? Não sei se a gente vai, se faz sentido ou deixa quieto. Ah, entendi o que você está dizendo. É, não, não, não, tem razão, acho.

**[00:26:39–00:27:11]** Tem razão. Ela não pode ser vinculada ao evento, não. Não, assim, não, não relação para um no caso, não tem que ser uma relação N para N, na verdade, né? Várias estações podem estar em vários eventos diferentes. Mas ela vai estar repetida em outro evento. Isso não impede que ela está repetida em outro evento, entendeu? Não impede.

**[00:27:11–00:27:44]** Este evento não impede ela estar repetido em outro evento. Você só diz que ela está mapeada naquele evento. Então, entendi o que você falou. Nada que um pós-processamento depois não faça a gente identificar estações que estão sendo repetidas. O negócio é só, como garantir que a gente vai conseguir fazer um processamento desse.

**[00:27:45–00:28:21]** Se a gente não tem informação correta, que identifica corretamente o equipamento, eu acho que é fudeu, porque teria que perguntar para equipamento, como é seu nome, para que a gente tivesse uma informação confiável. E o app de Grandes Eventos não vai perguntar para equipamento, porque o equipamento tem que estar do lado e a gente tem que ter essa comunicação ali configurada. É, eu não sei, acho que eu deixaria assim mesmo, deixa quieto mesmo, Augusto.

**[00:28:21–00:28:57]** e aí depois evolui, tentamente. É, porque aí é só informando o IP dela e dando um... usando um API universal, né, para perguntar para ela, ou aquela coisa do RFI já mesmo, né? É, tem esses dois caminhos. Provavelmente o RFI já não tem em todos, né? Tem equipamento que não gera informação e que pode ser que ele esteja aí no evento. É, um analisador experto qualquer aí, não...

**[00:28:57–00:29:35]** ou um analisador que está com a rubrica de RMX também. Tem algumas questões aí que o refúgio não vai saber responder. Deixe assim, velho, depois a gente evolui eventualmente. Mas vamos caminhando aí. Cada registro tem bem estação pertence a um único evento, ok? E dê evento da referência ao evento existente, as coordenadas aparente posição da estação e não precisa ser iguais, as coordenadas do evento, ok? Chaves e restrições, chave primária.

**[00:29:39–00:30:27]** Chave estrangeira, validação, ok. O ponto é confirmar se a identificação deve ser única dentro de cada vento. Imagino que sim. Só pergunte. Se o modelo será mais orado como descrição, como chave estrangeira para um cadastro próprio. Pronto é o que a gente está conversando, né? Tem dúvida também com a melhor approach. Porque assim, eu acho que só teria sentido se a gente conseguisse perguntar para equipamento quem iria.

**[00:30:28–00:31:16]** Para que a gente tivesse uma informação confiável. Se é declaração de fiscal, acho que vai ser furado de qualquer jeito. Precisão das coordenadas. Eu uso normalmente seis casos de s.m. Então, eu acho que além disso é só conversa-fiada. Sei lá. Mas... Seis casas são quantos nos 30 centímetros ou um metro? Eu acho que é...

**[00:31:16–00:31:52]** Eu acho que já é centímetro. Eu arriscaria aqui 11 metros, mas... Vocês estão confiantes que são centímetros, eu não vou fazer essa conta agora não. Porque o GPS já apora que é 15 metros, 30. E alguém no Google que é rapidão, mas é 11 centímetros a 1 metro. Ah, 11 centímetros, beleza. A depender que você tá, né? Beleza.


## Emissões e classificação

**[00:31:53–00:32:39]** É, vamos caminhar na ilha, tabela de emissão. Então, como estamos aí? Tabela de emissão, armazenas reis de emissões, na inseria emissão, o nome acompanha a time... Ok. ID da emissão, ID do evento, data da emissão, hora. Não existe um campo que pega o time stamp todo, não? E vira um string aí? Pode virar o time stamp todo. Não sei se isso foi feito por causa da...

**[00:32:39–00:33:09]** dos padrões da Anatel. Porque eu não vejo sentido nenhum estar separado assim. Também acho isso. Local, região, origem, captura e destação. Não, mas você pode estar falando de data e hora separada ali e tem o DH. Você pode colocar DH emissão types tempo inteiro. Aí é a escolha do modelo, entendeu?

**[00:33:10–00:33:45]** e ateja o o padrão da Anatel. O DT para colocar sua data, o HAH para colocar sua hora, para colocar data a hora DH. Não DH, André. Beleza. E D da estação. Esse campo não pode ser obrigatório aí não, ele está como condicional, o que que é isso? Essa terceira coluna aí é o que? Terceira coluna? É, de condicional, eu estou querendo...

**[00:33:45–00:34:27]** Obrigatório condicional. Chave estrangeira, quando a captura estiver vinculada a uma estação. Valeu da frequência em hertz, em megahertz. Valeu do largura em kilohertz. Descrição, faixa relacionada, identificação, diferente. E diferente para mim é buléano. É assim ou não?

**[00:34:35–00:35:13]** da cor aqui? Não, não tem. Aí você tem a observação, código de situação, ok? É o que estava lá na guia mesmo, né? Você tem que pagar pra fazer isso, Jesus, tem que pagar pra botar coisas. Beleza, tem problema não. O campo fiscal obrigatório na tela e possui um botão mais. Então, sobe aí no campo fiscal. Olhei desde a emissão, papapá, Tá bela isso, hein? Tá, ok.

**[00:35:13–00:35:56]** É porque deve ter um tabela auxiliar, né, que relaciona emissão com o fiscal. É que tem uma tabela fiscal, né? Que é estação, essa tabela que chama de, vá, baixei, baixei um pouquinho. A proposta de emitir vários fisicais participantes armazenados e relacionados abaixo e não como nomes ou lixas de identificador, ok, baixei. No relacionamento. Aí é o bridge emissão fiscal. Pronto, é isso aí, ok. Muitos para muitos, ok. Emissão imagem, aí pode ser emissão...

**[00:35:57–00:36:31]** documento anexo, sei lá como é que é, mas pode tirar o termo imagem também. ai nas chaves, que que é ai? chave primária, ok, é o padrão ali, ok. situação da emissão, os status funcionais são pendente, concluída pelo fiscal, concluída pelo corte anadu. acho que pode ser uma oportunidade de melhorar isso ai também cara, porque concluído pelo fiscal

**[00:36:32–00:37:10]** Dá uma sensação de que terminou, mas não terminou, porque o coordenador pode dizer não, abastalhado, está errado isso aqui. Eu acho que a gente pode ir para o padrão Anatel, do lado de fiscaliza, que é relatada e conferida, alguma coisa assim. Não precisa nem ser relatada pelo fiscal, já subintende-se que quem relata é o fiscal. Então, essa concluída pelo fiscal viria

**[00:37:10–00:37:46]** se transformaria em relatada, e a concluída pelo coordenador vira conferida ou aprovada, alguma coisa assim, porque no eFiscaliza a gente tem uma terceira instância, uma outra instância, que é o gerente que aprova. Eu acho que é isso, conferido ou aprovada, é simplificar a coisa. Então os códigos armazenados em qual situação ainda serão definidos, ok?

**[00:37:46–00:38:21]** A mensagem da tela informa que as emissões experintes serão submetidas à expressão da coordenação. As permissões entre elas devem ser definidas antes da implementação. Regras de consistência. Beleza, vamos caminhando aí, velho. Senão a gente vai passar a vida toda aqui. Pontos a confirmar. Opções dos seleitores, capturas realizadas por faixa, edificação e referente. Eu lembro que faixa tinha uma lista, né? Então, vai ser um drop down, né? Sim. Então, aí, ó.

**[00:38:21–00:38:53]** Quais selectores terão tabelas de domínio próprio? Então, eu acho que faixa tinha um domínio próprio. E aí você teria que substituir por uma chave estrangeira dessa tabela de referência. Sim, com certeza. Aí desculpa, eu tenho um pouco de dúvida quanto a isso. Quando você fala faixa, você fala exatamente o que? Tipo, VHF ou HF? Cara, não. É porque os caras têm uma nomenclatura lá própria.

**[00:38:54–00:39:21]** que eles chamam assim, aí é coisa que tá vindo ali do app que o Quintão construiu, né? E eu acho que é a forma que eles usam para sumarizar lá as ações. Aí teria que ver, eu já não lembro também os termos, mas eu diria rádio, celular, bloqueador, faixa de TV, tal, eles, microfone sem fio, radiação restrita, eles têm, que a gente pode mudar o nome, né?

**[00:39:22–00:39:50]** Porque para ser mais semântico, porque faixa realmente não tem nada a ver. Não, é porque tem coisas que, do jeito que eu estava pensando, tem coisas que sobrepõe, por exemplo, o HF lá de 300 mega, 3 gigas, Patron, por exemplo, satélite e banda L, que tem mega lá, na fase 1 GHz também. Então, era só essa dúvida aí para não ter coisa com o nome diferente que pegue as mesmas frequências.

**[00:39:50–00:40:33]** No RFFusion você tem isso, este canto? Não, tem não. Teria que ver, André, como é que está isso, cara? Eu sugeriria tirar esse nome faixa e colocar algo mais semântico. Eu acho que está mais associado à aplicação ou tecnologia do que a faixa propriamente. É porque eu não lembro quais eram as possibilidades lá no drop-down. Você lembra?

**[00:40:34–00:41:46]** Não, eu lembro. Mas aí é a questão de abrir a versão anterior e ver o que aparece lá no drop down. Mas eu riscaria que seria algo como aplicação ou tecnologia. Deixa eu ver se eu já tenho rodando aqui. Vai por rodar rapidinho. Quer que eu roda rapidinho? Vamos lá, abre lá a guia aí. Um minutinho. Um segundo eu põe para rodar.

**[00:41:46–00:42:28]** Vocês não estão vendo, mas tem um cidadão na minha frente aqui. Onde era mesmo aí? Emissão, a gente está lá. Aí eu acho que essa faixa relacionada, FN, SNA, SNN, SLP, radiação restrita está vinculada ao equipamento, a característica do equipamento. Aí tem ali vários serviços.

**[00:42:28–00:43:11]** TV, por exemplo, tem várias faxes, S&P tem várias faxes, satérias tem várias fa... outros. Enfim, tem que pensar no nome mais semântico aí, porque faixa realmente está furado. Acho relacionado. Aí, basicamente, serviço ou tecnologia relacionada. Mas aí tem que perguntar para o chat de Petit aí, o que ele sugere? Mostra aí para as coisas, o que que tem.

**[00:43:13–00:43:44]** O bolsonarismo se autodestruindo. Já querem queimar Tarsiso já. Eles são sacamas. Desde sempre, né? Porque eles querem fazer o curral eleitoral, que seja só a família, né? Sim, sim. Eles já estão autodestruindo Tarsiso, porque não pode ninguém aparecer, né? Tarsiso deveria ter sido candidato esse ano, né? Pois é, tinha boas chances de ter ganho na primeira...

**[00:43:44–00:44:19]** O Tassis é o cara que foi servido o público. Teria a chance de ser um cara de direita com um diálogo com a gente. Ele teria a chance maior. Não certeza, chance, não certeza. Vamos lá. Mas aí depois você vê, velho, a gente não precisa acompanhar senão. Vamos voltar ali para a tabela para o MD. Voltar. A tabela fiscal. Vamos tentar fazer uma leitura genâmica aí.


## Fiscais e funções por evento

**[00:44:19–00:45:01]** E dedo fiscal, nome, siga da unidade, coordenação, abordagem, monitoração. Eu fico pensando se... que o fiscal também muda de unidade, né? Ah, essa disco saía... pode se tornar inconsistente. É. Eu não sei se eu guardaria isso aí, não, cara. O assilio da unidade, por exemplo. Eu tô no Carnaval, eu tô inserindo um André, que é do Rio de Janeiro, no Carnaval do Salvador. Beleza, foda-se. Não problema, não.

**[00:45:01–00:45:32]** Você vai criar alguma validação vinculada à unidade? Eu não sei se a gente quer criar isso. Só se for para filtro, né? Isso é uma informação que o coordenador é interessante. Agora que pode ficar invado, pode, mas só ajuda o coordenador no dia a dia dele, né? É, pode ser. Também não me incomoda, não. Mas aí você vai ter que... Você tirar a garante que é em integral.

**[00:45:32–00:46:01]** Mas às vezes você atrapalha um pouco o coordenador no dia a dia, dá um pouco mais de trabalho pra ele. Você vai ter um bridge aí com eventos, né? Então você vai ter um tabela de N pra N aí, né? É. Bridge e evento fiscal, muitos para muitos. Ok. Então pra cada evento você vai ter ali um, ele pode ser coordenador no evento e pode ser abordagem no outro. Lembrando que...

**[00:46:01–00:46:36]** Teste e etiquetagem está onde? Eu acho que tem que ter um IC. Não, não. Eu acho que tem que ter ali, entre os papéis, tem um teste e etiquetagem. Teria que ter um IC Underline e teste e etiquetagem. Esse papel... Calma, até a tabela teste e etiquetagem. Vai chegar aí. Calma, calma, calma. Mas quem é que pode fazer teste e etiquetagem? Quem tem um perfil de teste e etiquetagem? Ah, não, desculpa. Entendi.

**[00:46:37–00:47:18]** Então, eu acho que tem mais um aí, tem um IC, teste e etiquetagem também. Você acha que deveria ter isso? Eu acho que já tinha. Não, não tinha não. Não tinha não. E cara, mas aí cada perfil novo que aparecer aí vai ter que alterar a tabela, né? Não. É... Ah, tá, sim. É, alterar a tabela não perde o dado anterior, não. Pois é, vai ser ruim aí, cara.

**[00:47:18–00:47:54]** Não dá pra fazer assim não. Essa tabela tá furando. Só uma coisa que em banco de dados já sofrou muito com isso, só o alter table. Calma, mas essa função do fiscal ele não pode estar nessa tabela. Essa tabela tem só o ID, o nome e a unidade. Ela termina aí. No futuro terá a senha. A bridge que relaciona

**[00:47:54–00:48:27]** O fiscal ao evento é que deve ter qual é a atribuição daquele fiscal com aquele ID para aquele evento. Tem certeza? Absoluta. Porque é o que o Maxwell está falando. Essa tabela aí vai ser única. Você vai ter o ID 1 fiscal, o ERIK, e aí você está definindo. O coordenador True, abordagem false, monitoração false.

**[00:48:27–00:48:55]** ai beleza, ai você me relaciona ao evento lá Carnaval de Salvador. ai a manhã eu vou para a Copa do Mundo, você vai ter que mudar a tabela de cima, só que porra aquele perfil era de Salvador. A atribuição tá, a atribuição é para cada evento, tem que alterar. Então essa tabela fiscal fica só os três primeiros campos e esses três últimos ai entram lá no evento.

**[00:48:56–00:49:29]** Tem que ver se em termos de banco de dados, se cabe na bridge, ou se é numa tabela auxiliar. Tem que caber, velho. Tem que ver se dentro do padrão da Anatel, se essa informação cabe ficar na bridge, entendeu? É só isso que estou aqui. Sim. Mas tem que ficar em algum lugar, né? Entendi. Aí nessa bridge de evento você vai ter um ID evento, ID fiscal e aqueles três, quatro campos de boleanas ali.

**[00:49:29–00:50:09]** Um perfil de cada um. Um unidade para muitos fiscais. Ah, então, sobe aí. Tabela unidade. Ah, tá. Então, aí você tá com a sigla da unidade, ok. Que a gente tem ainda. Pega ali da tabela da unidade. Baixa um pouquinho. Pega da tabela da unidade o nome da unidade, né? Ok. Beleza. Não precisa rever isso aí também, velho. Sim, sim. Então, baixa um pouquinho mais aí. Vamos caminhando aí.

**[00:50:16–00:50:46]** pontos a confirmar, obrigatoriedade de nome e unidade, tamanho dos campos, valores padrões, dos indicadores de papéis, pra mim é tudo false, o valor padrão. Então quando o cara entrar na guia lá insere um fiscal, teria que ser um registro nessa bridge aí, fiscal evento e tudo false. E aí o cara tem que marcar lá o checkbox, como já tava, né? política de exclusão, pra poupar na cidade de uma trícola.


## Incidentes e índices

**[00:50:46–00:51:32]** Beleza, tabela incidente, tabela incidente, baixe um pouco mais ainda, ID, ID do evento, código de estipo de incidente, código de situação, descrição do local, last of longitude, geometria do ponto, que porra é essa? Fira aí, sem... sem invenção, hein? Isso aí é coisa que o Bobão gosta, né, para acelerar.

**[00:51:32–00:52:04]** porra, de geometria do ponto. Lachore longe de tudo só. Taste de observação, teste de observação. Oh, o data e hora aí que o Max falou. Data, hora, criação. Pronto. Então só tira esse geometria do ponto aí. Isso aqui deve ser coisa... Isso é coisa da padrão da Anatel, sabia? É, mas não precisa não. Inútil a gente ignora. Pois inútil a gente ignora.

**[00:52:04–00:52:53]** Lat Long em graus das imagens e pronto. Domínios, abaixo um pouquinho mais aí. Relacionamentos. Cada incidente pertence ao evento, cada incidente possui um tipo de incidente, cada incidente possui uma situação atual. Cada chave, incidente fiscal, muitos para muitos. E substituir essa imagem por anexo, um incidente para muitas imagens. Beleza.

**[00:52:57–00:53:39]** Chaves, índices e validações, embaixo um pouquinho. Índices espacial. É, está, isso aí tem que apagar, velho. É a história desse índice espacial aí. O que isso? Validação de latitude, ok. Índice de situação. Ok, aí está, beleza, beleza. Caminhando aí. Isso aqui é Augusto, só, algo, isso aqui deve ser, será que isso aqui é a validação, ganhando o banco já? Parece que sim, né?

**[00:53:40–00:54:06]** É, isso aí é constrante, restrição. É constrante. Isso, eu não posso ter uma latitude menor que menos 90 e meio maior que 90, né? Isso a gente vai falar de coordenadas ali, né? As coordenadas convencionais. Assim que se espacial realmente, cara, eu não, né? Eu apagaria, não mexerei com esse negócio não.

**[00:54:07–00:54:34]** Índice espacial é para acelerar, é coisa bem que Lobão gosta, Lobão se tivesse aqui é mandar apagar a mão. Mas a gente aproveita que Lobão está aqui na reunião e aí a gente apaga. E outra coisa, índice do evento... É que vai ser nem ser usado. É, procurar pelo latilon, entendeu? É só índice do evento...

**[00:54:34–00:55:28]** Ele é o ID do evento. Então o ID do evento se não está enganado é a chave primária. A chave primária já atua como índice. Talvez eu não preciso nem tirar esse índice do evento ali, por exemplo. Já meio que já vem automática. Não precisa de sair também não, verdade. Pode botar o comentário aí. O ID do evento já é a Varmarike, PK, né? Então já atua como índice. Já atua, estou pensando aqui bem.

**[00:55:42–00:57:12]** Esse banco não vai crescer mesmo. Irrelevante, nem vai ser procurado por ele ser índice mesmo. Índice é uma coisa que não consome banco e acelera muito. Posso continuar? Pode ser. Outra bela Ticket. Ticket, evento. Nesse caso, um Ticket sempre está até lá de um evento, né? Mas esse ID do fiscal que eu acho que está errado aí, cara. Sim, está faltando coisa.


## Tickets, log e auditoria

**[00:57:12–00:57:47]** Porque tem que ser um bridge também, que você pode ter um ticket para vários fiscais. Sim. Sobe lá no incidente, na emissão, só para a gente ver como é que está. Aí, aí, pronto, aí no incidente não tem fiscal, está no bridge. Sobe lá em emissão. Emissão, também é a mesma coisa. O fiscal não está aí. O ticket também tem que ser a mesma coisa.

**[00:57:49–00:58:27]** Você pode ter um ou mais fiscal, então não dá para ser aquele ID direto ali não. É, botou aqui a confirmar. Então tem que ter um bridge aí. Código da situação do Ticket. Pois é, assim... Código de situação, não. Não precisa botar esse suffixo aí não. Prioridade, texto de observação, texto, motivo da evolução... É, isso aí é coisa que eu tenho dúvida, cara.

**[00:58:30–00:59:03]** O que assim, o negócio pode ir e voltar mil vezes? Sim. Então, o cara, eu fechei. Aí você revisou e devolveu. Aí eu fechei de novo. Aí você devolveu de novo. E isso pode ser infinita. Não terminar nunca esse processo. Então, eu acho que tem que ter uma outra tabela que guarda esse log de devolução e relato. E deveria ter, ao final do dia, um histórico, que você visse a coisa.

**[00:59:11–00:59:46]** Então eu tiraria daí, eu tiraria daí o texto de providência e o texto motivo de devolução e pode ocorrer em providências também, esse nome ruim, providência. Então esses dois campos eu tiraria daí, a data do atualização. O Eric, só uma coisa cara, eu estou olhando aqui o normal aqui.

**[00:59:46–01:00:15]** Pela wiki, da sg, de vantidade, ele fala o seguinte. Tabela de logs são aquelas que mantêm informações de operações realizadas no sistema. Nesse caso, verifique se existe a possibilidade de utilização de arquivos físicos. Eu não sei se valeu a pena colocar isso no arquivo, não sei. Aí eu estou só trazendo aqui a regra para vocês. Exato o problema que ele transforma o backup em uma...

**[01:00:15–01:00:42]** É a complexidade do backup, pioramente. Você não vai fazer mais backup do banco, só fazer backup do banco e do arquivo, né? A gente já tem, né? A gente já tem ao final do dia arquivos, porque a gente está abrindo a possibilidade do cara anexar porra toda tudo. Então seria só um anexo vinculado...

**[01:00:42–01:01:13]** Seguiria a mesma lógica do repositório de arquivos, autíquete. Mas os arquivos são quando é nexado, ele vai para dentro do banco, tá? Ele vai com um blob, para dentro do banco. Ah, ele está indo com um blob? Ele vai para o blog dentro do banco. Então, no caso, vocês precisam de uma tabela de log, né? Aquilo que qualquer operação que for feita tem que estar nessa tabela ali, né? O cara modificou, o cara...

**[01:01:13–01:01:41]** mudou está, derrubiu. Ainda não botei a tabela de auditoria ainda não. Isso não pece ainda não. O objetivo não é simplificar? Não, tudo bem. É porque assim, pelo que eu estou lendo aqui, tem a diferença entre log e histórico. O histórico está dizendo que mantém a situação anterior de um registro. Guarda que como se fosse a última informação de um registro não fica fazendo a time de log. Isso, isso aí.

**[01:01:42–01:02:11]** É, eu acho que a auditoria, André, eu acho que não precisa não, ela pode voar mesmo. Mas para esse caso específico do ticket, porque é o final do dia onde as pessoas vão trabalhar no ticket. Elas não vão trabalhar na emissão, emissão e incidente é só cadastro. Sim. E essas porras, se o coordenador quiser vir um ticket, pode ser tudo junto, enfim. Então, para o ticket, a gente precisa ter esse log.

**[01:02:11–01:02:44]** de fechou, abriu, fechou, abriu, fechou, abriu. Sim. Então, no ticket, eu criaria lá. Ticket criado. Está lá no log. O depois é ditado, campo tal, valor antigo, valor novo. Alterou o estado. O cara devolveu com esse texto. O cara finalizou de novo com esse texto. Então, para esta tabela específica,

**[01:02:46–01:03:51]** É o único que teria o log, né? É um PN, né? Um Ticket, pode ter N, Logs, né? Isso. Ok, aqui, o sono. Sim, aí só lembrando esse último aí também, né? Task de providência, data da atualização, todas as coisas aí, a própria data da criação, eu acho que a gente tira do log. Só se você quiser replicar aí.

**[01:03:52–01:04:23]** Mas acho que vai tudo pro log aí cara. Dato da criação, mas é no Ticket. Isso, pra mim vai tudo pro log. Vai lá pro log? Pode estar aí também, tem problema. Isso aqui é o único. Isso aqui é o único, ele foi criado uma vez no Ticket. Pronto, beleza, pode ficar aí. A atualização pode pro log. Isso, beleza. Então, atualização, esse texto de providência também sai fora.

**[01:04:25–01:04:59]** e ali no código de situação, você pode tirar o sufixo também ali do ticket e aí cada estância tem o seu co situação e o IDFiscal sai fora, você já colocou ali, está no grid. Ah tá, pode tirar isso aqui, está bom. Eu estou gravando, tudo isso que a gente está falando, eu vou gerar um arquivão que onde eu vai, vai estar tudo registrado bonitinho.

**[01:04:59–01:05:50]** ai vai da merda, vai beleza, vamos caminhando ai, ai tabela tíquete fiscal, um evento pode possuir vários tíquetes, cada tíquete pertence a um evento, um tíquete pode estar associado a zero ou várias emissões, um tíquete pode estar associado a zero ou vários incidentes, as associações.

**[01:05:50–01:06:26]** Não era o Bridge. Mas deve estar embaixo, né? Baixo um pouquinho mais. Mas a tabela Ticket Fiscal não seria o Bridge? Sim, acho que sim. Pela nomenclatura que está se usando. Entendeu? Primeira função do Bridge é a função da tabela Ticket Fiscal. Para ver se aqui esteja em excesso.

**[01:06:27–01:06:57]** As emissões de acessibilidade são independentes, a inclusão de um tipo não exige nem pede a inclusão do outro. As emissões de acessibilidade são dependentes ao mesmo nível do ticket. O vínculo opcional e de fiscal em tickets não, isso aí já morreu. Como tabela associativa, eu posso deixar a vista onde é melhor. Abaixo um pouquinho, pode ser que ele tenha colocado embaixo aí. Ah não, não colocou não. É, tem, então aquela ali são os bridges, né? Com as outras tabelas.

**[01:06:57–01:07:29]** Ausência de vínculos com emissões, incidentes é válida, não exigir uma sessão. Ao devolver um ticket concluído para fiscal, exigir e persistir. Essas questões aí que tem que ter cuidado desse motivo da devolução, tem que ter o log lá para... Vamos confirmar. Valores e códigos de domínio de situação, ok. Papel de ID fiscal morre. Então, isso aí vira pretty, ticket, fiscal.

**[01:07:29–01:08:03]** Se a providência era um campo atual ou registra uma tabela histórica própria, então a gente vai migrar para isso aí, com uma tabela de log, o campo providência. Se a tributação de pelo menos um fiscal será obrigatória, se um ticket pode ser criado sem emissão e sem incidente. Ah, não, né? Não. Como garantir no banco da aplicação que a emissão e incidente pertence a um evento de ticket? Você vai ter que olhar pro bridge, né?


## Teste, etiquetagem e cadastro de entidades

**[01:08:04–01:09:13]** Então na tabela de testa e etiquetagem, como estamos? Pode perfil. A gente não é melhor ter uma tabela com a quantidade não, cara. Tô pensando aqui porque vai ter entidade sem CNPJ, sem CPF, né? Fudeu, né? Então não dá. É, que seria a entidade estrangeira. O estrangeiro não tem CPF, não tem CNPJ.

**[01:09:14–01:09:59]** Sim. É porque está misturada aí, né? É que quando você põe como estrangeiro, ele não resiste, nem CPF, nem CNPJ. Aí fica nulo, né? Deixe vazio. Mas seria melhor guardar aí uma ID para essa tabela e tirar isso aí, ou não. Não deveria ter uma tabela, entidade. E o campo poderia ficar vazio, o nulo. Mas quando você faz o cadastro de uma entidade aí,

**[01:10:02–01:10:38]** Você, Salve, tabela, perfil, entidade. Você é da Pessoa Física Jurídica ou Estrangeiro? Ah, não, tudo bem. Pessoa Física Jurídica ou Estrangeiro, ok. Mas ali embaixo tem nome da entidade. Tem código de CNPJ. Tem... Oh, tá. Nome do responsável. Tudo isso está vinculado à entidade. Código de telefone. É em meio. Meu ponto é... Eu acho que a gente deveria tirar e sair daí. E no teste de etiquetagem...

**[01:10:38–01:11:15]** Tem um ID que joga lá pra essa tabela com tudo isso. E cada as entidades, então? Eu só não sei qual seria a chave dessa porra aí. O ID pode ter uma entidade estrangeira sem CPF, né? Ah, vai ter que ter um ID único, independente do CPF, independente do CNPJ. Sim. E aí eu fico pensando, porra, pode ser que tenha uma empresa grande.

**[01:11:15–01:11:45]** COFRE, COFRE presta serviço em Brasil todo. e o responsável dela aqui em Salvador é diferente do responsável do Rio, né? Sim, então não sei se talvez seja melhor aí, mas por outro lado, a COFRE chegou aqui com 100 equipamentos para etiquetar hoje e amanhã ela chega com outros 100. O responsável de hoje é Eric, aí eu vou anotar o nome Eric. O responsável de amanhã é Augusto, eu vou anotar o nome Augusto.

**[01:11:45–01:12:17]** meio confusão isso ai, velho. e a gente, ai pute, eu preciso ligar, ai eu olho aqui na linha, esse sistema está causando interferência. eu vejo que é o responsável Augusto. Augusto, porra velho, ou Augusto não atende ou ele atende e diz cara, não sou eu que estou aí hoje não. então se eu tivesse centralizado, eu ia ver que a empresa Coffre tem cinco responsáveis aqui. que poderia ser só uma tela de consulta, né? que responderia isso pra gente.

**[01:12:17–01:12:58]** Ou então a gente já organiza uma tabela de entidade. Aí complicou, né? Eu acho que é melhor, eu não sei, a sensação é que isso aí, como pode não ter um CNPJ CPF, você talvez deixe essa porra aí mesmo, mas aí a gente teria que ter uma tela de consulta, que eu consulto lá, cofre e vai vir todos os registros.

**[01:12:58–01:13:28]** que aparece asorra, porra, mas aí vai vir um quê? Vai vir um teste de etiquetagem. Mas você está nessa tabela. Eu sei, o questão aí do telefone também a gente resolva na regra de negócio, né? Tipo assim, tem um cara que é responsável, enfim, liga para ele e ele vai direcionar a pessoa correta, não sei. Você precisa sofrer aqui dentro do sistema com isso não.

**[01:13:28–01:13:57]** Não é, beleza. Eu acho que na consulta também a gente pode fazer. A gente pode ter uma consulta lá direcionada à entidade. E aí eu entro no nome da entidade. E aí a gente pesquisa na tabela de testa de etiquetagem todos os campos no underlying entidade que tem aquela palavrazinha chave que eu inseri. E aí ele vai retornar, eu achei esses 15 caras aqui. E aí na visualização da GUI a gente coloca nome à entidade

**[01:13:57–01:14:34]** Nome, responsável, contato, corte o telefone e dê em meio. E do lado, o IT do teste de etiquetagem, se o cara quiser entrar ali. Mas a gente pode ter uma visualização de GUI para resolver esse problema. Não, não, não, digo... Pode ter um responsável só e... Como é que é um nome lá? Um nome do... Sobe um pouquinho aí, André. Não... CO, CPF, CNPJ... Terei o que ter algum tipo.

**[01:14:34–01:15:07]** Pelo nome da entidade, aí você vai ter só uma entidade e um responsável, Eric. Entendeu? Você não precisa ter várias responsáveis na mesma entidade. Aí mesmo que você vá no primeiro dia e lê os equipamentos, sei lá, vai botar o Eric como responsável. No segundo dia eu chego com mais 100, deixa no Eric lá. Aí o Eric, a figura do Eric lá, redireciona caso precise. Perceba, perceba aqui.

**[01:15:07–01:15:36]** É, isso precisa ser uma tabela específica, cara. Perceba que todo dia o cara vai ter que escrever o nome da empresa, o CNPJ, isso é o que? Mas aí pensando na guia aqui, se o cara insere o nome do CNPJ, a gente já poderia fazer uma consulta lá naquela tabela específica de entidade. E aí essa consulta, a partir da guia, poderia ser via texto.

**[01:15:36–01:16:07]** Então se não tem CNPJ, antidade estrangeira, eu vou começar a escrever aqui o nome da entidade. E aí ele poderia me retornar ou o CNPJ CPF e aí ele retorna. E aí ele já preenche na tela de etiquetagem as informações que já vende lá dessa tabela de entidade. Não, beleza. Fica bom assim. Mas aí nessa tabela de entidade... Então isso aí tudo, André, pode sair fora dessa tabela aí, cara. Vira...

**[01:16:07–01:16:35]** ID entidade. Isso aqui é um domínio lá, tabela de domínio para entidade, TB entidade, sei lá. Isso, e aí eu sugiro que no da entidade a gente crie também um campo textual, tá? Para que a gente possa... Mas vem cá, quando essa tabela de entidade vai ser preenchida? Pelo teste de etiquetagem. Pelo teste de etiquetagem.

**[01:16:35–01:17:07]** O teste de etiquetagem ele primeiro consulta e se não tiver nada inclui registro. Ok. Se não tiver nada eu preencho esses campos e aí lá eu insiro nessa luta tabela. Isso. Mas eu sugiro que nesse domínio de entidade a gente tenha também o campo textual livre para que a gente possa dizer porque vai ter um campo responsável em meio telefone.

**[01:17:07–01:17:46]** Mas porra, eu tenho aqui 5 telefones, 10 emails e 3 responsáveis, eu coloco tudo lá nesse texto longo da descrição. Eu preciso dizer quais caracteres tem no texto longo ou é infinito? Infinito eu acho. Texto curto que eu preciso dizer, né? Acho que é limitado. Só perguntar para o chat. Ah, no Postgres não sei não cara, no MariaDB eu tinha que colocar lá tipo uma rede de caracteres.

**[01:17:46–01:18:19]** Contos caractérios, né? Não posso ouvir... Não, mas não se preocupe, não, André. Vamos caminhando aqui. Então, em relação a esta tabela, o importante é criar uma outra tabela de entidade, que vai ter todos esses campos aí, vinculados à entidade, inclusive um campo novo, texto, informações adicionais. E aí, na tabela de etiquetas, a gente tem só o ID.

**[01:18:19–01:19:47]** Desta entidade. Beleza, vamos caminhando aí. Aí tem código tipo, quantidade de equipamento, texto de observação, ok. Beleza, é isso aí. Então esse cara tem dois equipamentos, dois registros nessa tabela, dois equipamentos diferentes. Se é um equipamento com várias unidades, aí fica um registro só, ok. Tabela, testa etiquetagem frequência. Então ele vincula com a tabela de cima.


## Frequências, largura de banda e domínios

**[01:19:47–01:20:32]** E aí ele pega, então, você pode ter um pra N aí, né? Um teste pra N frequências. Duas frequências pelo botão geram dois registros dependentes e não duas colunas no teste. Ok. Eu só tenho dúvida, cara. Novamente, sobre essas obras, dessas faixa. Porque não é faixa, né? Então, valor e frequência megahertz, beleza. Eu acho que esse...

**[01:20:32–01:21:05]** Code, banda, banda selecionada para extra frequência, confirmar a unidade, os valores do seleitor, banda selecionada para extra frequência. Eu lembro que o pessoal tinha sugerido, a gente colocava a longe frequência megahertz e a largura de banda, né, quilohertz. E aí tinha lá um drop down, você pode até abrir aí. Qualquer espaço que eu... entrei no teste etiquetagem.

**[01:21:06–01:21:36]** Novo... Ai, eu tipo... Não, não é isso, né? Ah, tá, pronto. É, banda... Então, isso... Essa banda, na verdade, é largura de banda. Então, é largura de banda em kilohertz. Então, esse nome não é banda, substitui lá pro largura. Eu acho que lá em cima, na emissão, também tem escampo. Então, vamos pegar a mesma nomenclatura. E faixa, clica em faixa. Eu acho que é aquela mesma...

**[01:21:36–01:22:21]** Pronto, é aquela mesma zorra lá. Perceba que a lista é diferente. Sem... Oh, os caras ficam inventando um monte de lista, merda. Clica aí de novo nessa lista, hein? SLP VHF, SLP UHF, SLP 800M, SLP 12.4, radiação restrita. Loura, outra faixa autorizada pela Anatel. Ok, é uma outra tabela, essa porém, né? Beleza.

**[01:22:26–01:23:10]** Faixa também não é o melhor nome não, tem que ser algo mais semantico aí. Pensa aí. O code banda vira valor, largura, underline e kilohertz. Esse code banda aí de cima. E aí você tem que ver como é que você vai salvar isso. Se você vai salvar como texto, porque você está escolhendo lá de um drop down. Então aí seria code largura, kilohertz, né?

**[01:23:11–01:23:44]** Codem, Underline, Largura, Underline, Kilohertz. Aí depois olha lá em cima, na tabela de emissão, você tem que definir também a largura. Eu acho que está sendo salvo como decimal. Mas aí você confirme e depois deixa tudo igual. Então, data de criação, beleza. Lacha mais, hein. Domines e relacionamentos complementares. Perfira a entidade, então beleza. Isso aí, na verdade, vai ser um relacionamento lá da tabela nova, de entidade.

**[01:23:44–01:24:18]** Não, dessa aí. Então você vai ter um relacionamento com a tabela entidade. Tabela licença, tabela tipo de equipamento, tabela permissão, etiqueta, tabela faixa, banda, tabela, etiqueta, e anexos, tabela, etiqueta, anexo. Ai que bosta, que que pãe ele foi? Vou botar no espaço?


## Próximos passos e encerramento

**[01:24:37–01:25:08]** O que eu sugiro? Eu sugiro você montar estas tabelas. Você está usando o que? Postgre? Postgre é um nome. Montar as tabelas. E aí a gente faz uma inclusão aqui de um evento. Não via aqui, direto lá no banco, para que a gente possa ter aquela visão lá que o Augusta está mostrando lá, espacial do relacionamento e das coisas.

**[01:25:08–01:25:39]** Você sugere alguma coisa, Augusto? Próximo passo aqui, depois das justiça. Acho que é isso, cara. Vamos visualizar primeiro esse banco desenhado. O The Beaver faz isso, o próprio PopCoPilot lá, quando você fizer o esquema com o SQL, ele desenha direitinho. Aí parece que vai ficar um banco bem mais enxoto, assim.

**[01:25:39–01:26:06]** Estou de acordo era que a gente faz um cadastro ali primeiro, de um evento, ali a gente faz os testes. Será que depois vai ter face gráfico? Beleza, pode ser assim, André? Beleza, ótimo. Então beleza, papá, joga dura aí, a gente vai se falando aí. Eu comecei a brincar aqui, de gerar uma estrutura básica em fastepied.

**[01:26:06–01:26:37]** Começamos a programar na mão. Começamos a estudar como vai ser esse processo de programar na mão. Vici tinha uma ferramenta de desenhar, mas ferramenta é pago. Então, exclui isso. Vamos lá. Minha sugestão. Talvez tenha sido mal-entendido. Não é para você programar na mão. Mas é para você saber o que está acontecendo no projeto.

**[01:26:37–01:27:01]** Vou desenhar uma tela, vou desenhar uma tela, vou desenhar, vou pedir para ele gerar tela para mim, mas eu vou fazer o halter na mão, o principal que eu quero fazer na mão é o seguinte, inserte SQL, eu vou gerar o código desse inserte, mas eu quero na mão colocar, porque esse foi o principal que ele zoneou, entendeu? Eu não gostei disso.

**[01:27:02–01:27:27]** Você vai ter que ter, o que eu sugiro, cara? Então agora eu fiz uma refatoração do app Coleta. E app Coleta, cara, eu tinha uns 10 lugares que se comunicava com o instrumento. Então tinha 10 arquivos diferentes que mandava o comando e recebia coisa do instrumento. Você tem que centralizar isso em um lugar só. Se isso vai ser uma classe estática,

**[01:27:27–01:27:56]** uma classe abstrata com métodos estáticos, ou se isso vai ser métodos de uma classe que você estanciou, não sei, mas você tem que centralizar toda a comunicação com o banco em um lugar só. Deu merda, eu sei que é a comunicação com o banco, aquele arquivo específico ali do projeto. Exceto se foram milhões de consultas, aí você deixa ali quatro arquivos, na mesma subpasta.

**[01:27:56–01:28:32]** SQL, Communication ou Salaque Povo. Sim, sim. Mas assim, é importante a gente também não escrever todo código, a gente não está mais nesse mundo. Não, claro, claro. A gente só não pode perder controle do que está sendo escrito, do código. Tá bom? Mas aí vamos fazer isso cara, faz esses ajustes aí no banco, nas tabelas todas, que a gente está conversando aqui hoje.

**[01:28:32–01:29:02]** faz o desenho dela e vamos fazer umas inclusões sem Gui ainda para que a gente possa ver se está tudo bonitinho, os relacionamentos e aí depois você cai para dentro da Gui aí, pode ser? Beleza, com certeza. Então beleza, senhores, dá uma abração para todo mundo, a gente vai se falando aí. Valeu pessoal, se não falar mais, bom fim de semana e para vocês. Valeu, passando. É que sexta é feriado, né? É, sexta é feriado.

**[01:29:02–01:29:09]** Deixe-me filhar. Valeu galera, abração. Valeu, tchau tchau pessoal.

