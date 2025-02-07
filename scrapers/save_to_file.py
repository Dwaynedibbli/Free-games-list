import os

def save_to_file(games_by_platform):
    # Create a directory for game pages if it doesn’t exist
    os.makedirs('game_pages', exist_ok=True)

    # Create the main index page with platform links
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<html lang="en">\n<head>\n')
        f.write('    <meta charset="UTF-8">\n')
        f.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        f.write('    <title>Free Today</title>\n')
        f.write('    <link rel="stylesheet" type="text/css" href="styles/style.css">\n')
        f.write('</head>\n<body>\n')

        f.write('    <h1>Free Today - Free Games</h1>\n')
        f.write('    <p>Select a platform to see available free games:</p>\n')
        f.write('    <ul>\n')

        # Generate links to individual platform pages
        for platform, games in games_by_platform.items():
            game_count = len(games)
            page_name = f'game_pages/{platform.lower().replace(" ", "_")}.html'
            f.write(f'        <li><a href="{page_name}">{platform} ({game_count} games)</a></li>\n')

        f.write('    </ul>\n')
        f.write('</body>\n</html>\n')

    # Generate a separate page for each platform
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

            f.write(f'    <h1>{platform} - Free Games</h1>\n')
            f.write('    <ul>\n')

            if games:
                for game in games:
                    title = game['title'] if isinstance(game, dict) else game[0]
                    link = game['link'] if isinstance(game, dict) else game[1]
                    f.write(f'        <li><a href="{link}">{title}</a></li>\n')
            else:
                f.write('        <p>No free games available today.</p>\n')

            f.write('    </ul>\n')
            f.write('<p><a href="../index.html">Back to main page</a></p>\n')
            f.write('</body>\n</html>\n')