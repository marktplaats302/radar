import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_live_content():
    # We gebruiken een betrouwbare verzamelbron voor nieuwe Belgische releases
    # Deze feed wordt dagelijks ververst met wat er ÉCHT verschijnt.
    url = "https://www.flixwatch.co/regions/belgium/feed/"
    
    results = {"Netflix": {"Films": [], "Series": []}, "VRT MAX": {"Films": [], "Series": []}}
    
    try:
        # 1. Netflix & Co via RSS
        response = requests.get(url, timeout=15)
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.find_all('item', limit=15)
        
        for item in items:
            title = item.title.text.replace("New on Netflix:", "").strip()
            # Simpele logica: als 'Season' of 'Series' in de titel staat, is het een serie
            if any(x in title.lower() for x in ["season", "series", "s1", "s2", "aflevering"]):
                results["Netflix"]["Series"].append(title)
            else:
                results["Netflix"]["Films"].append(title)
                
        # 2. VRT MAX Directe Scrape
        vrt_r = requests.get("https://www.vrt.be/vrtmax/a-z/", timeout=10)
        vrt_soup = BeautifulSoup(vrt_r.text, 'html.parser')
        vrt_items = vrt_soup.select('.vrt-teaser__title', limit=6)
        for v in vrt_items:
            results["VRT MAX"]["Series"].append(v.text.strip())
            
    except Exception as e:
        print(f"Fout bij ophalen: {e}")
        
    return results

def make_page():
    data = get_live_content()
    nu = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    html = f"""
    <!DOCTYPE html>
    <html lang="nl">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <title>Live Streaming Radar BE</title>
    </head>
    <body class="bg-[#050505] text-slate-300 p-6 md:p-10 font-sans">
        <div class="max-w-4xl mx-auto">
            <header class="mb-10 border-b border-zinc-800 pb-6">
                <h1 class="text-4xl font-black italic text-white tracking-tighter uppercase">België <span class="text-red-600">Live Feed</span></h1>
                <p class="text-zinc-500 font-mono text-[10px] mt-2 uppercase tracking-[0.3em]">Scan uitgevoerd op: {nu}</p>
            </header>
    """

    for service, categories in data.items():
        color = "text-red-600" if service == "Netflix" else "text-yellow-400"
        html += f"""
        <div class="mb-12 bg-zinc-900/30 border border-zinc-800 p-6 rounded-2xl">
            <h2 class="text-3xl font-black mb-6 {color} italic uppercase">{service}</h2>
            <div class="grid md:grid-cols-2 gap-8">
                <div>
                    <h3 class="text-blue-500 text-[10px] font-black uppercase tracking-widest mb-4">Series (Nieuw)</h3>
                    <ul class="space-y-2">
                        {"".join([f"<li class='text-white font-bold'>• {t}</li>" for t in categories['Series']]) or "<li>Geen nieuwe series</li>"}
                    </ul>
                </div>
                <div>
                    <h3 class="text-red-500 text-[10px] font-black uppercase tracking-widest mb-4">Films (Nieuw)</h3>
                    <ul class="space-y-2">
                        {"".join([f"<li class='text-white font-bold'>• {t}</li>" for t in categories['Films']]) or "<li>Geen nieuwe films</li>"}
                    </ul>
                </div>
            </div>
        </div>
        """

    html += "</div></body></html>"
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    make_page()
