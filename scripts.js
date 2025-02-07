const quotes = [
    "The best loot is free loot.",
    "If it’s free, it’s for me.",
    "Never say no to a free game.",
    "Why grind for loot when you can get it for free?",
    "A free game a day keeps the boredom away.",
    "In a world of microtransactions, free games are a treasure.",
    "Respawn your wallet—play free games instead.",
    "Winning is great, but free games are better.",
    "The best games don’t cost a dime.",
    "No paywalls, no problem—just free games.",
    "Some call it luck. We call it Free Today.",
    "The best price tag? $0.",
    "In-game currency? How about real-world savings?",
    "Press Start… for free!",
    "Free games: because your backlog isn’t big enough already.",
    "Why wait for a sale when you can get it for free?",
    "Free games: the ultimate power-up for your wallet.",
    "No microtransactions. No subscriptions. Just free games.",
    "No loot boxes, no fees—just fun.",
    "Gaming is better when it’s free.",
    "Grab it today, because free doesn’t last forever.",
    "A true gamer never passes up free loot.",
    "Free games: the only cheat code you’ll ever need.",
    "Level up your library without spending a dime.",
    "Don’t just grind XP—grind for free games."
];

let quoteIndex = 0;

function changeQuote() {
    const quoteElement = document.getElementById("quote-text");
    quoteElement.style.opacity = 0;
    setTimeout(() => {
        quoteElement.textContent = quotes[quoteIndex];
        quoteElement.style.opacity = 1;
        quoteIndex = (quoteIndex + 1) % quotes.length;
    }, 500);
}

setInterval(changeQuote, 5000);
document.addEventListener("DOMContentLoaded", changeQuote);