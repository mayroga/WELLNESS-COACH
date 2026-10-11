from pathlib import Path
from fastapi import FastAPI
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
    return {"status":"ok","app":"WELLNESS COACH","version":VERSION,"activities":len(engine.get_activities("es"))}

@app.get("/api/config")
def config():
    return {"name":"WELLNESS COACH","version":VERSION,"audience":"40+","languages":["es","en"],"durations":[3,5,10],"program_days":7,"sections":engine.get_catalog(),"activity_count":len(engine.get_activities("es"))}

@app.get("/api/activities")
def activities(lang:str="es",section:str="all"):
    lang=lang if lang in ("es","en") else "es"
    section=section if section in ("all","plants","movement","calm","coach") else "all"
    return JSONResponse({"language":lang,"activities":engine.get_activities(lang,section)})

@app.get("/api/session")
def session(lang:str="es",kind:str="pause",minutes:int=3):
    lang=lang if lang in ("es","en") else "es"
    kind=kind if kind in ("pause","energy","calm","nature","coach","program") else "pause"
    return JSONResponse(engine.get_session(lang,kind,max(3,min(10,minutes))))

@app.get("/api/plant/{plant_id}")
def plant(plant_id:str,lang:str="es"):
    lang=lang if lang in ("es","en") else "es"
    data=engine.get_plant(plant_id,lang)
    if not data:return JSONResponse({"error":"Plant not found"},status_code=404)
    return JSONResponse(data)

@app.get("/api/program")
def program(lang:str="es",day:int=1):
    lang=lang if lang in ("es","en") else "es"
    return JSONResponse(engine.get_program_day(lang,max(1,min(7,day))))
