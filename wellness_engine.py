
from datetime import datetime,timezone
from copy import deepcopy
import hashlib
import random
import threading

VERSION="10.0.0"
APP_NAME="WELLNESS COACH"
COMPANY="May Roga LLC"
AUDIENCE="40+"
LANGUAGES=("es","en","pt")
SECTIONS=("movement","calm","coach")
MINUTES_ALLOWED=(3,5,10)
PROMPT_INTERVAL_SECONDS=10
PROGRAM_DAYS=7
_RECENT_SECONDS=1800
_LOCK=threading.RLock()
_RECENT={}
_SESSIONS={}
_MAX_SESSIONS=500

_NAMES={
"movement":{
"es":["Despierta el cuerpo","Movimiento suave al comenzar el día","Pausa para hombros y cuello","Camina con atención","Activa las manos","Equilibrio y estabilidad con apoyo","Movilidad de espalda","Estira las piernas con suavidad","Activa el cuerpo sentado","Pausa para las articulaciones","Movimiento consciente","Descanso activo de pantalla","Movilidad de caderas","Respira y mueve los brazos","Pausa para los pies","Recupera tu postura","Movimiento lento y controlado","Activa el cuerpo sin prisa","Camina dentro de casa","Cierra el día con movimiento suave"],
"en":["Wake Up Your Body","Gentle Morning Movement","Shoulder and Neck Break","Mindful Walking","Activate Your Hands","Supported Balance and Stability","Back Mobility","Gentle Leg Stretch","Activate Your Body While Seated","Joint-Friendly Break","Mindful Movement","Active Screen Break","Hip Mobility","Breathe and Move Your Arms","Foot Break","Reset Your Posture","Slow and Controlled Movement","Move Without Rushing","Walk Indoors","End the Day with Gentle Movement"],
"pt":["Desperte o corpo","Movimento suave ao começar o dia","Pausa para ombros e pescoço","Caminhada com atenção","Ative as mãos","Equilíbrio e estabilidade com apoio","Mobilidade das costas","Alongue as pernas suavemente","Ative o corpo sentado","Pausa para as articulações","Movimento consciente","Pausa ativa das telas","Mobilidade dos quadris","Respire e mova os braços","Pausa para os pés","Recupere a postura","Movimento lento e controlado","Ative o corpo sem pressa","Caminhe dentro de casa","Termine o dia com movimento suave"]
},
"calm":{
"es":["Respira y haz una pausa","Suelta la tensión del día","Un momento de tranquilidad","Respiración lenta y cómoda","Descansa la mente","Vuelve al momento presente","Pausa para bajar el ritmo","Relaja el rostro y los hombros","Escucha tu respiración","Recupera tu espacio interior","Pausa consciente entre tareas","Un minuto de silencio y atención","Deja pasar los pensamientos","Descanso mental sin exigencias","Pausa tranquila sentado","Respira antes de continuar","Reconoce cómo te sientes","Haz espacio para la calma","Cierra los ojos si te resulta cómodo","Termina el día con serenidad"],
"en":["Breathe and Take a Pause","Release the Day's Tension","A Moment of Calm","Slow, Comfortable Breathing","Rest Your Mind","Return to the Present Moment","Slow Down for a Moment","Relax Your Face and Shoulders","Listen to Your Breathing","Reconnect with Your Inner Space","Mindful Break Between Tasks","A Quiet Moment of Attention","Let Thoughts Pass","Mental Rest Without Pressure","A Calm Seated Pause","Breathe Before Continuing","Notice How You Feel","Make Room for Calm","Close Your Eyes if Comfortable","End the Day with Calm"],
"pt":["Respire e faça uma pausa","Solte a tensão do dia","Um momento de tranquilidade","Respiração lenta e confortável","Descanse a mente","Volte ao momento presente","Diminua o ritmo por um momento","Relaxe o rosto e os ombros","Escute sua respiração","Recupere seu espaço interior","Pausa consciente entre tarefas","Um momento de silêncio e atenção","Deixe os pensamentos passarem","Descanso mental sem cobranças","Pausa tranquila sentado","Respire antes de continuar","Perceba como você se sente","Abra espaço para a calma","Feche os olhos se for confortável","Termine o dia com serenidade"]
},
"coach":{
"es":["Organiza tu siguiente paso","Empieza con una tarea pequeña","Haz una pausa y elige","Aclara lo que necesitas hoy","Divide una tarea en pasos","Recupera tu atención","Reconoce un avance cotidiano","Crea una rutina sencilla","Elige una prioridad realista","Prepara tu próximo momento","Ordena tus ideas con calma","Practica decir no a una tarea","Haz espacio para lo importante","Revisa tu día sin juzgarte","Elige un hábito pequeño","Recupera el enfoque con una pausa","Planifica sin exigirte demasiado","Pide apoyo cuando lo necesites","Prepara un cierre tranquilo","Elige cómo continuar"],
"en":["Organize Your Next Step","Start with One Small Task","Pause and Choose","Clarify What You Need Today","Break a Task into Steps","Bring Back Your Attention","Notice Everyday Progress","Create a Simple Routine","Choose a Realistic Priority","Prepare for Your Next Moment","Sort Your Thoughts Calmly","Practice Saying No to a Task","Make Room for What Matters","Review Your Day Without Judgment","Choose a Small Habit","Refocus with a Pause","Plan Without Overloading Yourself","Ask for Support When Needed","Prepare a Calm Finish","Choose How to Continue"],
"pt":["Organize seu próximo passo","Comece com uma pequena tarefa","Faça uma pausa e escolha","Esclareça o que precisa hoje","Divida uma tarefa em etapas","Recupere sua atenção","Reconheça um avanço cotidiano","Crie uma rotina simples","Escolha uma prioridade realista","Prepare seu próximo momento","Organize suas ideias com calma","Pratique dizer não a uma tarefa","Abra espaço para o que importa","Revise seu dia sem se julgar","Escolha um pequeno hábito","Recupere o foco com uma pausa","Planeje sem se sobrecarregar","Peça apoio quando precisar","Prepare um encerramento tranquilo","Escolha como continuar"]
}
}

_DESC={
"movement":{
"es":"Actividad cotidiana de movimiento suave, adaptable a tu comodidad y a tu propio ritmo.",
"en":"A gentle everyday movement activity that you can adapt to your comfort and pace.",
"pt":"Atividade cotidiana de movimento suave, adaptável ao seu conforto e ritmo."
},
"calm":{
"es":"Pausa de atención y tranquilidad sin exigencias. Respira de forma cómoda y natural.",
"en":"A mindful pause for calm without pressure. Breathe comfortably and naturally.",
"pt":"Pausa de atenção e tranquilidade sem cobranças. Respire de forma confortável e natural."
},
"coach":{
"es":"Ejercicio práctico para organizar tus decisiones cotidianas y elegir un paso manejable.",
"en":"A practical exercise to organize everyday decisions and choose a manageable next step.",
"pt":"Exercício prático para organizar decisões cotidianas e escolher um próximo passo possível."
}
}

_STEPS={
"movement":{
"es":[
"Busca una posición cómoda y estable. Si lo necesitas, siéntate o utiliza un apoyo firme.",
"Comienza despacio y observa cómo responde tu cuerpo. No fuerces ningún movimiento.",
"Mueve una parte del cuerpo con suavidad, dentro de un rango cómodo.",
"Continúa a tu ritmo y mantén una respiración natural. Descansa cuando lo necesites.",
"Reduce el movimiento poco a poco y vuelve a una posición cómoda.",
"Nota cómo te encuentras. Puedes terminar aquí o continuar con tu día."
],
"en":[
"Find a comfortable, stable position. Sit down or use firm support if needed.",
"Begin slowly and notice how your body responds. Do not force any movement.",
"Move one part of your body gently, within a comfortable range.",
"Continue at your own pace and breathe naturally. Rest whenever you need to.",
"Gradually reduce the movement and return to a comfortable position.",
"Notice how you feel. You can finish here or continue with your day."
],
"pt":[
"Encontre uma posição confortável e estável. Sente-se ou use um apoio firme se precisar.",
"Comece devagar e observe como seu corpo responde. Não force nenhum movimento.",
"Mova uma parte do corpo suavemente, dentro de um limite confortável.",
"Continue no seu ritmo e respire naturalmente. Descanse quando precisar.",
"Reduza o movimento aos poucos e volte a uma posição confortável.",
"Perceba como você está. Pode terminar aqui ou continuar seu dia."
]
},
"calm":{
"es":[
"Adopta una postura cómoda y permite que el cuerpo descanse.",
"Observa tu respiración sin intentar cambiarla ni hacerla más profunda.",
"Dirige la atención a las sensaciones del momento, sin juzgarlas.",
"Si aparecen pensamientos, reconócelos y vuelve con suavidad a tu respiración.",
"Deja que el ritmo se mantenga cómodo. No necesitas lograr una sensación especial.",
"Termina a tu ritmo y observa cómo te sientes antes de continuar."
],
"en":[
"Choose a comfortable posture and allow your body to rest.",
"Notice your breathing without trying to change it or make it deeper.",
"Bring your attention to present sensations without judging them.",
"If thoughts appear, acknowledge them and gently return to your breathing.",
"Let your breathing remain comfortable. You do not need to achieve a special feeling.",
"Finish at your own pace and notice how you feel before continuing."
],
"pt":[
"Escolha uma postura confortável e permita que o corpo descanse.",
"Observe sua respiração sem tentar mudá-la nem torná-la mais profunda.",
"Leve a atenção às sensações do momento, sem julgá-las.",
"Se surgirem pensamentos, reconheça-os e volte suavemente à respiração.",
"Deixe o ritmo continuar confortável. Você não precisa alcançar uma sensação especial.",
"Termine no seu ritmo e perceba como está antes de continuar."
]
},
"coach":{
"es":[
"Detente un momento y piensa qué necesitas atender ahora, sin exigirte resolverlo todo.",
"Elige una sola situación o tarea concreta en la que quieras centrarte.",
"Describe el siguiente paso con palabras sencillas y realistas.",
"Si parece demasiado grande, divídelo en una acción más pequeña.",
"Decide cuándo o dónde podrías dar ese paso. Ajusta el plan a tu día real.",
"Resume tu elección y reconoce que puedes revisarla cuando lo necesites."
],
"en":[
"Pause and consider what needs your attention now, without expecting yourself to solve everything.",
"Choose one specific situation or task to focus on.",
"Describe the next step in simple, realistic words.",
"If it feels too big, break it into a smaller action.",
"Decide when or where you could take that step. Fit the plan to your actual day.",
"Summarize your choice and remember that you can revise it whenever needed."
],
"pt":[
"Pare por um momento e pense no que precisa de atenção agora, sem exigir resolver tudo.",
"Escolha uma situação ou tarefa específica para focar.",
"Descreva o próximo passo com palavras simples e realistas.",
"Se parecer grande demais, divida em uma ação menor.",
"Decida quando ou onde poderá dar esse passo. Ajuste o plano ao seu dia real.",
"Resuma sua escolha e lembre-se de que pode revê-la quando precisar."
]
}
}

_SECTION_LABELS={
"es":{"all":"Todas las actividades","movement":"Movimiento","calm":"Calma","coach":"Rutinas cotidianas"},
"en":{"all":"All activities","movement":"Movement","calm":"Calm","coach":"Everyday routines"},
"pt":{"all":"Todas as atividades","movement":"Movimento","calm":"Calma","coach":"Rotinas cotidianas"}
}

_PROGRAM={
"es":[
("Empezar con calma","Elige una actividad sencilla y observa cómo te encuentras."),
("Moverte a tu ritmo","Haz una pausa de movimiento suave que puedas adaptar."),
("Respirar con atención","Reserva unos minutos para descansar y observar tu respiración."),
("Ordenar una prioridad","Escoge una tarea pequeña que tenga sentido para ti."),
("Crear una pausa cotidiana","Identifica un momento realista del día para hacer una pausa."),
("Reconocer lo que funciona","Observa qué actividad te resultó cómoda y qué podrías ajustar."),
("Elegir cómo continuar","Selecciona una práctica que quieras repetir o modificar.")
],
"en":[
("Begin Calmly","Choose a simple activity and notice how you feel."),
("Move at Your Own Pace","Take a gentle movement break that you can adapt."),
("Breathe Mindfully","Set aside a few minutes to rest and notice your breathing."),
("Organize One Priority","Choose a small task that matters to you."),
("Create an Everyday Pause","Identify a realistic moment in your day for a pause."),
("Notice What Works","Consider which activity felt comfortable and what you might adjust."),
("Choose How to Continue","Select a practice you would like to repeat or adapt.")
],
"pt":[
("Comece com calma","Escolha uma atividade simples e perceba como você está."),
("Movimente-se no seu ritmo","Faça uma pausa de movimento suave que possa adaptar."),
("Respire com atenção","Reserve alguns minutos para descansar e observar sua respiração."),
("Organize uma prioridade","Escolha uma pequena tarefa que faça sentido para você."),
("Crie uma pausa cotidiana","Identifique um momento realista do dia para fazer uma pausa."),
("Reconheça o que funciona","Observe qual atividade foi confortável e o que pode ajustar."),
("Escolha como continuar","Selecione uma prática que deseja repetir ou adaptar.")
]
}

def _lang(lang):
    return lang if lang in LANGUAGES else "es"

def _section(section):
    if section in SECTIONS:
        return section
    aliases={
        "pause":"calm","energy":"movement","nature":"calm",
        "program":"coach","routine":"coach","daily":"coach"
    }
    return aliases.get(str(section or "").lower(),"coach")

def _duration(minutes):
    try:
        value=int(minutes)
    except (TypeError,ValueError):
        value=3
    return min(MINUTES_ALLOWED,key=lambda n:abs(n-value))

def _make_catalog():
    result=[]
    for section in SECTIONS:
        for i,title in enumerate(_NAMES[section]["es"],1):
            aid=f"{section}_{i:02d}"
            titles={lang:_NAMES[section][lang][i-1] for lang in LANGUAGES}
            descriptions={lang:_DESC[section][lang] for lang in LANGUAGES}
            result.append({
                "id":aid,
                "kind":section,
                "section":section,
                "title":titles,
                "name":titles,
                "description":descriptions,
                "duration_options":list(MINUTES_ALLOWED),
                "minutes":5,
                "steps":{lang:list(_STEPS[section][lang]) for lang in LANGUAGES},
                "plant_id":None
            })
    return result

_CATALOG=_make_catalog()
_BY_ID={item["id"]:item for item in _CATALOG}

def get_catalog(lang="es"):
    lang=_lang(lang)
    return {
        "language":lang,
        "sections":[
            {"id":s,"name":_SECTION_LABELS[lang][s],
             "count":sum(1 for a in _CATALOG if a["section"]==s)}
            for s in ("all",)+SECTIONS
        ],
        "durations":list(MINUTES_ALLOWED),
        "program_days":PROGRAM_DAYS
    }

def get_activities(lang="es",section="all"):
    lang=_lang(lang)
    section=section if section in ("all",)+SECTIONS else "all"
    result=[]
    for item in _CATALOG:
        if section!="all" and item["section"]!=section:
            continue
        result.append({
            "id":item["id"],
            "kind":item["kind"],
            "section":item["section"],
            "title":item["title"][lang],
            "name":item["name"][lang],
            "description":item["description"][lang],
            "minutes":item["minutes"],
            "duration_options":list(MINUTES_ALLOWED),
            "steps":list(item["steps"][lang])
        })
    return result

def get_activity(activity_id,lang="es"):
    lang=_lang(lang)
    item=_BY_ID.get(str(activity_id))
    if not item:
        return None
    return {
        "id":item["id"],
        "kind":item["kind"],
        "section":item["section"],
        "title":item["title"][lang],
        "name":item["name"][lang],
        "description":item["description"][lang],
        "minutes":item["minutes"],
        "duration_options":list(MINUTES_ALLOWED),
        "steps":list(item["steps"][lang])
    }

def get_plant(plant_id,lang="es"):
    return None

def _section_for_kind(kind):
    return _section(kind)

def _choose_activity(section,allow_repeat=False):
    section=_section(section)
    now=datetime.now(timezone.utc).timestamp()
    with _LOCK:
        expired=[key for key,stamp in _RECENT.items() if now-stamp>_RECENT_SECONDS]
        for key in expired:
            _RECENT.pop(key,None)
        choices=[a for a in _CATALOG if a["section"]==section]
        if not allow_repeat:
            fresh=[a for a in choices if now-_RECENT.get(a["id"],0)>_RECENT_SECONDS]
            if fresh:
                choices=fresh
        chosen=random.choice(choices)
        _RECENT[chosen["id"]]=now
        return chosen

def create_session_id(activity_id=None):
    seed=f"{activity_id or ''}|{datetime.now(timezone.utc).isoformat()}|{random.random()}"
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:24]

def _remember_session(session_data):
    with _LOCK:
        _SESSIONS[session_data["session_id"]]=deepcopy(session_data)
        while len(_SESSIONS)>_MAX_SESSIONS:
            _SESSIONS.pop(next(iter(_SESSIONS)))
    return session_data

def get_session(lang="es",kind="pause",minutes=3,allow_repeat=False,activity_id=None):
    lang=_lang(lang)
    duration=_duration(minutes)
    section=_section(kind)
    chosen=_BY_ID.get(str(activity_id)) if activity_id else None
    if chosen and chosen["section"]!=section:
        section=chosen["section"]
    if not chosen:
        chosen=_choose_activity(section,allow_repeat=allow_repeat)
    steps=list(chosen["steps"][lang])
    seconds=duration*60
    step_seconds=seconds/len(steps)
    session_id=create_session_id(chosen["id"])
    session_data={
        "session_id":session_id,
        "id":chosen["id"],
        "kind":chosen["kind"],
        "section":chosen["section"],
        "language":lang,
        "title":chosen["title"][lang],
        "name":chosen["name"][lang],
        "description":chosen["description"][lang],
        "minutes":duration,
        "duration_minutes":duration,
        "duration_seconds":seconds,
        "prompt_interval_seconds":PROMPT_INTERVAL_SECONDS,
        "step_seconds":step_seconds,
        "steps":steps,
        "instructions":steps,
        "total_steps":len(steps),
        "allow_repeat":bool(allow_repeat),
        "created_at":datetime.now(timezone.utc).isoformat(),
        "voice_text":steps[0] if steps else "",
        "voice_language":{"es":"es-ES","en":"en-US","pt":"pt-PT"}[lang],
        "safety_note":{
            "es":"Adapta la actividad a tu comodidad. No fuerces movimientos ni la respiración; detente si sientes dolor, mareo o malestar.",
            "en":"Adapt the activity to your comfort. Do not force movement or breathing; stop if you feel pain, dizziness, or discomfort.",
            "pt":"Adapte a atividade ao seu conforto. Não force movimentos nem a respiração; pare se sentir dor, tontura ou desconforto."
        }[lang]
    }
    return _remember_session(session_data)

def get_session_by_id(session_id):
    with _LOCK:
        value=_SESSIONS.get(str(session_id))
        return deepcopy(value) if value else None

def get_program_day(lang="es",day=1):
    lang=_lang(lang)
    try:
        day=int(day)
    except (TypeError,ValueError):
        day=1
    day=max(1,min(PROGRAM_DAYS,day))
    title,goal=_PROGRAM[lang][day-1]
    section=("calm","movement","calm","coach","coach","movement","coach")[day-1]
    chosen=_choose_activity(section,allow_repeat=True)
    activity=get_activity(chosen["id"],lang)
    return {
        "day":day,
        "total_days":PROGRAM_DAYS,
        "language":lang,
        "title":title,
        "goal":goal,
        "description":goal,
        "section":section,
        "activity":activity,
        "minutes":5,
        "duration_options":list(MINUTES_ALLOWED)
    }

def get_health():
    return {
        "status":"ok",
        "app":APP_NAME,
        "version":VERSION,
        "timestamp":datetime.now(timezone.utc).isoformat(),
        "activities":len(_CATALOG),
        "languages":list(LANGUAGES),
        "durations":list(MINUTES_ALLOWED),
        "program_days":PROGRAM_DAYS
    }

def get_config():
    return {
        "name":APP_NAME,
        "company":COMPANY,
        "version":VERSION,
        "audience":AUDIENCE,
        "languages":list(LANGUAGES),
        "durations":list(MINUTES_ALLOWED),
        "program_days":PROGRAM_DAYS,
        "sections":get_catalog("es")["sections"],
        "activity_count":len(_CATALOG),
        "prompt_interval_seconds":PROMPT_INTERVAL_SECONDS
    }

catalog=get_catalog
activities=get_activities
activity=get_activity
plant=get_plant
session=get_session
program_day=get_program_day
health=get_health
config=get_config
