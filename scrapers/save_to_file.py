from datetime import datetime

# Save the scraped data to the index.html file
def save_to_file(games_by_platform):
    today = datetime.now().strftime("%B %d, %Y")

    # Debugging: Print the games being passed to save_to_file
    print(f"Saving Steam games: {games_by_platform['Steam']}")
    print(f"Saving GOG games: {games_by_platform['GOG']}")

    # Writing to the root folder, adjust the path as needed for your web environment
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<html lang="en">\n<head>\n')
        f.write('    <meta charset="UTF-8">\n')
        f.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        f.write('    <title>Free Games Today</title>\n')
        f.write('    <link rel="stylesheet" type="text/css" href="styles/style.css">\n')  # Link to CSS
        f.write('</head>\n<body>\n')
        f.write(f'    <h1>Free Games Today</h1>\n')
        
        f.write('    <div class="game-list">\n')

        # Write Steam games
        f.write(f'        <h2>Steam</h2>\n')
        if games_by_platform["Steam"]:
            for game in games_by_platform["Steam"]:
                title, link = game
                f.write(f'        <a href="{link}">{title}</a><br>\n')
        else:
            f.write('        <p>No free games available today.</p>\n')

        # Write GOG games
        f.write(f'        <h2>GOG</h2>\n')
        if games_by_platform["GOG"]:
            for game in games_by_platform["GOG"]:
                title, link = game
                f.write(f'        <a href="{link}">{title}</a><br>\n')
        else:
            f.write('        <p>No free games available today.</p>\n')

        f.write('    </div>\n')

        f.write('<footer>\n')
        f.write(f'    <p>Generated on {today}</p>\n')
        f.write('</footer>\n')

        f.write('</body>\n</html>')
