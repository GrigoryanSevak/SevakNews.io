document.addEventListener("DOMContentLoaded", function() {
    const button = document.getElementById("button");
    const overlay = document.querySelector(".overlay");

    button.addEventListener("click", function() {
        overlay.style.display = "flex";
    });

    overlay.addEventListener("click", function(event) {
        if (event.target === overlay) {
            overlay.style.display = "none";
        }
    });
});