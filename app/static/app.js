// Scripts da aplicação.

document.addEventListener("DOMContentLoaded", () => {
    const evento = document.getElementById("evento");
    evento?.addEventListener("change", () => {
        const url = evento.selectedOptions[0]?.dataset.url;
        if (url) window.location.href = url;
    });
});
document.addEventListener("DOMContentLoaded", () => {
    const evento = document.getElementById("evento");
    evento?.addEventListener("change", () => {
        const url = evento.selectedOptions[0]?.dataset.url;
        if (url) window.location.href = url;
    });
});
