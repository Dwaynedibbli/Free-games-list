from datetime import datetime

# Save the scraped data to the index.html file
def save_to_file(games_by_platform):
    today = datetime.now().strftime("%B %d, %Y")

    with open('../index.html', 'w', encoding='utf-8') as f:  # Adjust path to write to root
        f.write('<!DOCTYPE html>\n')
        f.write('<html lang="en">\n<head>\n')
        f.write('    <meta charset="UTF-8">\n')
        f.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        f.write('    <title>Free Games Today</title>\n')
        f.write('    <link rel="stylesheet" type="text/css" href="styles/style.css">\n')  # Link to CSS
        f.write('</head>\n<body>\n')
        f.write(f'    <h1>Free Games Today</h1>\n')
        
        # ASCII Art (Optional)
        f.write('<div class="ascii-art">╔════════════════════════╗</div>\n')

        f.write('    <div class="game-list">\n')

        # Write Steam games
        f.write(f'        <h2>Steam</h2>\n')
        if games_by_platform["Steam"]:
            for title, link in games_by_platform["Steam"]:
                f.write(f'        <a href="{link}">{title}</a><br>\n')
        else:
            f.write('        <p>No free games available today.</p>\n')

        # Write GOG games
        f.write(f'        <h2>GOG</h2>\n')
        if games_by_platform["GOG"]:
            for game in games_by_platform["GOG"]:
                title = game['title']
                link = game['link']
                f.write(f'        <a href="{link}">{title}</a><br>\n')
        else:
            f.write('        <p>No free games available today.</p>\n')

        f.write('    </div>\n')

        # Include the external legal disclaimer from styles folder
        f.write('<footer>\n')
        f.write('    <p><link rel="stylesheet" type="text/css" href="styles/disclaimer.css"></p>\n')  # Linking to disclaimer
        f.write(f'    <p>Generated on {today}</p>\n')
        f.write('</footer>\n')

        f.write('</body>\n</html>')
