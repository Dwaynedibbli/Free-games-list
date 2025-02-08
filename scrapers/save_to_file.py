def save_to_file(games_by_platform):
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(f'<!DOCTYPE html>\n<html lang="en">\n<head>\n')
        f.write('    <meta charset="UTF-8">\n')
        f.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        f.write('    <title>Free Games Today</title>\n')
        f.write('    <link rel="stylesheet" href="style.css">\n')
        f.write('    <script src="scripts.js" defer></script>\n')
        f.write('</head>\n<body>\n')

        # ✅ Embed game data as a JSON object inside `index.html`
        f.write(f'    <script id="game-data" type="application/json">\n')
        f.write(json.dumps(games_by_platform, indent=4))
        f.write('\n    </script>\n')

        f.write('    <div class="title-container">\n')
        f.write('        <img src="logo.png" alt="Free Today Logo" class="logo">\n')
        f.write('        <h1>Free Today</h1>\n')
        f.write('    </div>\n')

        f.write('    <h2>Free Games Today</h2>\n')
        f.write('    <div class="platform-container">\n')
        for platform in games_by_platform.keys():
            f.write(f'        <p><a href="#" onclick="showGames(\'{platform}\')">{platform} (<span id="{platform.lower()}-count">0</span> games)</a></p>\n')
        f.write('    </div>\n')

        f.write('    <h2 id="platform-title">All Free Games</h2>\n')
        f.write('    <div class="game-list" id="game-list">\n')
        f.write('        <p>Select a platform to view available games.</p>\n')
        f.write('    </div>\n')

        f.write('    <footer>\n')
        f.write('        <p>Disclaimer: Free games are subject to availability. Check the respective platforms for up-to-date information.</p>\n')
        f.write('    </footer>\n')

        f.write('</body>\n</html>\n')

    print("✅ Game data saved inside index.html")