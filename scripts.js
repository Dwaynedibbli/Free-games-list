document.addEventListener("DOMContentLoaded", function () {
    const quotes = [
        "Game on!",
        "Press start to play!",
        "Level up your collection!",
        "Don't miss out on these freebies!",
        "Claim your free games before they disappear!",
        "A new day, a new game!",
        "Adventure awaits!"
    ];

    function rotateQuote() {
        const randomIndex = Math.floor(Math.random() * quotes.length);
        const quoteElement = document.createElement("p");
        quoteElement.textContent = quotes[randomIndex];
        quoteElement.classList.add("quote");

        document.body.appendChild(quoteElement);

        setTimeout(() => {
            quoteElement.remove();
        }, 5000);
    }

    setInterval(rotateQuote, 10000);
});
