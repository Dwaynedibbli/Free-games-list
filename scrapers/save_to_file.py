from datetime import datetime

# Save the scraped data to the index.html file
def save_to_file(games_by_platform):
    today = datetime.now().strftime("%B %d, %Y")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<html lang="en">\n<head>\n')
        f.write('    <meta charset="UTF-8">\n')
        f.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        f.write('    <title>Free Games Today</title>\n')
        f.write('    <link rel="stylesheet" type="text/css" href="styles/style.css">\n')
        f.write('</head>\n<body>\n')

        # Page title
        f.write(f'    <h1>Free Games Today</h1>\n')
        
        f.write('    <div class="platform-container">\n')

        # Write Steam games
        f.write(f'        <div class="platform-column">\n')
        f.write(f'        <h2>Steam</h2>\n')
        if games_by_platform["Steam"]:
            for game in games_by_platform["Steam"]:
                title, link = game  # Steam scraper uses tuple format
                f.write(f'        <div class="game-item">\n')
                f.write(f'            <a href="{link}">{title}</a><br>\n')
                f.write(f'        </div>\n')
        else:
            f.write('        <p>No free games available today.</p>\n')
        f.write(f'        </div>\n')

        # Write GOG games
        f.write(f'        <div class="platform-column">\n')
        f.write(f'        <h2>GOG</h2>\n')
        if games_by_platform["GOG"]:
            for game in games_by_platform["GOG"]:
                title = game['title']  # Access the 'title' key from the dictionary
                link = game['link']    # Access the 'link' key from the dictionary
                f.write(f'        <div class="game-item">\n')
                f.write(f'            <a href="{link}">{title}</a><br>\n')
                f.write(f'        </div>\n')
        else:
            f.write('        <p>No free games available today.</p>\n')
        f.write(f'        </div>\n')

        # Write Epic Games
        f.write(f'        <div class="platform-column">\n')
        f.write(f'        <h2>Epic Games</h2>\n')
        if games_by_platform["Epic"]:
            for game in games_by_platform["Epic"]:
                title = game['title']  # Access the 'title' key from the dictionary
                link = game['link']    # Access the 'link' key from the dictionary
                f.write(f'        <div class="game-item">\n')
                f.write(f'            <a href="{link}">{title}</a><br>\n')
                f.write(f'        </div>\n')
        else:
            f.write('        <p>No free games available today.</p>\n')
        f.write(f'        </div>\n')

        f.write('    </div>\n')  # End of platform-container

        # Footer with date
        f.write('<footer>\n')
        f.write(f'    <p>Generated on {today}</p>\n')
        f.write('</footer>\n')

        f.write('</body>\n</html>')
