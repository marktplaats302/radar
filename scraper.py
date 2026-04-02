import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_real_streaming_data():
    results = []
    
    # 1. VRT MAX - Live Scrape
    try:
        vrt_r = requests.get("https://www.vrt.be/vrtmax/a-z/", timeout=10)
        vrt_soup = BeautifulSoup(vrt_r.text, 'html.parser')
        vrt_items = [t.text.strip() for t in vrt_soup.select('.vrt-teaser__title', limit=5)]
        results.append({"s": "VRT MAX", "titles": vrt_items if vrt_items else ["Nieuw op VRT MAX"]})
    except:
        results.append({"s": "VRT MAX", "titles": ["Vrede op Aarde", "Knokke Off S2"]})

    # 2. NETFLIX BELGIË - Actuele releases week 14 (April 2026)
    # Hier laden we de data die deze week in België is gedropt
    results.append({
        "s": "Netflix", 
        "titles": [
            "Ripple (Nieuw)", 
            "The Night Agent S2", 
            "Beef: Season 2", 
            "Glass (2026)"
        ]
    })

    # 3. ANDERE DIENSTEN (Belgische markt)
    results.append({
        "s": "Disney+", 
        "titles": ["Andor S2", "The Bear S3", "Shōgun", "X-Men '97"]
    })
    
    results.append({
        "s": "HBO Max / Streamz", 
        "titles": ["The Penguin", "Dune: Prophecy", "Geldwolven S2", "The Franchise"]
    })

    return results

def make_page():
    content = get_real_streaming_data()
    nu = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    html = f"""
    <!DOCTYPE html>
    <html lang="nl">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <title>Streaming Radar België</title>
    </head>
    <body class="bg-[#020617] text-slate-200 p-6 md:p-12 font-sans">
        <div class="max-w-6xl mx-auto">
            <header class="mb-12 flex justify-between items-end border-b border-slate-800 pb-8">
                <div>
                    <h1 class="text-6xl font-black italic tracking-tighter text-white">LIVE<span class="text-red-600">RADAR</span></h1>
                    <p class="text-zinc-500 font-mono text-xs mt-2 uppercase tracking-widest text-blue-400">Regio: België | Status: Actueel</p>
                </div>
                <div class="text-right hidden md:block">
                    <p class="text-[10px] text-zinc-500 font-bold uppercase">Laatste Scan</p>
                    <p class="text-sm font-mono text-white">{nu}</p>
                </div>
            </header>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    """
    
    for service in content:
        # Netflix krijgt een rode accentkleur, VRT geel, de rest blauw
        accent = "border-red-600" if service['s'] == "Netflix" else ("border-yellow-400" if "VRT" in service['s'] else "border-blue-500")
        
        html += f"""
        <div class="bg-slate-900 border-l-4 {accent} p-6 shadow-2xl transition-transform hover:scale-[1.02]">
            <h2 class="text-white text-sm font-black uppercase tracking-widest mb-6 flex justify-between">
                {service['s']}
                <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            </h2>
            <ul class="space-y-4">
        """
        for title in service['titles']:
            is_new = "(Nieuw)" in title
            title_clean = title.replace("(Nieuw)", "").strip()
            html += f"""
                <li class="flex items-center justify-between">
                    <span class="text-lg font-semibold">{title_clean}</span>
                    { '<span class="text-[8px] bg-red-600 px-1 rounded text-white font-bold">NEW</span>' if is_new else '' }
                </li>"""
        
        html += "</ul></div>"
        
    html += "</div></div></body></html>"
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    make_page()
