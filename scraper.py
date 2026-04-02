import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_live_data():
    services = {
        "Netflix": "https://www.flixwatch.co/regions/belgium/feed/",
        "Disney+": "https://www.flixwatch.co/streaming-services/disney-plus/feed/",
        "VRT MAX": "https://www.vrt.be/vrtmax/a-z/"
    }
    
    results = []

    for name, url in services.items():
        titles = []
        try:
            # Voor VRT MAX gebruiken we de directe scraper die we al hadden
            if name == "VRT MAX":
                r = requests.get(url, timeout=10)
                soup = BeautifulSoup(r.text, 'html.parser')
                items = soup.select('.vrt-teaser__title', limit=5)
                titles = [i.text.strip() for i in items]
            
            # Voor Netflix/Disney gebruiken we hun RSS feeds (veel betrouwbaarder)
            else:
                r = requests.get(url, timeout=10)
                soup = BeautifulSoup(r.content, features="xml")
                items = soup.find_all('item', limit=5)
                titles = [item.title.text.replace("New on Netflix:", "").strip() for item in items]
                
        except Exception as e:
            print(f"Fout bij {name}: {e}")
            # Fallback titels als de site offline is
            titles = ["Nieuwe releases checken...", "Update volgt"]

        results.append({"s": name, "titles": titles})

    return results

def make_page():
    content = get_live_data()
    nu = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    html = f"""
    <!DOCTYPE html>
    <html lang="nl">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <title>Streaming Radar BE</title>
    </head>
    <body class="bg-[#050505] text-white p-6 font-sans">
        <div class="max-w-4xl mx-auto">
            <header class="mb-10 border-b border-zinc-800 pb-6">
                <h1 class="text-4xl font-black italic">BELGIË <span class="text-red-600">RADAR</span></h1>
                <p class="text-zinc-500 font-mono text-[10px] mt-2 uppercase tracking-[0.3em]">Live Feed • {nu}</p>
            </header>
            <div class="grid gap-6">
    """
    
    for service in content:
        color = "border-red-600" if service['s'] == "Netflix" else "border-blue-600"
        if service['s'] == "VRT MAX": color = "border-yellow-400"
        
        html += f"""
        <div class="bg-zinc-900/50 border-l-4 {color} p-6 rounded-r-xl">
            <h2 class="text-xs font-black uppercase tracking-widest text-zinc-400 mb-4">{service['s']}</h2>
            <ul class="space-y-2">"""
        
        for t in service['titles']:
            html += f"<li class='text-lg font-bold'>• {t}</li>"
            
        html += "</ul></div>"
        
    html += "</div></div></body></html>"
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    make_page()
