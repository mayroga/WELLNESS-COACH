
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
import wellness_engine as engine

BASE_DIR=Path(__file__).resolve().parent
STATIC_DIR=BASE_DIR/"static"
STATIC_DIR.mkdir(exist_ok=True)
app=FastAPI(title="WELLNESS COACH",description="Acompañamiento de bienestar general para adultos de 40 años en adelante.",version="2.0.0")
app.mount("/static",StaticFiles(directory=str(STATIC_DIR)),name="static")

@app.get("/",response_class=HTMLResponse)
def home():
    p=STATIC_DIR/"index.html"
    if not p.exists():
        return HTMLResponse("<h1>WELLNESS COACH</h1><p>Falta el archivo static/index.html.</p>",status_code=503)
    return HTMLResponse(p.read_text(encoding="utf-8"))

@app.get("/health")
def health():
    return {"status":"ok","app":"WELLNESS COACH","version":"2.0.0"}

@app.get("/api/config")
def config():
    return {"name":"WELLNESS COACH","version":"2.0.0","audience":"40+","languages":["es","en"],"durations":[3,5,10],"program_days":7,"sections":engine.get_catalog()}

@app.get("/api/activities")
def activities(lang:str="es",section:str="all"):
    if lang not in ("es","en"): lang="es"
    data=engine.get_activities(lang,section)
    return JSONResponse({"language":lang,"activities":data})

@app.get("/api/session")
def session(lang:str="es",kind:str="pause",minutes:int=3):
    if lang not in ("es","en"): lang="es"
    if kind not in ("pause","energy","calm","nature","coach","program"): kind="pause"
    minutes=max(3,min(10,minutes))
    return JSONResponse(engine.get_session(lang,kind,minutes))

@app.get("/api/plant/{plant_id}")
def plant(plant_id:str,lang:str="es"):
    if lang not in ("es","en"): lang="es"
    data=engine.get_plant(plant_id,lang)
    if not data: return JSONResponse({"error":"Plant not found"},status_code=404)
    return JSONResponse(data)

@app.get("/api/program")
def program(lang:str="es",day:int=1):
    if lang not in ("es","en"): lang="es"
    day=max(1,min(7,day))
    return JSONResponse(engine.get_program_day(lang,day))
