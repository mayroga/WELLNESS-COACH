from pathlib import Path
from fastapi import FastAPI,HTTPException,Query
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
import wellness_engine as engine

BASE_DIR=Path(__file__).resolve().parent
STATIC_DIR=BASE_DIR/"static"
INDEX_FILE=STATIC_DIR/"index.html"
STATIC_DIR.mkdir(parents=True,exist_ok=True)
VERSION="11.0.0"
LANGUAGES=("es","en","pt")
DURATIONS=(3,5,10)
SECTIONS=("all","calm","movement","coach")
KINDS=("pause","energy","calm","nature","plants","movement","coach","routine","daily","program")
app=FastAPI(title="WELLNESS COACH",description="Guía de bienestar cotidiano para personas adultas. No ofrece diagnóstico ni tratamiento médico.",version=VERSION)
app.mount("/static",StaticFiles(directory=str(STATIC_DIR)),name="static")

def valid_lang(lang):
    lang=str(lang or "es").strip().lower()
    return lang if lang in LANGUAGES else "es"

def valid_section(section):
    section=str(section or "all").strip().lower()
    if section in ("nature","plants"):
        return "all"
    return section if section in SECTIONS else "all"

def valid_duration(minutes):
    try:
        minutes=int(minutes)
    except (TypeError,ValueError):
        minutes=3
    return min(DURATIONS,key=lambda n:abs(n-minutes))

@app.get("/",response_class=HTMLResponse)
def home():
    if not INDEX_FILE.is_file():
        return HTMLResponse("<h1>WELLNESS COACH</h1><p>No se encontró static/index.html.</p>",status_code=503)
    try:
        return HTMLResponse(INDEX_FILE.read_text(encoding="utf-8"))
    except OSError:
        return HTMLResponse("<h1>WELLNESS COACH</h1><p>No se pudo cargar la aplicación.</p>",status_code=500)

@app.get("/health")
def health():
    data=engine.get_health()
    data.update({"status":"ok","app":"WELLNESS COACH","version":VERSION,"engine_version":engine.VERSION,"activity_count":len(engine.get_activities("es","all")),"plant_count":0,"languages":list(LANGUAGES),"durations":list(DURATIONS)})
    return JSONResponse(data)

@app.get("/api/config")
def config():
    data=engine.get_config()
    data.update({"name":"WELLNESS COACH","company":"May Roga LLC","version":VERSION,"engine_version":engine.VERSION,"audience":"40+","languages":list(LANGUAGES),"durations":list(DURATIONS),"sections":engine.get_catalog("es")["sections"],"activity_count":len(engine.get_activities("es","all")),"plant_count":0,"program_days":7,"voice_order":"show_text_then_speak_same_text"})
    return JSONResponse(data)

@app.get("/api/activities")
def activities(lang:str=Query("es"),section:str=Query("all")):
    lang=valid_lang(lang)
    section=valid_section(section)
    result=engine.get_activities(lang,section)
    return JSONResponse({"app":"WELLNESS COACH","version":VERSION,"language":lang,"section":section,"count":len(result),"activities":result})

@app.get("/api/session")
def session(lang:str=Query("es"),kind:str=Query("calm"),minutes:int=Query(3,ge=1,le=60),allow_repeat:bool=Query(False),activity_id:str|None=Query(None)):
    lang=valid_lang(lang)
    kind=str(kind or "calm").strip().lower()
    if kind in ("nature","plants"):
        kind="calm"
    if kind not in KINDS:
        kind="calm"
    duration=valid_duration(minutes)
    try:
        data=engine.get_session(activity_id=activity_id,minutes=duration,lang=lang,kind=kind)
    except Exception as exc:
        raise HTTPException(status_code=500,detail="No se pudo preparar la sesión. Inténtalo de nuevo.") from exc
    if not isinstance(data,dict) or not data.get("steps"):
        raise HTTPException(status_code=500,detail="La sesión no contiene instrucciones.")
    data["app"]="WELLNESS COACH"
    data["version"]=VERSION
    data["language"]=lang
    data["minutes"]=duration
    data["duration_minutes"]=duration
    data["duration_seconds"]=duration*60
    data["total_steps"]=len(data["steps"])
    data["instructions"]=list(data["steps"])
    data["step_interval_seconds"]=duration*60/len(data["steps"])
    data["prompt_interval_seconds"]=data["step_interval_seconds"]
    data["voice_order"]="show_text_then_speak_same_text"
    return JSONResponse(data)

@app.get("/api/program")
def program(lang:str=Query("es"),day:int=Query(1,ge=1,le=7)):
    lang=valid_lang(lang)
    try:
        data=engine.get_program_day(lang=lang,day=day)
    except Exception as exc:
        raise HTTPException(status_code=500,detail="No se pudo preparar el programa.") from exc
    data["app"]="WELLNESS COACH"
    data["version"]=VERSION
    data["language"]=lang
    data["day"]=day
    data["total_days"]=7
    return JSONResponse(data)

@app.get("/api/plant/{plant_id}")
def removed_plant(plant_id:str):
    raise HTTPException(status_code=404,detail="Esta versión de WELLNESS COACH no incluye contenido sobre plantas.")

@app.get("/api/ping")
def ping():
    return {"status":"ok","app":"WELLNESS COACH","version":VERSION}

@app.get("/robots.txt")
def robots():
    return HTMLResponse("User-agent: *\nDisallow: /",media_type="text/plain")
