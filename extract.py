import re
import base64

with open('TRACTION.html', 'r', encoding='utf-8') as f:
    html = f.read()

match = re.search(r'data:image/png;base64,([^"\'\>]+)', html)
if match:
    base64_str = match.group(1)
    with open('car.png', 'wb') as f:
        f.write(base64.b64decode(base64_str))
    
    html = html.replace('data:image/png;base64,' + base64_str, 'car.png')
    
    with open('TRACTION.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Extracted car.png and updated TRACTION.html!")
else:
    print("Could not find base64 string.")
