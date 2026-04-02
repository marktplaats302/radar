import requests
from datetime import datetime

def get_updates():
    # Hier simuleren we de actuele scan van de 6 diensten
    # In een live-omgeving vult de AI dit aan met echte data
    shows = [
        {"s": "Netflix", "t": "The Night Agent S2"},
        {"s": "Disney+", "t": "Andor: Season 2"},
        {"s": "HBO Max", "t": "The Penguin"},
        {"s": "VRT MAX", "t": "Vrede op Aarde"},
        {"s": "Apple TV+", "t": "Severance S2"},
        {"s": "Prime", "t": "Reacher"}
    ]
    return shows

def make_page():
    shows = get_updates()
    nu = datetime.now().strftime("%d/%m/%Y %H:%M")
    html = f"<html><head><script src='https://cdn.tailwindcss.com'></script></head>"
    html += f"<body class='bg-black text-white p-10'><h1 class='text-4xl font-bold mb-5'>STREAMING RADAR</h1>"
    html += f"<p class='text-gray-500 mb-8 italic text-sm font-mono'>Update: {nu}</p><div class='grid gap-4'>"
    for s in shows:
        border = "border-l-4 border-yellow-400" if s['s'] == "VRT MAX" else "border-l-4 border-blue-600"
        html += f"<div class='bg-zinc-900 p-4 rounded {border}'><strong>{s['s']}:</strong> {s['t']}</div>"
    html += "</div></body></html>"
    with open("index.html", "w") as f: f.write(html)

make_page()
