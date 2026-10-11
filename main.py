
from pathlib import Path
from fastapi import FastAPI,Query
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
import wellness_engine as engine

BASE_DIR=Path(__file__).resolve().parent
STATIC_DIR=BASE_DIR/"static"
STATIC_DIR.mkdir(exist_ok=True)
VERSION="4.0.0"
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
    return {"status":"ok","app":"WELLNESS COACH","version":VERSION}

@app.get("/api/config")
def config():
    return {"name":"WELLNESS COACH","version":VERSION,"languages":["es","en"],"durations":[3,5,10],"activity_count":len(engine.get_activities("es","all")),"program_days":7,"sections":engine.get_catalog()}

@app.get("/api/activities")
def activities(lang:str="es",section:str="all"):
    lang=lang if lang in ("es","en") else "es"
    return JSONResponse({"language":lang,"activities":engine.get_activities(lang,section)})

@app.get("/api/session")
def session(lang:str="es",kind:str="pause",minutes:int=3):
    lang=lang if lang in ("es","en") else "es"
    minutes=max(3,min(10,minutes))
    return JSONResponse(engine.get_session(lang,kind,minutes))

@app.get("/api/activity/{activity_id}")
def activity(activity_id:str,lang:str="es"):
    lang=lang if lang in ("es","en") else "es"
    data=engine.get_activity(activity_id,lang)
    if not data:
        return JSONResponse({"error":"Activity not found"},status_code=404)
    return JSONResponse(data)

@app.get("/api/plant/{plant_id}")
def plant(plant_id:str,lang:str="es"):
    lang=lang if lang in ("es","en") else "es"
    data=engine.get_plant(plant_id,lang)
    if not data:
        return JSONResponse({"error":"Plant not found"},status_code=404)
    return JSONResponse(data)

@app.get("/api/program")
def program(lang:str="es",day:int=Query(default=1,ge=1,le=7)):
    lang=lang if lang in ("es","en") else "es"
    return JSONResponse(engine.get_program_day(lang,day))
