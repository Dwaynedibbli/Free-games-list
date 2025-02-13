import os

def save_to_file(games_by_platform):
    os.makedirs('game_pages', exist_ok=True)

    # Main Index Page
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<html lang="en">\n<head>\n')
        f.write('    <meta charset="UTF-8">\n')
        f.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        f.write('    <title>Free Today - Free Games</title>\n')
        f.write('    <link rel="stylesheet" type="text/css" href="styles/style.css">\n')
        f.write('</head>\n<body>\n')

        # Header with Logo and Title as a Link
        f.write('    <div class="title-container">\n')
        f.write('        <a href="index.html" style="text-decoration: none; color: inherit;">\n')
        f.write('            <img src="styles/logo.png" alt="Logo" class="logo">\n')
        f.write('            <h1>Free Today - Free Games</h1>\n')
        f.write('        </a>\n')
        f.write('    </div>\n')

        # Ad Banner
        f.write('    <div class="ad-banner">Advertisement Space</div>\n')

        # Platform links
        f.write('    <div class="platform-container">\n')
        for platform, games in games_by_platform.items():
            game_count = len(games)
            page_name = f'game_pages/{platform.lower().replace(" ", "_")}.html'
            f.write(f'        <div class="platform-card"><a href="{page_name}">{platform} ({game_count} games)</a></div>\n')
        f.write('    </div>\n')
        f.write('</body>\n</html>\n')

    # Generate Pages for Each Platform
    for platform, games in games_by_platform.items():
        page_name = f'game_pages/{platform.lower().replace(" ", "_")}.html'
        with open(page_name, 'w', encoding='utf-8') as f:
            f.write('<!DOCTYPE html>\n')
            f.write('<html lang="en">\n<head>\n')
            f.write(f'    <title>{platform} - Free Games</title>\n')
            f.write('    <meta charset="UTF-8">\n')
            f.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
            f.write('    <link rel="stylesheet" type="text/css" href="../styles/style.css">\n')
            f.write('</head>\n<body>\n')

            # Header with Logo and Title as a Link
            f.write('    <div class="title-container">\n')
            f.write('        <a href="../index.html" style="text-decoration: none; color: inherit;">\n')
            f.write('            <img src="../styles/logo.png" alt="Logo" class="logo">\n')
            f.write(f'            <h1>{platform} - Free Games</h1>\n')
            f.write('        </a>\n')
            f.write('    </div>\n')

            # Ad Banner
            f.write('    <div class="ad-banner">Advertisement Space</div>\n')

            # Game listing
            f.write('    <div class="game-container">\n')
            if games:
                for game in games:
                    title = game['title'] if isinstance(game, dict) else game[0]
                    link = game['link'] if isinstance(game, dict) else game[1]
                    f.write(f'        <div class="game-item"><a href="{link}">{title}</a></div>\n')
            else:
                f.write('        <p>No free games available today.</p>\n')
            f.write('    </div>\n')
            
            # Footer with Disclaimer
            f.write('<footer>\n')
            f.write('    <p>This website is for informational purposes only. The free games listed are subject to availability and changes. Please refer to the respective platforms for the most up-to-date information.</p>\n')
            f.write('</footer>\n')
            f.write('</body>\n</html>\n')
