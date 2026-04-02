import requests
from datetime import datetime, timedelta

def get_week_range():
    # Berekent de start (maandag) en het einde (zondag) van de huidige week
    today = datetime.now()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    return start.strftime("%d/%b"), end.strftime("%d/%b")

def get_updates():
    # In een volledige scraping-setup zou de robot hier door de tijdlijn van JustWatch/VRT MAX lopen
    # Hier is de gefilterde lijst voor DEZE WEEK (Voorbeeld data die de robot ophaalt)
    shows = [
        {"s": "Netflix", "t": "The Night Agent S2", "d": "Maandag 30/03", "status": "Nu te zien"},
        {"s": "Disney+", "t": "Andor: Season 2", "d": "Woensdag 01/04", "status": "Nu te zien"},
        {"s": "VRT MAX", "t": "Vrede op Aarde", "d": "Dagelijks", "status": "Nieuwe afleveringen"},
        {"s": "HBO Max", "t": "A Knight of the Seven Kingdoms", "d": "Vrijdag 03/04", "status": "Verwacht"},
        {"s": "Apple TV+", "t": "Silo: Season 2", "d": "Vrijdag 03/04", "status": "Verwacht"},
        {"s": "Prime", "t": "Citadel: Diana", "d": "Donderdag 02/04", "status": "Vandaag toegevoegd"}
    ]
    return shows

def make_page():
    shows = get_updates()
    start_wk, end_wk = get_week_range()
    nu = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    html = f"""
    <html><head><script src='https://cdn.tailwindcss.com'></script></head>
    <body class='bg-black text-white p-6 md:p-12 font-sans'>
        <div class='max-w-4xl mx-auto'>
            <header class='border-b border-zinc-800 pb-6 mb-8'>
                <h1 class='text-5xl font-black italic tracking-tighter'>WEEK <span class='text-blue-500'>RADAR</span></h1>
                <p class='text-zinc-500 font-mono text-sm mt-2'>PERIODE: {start_wk} TOT {end_wk} | SCAN: {nu}</p>
            </header>
            <div class='grid gap-6'>
    """
    
    for s in shows:
        accent = "border-yellow-400 shadow-[0_0_15px_rgba(253,224,71,0.1)]" if s['s'] == "VRT MAX" else "border-zinc-800"
        status_color = "text-green-400" if "Nu" in s['status'] or "Vandaag" in s['status'] else "text-blue-400"
        
        html += f"""
                <div class='bg-zinc-900/50 p-6 rounded-2xl border {accent} flex justify-between items-center'>
                    <div>
                        <p class='text-[10px] font-bold text-zinc-500 uppercase tracking-[0.2em] mb-1'>{s['s']}</p>
                        <h2 class='text-2xl font-bold'>{s['t']}</h2>
                        <p class='text-sm mt-1 {status_color} font-medium'>{s['status']} • {s['d']}</p>
                    </div>
                    <div class='hidden md:block'>
                        <span class='px-4 py-2 rounded-full bg-zinc-800 text-xs font-bold uppercase'>Info</span>
                    </div>
                </div>"""
    
    html += "</div><footer class='mt-12 text-zinc-600 text-[10px] text-center uppercase tracking-widest'>Geautomatiseerde Weekly Pipeline v2.0</footer></div></body></html>"
    
    with open("index.html", "w", encoding="utf-8") as f: 
        f.write(html)

make_page()
