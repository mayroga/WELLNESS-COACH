
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
import wellness_engine as engine

BASE_DIR=Path(__file__).resolve().parent
STATIC_DIR=BASE_DIR/"static"
STATIC_DIR.mkdir(exist_ok=True)
VERSION="9.0.0"
LANGUAGES=("es","en","pt")
SECTIONS=("all","movement","calm","coach")

app=FastAPI(
    title="WELLNESS COACH",
    description="Actividades generales de bienestar cotidiano.",
    version=VERSION
)
app.mount("/static",StaticFiles(directory=str(STATIC_DIR)),name="static")

@app.get("/",response_class=HTMLResponse)
def home():
    p=STATIC_DIR/"index.html"
    if not p.exists():
        return HTMLResponse("<h1>WELLNESS COACH</h1><p>Falta static/index.html.</p>",status_code=503)
    return HTMLResponse(p.read_text(encoding="utf-8"))

@app.get("/health")
def health():
    data=engine.get_health()
    data["version"]=VERSION
    data["activities"]=len(engine.get_activities("es"))
    return data

@app.get("/api/config")
def config():
    return {
        "name":"WELLNESS COACH",
        "version":VERSION,
        "audience":"40+",
        "languages":list(LANGUAGES),
        "durations":[3,5,10],
        "program_days":7,
        "sections":engine.get_catalog("es"),
        "activity_count":len(engine.get_activities("es"))
    }

@app.get("/api/activities")
def activities(lang:str="es",section:str="all"):
    lang=lang if lang in LANGUAGES else "es"
    section=section if section in SECTIONS else "all"
    return JSONResponse({
        "language":lang,
        "activities":engine.get_activities(lang,section)
    })

@app.get("/api/session")
def session(lang:str="es",kind:str="pause",minutes:int=3,allow_repeat:bool=False):
    lang=lang if lang in LANGUAGES else "es"
    if kind not in ("pause","energy","calm","nature","coach","program","movement"):
        kind="pause"
    minutes=max(3,min(10,minutes))
    return JSONResponse(engine.get_session(
        lang,kind,minutes,allow_repeat=allow_repeat
    ))

@app.get("/api/plant/{plant_id}")
def plant(plant_id:str,lang:str="es"):
    return JSONResponse({
        "error":"Plant profiles are no longer available.",
        "language":lang if lang in LANGUAGES else "es",
        "plant_id":plant_id
    },status_code=404)

@app.get("/api/program")
def program(lang:str="es",day:int=1):
    lang=lang if lang in LANGUAGES else "es"
    day=max(1,min(7,day))
    return JSONResponse(engine.get_program_day(lang,day))
