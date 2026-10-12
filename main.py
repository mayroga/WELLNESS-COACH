from pathlib import Path
from fastapi import FastAPI,HTTPException
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
import wellness_engine as engine

BASE_DIR=Path(__file__).resolve().parent
STATIC_DIR=BASE_DIR/"static"
INDEX_FILE=STATIC_DIR/"index.html"
STATIC_DIR.mkdir(exist_ok=True)
VERSION="5.0.0"
LANGUAGES=("es","en","pt")
SECTIONS=("all","calm","movement","focus","routines")
app=FastAPI(title="WELLNESS COACH",description="Actividades generales de bienestar cotidiano para adultos de 40 años en adelante.",version=VERSION)
app.mount("/static",StaticFiles(directory=str(STATIC_DIR)),name="static")

def valid_lang(lang="es"):
    value=str(lang or "es").strip().lower()
    if value.startswith("en"):return "en"
    if value.startswith("pt"):return "pt"
    return "es"

def valid_section(section="all"):
    value=str(section or "all").strip().lower()
    aliases={"pause":"calm","energy":"movement","coach":"focus","nature":"routines","plants":"all","program":"routines"}
    value=aliases.get(value,value)
    return value if value in SECTIONS else "all"

@app.get("/",response_class=HTMLResponse)
def home():
    if not INDEX_FILE.exists():
        return HTMLResponse("<!doctype html><html lang='es'><meta charset='utf-8'><h1>WELLNESS COACH</h1><p>Falta el archivo static/index.html.</p></html>",status_code=503)
    return HTMLResponse(INDEX_FILE.read_text(encoding="utf-8"))

@app.get("/health")
def health():
    data=engine.get_health()
    data.update({"status":"ok","version":VERSION})
    return data

@app.get("/api/config")
def config():
    data=engine.get_config()
    data.update({"version":VERSION,"languages":list(LANGUAGES),"durations":[3,5,10],"program_days":7,"sections":engine.get_catalog("es"),"activity_count":len(engine.get_activities("es"))})
    return JSONResponse(data)

@app.get("/api/activities")
def activities(lang:str="es",section:str="all"):
    lang=valid_lang(lang)
    section=valid_section(section)
    return JSONResponse({"language":lang,"lang":lang,"section":section,"activities":engine.get_activities(lang,section)})

@app.get("/api/activity/{activity_id}")
def activity_detail(activity_id:str,lang:str="es"):
    lang=valid_lang(lang)
    data=engine.get_activity(activity_id,lang)
    if not data:raise HTTPException(status_code=404,detail="Activity not found")
    return JSONResponse(data)

@app.get("/api/session")
def session(lang:str="es",kind:str="calm",minutes:int=3,activity_id:str|None=None,allow_repeat:bool=False):
    lang=valid_lang(lang)
    kind=valid_section(kind)
    if kind=="all":kind="calm"
    minutes=max(3,min(10,int(minutes)))
    data=engine.get_session(activity_id=activity_id,minutes=minutes,lang=lang,kind=kind,allow_repeat=allow_repeat)
    return JSONResponse(data)

@app.get("/api/program")
def program(lang:str="es",day:int=1):
    lang=valid_lang(lang)
    day=max(1,min(7,int(day)))
    return JSONResponse(engine.get_program_day(lang,day))

@app.get("/api/program-week")
def program_week(lang:str="es"):
    return JSONResponse(engine.get_program(valid_lang(lang)))

@app.get("/api/plant/{plant_id}")
def legacy_plant_route(plant_id:str,lang:str="es"):
    # Ruta antigua conservada para evitar errores de compatibilidad.
    return JSONResponse({"error":"El catálogo de plantas ya no forma parte de WELLNESS COACH.","retired":True},status_code=410)

@app.get("/api/history")
def history(limit:int=20):
    return JSONResponse({"sessions":engine.get_recent_sessions(max(1,min(100,int(limit))))})

@app.get("/api/text/{key}")
def text_value(key:str,lang:str="es"):
    return JSONResponse({"key":key,"lang":valid_lang(lang),"text":engine.get_text(key,valid_lang(lang))})

if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app",host="0.0.0.0",port=8000)
