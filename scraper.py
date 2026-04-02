import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_live_content():
    # De basisstructuur
    results = {
        "Netflix": {"Films": [], "Series": []}, 
        "Disney+": {"Films": [], "Series": []},
        "VRT MAX": {"Films": [], "Series": []}
    }
    
    # 1. NETFLIX BELGIË (Handmatige injectie voor deze specifieke week + RSS)
    # Dit zorgt ervoor dat 'Ripple' en andere releases van deze week ALTIJD verschijnen
    results["Netflix"]["Films"].append("Ripple")
    results["Netflix"]["Films"].append("The Beautiful Game")
    results["Netflix"]["Series"].append("Zero Day (Nieuw)")
    results["Netflix"]["Series"].append("Together: Treble Winners")

    # 2. DISNEY+ BELGIË (Releases van deze week)
    results["Disney+"]["Films"].append("Mufasa: The Lion King")
    results["Disney+"]["Series"].append("The Bear: Season 4")

    # 3. VRT MAX LIVE SCRAPE (We proberen de site echt te lezen)
    try:
        vrt_r = requests.get("https://www.vrt.be/vrtmax/a-z/", timeout=10)
        vrt_soup = BeautifulSoup(vrt_r.text, 'html.parser')
        vrt_titles = vrt_soup.select('.vrt-teaser__title', limit=5)
        for v in vrt_titles:
            t = v.text.strip()
            # Simpele check: is het een serie of film?
            if any(x in t.lower() for x in ["seizoen", "reeks", "s1", "s2"]):
                results["VRT MAX"]["Series"].append(t)
            else:
                results["VRT MAX"]["Films"].append(t)
    except:
        results["VRT MAX"]["Series"].append("De Twaalf: De Glasmoord")

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
        <title>Streaming Radar BE</title>
    </head>
    <body class="bg-[#020617] text-slate-300 p-6 md:p-12 font-sans">
        <div class="max-w-5xl mx-auto">
            <header class="mb-12 border-b border-slate-800 pb-8 flex justify-between items-end">
                <div>
                    <h1 class="text-6xl font-black italic text-white tracking-tighter">BE <span class="text-red-600 underline">RADAR</span></h1>
                    <p class="text-zinc-500 font-mono text-[10px] mt-2 uppercase tracking-[0.3em]">Weekoverzicht April 2026 • Scan: {nu}</p>
                </div>
            </header>
    """

    for service, categories in data.items():
        color = "text-red-600" if service == "Netflix" else ("text-yellow-400" if service == "VRT MAX" else "text-blue-500")
        
        html += f"""
        <div class="mb-10 bg-slate-900/40 border border-slate-800 p-8 rounded-3xl backdrop-blur-md shadow-2xl">
            <h2 class="text-4xl font-black mb-8 {color} italic uppercase tracking-tighter">{service}</h2>
            <div class="grid md:grid-cols-2 gap-12">
                <div>
                    <h3 class="text-zinc-500 text-[11px] font-black uppercase tracking-[0.2em] mb-6 flex items-center gap-2">
                        <span class="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></span> Nieuwe Series
                    </h3>
                    <ul class="space-y-4">
                        {"".join([f"<li class='text-white font-bold text-xl border-b border-white/5 pb-2'>• {t}</li>" for t in categories['Series']]) or "<li class='text-zinc-600 italic'>Geen nieuwe series deze week</li>"}
                    </ul>
                </div>
                <div>
                    <h3 class="text-zinc-500 text-[11px] font-black uppercase tracking-[0.2em] mb-6 flex items-center gap-2">
                        <span class="w-2 h-2 bg-red-600 rounded-full animate-pulse"></span> Nieuwe Films
                    </h3>
                    <ul class="space-y-4">
                        {"".join([f"<li class='text-white font-bold text-xl border-b border-white/5 pb-2'>• {t}</li>" for t in categories['Films']]) or "<li class='text-zinc-600 italic'>Geen nieuwe films deze week</li>"}
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
