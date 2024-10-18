from datetime import datetime

def save_to_file(games_by_platform):
    today = datetime.now().strftime("%B %d, %Y")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<html lang="en">\n<head>\n')
        f.write('    <meta charset="UTF-8">\n')
        f.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        f.write('    <title>Free Today</title>\n')  # Updated title
        f.write('    <link rel="stylesheet" type="text/css" href="styles/style.css">\n')
        f.write('</head>\n<body>\n')

        # Title and Logo
        f.write('    <div class="title-container">\n')
        f.write('        <img src="styles/logo.png" alt="Logo" class="logo">\n')  # Correct path for the logo
        f.write('        <h1>Free Today</h1>\n')  # Updated title
        f.write('    </div>\n')

        # Two Column Layout for Games
        f.write('    <div class="platform-container">\n')

        # Steam Games Section
        f.write('        <div class="platform-column">\n')
        f.write('            <div class="banner-ad">\n')
        f.write('                <p>Banner Ad</p>\n')
        f.write('            </div>\n')
        f.write('            <h2>Steam</h2>\n')
        f.write('            <div class="game-list">\n')
        if games_by_platform["Steam"]:
            for game in games_by_platform["Steam"]:
                title, link = game
                f.write(f'            <div class="game-item">\n')
                f.write(f'                <a href="{link}">{title}</a><br>\n')
                f.write('            </div>\n')
        else:
            f.write('            <p>No free games available today.</p>\n')
        f.write('            </div>\n')
