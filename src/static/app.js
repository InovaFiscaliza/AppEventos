// Scripts da aplicação.

/** Consulta o usuário da sessão corporativa; retorna null se não houver sessão válida. */
async function buscarUsuarioAnatel(url) {
    if (!url) return null;
    try {
        // O RF Fusion fica em outro endereço; "include" envia os cookies da sessão da Anatel.
        const resposta = await fetch(url, {
            method: "GET",
            credentials: "include",
            headers: { Accept: "application/json" },
        });
        const tipo = resposta.headers.get("content-type") || "";
        // Sessão expirada vira redirecionamento para a página de login, que não é JSON.
        if (resposta.redirected || !resposta.ok || !tipo.includes("application/json")) {
            return null;
        }
        return await resposta.json();
    } catch (erro) {
        console.warn("Usuário Anatel indisponível:", erro);
        return null;
    }
}

/** Mostra a foto no avatar ou, sem foto https válida, as iniciais do nome. */
function mostrarFotoAnatel(avatar, usuario) {
    if (!avatar) return;
    const foto = avatar.querySelector("img");
    const iniciais = avatar.querySelector("span");

    if (usuario.NA_URL_PROFILE_IMG) {
        try {
            const endereco = new URL(usuario.NA_URL_PROFILE_IMG, window.location.href);
            if (endereco.protocol === "https:") {
                foto.src = endereco.href;
                foto.hidden = false;
                return;
            }
        } catch {
            // Endereço inválido: segue para as iniciais.
        }
    }

    const partes = usuario.NA_USER_NAME.trim().split(/\s+/);
    const primeira = partes[0][0];
    const ultima = partes.length > 1 ? partes[partes.length - 1][0] : "";
    iniciais.textContent = (primeira + ultima).toUpperCase();
    iniciais.hidden = false;
}

/** Mostra nome, cargo, unidade e foto; serve só para exibição, nunca para permissões. */
function mostrarUsuarioAnatel(usuario) {
    if (!usuario?.NA_USER_NAME) {
        const aviso = document.querySelector("#usuario-anatel-ausente");
        if (aviso) aviso.hidden = false;
        return;
    }

    const linhaLogin = document.querySelector("#usuario-anatel-login");
    if (linhaLogin) {
        document.querySelector("#usuario-anatel-login-nome").textContent = usuario.NA_USER_NAME;
        mostrarFotoAnatel(document.querySelector("#usuario-anatel-login-foto"), usuario);
        linhaLogin.hidden = false;
    }

    const caixa = document.querySelector("#usuario-anatel");
    if (!caixa) return;

    document.querySelector("#usuario-anatel-nome").textContent = usuario.NA_USER_NAME;
    document.querySelector("#usuario-anatel-detalhe").textContent = [
        usuario.NA_JOB_TITLE,
        usuario.NA_DEPARTMENT,
    ].filter(Boolean).join(" — ");
    mostrarFotoAnatel(document.querySelector("#usuario-anatel-foto"), usuario);

    caixa.hidden = false;
}

document.addEventListener("DOMContentLoaded", async () => {
    const url = document.body.dataset.urlUsuarioAnatel;
    mostrarUsuarioAnatel(await buscarUsuarioAnatel(url));
});

// Opções com data-url (ex.: "+ Criar Evento") abrem a tela correspondente.
document.addEventListener("DOMContentLoaded", () => {
    for (const campo of document.querySelectorAll("#evento, #usuario")) {
        campo.addEventListener("change", () => {
            const url = campo.selectedOptions[0]?.dataset.url;
            if (url) window.location.href = url;
        });
    }

    // Por enquanto só o usuário "Cadastrar Usuário" (data-login) pode entrar.
    const usuario = document.querySelector("#usuario");
    const senha = document.querySelector("#senha");
    const entrar = document.querySelector("#entrar");
    if (usuario && senha && entrar) {
        usuario.addEventListener("change", () => {
            const liberado = usuario.selectedOptions[0]?.dataset.login === "liberado";
            senha.disabled = !liberado;
            senha.required = liberado;
            entrar.disabled = !liberado;
            if (liberado) senha.focus();
        });
    }
});
