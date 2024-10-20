def save_to_file(games_by_platform):
    with open('index.html', 'a', encoding='utf-8') as f:  # Append mode to add data to index.html
        f.write('    <div class="platform-container">\n')

        # Write Steam games
        f.write('        <div class="platform-column">\n')
        f.write('            <h2>Steam</h2>\n')
        f.write('            <div class="game-list">\n')
        if games_by_platform["Steam"]:
            for game in games_by_platform["Steam"]:
                title, link = game  # Steam scraper uses tuple format
                f.write(f'            <div class="game-item">\n')
                f.write(f'                <a href="{link}">{title}</a><br>\n')
                f.write('            </div>\n')
        else:
            f.write('            <p>No free games available today.</p>\n')
        f.write('            </div>\n')  # End of Steam game list
        f.write('        </div>\n')  # End of Steam column

        # Write GOG games
        f.write('        <div class="platform-column">\n')
        f.write('            <h2>GOG</h2>\n')
        f.write('            <div class="game-list">\n')
        if games_by_platform["GOG"]:
            for game in games_by_platform["GOG"]:
                title = game['title']
                link = game['link']
                f.write(f'            <div class="game-item">\n')
                f.write(f'                <a href="{link}">{title}</a><br>\n')
                f.write('            </div>\n')
        else:
            f.write('            <p>No free games available today.</p>\n')
        f.write('            </div>\n')  # End of GOG game list
        f.write('        </div>\n')  # End of GOG column

        # Write Epic games
        f.write('        <div class="platform-column">\n')
        f.write('            <h2>Epic Games</h2>\n')
        f.write('            <div class="game-list">\n')
        if games_by_platform["Epic"]:
            for game in games_by_platform["Epic"]:
                title = game['title']
                link = game['link']
                f.write(f'            <div class="game-item">\n')
                f.write(f'                <a href="{link}">{title}</a><br>\n')
                f.write('            </div>\n')
        else:
            f.write('            <p>No free games available today.</p>\n')
        f.write('            </div>\n')  # End of Epic game list
        f.write('        </div>\n')  # End of Epic column

        # Write Google Play games
        f.write('        <div class="platform-column">\n')
        f.write('            <h2>Google Play Store</h2>\n')
        f.write('            <div class="game-list">\n')
        if games_by_platform["Google Play"]:
            for game in games_by_platform["Google Play"]:
                title = game['title']
                link = game['link']
                f.write(f'            <div class="game-item">\n')
                f.write(f'                <a href="{link}">{title}</a><br>\n')
                f.write('            </div>\n')
        else:
            f.write('            <p>No free games available today.</p>\n')
        f.write('            </div>\n')  # End of Google Play game list
        f.write('        </div>\n')  # End of Google Play column
