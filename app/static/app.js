// Scripts da aplicação.

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
