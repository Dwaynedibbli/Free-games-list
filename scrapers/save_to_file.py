def save_to_file(games_by_platform):
    # Generate a summary index page
    with open("index.html", "w", encoding="utf-8") as index_file:
        index_file.write("<!DOCTYPE html>\n<html lang='en'>\n<head>\n")
        index_file.write("<meta charset='UTF-8'>\n<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
        index_file.write("<title>Free Today</title>\n<link rel='stylesheet' type='text/css' href='styles/style.css'>\n")
        index_file.write("</head>\n<body>\n")
        index_file.write("<div class='title-container'>\n<h1>Free Today</h1>\n</div>\n")
        index_file.write("<div class='platform-container'>\n")

        for platform, games in games_by_platform.items():
            platform_filename = f"{platform.lower().replace(' ', '_')}.html"

            index_file.write(f"<div class='platform-column'>\n<h2><a href='{platform_filename}'>{platform} ({len(games)} free games)</a></h2>\n</div>\n")

            # Generate platform-specific pages
            with open(platform_filename, "w", encoding="utf-8") as platform_file:
                platform_file.write(f"<!DOCTYPE html>\n<html lang='en'>\n<head>\n")
                platform_file.write(f"<meta charset='UTF-8'>\n<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
                platform_file.write(f"<title>{platform} Free Games</title>\n<link rel='stylesheet' type='text/css' href='styles/style.css'>\n")
                platform_file.write("</head>\n<body>\n")
                platform_file.write(f"<h1>{platform} Free Games</h1>\n")
                platform_file.write(f"<a href='index.html'>← Back to Main Page</a>\n")
                platform_file.write("<ul>\n")

                for game in games:
                    title = game["title"]
                    link = game["link"]
                    platform_file.write(f"<li><a href='{link}' class='game-link'>{title}</a></li>\n")

                platform_file.write("</ul>\n</body>\n</html>")

        index_file.write("</div>\n</body>\n</html>")