// Scripts da aplicação.

// Opções com data-url (ex.: "+ Criar Evento") abrem a tela correspondente.
document.addEventListener("DOMContentLoaded", () => {
    for (const campo of document.querySelectorAll("#evento")) {
        campo.addEventListener("change", () => {
            const url = campo.selectedOptions[0]?.dataset.url;
            if (url) {
                window.location.href = url;
            } else if (campo.form.dataset.selecaoHabilitada === "true") {
                campo.form.requestSubmit();
            }
        });
    }

    const menuPerfil = document.querySelector(".app-perfil-menu");
    if (menuPerfil) {
        document.addEventListener("click", (evento) => {
            if (!menuPerfil.contains(evento.target)) menuPerfil.open = false;
        });
        menuPerfil.addEventListener("keydown", (evento) => {
            if (evento.key === "Escape" && menuPerfil.open) {
                menuPerfil.open = false;
                menuPerfil.querySelector("summary").focus();
            }
        });
    }
});
