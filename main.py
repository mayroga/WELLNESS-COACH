from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
import wellness_engine as engine

BASE_DIR=Path(__file__).resolve().parent
STATIC_DIR=BASE_DIR/"static"
STATIC_DIR.mkdir(exist_ok=True)
VERSION="4.2.0"
LANGUAGES=("es","en","pt")
app=FastAPI(title="WELLNESS COACH",description="Actividades generales de bienestar para adultos.",version=VERSION)
app.mount("/static",StaticFiles(directory=str(STATIC_DIR)),name="static")

@app.get("/",response_class=HTMLResponse)
def home():
    p=STATIC_DIR/"index.html"
    if not p.exists():
        return HTMLResponse("<h1>WELLNESS COACH</h1><p>Falta static/index.html.</p>",status_code=503)
    return HTMLResponse(p.read_text(encoding="utf-8"))

@app.get("/health")
def health():
    return {"status":"ok","app":"WELLNESS COACH","version":VERSION,"activities":len(engine.get_activities("es")),"plants":0,"plant_count":0,"languages":list(LANGUAGES)}

@app.get("/api/config")
def config(lang:str="es"):
    lang=lang if lang in LANGUAGES else "es"
    data=engine.get_config()
    data.update({"name":"WELLNESS COACH","version":VERSION,"engine_version":engine.VERSION,"audience":"40+","languages":list(LANGUAGES),"durations":[3,5,10],"program_days":7,"sections":engine.get_catalog(lang),"activity_count":len(engine.get_activities(lang)),"plant_count":0})
    return data

@app.get("/api/activities")
def activities(lang:str="es",section:str="all"):
    lang=lang if lang in LANGUAGES else "es"
    section=section if section in ("all","movement","calm","coach") else ("plants" if section in ("plants","nature") else "all")
    return JSONResponse({"language":lang,"activities":engine.get_activities(lang,section)})

@app.get("/api/session")
def session(lang:str="es",kind:str="pause",minutes:int=3,activity_id:str|None=None):
    lang=lang if lang in LANGUAGES else "es"
    kind=kind if kind in ("pause","energy","calm","movement","coach","routine","daily","program","nature","plants") else "pause"
    duration=minutes if minutes in (3,5,10) else min((3,5,10),key=lambda n:abs(n-minutes))
    data=engine.get_session(activity_id=activity_id,kind=kind,minutes=duration,lang=lang)
    return JSONResponse(data)

@app.get("/api/plant/{plant_id}")
def plant(plant_id:str,lang:str="es"):
    return JSONResponse({"error":"Plant activities are not included in this version."},status_code=404)

@app.get("/api/program")
def program(lang:str="es",day:int=1):
    lang=lang if lang in LANGUAGES else "es"
    return JSONResponse(engine.get_program_day(lang,max(1,min(7,day))))

@app.get("/api/ping")
def ping():
    return {"status":"ok","app":"WELLNESS COACH","version":VERSION}
