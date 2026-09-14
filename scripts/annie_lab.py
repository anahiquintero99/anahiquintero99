#!/usr/bin/env python3
"""Annie Lab v1 — laboratorio virtual (cristal y cromo rosa) generado con datos reales de GitHub.
Uso: python3 scripts/annie_lab.py [dist/annie-lab.svg]   · Solo stdlib."""
import os, sys, json, random, datetime, html, urllib.request
from zoneinfo import ZoneInfo

USER = "anahiquintero99"
TOKEN = os.environ.get("PROFILE_TOKEN") or os.environ.get("GITHUB_TOKEN") or os.popen("gh auth token").read().strip()
OUT = sys.argv[1] if len(sys.argv) > 1 else "dist/annie-lab.svg"
# Mapa repo → sector. Vive FUERA del repo (es privado): ~/.config/annie-lab/sectores.json en la Mac.
try: SECTOR = json.load(open(os.path.expanduser("~/.config/annie-lab/sectores.json"), encoding="utf-8"))
except Exception: SECTOR = {}

Q = """query($u:String!){ user(login:$u){
  repositories(first:100, ownerAffiliations:OWNER, orderBy:{field:PUSHED_AT,direction:DESC}){ totalCount
    nodes{ name isPrivate pushedAt stargazerCount languages(first:5,orderBy:{field:SIZE,direction:DESC}){ edges{ size node{ name } } } } }
  pullRequests{ totalCount } followers{ totalCount }
  contributionsCollection{ totalCommitContributions restrictedContributionsCount
    contributionCalendar{ totalContributions weeks{ contributionDays{ date contributionCount } } } } } }"""
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SNAP = os.path.join(ROOT, "data", "stats.json")

def gh_json(url, data=None):
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None,
                                 headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=60) as r: return json.load(r)

# Estadísticas. Con PROFILE_TOKEN (o gh local) se consultan en vivo y se guarda una foto AGREGADA en data/stats.json
# (totales, calendario, lenguajes y sectores); nunca nombres de repos privados. Sin PAT, el Action usa esa foto.
def sector(r): return SECTOR.get(r["name"], r["name"] if not r["isPrivate"] else "privado")
def agregar(u):
    cal = u["contributionsCollection"]["contributionCalendar"]
    langs = {}
    for r in u["repositories"]["nodes"]:
        for e in r["languages"]["edges"]: langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    repos = [r for r in u["repositories"]["nodes"] if r["pushedAt"]]
    return {"repos": u["repositories"]["totalCount"], "prs": u["pullRequests"]["totalCount"], "followers": u["followers"]["totalCount"],
            "commits": u["contributionsCollection"]["totalCommitContributions"] + u["contributionsCollection"]["restrictedContributionsCount"],
            "total": cal["totalContributions"], "weeks": [[d["date"], d["contributionCount"]] for w in cal["weeks"] for d in w["contributionDays"]],
            "langs": sorted(langs.items(), key=lambda x: -x[1])[:5],
            "sectores_recientes": list(dict.fromkeys(sector(r) for r in repos[:6]))[:4],
            "semana": sum(1 for r in repos if (datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.fromisoformat(r["pushedAt"].replace("Z", "+00:00"))).days < 7)}
if os.environ.get("PROFILE_TOKEN") or not os.environ.get("GITHUB_ACTIONS"):
    st = agregar(gh_json("https://api.github.com/graphql", {"query": Q, "variables": {"u": USER}})["data"]["user"])
    os.makedirs(os.path.dirname(SNAP), exist_ok=True); json.dump(st, open(SNAP, "w", encoding="utf-8"), ensure_ascii=False)
else:
    st = json.load(open(SNAP, encoding="utf-8"))

visitas = []

CDMX = ZoneInfo("America/Mexico_City"); now = datetime.datetime.now(CDMX); today = now.date().isoformat()
days = [{"date": d, "contributionCount": c} for d, c in st["weeks"] if d <= today]
counts = [d["contributionCount"] for d in days]
streak = 0
for d in reversed(days):
    if d["contributionCount"] > 0: streak += 1
    elif d["date"] == today: continue
    else: break
wk = [c for _, c in st["weeks"]]
weeks = [sum(wk[i:i+7]) for i in range(0, len(wk), 7)][-26:]
commits, total = st["commits"], st["total"]
hoy = counts[-1] if days and days[-1]["date"] == today else 0
sectores_rec = st["sectores_recientes"]; nsemana = st["semana"]
top = st["langs"]; lsum = sum(v for _, v in top) or 1
try: adastra = json.load(open(os.path.join(ROOT, "data", "ad-astra.json"), encoding="utf-8"))["rutas"]
except Exception: adastra = []
status = "SHIPPING" if hoy > 0 else ("STABLE" if streak > 0 else "STANDBY")
noche = now.hour >= 19 or now.hour < 7

SANS = 'Avenir Next, Futura, Jost, Helvetica Neue, Arial, sans-serif'; SERIF = 'Cormorant Garamond, Baskerville, Georgia, serif'; MONO = 'SF Mono, Menlo, JetBrains Mono, Consolas, monospace'
INK, INK2, PINK, LAV = "#2B1A24", "#7A4A62", "#E84393", "#9B7BEA"

def glitter(n):
    g = ""
    for _ in range(n):
        x, y, r = random.randint(8, W-8), random.randint(8, H-8), random.choice([1, 1.4, 1.9])
        g += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff"><animate attributeName="opacity" values=".1;1;.1" dur="{random.choice([1.8,2.3,2.9,3.4])}s" begin="{random.random()*3:.1f}s" repeatCount="indefinite"/></circle>'
    return g


def icon(name, x, y, w):
    f = os.path.join(ROOT, "assets", "3d", "160", f"{name}-pink.png")
    if not os.path.exists(f): return ""
    b64 = __import__("base64").b64encode(open(f, "rb").read()).decode()
    return f'<image href="data:image/png;base64,{b64}" x="{x}" y="{y}" width="{w}" height="{w}"/>'

def panel(x, y, w, h, code, title, ico=None):
    p = (f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="url(#glass)" stroke="url(#edge)" stroke-width="1.2"/></g>'
         f'<rect x="{x+1}" y="{y+1}" width="{w-2}" height="{h*.4:.0f}" rx="19" fill="url(#shine)"/>'
         f'<rect x="{x+16}" y="{y+h-3}" width="{w-32}" height="3" rx="1.5" fill="url(#chrome)"/>'
         f'<text x="{x+22}" y="{y+28}" class="mono">{code} · {title}</text>'
         f'<line x1="{x+22}" y1="{y+38}" x2="{x+w-22}" y2="{y+38}" class="hair"/>')
    if ico: p += icon(ico, x+w-64, y-26, 52)
    return p

def monitor(x, y, w, h):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="url(#chromeV)" stroke="#8F3D66" stroke-opacity=".4"/>'
            f'<rect x="{x+6}" y="{y+6}" width="{w-12}" height="{h-12}" rx="7" fill="#2B0F20"/>'
            f'<rect x="{x+6}" y="{y+6}" width="{w-12}" height="{(h-12)*.35:.0f}" rx="7" fill="url(#screenShine)"/>'
            f'<rect x="{x+w/2-18}" y="{y+h}" width="36" height="8" rx="2" fill="url(#chromeV)"/>')

def ufo(x, y, s, dur, dx=0):
    return (f'<g><animateTransform attributeName="transform" type="translate" values="{x} {y};{x+dx} {y-10};{x} {y}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<g transform="scale({s})"><ellipse cx="0" cy="0" rx="42" ry="12" fill="url(#chromeV)" stroke="#8F3D66" stroke-opacity=".4"/><ellipse cx="0" cy="-8" rx="18" ry="12" fill="#fff" fill-opacity=".75" stroke="#fff"/>'
            f'<ellipse cx="0" cy="14" rx="26" ry="16" fill="url(#beam)" opacity=".7"/>'
            + "".join(f'<circle cx="{-30 + i*15}" cy="4" r="2" fill="#fff"><animate attributeName="opacity" values=".2;1;.2" dur="1.2s" begin="{i*.2}s" repeatCount="indefinite"/></circle>' for i in range(5)) + '</g></g>')

W, H = 1200, 760
random.seed(13)

# ---------- NÚCLEO ----------
nucleo = panel(40, 90, 290, 340, "AQ—010", "NÚCLEO", "bulb")
nucleo += (f'<ellipse cx="185" cy="150" rx="62" ry="12" fill="url(#chromeV)" stroke="#8F3D66" stroke-opacity=".4"/>'
           f'<rect x="130" y="150" width="110" height="150" fill="#fff" fill-opacity=".28" stroke="#fff" stroke-opacity=".9" stroke-width="1.2"/>'
           f'<rect x="140" y="156" width="10" height="138" rx="5" fill="#fff" opacity=".6"/><rect x="222" y="156" width="4" height="138" rx="2" fill="#fff" opacity=".35"/>'
           f'<g><animateTransform attributeName="transform" type="rotate" values="0 185 225;360 185 225" dur="9s" repeatCount="indefinite"/><ellipse cx="185" cy="225" rx="44" ry="14" fill="none" stroke="#fff" stroke-opacity=".8" stroke-width="1.5"/><circle cx="229" cy="225" r="3" fill="#fff" filter="url(#glow)"/></g>'
           f'<g><animateTransform attributeName="transform" type="rotate" values="360 185 225;0 185 225" dur="13s" repeatCount="indefinite"/><ellipse cx="185" cy="225" rx="14" ry="46" fill="none" stroke="{LAV}" stroke-opacity=".7" stroke-width="1.5"/><circle cx="185" cy="179" r="3" fill="#fff" filter="url(#glow)"/></g>'
           f'<circle cx="185" cy="225" r="30" fill="url(#core)" filter="url(#glow)"><animate attributeName="r" values="28;34;28" dur="2.8s" repeatCount="indefinite"/></circle>'
           f'<circle cx="185" cy="225" r="11" fill="#fff" opacity=".95"><animate attributeName="opacity" values=".7;1;.7" dur="2.8s" repeatCount="indefinite"/></circle>'
           f'<ellipse cx="185" cy="300" rx="62" ry="12" fill="url(#chromeV)" stroke="#8F3D66" stroke-opacity=".4"/>'
           f'<rect x="110" y="312" width="150" height="10" rx="5" fill="url(#chrome)"/>'
           f'<path d="M40 225 h88 M242 225 h88" stroke="url(#chromeV)" stroke-width="12" stroke-linecap="round"/>')
nucleo += monitor(62, 334, 246, 78) + (f'<text x="76" y="356" class="scr">CORE</text><text x="76" y="384" class="scrbig" font-size="22">{streak} <tspan font-size="10" font-weight="400" fill="#F3B8D2">DÍAS DE RACHA</tspan></text>'
                                       f'<text x="294" y="356" text-anchor="end" class="scr">{status}</text><text x="294" y="384" text-anchor="end" class="scrbig" font-size="13">{commits:,} <tspan font-size="9" font-weight="400" fill="#F3B8D2">COMMITS 2026</tspan></text>')

# ---------- SEÑALES ----------
sen = panel(350, 90, 430, 340, "AQ—020", "SALA DE SEÑALES", "chart")
mx = max(weeks) or 1
pts = [(384 + i * (170 / 25), 240 - (w / mx) * 70) for i, w in enumerate(weeks)]
wave = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
sen += monitor(372, 150, 194, 108) + f'<polyline points="{wave}" fill="none" stroke="{PINK}" stroke-width="2" stroke-linejoin="round"/>' \
       f'<text x="384" y="170" class="scr">ACTIVITY · 26 W</text><circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="3.5" fill="#fff" filter="url(#glow)"/>'
estado = sectores_rec[0] if sectores_rec else "—"
sen += monitor(584, 150, 174, 108) + (f'<text x="596" y="170" class="scr">CURRENT STATE</text>'
       f'<text x="671" y="208" text-anchor="middle" class="scrbig" font-size="14">{html.escape(estado)}</text>'
       f'<text x="671" y="236" text-anchor="middle" class="scr" font-size="8">HOY {hoy} · CONF {min(99, 60 + streak * 3)}%</text>')
sen += monitor(372, 288, 386, 122) + '<text x="384" y="308" class="scr">LANGUAGE SPECTRUM</text>'
for i, (n, v) in enumerate(top):
    p = v / lsum; x = 390 + i * 74
    sen += f'<rect x="{x}" y="{380 - p*56:.0f}" width="58" height="{max(3, p*56):.0f}" rx="3" fill="{[PINK, "#F06AB5", LAV, "#FF9ECF", "#C9A7F5"][i]}"/>' \
           f'<text x="{x+29}" y="394" text-anchor="middle" class="scr" font-size="7" letter-spacing="1">{html.escape({"TypeScript":"TS","JavaScript":"JS"}.get(n, n)).upper()} {p*100:.0f}%</text>'

# ---------- ESTACIÓN DE MANDO (grande) ----------
mando = panel(800, 90, 360, 630, "AQ—030", "ESTACIÓN DE MANDO", "computer")
heart = "M980 172 C950 142 900 152 900 196 C900 238 950 262 980 292 C1010 262 1060 238 1060 196 C1060 152 1010 142 980 172Z"
mando += (f'<path d="{heart}" fill="url(#chromeV)" stroke="#8F3D66" stroke-opacity=".4"/>'
          f'<path d="M980 184 C958 162 918 170 918 200 C918 232 958 252 980 276 C1002 252 1042 232 1042 200 C1042 170 1002 162 980 184Z" fill="#2B0F20"/>'
          f'<text x="980" y="200" text-anchor="middle" class="scr" font-size="7.5">NOW BUILDING</text>'
          f'<text x="980" y="222" text-anchor="middle" class="scrbig" font-size="13">{html.escape(sectores_rec[0] if sectores_rec else "—")}</text>'
          f'<text x="980" y="242" text-anchor="middle" class="scr" font-size="7.5">{hoy} HOY</text>'
          f'<rect x="900" y="304" width="160" height="26" rx="6" fill="url(#chromeV)" stroke="#8F3D66" stroke-opacity=".3"/>'
          + "".join(f'<rect x="{908 + i*11}" y="310" width="8" height="6" rx="1.5" fill="#F3B8D2"/><rect x="{908 + i*11}" y="319" width="8" height="6" rx="1.5" fill="#F3B8D2"/>' for i in range(14)))
mando += '<text x="822" y="366" class="mono" font-size="9">EN LA MESA</text>'
for i, sec in enumerate(sectores_rec[1:4]):
    mando += f'<text x="822" y="{386 + i*20}" class="k">· {html.escape(sec)}</text>'
mando += '<line x1="822" y1="452" x2="1138" y2="452" class="hair"/><text x="822" y="474" class="mono" font-size="9">HERRAMIENTAS</text>'
tools = [("computer", "Web"), ("mobile", "Apps"), ("tools", "Automatización"), ("shield", "Seguridad"), ("target", "Producto"), ("bulb", "IA · agentes"), ("chart", "Datos"), ("clock", "Deploy en días")]
for i, (ic, lab) in enumerate(tools):
    cx = 822 + (i % 4) * 82; cy = 484 + (i // 4) * 92
    mando += icon(ic, cx, cy, 56) + f'<text x="{cx+28}" y="{cy+70}" text-anchor="middle" class="k" font-size="9.5">{lab}</text>'
mando += '<line x1="822" y1="672" x2="1138" y2="672" class="hair"/><text x="822" y="692" class="mono" font-size="9">STACK</text><text x="822" y="708" class="k" font-size="10.5">React · Node · Flutter · Python · GCP · Postgres · Stripe</text>'

# ---------- GALERÍA ----------
gal = panel(40, 450, 740, 270, "AQ—060", "GALERÍA", "star")
premios = [("trophy", "FAMEX 25", "Líder Espacial", "Emergente"), ("crown", "LÍDERES 26", "Perfil", "destacado"), ("moon", "IAC 25", "Paper", "neuromórfica"),
           ("mic", "DIPUTADOS 26", "Panel", "de IA"), ("medal", "NASA 25", "Mentora", "Space Apps")]
gal += '<rect x="62" y="590" width="696" height="6" rx="3" fill="url(#chromeV)" stroke="#8F3D66" stroke-opacity=".3"/><rect x="62" y="596" width="696" height="10" fill="#fff" fill-opacity=".25"/>'
for i, (ic, a_, b_, c_) in enumerate(premios):
    x = 110 + i * 145
    gal += (f'<ellipse cx="{x}" cy="588" rx="30" ry="6" fill="#D8347F" opacity=".18" filter="url(#glow)"/>'
            + icon(ic, x - 36, 504, 72) +
            f'<text x="{x}" y="622" text-anchor="middle" class="mono" font-size="7" letter-spacing="1.5">{a_}</text>'
            f'<text x="{x}" y="638" text-anchor="middle" class="k" font-size="10">{b_}</text><text x="{x}" y="651" text-anchor="middle" class="k" font-size="10">{c_}</text>')
gal += '<text x="62" y="700" class="mono" font-size="8">TALENT LAND · IAC · 11+ PONENCIAS · 6+ UNIVERSIDADES</text>'

naves = ufo(230, 52, .55, 4.2, 30) + ufo(1010, 60, .4, 3.4, -24) + ufo(640, 440, .35, 5, 40)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{SANS}">
<defs>
<linearGradient id="room" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{'#6B2452' if noche else '#FFD9EA'}"/><stop offset=".5" stop-color="{'#8A2F6A' if noche else '#FFC2DE'}"/><stop offset="1" stop-color="{'#4A1838' if noche else '#E9B8F4'}"/></linearGradient>
<linearGradient id="chrome" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C96A9A"/><stop offset=".22" stop-color="#FFE6F1"/><stop offset=".45" stop-color="#E88BBE"/><stop offset=".62" stop-color="#FFFFFF"/><stop offset=".82" stop-color="#D9779F"/><stop offset="1" stop-color="#8F3D66"/></linearGradient>
<linearGradient id="chromeV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF4F9"/><stop offset=".35" stop-color="#F3B8D2"/><stop offset=".5" stop-color="#FFFFFF"/><stop offset=".7" stop-color="#E594BF"/><stop offset="1" stop-color="#A9507C"/></linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".66"/><stop offset="1" stop-color="#fff" stop-opacity=".36"/></linearGradient>
<linearGradient id="shine" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".6"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="screenShine" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".12"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".5" stop-color="#F3B8CE"/><stop offset="1" stop-color="#fff" stop-opacity=".7"/></linearGradient>
<linearGradient id="acc" x1="0" x2="1"><stop offset="0" stop-color="{PINK}"/><stop offset="1" stop-color="{LAV}"/></linearGradient>
<linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD6EA"/><stop offset="1" stop-color="#FFD6EA" stop-opacity="0"/></linearGradient>
<linearGradient id="holo" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFB6D9" stop-opacity=".9"/><stop offset=".35" stop-color="#C9A7F5" stop-opacity=".7"/><stop offset=".7" stop-color="#A9E4FF" stop-opacity=".7"/><stop offset="1" stop-color="#FFD9A8" stop-opacity=".8"/></linearGradient>
<radialGradient id="sph" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".25" stop-color="#FFD1E6"/><stop offset=".6" stop-color="#F58BC0"/><stop offset="1" stop-color="#B8347A"/></radialGradient>
<radialGradient id="core" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff"/><stop offset=".4" stop-color="#FFB6D9"/><stop offset=".8" stop-color="{PINK}" stop-opacity=".6"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/></radialGradient>
<filter id="sh" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#D8347F" flood-opacity=".16"/></filter>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="blur" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="26"/></filter>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="linear" slope=".05"/></feComponentTransfer></filter>
<clipPath id="f"><rect width="{W}" height="{H}" rx="8"/></clipPath>
<style>
.mono{{font-family:{MONO};font-size:10px;letter-spacing:2.5px;fill:{INK2}}} .k{{font-family:{SANS};font-size:12px;fill:{INK}}}
.big{{font-family:{SANS};font-weight:300;font-size:44px;fill:#B0306E}} .hair{{stroke:{INK};stroke-opacity:.18;stroke-width:1}}
.scr{{font-family:{MONO};font-size:9px;letter-spacing:1.5px;fill:#F3B8D2}} .scrbig{{font-family:{SANS};font-size:15px;font-weight:600;fill:#fff}}
.hdr{{font-family:{MONO};font-size:12px;letter-spacing:4px;fill:{'#FFD6EA' if noche else INK2};font-weight:700}}
</style></defs>
<g clip-path="url(#f)">
<rect width="{W}" height="{H}" fill="url(#room)"/>
<polygon points="760,0 1200,0 1200,940 560,940" fill="url(#chrome)" opacity="{'.25' if noche else '.4'}"/>
<polygon points="800,0 840,0 640,940 600,940" fill="#fff" opacity=".3"/>
<g stroke="#fff" stroke-opacity=".25">{"".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>' for x in range(0, W, 60))}{"".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(0, H, 60))}</g>
<g fill="#fff" filter="url(#blur)" opacity=".7"><ellipse cx="180" cy="930" rx="300" ry="60"/><ellipse cx="1050" cy="20" rx="260" ry="50"/></g>
<rect x="440" y="0" width="320" height="8" rx="4" fill="#fff" opacity=".95" filter="url(#glow)"/>
{glitter(70)}
<text x="600" y="48" text-anchor="middle" class="hdr">AQ—000 · ANNIE LAB · CDMX {now:%H:%M} · STATUS: {status} ✦</text>{icon("rocket", 900, 18, 44)}
<text x="40" y="48" class="hdr" font-size="10">{'NIGHT MODE' if noche else 'DAY MODE'}</text><text x="1160" y="48" text-anchor="end" class="hdr" font-size="10">{now:%d.%m.%Y}</text>
<path d="M596 62 l7 -12" stroke="url(#chrome)" stroke-width="4" stroke-linecap="round"/>
{naves}{nucleo}{sen}{mando}{gal}
<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".5"/>
</g></svg>'''
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w", encoding="utf-8").write(svg)
print(f"annie-lab.svg · visitas {len(visitas)} · {status} · racha {streak} · hoy {hoy} · estado {estado} · {'noche' if noche else 'día'}")
