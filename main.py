
from pathlib import Path
from fastapi import FastAPI,HTTPException,Query
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
import wellness_engine as engine

BASE_DIR=Path(__file__).resolve().parent
STATIC_DIR=BASE_DIR/"static"
INDEX_FILE=STATIC_DIR/"index.html"
STATIC_DIR.mkdir(parents=True,exist_ok=True)
VERSION="10.0.0"
LANGUAGES=("es","en","pt")
SECTIONS=("all","movement","calm","coach")
KINDS=("pause","energy","calm","nature","coach","program","movement","routine","daily")

app=FastAPI(
    title="WELLNESS COACH",
    description="Actividades generales de bienestar cotidiano para personas adultas.",
    version=VERSION
)

app.mount("/static",StaticFiles(directory=str(STATIC_DIR)),name="static")

def valid_lang(lang):
    return lang if lang in LANGUAGES else "es"

def valid_section(section):
    return section if section in SECTIONS else "all"

@app.get("/",response_class=HTMLResponse)
def home():
    if not INDEX_FILE.is_file():
        return HTMLResponse(
            "<!doctype html><html lang='es'><meta charset='utf-8'><title>WELLNESS COACH</title><h1>WELLNESS COACH</h1><p>Falta el archivo static/index.html.</p></html>",
            status_code=503
        )
    try:
        return HTMLResponse(INDEX_FILE.read_text(encoding="utf-8"))
    except OSError:
        return HTMLResponse(
            "<!doctype html><html lang='es'><meta charset='utf-8'><h1>WELLNESS COACH</h1><p>No se pudo cargar la página. Inténtalo de nuevo.</p></html>",
            status_code=500
        )

@app.get("/health")
def health():
    data=engine.get_health()
    data["status"]="ok"
    data["app"]="WELLNESS COACH"
    data["version"]=VERSION
    data["engine_version"]=getattr(engine,"VERSION",VERSION)
    data["activities"]=len(engine.get_activities("es","all"))
    return data

@app.get("/api/config")
def config():
    data=engine.get_config()
    data.update({
        "name":"WELLNESS COACH",
        "version":VERSION,
        "engine_version":getattr(engine,"VERSION",VERSION),
        "audience":"40+",
        "languages":list(LANGUAGES),
        "durations":[3,5,10],
        "program_days":7,
        "sections":engine.get_catalog("es"),
        "activity_count":len(engine.get_activities("es","all")),
        "prompt_interval_seconds":getattr(engine,"PROMPT_INTERVAL_SECONDS",10)
    })
    return data

@app.get("/api/activities")
def activities(
    lang:str=Query("es"),
    section:str=Query("all")
):
    lang=valid_lang(lang)
    section=valid_section(section)
    return JSONResponse({
        "language":lang,
        "section":section,
        "activities":engine.get_activities(lang,section)
    })

@app.get("/api/session")
def session(
    lang:str=Query("es"),
    kind:str=Query("pause"),
    minutes:int=Query(3,ge=1,le=60),
    allow_repeat:bool=Query(False),
    activity_id:str|None=Query(None)
):
    lang=valid_lang(lang)
    kind=kind.strip().lower() if isinstance(kind,str) else "pause"
    if kind not in KINDS:
        kind="pause"
    duration=minutes if minutes in (3,5,10) else min((3,5,10),key=lambda n:abs(n-minutes))
    try:
        data=engine.get_session(
            lang=lang,
            kind=kind,
            minutes=duration,
            allow_repeat=allow_repeat,
            activity_id=activity_id
        )
    except TypeError:
        data=engine.get_session(
            lang,
            kind,
            duration,
            allow_repeat=allow_repeat
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo preparar la sesión. Inténtalo de nuevo."
        )
    if not isinstance(data,dict) or not data.get("steps"):
        raise HTTPException(
            status_code=500,
            detail="No hay instrucciones disponibles para esta sesión."
        )
    data["language"]=lang
    data["minutes"]=int(data.get("minutes",duration))
    data["duration_minutes"]=int(data.get("duration_minutes",duration))
    data["duration_seconds"]=int(data.get("duration_seconds",data["minutes"]*60))
    return JSONResponse(data)

@app.get("/api/plant/{plant_id}")
def plant(plant_id:str,lang:str=Query("es")):
    return JSONResponse({
        "error":"Plant profiles are not available.",
        "language":valid_lang(lang),
        "plant_id":plant_id
    },status_code=404)

@app.get("/api/program")
def program(
    lang:str=Query("es"),
    day:int=Query(1,ge=1,le=7)
):
    lang=valid_lang(lang)
    day=max(1,min(7,day))
    try:
        data=engine.get_program_day(lang,day)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo cargar el día del programa. Inténtalo de nuevo."
        )
    if not isinstance(data,dict):
        raise HTTPException(
            status_code=500,
            detail="El programa no está disponible en este momento."
        )
    data["language"]=lang
    data["day"]=day
    data["total_days"]=7
    return JSONResponse(data)
