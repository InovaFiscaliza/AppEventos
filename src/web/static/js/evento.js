/**
 * Controla o mapa, a consulta de município, a equipe e a revisão do cadastro.
 */

/** Botão que abre o mapa dentro do cadastro. */
const abrirMapa = document.getElementById("abrir-mapa-evento");

/** Botão que fecha o mapa sem aplicar a seleção. */
const cancelarMapa = document.getElementById("cancelar-mapa-evento");

/** Diálogo que contém o mapa de seleção do local. */
const dialogMapa = document.getElementById("dialog-mapa-evento");

/** Botão que aplica o ponto selecionado aos campos de coordenadas. */
const confirmarMapa = document.getElementById("confirmar-mapa-evento");

const expandirMapa = document.getElementById("expandir-mapa-evento");
const zoomComRolagem = document.getElementById("zoom-scroll-evento");

/** Campo de latitude, editável manualmente e preenchido também pelo mapa. */
const latitudeEvento = document.getElementById("latitude");

/** Campo de longitude, editável manualmente e preenchido também pelo mapa. */
const longitudeEvento = document.getElementById("longitude");

/** Instância do Leaflet criada na primeira abertura e reutilizada nas seguintes. */
let mapaEvento;

/** Marcador do Leaflet reutilizado a cada seleção. */
let marcadorEvento;

/** Coordenadas temporárias da seleção atual, limpas a cada abertura do mapa. */
let pontoSelecionado;

abrirMapa.disabled = !window.L;

// Abre o diálogo antes de inicializar o Leaflet para que o mapa tenha dimensões visíveis.
abrirMapa.addEventListener("click", () => {
    dialogMapa.showModal();

    if (!mapaEvento) {
        mapaEvento = L.map("mapa-evento", { scrollWheelZoom: zoomComRolagem.checked })
            .setView([-14.2, -51.9], 4);

        L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 19,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        }).addTo(mapaEvento);

        marcadorEvento = L.marker([0, 0]);

        // Guarda o ponto clicado para que ele possa ser aplicado ao confirmar a seleção.
        mapaEvento.on("click", ({ latlng }) => {
            pontoSelecionado = latlng.wrap();
            marcadorEvento.setLatLng(pontoSelecionado).addTo(mapaEvento);
            confirmarMapa.disabled = false;
        });
    }

    pontoSelecionado = null;
    marcadorEvento.remove();
    confirmarMapa.disabled = true;
    // Recalcula as dimensões do mapa após a abertura do diálogo.
    mapaEvento.invalidateSize();
});

expandirMapa.addEventListener("click", () => {
    const expandido = dialogMapa.classList.toggle("evento-mapa-expandido");
    expandirMapa.textContent = expandido ? "Restaurar tamanho" : "Expandir mapa";
    mapaEvento.invalidateSize();
});

zoomComRolagem.addEventListener("change", () => {
    if (zoomComRolagem.checked) {
        mapaEvento.scrollWheelZoom.enable();
    } else {
        mapaEvento.scrollWheelZoom.disable();
    }
});

cancelarMapa.addEventListener("click", () => dialogMapa.close());

// Aplica as coordenadas ao formulário com seis casas decimais e fecha o mapa.
confirmarMapa.addEventListener("click", () => {
    if (!pontoSelecionado) return;

    latitudeEvento.value = pontoSelecionado.lat.toFixed(6);
    longitudeEvento.value = pontoSelecionado.lng.toFixed(6);
    dialogMapa.close();
    consultarMunicipio();
});

/** Campo somente leitura que exibe o nome e a UF do município encontrado. */
const municipioEvento = document.getElementById("municipio-evento");
/** Região que anuncia o andamento e o resultado da consulta. */
const statusMunicipio = document.getElementById("municipio-evento-status");

/**
 * Controlador da consulta mais recente. Permite cancelá-la ao editar as coordenadas.
 * @type {AbortController | undefined}
 */
let consultaMunicipio;
/** Indica que o resumo ainda aguarda a consulta da localização. */
let consultandoMunicipio = false;

/**
 * Cancela a consulta anterior e limpa o município e a mensagem exibidos.
 * @returns {void}
 */
function limparMunicipio() {
    consultaMunicipio?.abort();
    consultandoMunicipio = false;
    municipioEvento.value = "";
    statusMunicipio.textContent = "";
}

/**
 * Consulta o FastAPI quando a latitude e a longitude estão preenchidas e válidas.
 * Exibe o nome e a UF quando encontra um município ou informa o resultado da consulta.
 * @returns {Promise<void>}
 */
async function consultarMunicipio() {
    limparMunicipio();

    const latitude = latitudeEvento.value;
    const longitude = longitudeEvento.value;

    if (!latitude || !longitude ||
        !latitudeEvento.validity.valid || !longitudeEvento.validity.valid) {
        return;
    }

    const consulta = new AbortController();
    consultaMunicipio = consulta;
    consultandoMunicipio = true;
    statusMunicipio.textContent = "Identificando município…";

    const parametros = new URLSearchParams({ latitude, longitude });

    try {
        const resposta = await fetch(`${municipioEvento.dataset.consultaUrl}?${parametros}`, {
            signal: consulta.signal,
        });

        if (!resposta.ok) throw new Error("Falha na consulta");

        const municipio = await resposta.json();
        if (consulta.signal.aborted) return;

        if (municipio) {
            municipioEvento.value = `${municipio.nome} (${municipio.uf})`;
            statusMunicipio.textContent = "";
        } else {
            statusMunicipio.textContent = "Nenhum município identificado nesse ponto.";
        }
    } catch {
        if (!consulta.signal.aborted) {
            statusMunicipio.textContent = "Não foi possível consultar o município.";
        }
    } finally {
        if (!consulta.signal.aborted) {
            consultandoMunicipio = false;
            if (dialogConfirmacao.open) atualizarMunicipioNoResumo();
        }
    }
}

// Limpa o resultado enquanto o usuário digita e consulta ao concluir a edição.
for (const campo of [latitudeEvento, longitudeEvento]) {
    campo.addEventListener("input", limparMunicipio);
    campo.addEventListener("change", consultarMunicipio);
}

const formularioEvento = document.getElementById("formulario-evento");
const fiscalResponsavel = formularioEvento.elements.namedItem("id_fiscal_responsavel");
const buscaFiscal = document.getElementById("buscar-fiscal-evento");
const resultadosFiscais = document.getElementById("resultados-fiscais-evento");
const statusBuscaFiscais = document.getElementById("status-busca-fiscais");
const equipeFiscais = document.getElementById("equipe-fiscais-evento");
const equipeVazia = document.getElementById("equipe-evento-vazia");
const valoresEquipe = document.getElementById("equipe-fiscais-valores");
const statusEquipe = document.getElementById("status-equipe-evento");

/**
 * Normaliza um nome para busca, removendo acentos e diferenças de caixa.
 * @param {string} nome Nome cadastrado ou texto digitado.
 * @returns {string} Texto usado na comparação.
 */
function normalizarBuscaFiscal(nome) {
    return nome.trim().normalize("NFD").replace(/\p{Diacritic}/gu, "").toLocaleLowerCase("pt-BR");
}

/** Cadastro de fiscais fornecido pelo seletor de responsável. */
const fiscaisPorId = new Map(
    Array.from(fiscalResponsavel.options)
        .filter((opcao) => opcao.value)
        .map((opcao) => {
            const nome = opcao.textContent.trim();
            return [opcao.value, { nome, busca: normalizarBuscaFiscal(nome) }];
        })
);

/** Seleções explícitas, restauradas dos campos ocultos em caso de erro. */
const fiscaisAdicionados = new Set(
    Array.from(valoresEquipe.querySelectorAll("input")).map((campo) => campo.value)
);

/** Exibe os fiscais disponíveis e limita a lista inicial de resultados. */
function renderizarResultadosFiscais() {
    const termo = normalizarBuscaFiscal(buscaFiscal.value);
    resultadosFiscais.replaceChildren();
    statusBuscaFiscais.textContent = "";
    if (!termo) return;

    const encontrados = [...fiscaisPorId].filter(([id, fiscal]) =>
        id !== fiscalResponsavel.value && !fiscaisAdicionados.has(id) && fiscal.busca.includes(termo)
    );

    for (const [id, fiscal] of encontrados.slice(0, 8)) {
        const item = document.createElement("li");
        item.className = "evento-fiscal-linha";
        const adicionar = document.createElement("button");
        adicionar.type = "button";
        adicionar.className = "btn btn-secondary evento-fiscal-adicionar";
        adicionar.textContent = "+";
        adicionar.setAttribute("aria-label", `Adicionar ${fiscal.nome}`);
        adicionar.addEventListener("click", () => {
            fiscaisAdicionados.add(id);
            buscaFiscal.value = "";
            atualizarEquipe();
            statusEquipe.textContent = `${fiscal.nome} foi adicionado à equipe.`;
            buscaFiscal.focus();
        });
        item.append(fiscal.nome, adicionar);
        resultadosFiscais.append(item);
    }

    if (!encontrados.length) {
        statusBuscaFiscais.textContent = "Nenhum fiscal disponível corresponde à busca.";
    } else if (encontrados.length > 8) {
        statusBuscaFiscais.textContent = "Exibindo 8 resultados. Refine a busca para ver outros nomes.";
    }
}

/** Atualiza a lista e os IDs enviados pelo formulário. */
function atualizarEquipe() {
    equipeFiscais.replaceChildren();
    valoresEquipe.replaceChildren();

    const responsavel = fiscalResponsavel.value;
    const membros = new Set([responsavel, ...fiscaisAdicionados]);
    membros.delete("");
    equipeVazia.hidden = membros.size > 0;

    for (const id of membros) {
        const { nome } = fiscaisPorId.get(id);
        const item = document.createElement("li");
        item.className = "evento-fiscal-linha";
        item.append(nome);

        if (id === responsavel) {
            const papel = document.createElement("span");
            papel.className = "evento-fiscal-papel";
            papel.textContent = "Responsável";
            item.append(papel);
        } else {
            const remover = document.createElement("button");
            remover.type = "button";
            remover.className = "btn btn-secondary evento-fiscal-remover";
            remover.textContent = "−";
            remover.setAttribute("aria-label", `Remover ${nome}`);
            remover.addEventListener("click", () => {
                fiscaisAdicionados.delete(id);
                participantesSugeridos.delete(id);
                atualizarEquipe();
                statusEquipe.textContent = `${nome} foi removido da equipe.`;
                buscaFiscal.focus();
            });
            item.append(remover);
        }
        equipeFiscais.append(item);
    }

    for (const id of fiscaisAdicionados) {
        const campo = document.createElement("input");
        campo.type = "hidden";
        campo.name = "ids_fiscais";
        campo.value = id;
        valoresEquipe.append(campo);
    }

    renderizarResultadosFiscais();
}

buscaFiscal.addEventListener("input", renderizarResultadosFiscais);
buscaFiscal.addEventListener("keydown", (evento) => {
    if (evento.key !== "Enter" || evento.isComposing) return;
    evento.preventDefault();
    resultadosFiscais.querySelector("button")?.click();
});
fiscalResponsavel.addEventListener("change", atualizarEquipe);
atualizarEquipe();

const codigoAcao = document.getElementById("codigo-acao-evento");
const consultarAcao = document.getElementById("consultar-acao-evento");
const statusAcao = document.getElementById("status-acao-evento");

/** Identificador retornado pela última consulta do código atual. */
let identificadorAcao = "";
/** Cancela a consulta anterior quando o código muda ou é consultado novamente. */
let consultaAcao;
/** ID preenchido pela consulta, separado das escolhas manuais. */
let responsavelSugerido = "";
/** Participantes preenchidos pela consulta para o código atual. */
const participantesSugeridos = new Set();

fiscalResponsavel.addEventListener("change", () => { responsavelSugerido = ""; });

codigoAcao.addEventListener("input", () => {
    consultaAcao?.abort();
    consultaAcao = undefined;
    identificadorAcao = "";
    statusAcao.textContent = "";
    if (responsavelSugerido && fiscalResponsavel.value === responsavelSugerido) {
        fiscalResponsavel.value = "";
    }
    responsavelSugerido = "";
    for (const id of participantesSugeridos) fiscaisAdicionados.delete(id);
    participantesSugeridos.clear();
    atualizarEquipe();
});

consultarAcao.addEventListener("click", async () => {
    if (!codigoAcao.value || !codigoAcao.validity.valid) {
        statusAcao.textContent = "Informe um código de ação válido.";
        codigoAcao.focus();
        return;
    }

    consultaAcao?.abort();
    const consulta = new AbortController();
    consultaAcao = consulta;
    identificadorAcao = "";
    statusAcao.textContent = "Consultando ação…";
    const parametros = new URLSearchParams({ codigo: codigoAcao.value });
    try {
        const resposta = await fetch(`${codigoAcao.dataset.acaoUrl}?${parametros}`, {
            signal: consulta.signal,
            cache: "no-store",
        });
        if (consulta.signal.aborted) return;

        if (resposta.status === 404) {
            statusAcao.textContent = "Nenhuma ação de inspeção encontrada para esse código.";
            return;
        }
        if (!resposta.ok) throw new Error("Falha na consulta");
        const acao = await resposta.json();
        if (consulta.signal.aborted) return;

        identificadorAcao = acao.identificador;
        if (!fiscalResponsavel.value && fiscaisPorId.has(String(acao.responsavel))) {
            responsavelSugerido = String(acao.responsavel);
            fiscalResponsavel.value = responsavelSugerido;
        }
        for (const id of acao.participantes.map(String)) {
            if (fiscaisPorId.has(id) && !fiscaisAdicionados.has(id)) {
                participantesSugeridos.add(id);
                fiscaisAdicionados.add(id);
            }
        }
        atualizarEquipe();
        statusAcao.textContent = acao.equipe_incompleta
            ? `${identificadorAcao}. Revise a equipe. Há fiscais sem correspondência no cadastro local.`
            : identificadorAcao;
    } catch {
        if (!consulta.signal.aborted) {
            statusAcao.textContent = "Não foi possível consultar a ação no eFiscaliza.";
        }
    } finally {
        if (consultaAcao === consulta) consultaAcao = undefined;
    }
});

const dialogConfirmacao = document.getElementById("confirmacao-evento");
const confirmarCadastro = document.getElementById("confirmar-cadastro-evento");
const voltarRevisao = document.getElementById("voltar-revisao-evento");
const resumoMunicipio = document.getElementById("resumo-municipio-evento");

/** Autoriza o envio disparado pelo botão de confirmação do resumo. */
let cadastroConfirmado = false;

/** Atualiza o município do resumo quando a busca termina. */
function atualizarMunicipioNoResumo() {
    resumoMunicipio.textContent = municipioEvento.value || statusMunicipio.textContent || "Não informado";
    confirmarCadastro.disabled = consultandoMunicipio;
}

/** Monta o resumo com os valores atuais, antes de abrir a confirmação. */
function preencherResumoEvento() {
    const campos = formularioEvento.elements;
    const datas = ["data_inicio", "data_fim"]
        .map((nome) => campos.namedItem(nome).value.split("-").reverse().join("/"))
        .filter(Boolean);
    const coordenadas = [latitudeEvento.value, longitudeEvento.value].filter(Boolean);
    const responsavel = fiscalResponsavel.value;
    const equipe = [...fiscaisAdicionados]
        .filter((id) => id !== responsavel)
        .map((id) => fiscaisPorId.get(id).nome);
    const valores = {
        nome: campos.namedItem("nome").value.trim(),
        acao: identificadorAcao || codigoAcao.value,
        periodo: datas.join(" a "),
        coordenadas: coordenadas.join(", "),
        responsavel: fiscaisPorId.get(responsavel)?.nome,
        equipe: equipe.join(", "),
        teste: campos.namedItem("teste_etiquetagem").value === "1" ? "Sim" : "Não",
        observacao: campos.namedItem("observacao").value.trim(),
    };
    for (const [campo, valor] of Object.entries(valores)) {
        document.getElementById(`resumo-${campo}-evento`).textContent = valor || "Não informado";
    }
    atualizarMunicipioNoResumo();
}

formularioEvento.addEventListener("submit", (evento) => {
    if (cadastroConfirmado) return;

    evento.preventDefault();
    if (consultaAcao) return;
    preencherResumoEvento();
    dialogConfirmacao.showModal();
});

voltarRevisao.addEventListener("click", () => dialogConfirmacao.close());
confirmarCadastro.addEventListener("click", () => {
    cadastroConfirmado = true;
    confirmarCadastro.disabled = true;
    formularioEvento.requestSubmit();
    cadastroConfirmado = false;
});

// Leva o foco ao erro devolvido pelo servidor e recompõe a localização, se necessário.
const erroFormulario = document.getElementById("evento-form-erro");
if (erroFormulario) {
    erroFormulario.focus();
    if (!municipioEvento.value) consultarMunicipio();
}
