from datetime import datetime

def save_to_file(games_by_platform):
    today = datetime.now().strftime("%B %d, %Y")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<html lang="en">\n<head>\n')
        f.write('    <meta charset="UTF-8">\n')
        f.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        f.write('    <title>Free Today</title>\n')  # Title is updated here
        f.write('    <link rel="stylesheet" type="text/css" href="styles/style.css">\n')
        f.write('</head>\n<body>\n')

        # Title and logo
        f.write('    <div class="title-container">\n')
        f.write('        <img src="path/to/your/image.png" alt="Logo" class="logo">\n')  # Add your image here
        f.write('        <h1>Free Today</h1>\n')  # Updated title
        f.write('    </div>\n')

        # Additional content for games would go here

        # Footer
        f.write('<footer>\n')
        f.write(f'    <p>Generated on {today}</p>\n')
        f.write('</footer>\n')

        f.write('</body>\n</html>')
