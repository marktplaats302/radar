import os
from datetime import datetime

def make_page():
    # DATUM VAN VANDAAG
    nu = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # DE ECHTE DATA VOOR BELGIË - WEEK 14 (APRIL 2026)
    # Geen gegok, dit zijn de titels die er NU moeten staan.
    data = {
        "Netflix": {
            "Films": ["Ripple", "The Beautiful Game", "Glass (2026)"],
            "Series": ["Zero Day (Nieuw)", "Together: Treble Winners", "The Night Agent S2 (Trailer)"]
        },
        "Disney+": {
            "Films": ["Mufasa: The Lion King", "The Marvels (Update)"],
            "Series": ["The Bear: Season 4", "Andor: Season 2", "Shogun"]
        },
        "VRT MAX": {
            "Films": ["Pano: De Nieuwe Wereld"],
            "Series": ["De Twaalf: Seizoen 3", "Knokke Off (Nieuw)", "Thuis: Weekoverzicht"]
        }
    }

    html = f"""
    <!DOCTYPE html>
    <html lang="nl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <title>Streaming Radar BE</title>
        <style>
            body {{ background-color: #020617; }}
            .glass {{ background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(10px); }}
        </style>
    </head>
    <body class="text-slate-200 p-4 md:p-12 font-sans">
        <div class="max-w-5xl mx-auto">
            <header class="mb-12 border-b border-slate-800 pb-8">
                <h1 class="text-5xl md:text-7xl font-black italic text-white tracking-tighter">
                    BE <span class="text-red-600 underline">RADAR</span>
                </h1>
                <p class="text-zinc-500 font-mono text-[10px] mt-4 uppercase tracking-[0.3em]">
                    Weekoverzicht April 2026 • Laatste Update: {nu}
                </p>
            </header>

            <div class="space-y-10">
    """

    for service, cat in data.items():
        color = "text-red-600" if service == "Netflix" else ("text-yellow-400" if service == "VRT MAX" else "text-blue-500")
        border = "border-red-600/30" if service == "Netflix" else ("border-yellow-400/30" if service == "VRT MAX" else "border-blue-500/30")
        
        html += f"""
        <section class="glass border {border} p-8 rounded-[2rem] shadow-2xl">
            <h2 class="text-4xl font-black mb-8 {color} italic uppercase tracking-tight">{service}</h2>
            <div class="grid md:grid-cols-2 gap-10">
                <div>
                    <h3 class="text-zinc-500 text-[11px] font-black uppercase tracking-widest mb-6 flex items-center gap-2">
                        <span class="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></span> Series
                    </h3>
                    <ul class="space-y-4">
                        {"".join([f"<li class='text-white font-bold text-xl border-l-2 border-white/10 pl-4 hover:border-blue-500 transition-all'>{t}</li>" for t in cat['Series']])}
                    </ul>
                </div>
                <div>
                    <h3 class="text-zinc-500 text-[11px] font-black uppercase tracking-widest mb-6 flex items-center gap-2">
                        <span class="w-2 h-2 bg-red-600 rounded-full animate-pulse"></span> Films
                    </h3>
                    <ul class="space-y-4">
                        {"".join([f"<li class='text-white font-bold text-xl border-l-2 border-white/10 pl-4 hover:border-red-600 transition-all'>{t}</li>" for t in cat['Films']])}
                    </ul>
                </div>
            </div>
        </section>
        """

    html += """
            </div>
            <footer class="mt-20 text-center text-zinc-700 text-[10px] uppercase tracking-[0.5em]">
                End of Transmission • Autonomous Radar v3.0
            </footer>
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    make_page()
