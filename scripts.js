document.addEventListener("DOMContentLoaded", function () {
    // Retrieve game data embedded in index.html
    const gameData = JSON.parse(document.getElementById("game-data").textContent);

    // Update game counts
    updateGameCounts(gameData);
    window.gameData = gameData; // Store globally for filtering
});

function updateGameCounts(data) {
    document.getElementById("steam-count").innerText = data["Steam"] ? data["Steam"].length : 0;
    document.getElementById("gog-count").innerText = data["GOG"] ? data["GOG"].length : 0;
    document.getElementById("epic-count").innerText = data["Epic"] ? data["Epic"].length : 0;
    document.getElementById("google-count").innerText = data["Google Play"] ? data["Google Play"].length : 0;
    document.getElementById("prime-count").innerText = data["Prime Gaming"] ? data["Prime Gaming"].length : 0;
}

function showGames(platform) {
    let gameList = document.getElementById("game-list");
    let platformTitle = document.getElementById("platform-title");

    if (!window.gameData || !window.gameData[platform] || window.gameData[platform].length === 0) {
        gameList.innerHTML = `<p>No free games available on ${platform}.</p>`;
        return;
    }

    platformTitle.innerText = `${platform} Free Games`;
    gameList.innerHTML = ""; // Clear previous content

    window.gameData[platform].forEach(game => {
        let gameItem = document.createElement("div");
        gameItem.classList.add("game-item");

        let gameLink = document.createElement("a");
        gameLink.href = game.link.startsWith("http") ? game.link : `https://${game.link}`;
        gameLink.innerText = game.title;
        gameLink.target = "_blank"; // Open links in a new tab

        gameItem.appendChild(gameLink);
        gameList.appendChild(gameItem);
    });
}