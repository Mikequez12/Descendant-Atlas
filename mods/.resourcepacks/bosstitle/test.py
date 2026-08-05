import requests
import base64
import json
"""
name = "Mikequez12" # Example username

data = requests.get(
    f"https://api.mojang.com/users/profiles/minecraft/{name}"
).json()

uuid = data["id"]

profile = requests.get(
    f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
).json()

texture_data = profile["properties"][0]["value"]

decoded = base64.b64decode(texture_data)
texture_json = decoded.decode()

texture_url = json.loads(texture_json)["textures"]["SKIN"]["url"]

skin = requests.get(texture_url).content

open("skin.png", "wb").write(skin)
"""
from PIL import Image

img = Image.open("skin.png").convert("RGBA")

face = img.crop((8, 8, 16, 16))
hat = img.crop((40, 8, 48, 16))

face.alpha_composite(hat)

pixels = list(face.getdata())

l = []
w = 8
for n,rgba in enumerate(pixels):
    i = n // w + 1
    r,g,b,a = rgba
    hex_ = "#{:02x}{:02x}{:02x}".format(r,g,b)
    l.append('{text:"'+chr(int(f"F00{i:X}", 16))+(f'\uF101' if n != (w * w - 1) else '')+('\uF101'*w if n % w == (w - 1) and i < w else '')+'",color:"'+hex_+'"}')
l.append(r'{text:" ",color:white}')

print(','.join(map(lambda obj:repr(obj)[1:-1],l)))

# tellraw @a {text:"\uF001\uF002\uF003\uF004\uF005\uF006\uF007\uF008\uF101\uF102"}