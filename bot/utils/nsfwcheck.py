import base64
import requests
import os

url = "http://localhost:8080/sync"
endings = ["jpg", "jpeg", "png", "bmp", "webp", "gif"]

def getimg(filename):
    b64_file = base64.b64encode(open(filename, "rb").read()).decode("utf-8")
    data = {filename: b64_file}

    return requests.post(url, json={"data": data, "webhook": ""},).json()


def check_nsfw(url, filename):
    valid_end = False
    for ending in endings:
        if filename.endswith(ending):
            valid_end = True
    if not valid_end: return
    r = requests.get(url, allow_redirects=True)
    with open(f"./temp/{filename}", 'wb') as f:
        f.write(r.content)
    result = getimg(f"./temp/{filename}")
    os.remove(f"./temp/{filename}")
    return result["prediction"][filename]["unsafe"] > 0.85