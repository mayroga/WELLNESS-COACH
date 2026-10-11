from copy import deepcopy
import random
import math

VERSION="5.0.1"
PROMPT_INTERVAL_SECONDS=4.5
MINUTES_MIN=3
MINUTES_MAX=10

SECTIONS={
"plants":{"es":"Plantas y naturaleza","en":"Plants and nature"},
"movement":{"es":"Energía y movimiento","en":"Energy and movement"},
"calm":{"es":"Calma y atención","en":"Calm and mindfulness"},
"coach":{"es":"Mi coach de bienestar","en":"My wellness coach"}}

# id, categoría, título ES, título EN, enfoque ES, enfoque EN
ACTIVITY_DEFS=[
("p01","plants","Mira una planta con atención","Observe a plant closely","una planta","a plant"),
("p02","plants","Descubre una hierba aromática","Discover an aromatic herb","una hierba aromática","an aromatic herb"),
("p03","plants","Una ventana hacia la naturaleza","A window into nature","el paisaje exterior","the outdoor view"),
("p04","plants","Colores que te rodean","Colors around you","los colores del entorno","the colors around you"),
("p05","plants","Escucha el paisaje","Listen to the landscape","los sonidos del entorno","the sounds around you"),
("p06","plants","Pequeño rincón verde","A small green corner","un rincón natural","a natural corner"),
("p07","plants","Formas de las hojas","Leaf shapes","las formas de las hojas","leaf shapes"),
("p08","plants","Detalles de una flor","Details of a flower","los detalles de una flor","the details of a flower"),
("p09","plants","Observa las ramas","Observe the branches","las ramas de un árbol","tree branches"),
("p10","plants","Luz y sombra natural","Natural light and shadow","la luz y la sombra","light and shadow"),
("p11","plants","Nubes en movimiento","Moving clouds","las nubes","the clouds"),
("p12","plants","Texturas de la naturaleza","Textures in nature","las texturas naturales","natural textures"),
("p13","plants","Un jardín imaginado","An imagined garden","un jardín imaginario","an imagined garden"),
("p14","plants","Pequeños cambios del paisaje","Small changes in the landscape","los cambios del paisaje","changes in the landscape"),
("p15","plants","El color del cielo","The color of the sky","el color del cielo","the color of the sky"),
("p16","plants","Agua y reflejos","Water and reflections","el agua y sus reflejos","water and its reflections"),
("p17","plants","Un árbol cercano","A nearby tree","un árbol cercano","a nearby tree"),
("p18","plants","Naturaleza en una fotografía","Nature in a photograph","una fotografía natural","a nature photograph"),
("p19","plants","Cuida una planta con seguridad","Care for a plant safely","el cuidado de una planta","plant care"),
("p20","plants","Encuentra un detalle natural","Find a natural detail","un detalle natural","a natural detail"),
("m01","movement","Despierta los hombros","Wake up your shoulders","los hombros","the shoulders"),
("m02","movement","Manos más despiertas","Wake up your hands","las manos","the hands"),
("m03","movement","Activa los tobillos","Move your ankles","los tobillos","the ankles"),
("m04","movement","Cambia de postura","Change your posture","la postura","posture"),
("m05","movement","Paseo consciente y seguro","A mindful, safe walk","un paseo seguro","a safe walk"),
("m06","movement","Estiramiento de brazos adaptable","An adaptable arm stretch","los brazos","the arms"),
("m07","movement","Abre y relaja las manos","Open and relax your hands","las manos abiertas","open hands"),
("m08","movement","Descansa la espalda","Give your back a rest","la espalda","the back"),
("m09","movement","Movimiento suave de cuello","Gentle neck movement","el cuello","the neck"),
("m10","movement","Eleva suavemente los talones","Gently lift your heels","los talones","the heels"),
("m11","movement","Extiende una pierna sentado","Extend one leg while seated","una pierna sentado","one leg while seated"),
("m12","movement","Activa los dedos de los pies","Move your toes","los dedos de los pies","the toes"),
("m13","movement","Coordina manos y mirada","Coordinate hands and eyes","las manos y la mirada","hands and eyes"),
("m14","movement","Balanceo cómodo de brazos","Comfortable arm swings","el balanceo de brazos","arm swings"),
("m15","movement","Pausa para cambiar de posición","A posture-change break","el cambio de posición","a posture change"),
("m16","movement","Movimiento lateral de manos","Move your hands sideways","las manos hacia los lados","hands moving sideways"),
("m17","movement","Despierta los dedos","Wake up your fingers","los dedos","the fingers"),
("m18","movement","Marcha suave sentado","Gentle seated marching","la marcha sentado","seated marching"),
("m19","movement","Estira sin forzar","Stretch without forcing","un estiramiento suave","a gentle stretch"),
("m20","movement","Termina en una postura cómoda","Finish in a comfortable posture","una postura cómoda","a comfortable posture"),
("c01","calm","Una pausa sin exigencias","A pause without demands","una pausa tranquila","a quiet pause"),
("c02","calm","Los cinco sentidos","The five senses","los sentidos","the senses"),
("c03","calm","Reconoce algo que valoras","Notice something you value","algo cotidiano que valoras","something you value"),
("c04","calm","Imagina un lugar agradable","Picture a pleasant place","un lugar agradable","a pleasant place"),
("c05","calm","Suelta una tarea de la mente","Set one task aside","una tarea pendiente","a pending task"),
("c06","calm","Escucha una canción con atención","Listen to a song attentively","una canción","a song"),
("c07","calm","Observa sin juzgar","Observe without judging","lo que tienes delante","what is in front of you"),
("c08","calm","Regresa al momento presente","Return to the present","el momento presente","the present moment"),
("c09","calm","Descanso para la mirada","A rest for your eyes","la mirada","your gaze"),
("c10","calm","Un sonido a la vez","One sound at a time","un sonido","one sound"),
("c11","calm","Respiración natural","Natural breathing","la respiración natural","natural breathing"),
("c12","calm","Siente el apoyo de la silla","Feel the chair supporting you","el apoyo de la silla","the support of the chair"),
("c13","calm","Ordena el espacio visual","Organize your visual space","el espacio que ves","the space you see"),
("c14","calm","Una imagen de tranquilidad","An image of calm","una imagen tranquila","a calm image"),
("c15","calm","Haz una pausa sensorial","Take a sensory pause","una pausa sensorial","a sensory pause"),
("c16","calm","Observa cómo cambia la luz","Notice changing light","los cambios de luz","changes in light"),
("c17","calm","Deja pasar un pensamiento","Let a thought pass","un pensamiento","a thought"),
("c18","calm","Elige un detalle agradable","Choose a pleasant detail","un detalle agradable","a pleasant detail"),
("c19","calm","Baja el ritmo sin prisa","Slow down without rushing","un ritmo más tranquilo","a calmer pace"),
("c20","calm","Cierra la pausa a tu manera","End the pause your way","el cierre de la pausa","the end of the pause"),
("w01","coach","Elige tu prioridad de hoy","Choose today's priority","tu prioridad de hoy","today's priority"),
("w02","coach","Revisa lo que ya lograste","Notice what you have already done","un logro real","a real accomplishment"),
("w03","coach","Prepara un plan sencillo","Make a simple plan","un plan sencillo","a simple plan"),
("w04","coach","Practica una decisión pequeña","Practice a small decision","una decisión cotidiana","an everyday decision"),
("w05","coach","Protege un espacio para ti","Protect a little time for yourself","un espacio para ti","time for yourself"),
("w06","coach","Háblate con respeto","Speak to yourself with respect","un mensaje respetuoso","a respectful message"),
("w07","coach","Divide una tarea en pasos","Break a task into steps","una tarea grande","a large task"),
("w08","coach","Define qué significa terminar","Define what finished means","el resultado esperado","the expected result"),
("w09","coach","Prepara lo que necesitas","Prepare what you need","los recursos necesarios","the resources you need"),
("w10","coach","Elige un primer paso posible","Choose a possible first step","el primer paso","the first step"),
("w11","coach","Revisa tu tiempo disponible","Review your available time","el tiempo disponible","the time available"),
("w12","coach","Pide ayuda concreta si hace falta","Ask for specific help if needed","una ayuda concreta","specific help"),
("w13","coach","Aprende de una experiencia","Learn from an experience","una experiencia reciente","a recent experience"),
("w14","coach","Reconoce una habilidad propia","Recognize a skill you have","una habilidad propia","a skill you have"),
("w15","coach","Haz espacio para descansar","Make room for rest","un descanso posible","a possible break"),
("w16","coach","Simplifica una elección","Simplify a choice","una elección difícil","a difficult choice"),
("w17","coach","Revisa lo que puedes controlar","Review what you can control","lo que puedes controlar","what you can control"),
("w18","coach","Elige una acción realista","Choose a realistic action","una acción realista","a realistic action"),
("w19","coach","Prepara el siguiente momento","Prepare for the next moment","el siguiente momento","the next moment"),
("w20","coach","Reconoce tu esfuerzo de hoy","Recognize today's effort","tu esfuerzo de hoy","your effort today")
]

# Cada sección contiene directamente las listas ES y EN.
# Cada lista contiene 20 indicaciones.
PROMPT_TEMPLATES={
"plants":{
"es":[
"Observa {f} durante unos segundos.","Busca una forma que destaque en {f}.","Encuentra un detalle pequeño en {f}.","Compara dos partes de {f}.","Nota un cambio de color en {f}.","Mira {f} desde otro ángulo seguro.","Elige una parte de {f} y descríbela.","Busca una línea o curva en {f}.","Identifica una zona clara en {f}.","Encuentra una zona oscura en {f}.","Observa qué queda cerca de {f}.","Fíjate en el fondo que rodea {f}.","Elige una palabra para describir {f}.","Mira {f} sin apresurarte.","Descubre algo nuevo en {f}.","Compara lo grande y lo pequeño en {f}.","Observa la luz que alcanza {f}.","Escoge tu detalle favorito de {f}.","Recuerda un detalle que viste en {f}.","Vuelve a mirar {f} una última vez."
],
"en":[
"Observe {f} for a few seconds.","Find a shape that stands out in {f}.","Notice one small detail in {f}.","Compare two parts of {f}.","Notice a color change in {f}.","View {f} from another safe angle.","Choose one part of {f} and describe it.","Find a line or curve in {f}.","Identify a bright area in {f}.","Find a darker area in {f}.","Notice what is near {f}.","Look at the background around {f}.","Choose one word to describe {f}.","Look at {f} without rushing.","Discover something new in {f}.","Compare large and small details in {f}.","Notice the light reaching {f}.","Choose your favorite detail in {f}.","Recall one detail you saw in {f}.","Take one final look at {f}."
]},
"movement":{
"es":[
"Busca una postura estable antes de mover {f}.","Haz un movimiento pequeño con {f}, si resulta cómodo.","Reduce el recorrido de {f} si lo necesitas.","Mueve {f} despacio y sin rebotes.","Haz una pausa y relaja {f}.","Comprueba si {f} está cómodo.","Cambia suavemente la posición de {f}.","Deja que {f} descanse un momento.","Repite el movimiento solo si te resulta cómodo.","Mantén el movimiento dentro de un rango natural.","Evita forzar {f}.","Respira con normalidad mientras mueves {f}.","Detente si aparece dolor o mareo.","Busca apoyo estable antes de continuar.","Haz el movimiento más pequeño si lo prefieres.","Regresa lentamente a la posición inicial.","Compara cómo se siente {f} al descansar.","Elige la opción más cómoda para {f}.","Termina el movimiento sin prisa.","Quédate en una postura segura y cómoda."
],
"en":[
"Find a stable position before moving {f}.","Make a small movement with {f}, if comfortable.","Use a smaller range for {f} if needed.","Move {f} slowly, without bouncing.","Pause and relax {f}.","Check whether {f} feels comfortable.","Gently change the position of {f}.","Let {f} rest for a moment.","Repeat only if the movement feels comfortable.","Keep the movement within a natural range.","Do not force {f}.","Breathe normally while moving {f}.","Stop if you feel pain or dizziness.","Find stable support before continuing.","Make the movement smaller if you prefer.","Slowly return to the starting position.","Notice how {f} feels while resting.","Choose the most comfortable option for {f}.","Finish the movement without rushing.","Stay in a safe, comfortable position."
]},
"calm":{
"es":[
"Dirige suavemente la atención hacia {f}.","Observa {f} sin intentar cambiarlo.","Nombra mentalmente un detalle de {f}.","Permite que {f} esté como está.","Vuelve a {f} cuando te distraigas.","No necesitas hacerlo perfectamente con {f}.","Dedica unos segundos a {f}.","Nota qué es sencillo de reconocer en {f}.","Deja pasar cualquier pensamiento y vuelve a {f}.","Elige una palabra neutral para {f}.","Mira o escucha {f} a tu propio ritmo.","Relaja la mandíbula si te resulta cómodo.","Deja caer los hombros sin forzarlos.","Respira como lo haces normalmente.","Siente el apoyo de la superficie bajo tu cuerpo.","Observa un detalle presente en {f}.","No hace falta sentir algo especial con {f}.","Permite que la atención vuelva a {f}.","Agradece este breve momento de pausa.","Termina observando {f} una vez más."
],
"en":[
"Direct your attention gently toward {f}.","Notice {f} without trying to change it.","Silently name one detail of {f}.","Allow {f} to be just as it is.","Return to {f} when your mind wanders.","You do not need to do {f} perfectly.","Spend a few seconds with {f}.","Notice what is easy to recognize in {f}.","Let a thought pass, then return to {f}.","Choose a neutral word for {f}.","Look at or listen to {f} at your own pace.","Relax your jaw if that feels comfortable.","Let your shoulders drop without forcing them.","Breathe in your usual, natural way.","Feel the surface supporting your body.","Notice one detail present in {f}.","You do not need to feel anything special about {f}.","Allow your attention to return to {f}.","Appreciate this brief moment of pause.","Finish by noticing {f} one more time."
]},
"coach":{
"es":[
"Define un resultado concreto para {f}.","Identifica el primer paso de {f}.","Piensa qué necesitas preparar para {f}.","Reduce {f} a una acción que puedas explicar.","Decide cuándo revisarás {f}.","Elige una opción realista para {f}.","Separa lo urgente de lo que puede esperar en {f}.","Nombra un obstáculo práctico de {f}.","Busca una forma sencilla de facilitar {f}.","Comprueba si el tiempo para {f} es realista.","Decide qué significa completar {f}.","Elige un recurso que ayude con {f}.","Si hace falta, piensa a quién pedir ayuda con {f}.","Evita intentar resolver todo {f} a la vez.","Haz que el primer paso de {f} sea pequeño.","Revisa qué parte de {f} depende de ti.","Escoge una fecha o momento para {f}.","Imagina cómo comprobarás el avance de {f}.","Ajusta {f} si las circunstancias cambian.","Resume tu siguiente acción para {f}."
],
"en":[
"Define a concrete result for {f}.","Identify the first step for {f}.","Think about what you need to prepare for {f}.","Reduce {f} to an action you can explain.","Decide when you will review {f}.","Choose a realistic option for {f}.","Separate urgent parts from what can wait in {f}.","Name one practical obstacle to {f}.","Find a simple way to make {f} easier.","Check whether the time for {f} is realistic.","Decide what completing {f} means.","Choose a resource that can help with {f}.","If needed, decide whom to ask for help with {f}.","Avoid trying to solve all of {f} at once.","Make the first step for {f} small.","Review which part of {f} you can control.","Choose a date or time for {f}.","Picture how you will check progress on {f}.","Adjust {f} if circumstances change.","Summarize your next action for {f}."
]}}

# Comprueba la estructura antes de generar el catálogo.
for _section in SECTIONS:
    if _section not in PROMPT_TEMPLATES:
        raise ValueError(f"Falta la sección de plantillas: {_section}")
    for _lang in ("es","en"):
        if _lang not in PROMPT_TEMPLATES[_section]:
            raise ValueError(f"Falta el idioma {_lang} en {_section}")
        if len(PROMPT_TEMPLATES[_section][_lang])!=20:
            raise ValueError(f"La sección {_section}, idioma {_lang}, debe tener 20 plantillas")
        if any("{f}" not in _template for _template in PROMPT_TEMPLATES[_section][_lang]):
            raise ValueError(f"Hay una plantilla sin el marcador {{f}} en {_section}/{_lang}")

def _make_steps(section,focus_es,focus_en,lang):
    lang=lang if lang in ("es","en") else "es"
    focus=focus_es if lang=="es" else focus_en
    templates=PROMPT_TEMPLATES[section][lang]
    return [template.format(f=focus) for template in templates]

def _description(section,focus_es,focus_en,lang):
    focus=focus_es if lang=="es" else focus_en
    if section=="plants":
        return (f"Observa {focus} con curiosidad y sin prisa. Puedes usar algo real o una imagen; no necesitas tocar ni ingerir ninguna planta." if lang=="es" else f"Observe {focus} with curiosity and without rushing. Use a real object or a picture; you do not need to touch or ingest any plant.")
    if section=="movement":
        return (f"Una actividad adaptable centrada en {focus}. Haz únicamente los movimientos que te resulten cómodos y seguros; puedes permanecer sentado." if lang=="es" else f"An adaptable activity focused on {focus}. Do only movements that feel comfortable and safe; you can remain seated.")
    if section=="calm":
        return (f"Una pausa breve para prestar atención a {focus}, sin exigirte un resultado ni cambiar cómo te sientes." if lang=="es" else f"A short pause to pay attention to {focus}, without demanding a result or trying to change how you feel.")
    return (f"Una práctica concreta para organizar {focus} en pasos sencillos, realistas y manejables." if lang=="es" else f"A practical exercise to organize {focus} into simple, realistic, manageable steps.")

# RAW conserva la estructura de ocho elementos.
RAW=[]
for aid,section,title_es,title_en,focus_es,focus_en in ACTIVITY_DEFS:
    desc_es=_description(section,focus_es,focus_en,"es")
    desc_en=_description(section,focus_es,focus_en,"en")
    steps_es=_make_steps(section,focus_es,focus_en,"es")
    steps_en=_make_steps(section,focus_es,focus_en,"en")
    RAW.append((aid,section,title_es,title_en,desc_es,desc_en,steps_es,steps_en))

RAW_BY_ID={item[0]:item for item in RAW}
SECTION_KIND={"plants":"nature","movement":"energy","calm":"calm","coach":"coach"}

def _normalize_lang(lang):
    return lang if lang in ("es","en") else "es"

def _normalize_minutes(minutes,default=3):
    try:
        value=int(minutes)
    except (TypeError,ValueError,OverflowError):
        value=default
    return max(MINUTES_MIN,min(MINUTES_MAX,value))

def _activity(raw,lang="es"):
    lang=_normalize_lang(lang)
    aid,section,title_es,title_en,desc_es,desc_en,steps_es,steps_en=raw
    return {
        "id":aid,
        "section":section,
        "kind":SECTION_KIND[section],
        "minutes":5,
        "title":title_es if lang=="es" else title_en,
        "description":desc_es if lang=="es" else desc_en,
        "steps":deepcopy(steps_es if lang=="es" else steps_en),
        "language":lang,
        "step_count":20,
        "prompt_interval_seconds":PROMPT_INTERVAL_SECONDS
    }

def get_catalog():
    return [
        {"id":key,"title":value["es"],"title_en":value["en"],
         "count":sum(1 for activity in RAW if activity[1]==key)}
        for key,value in SECTIONS.items()
    ]

def get_activities(lang="es",section="all"):
    lang=_normalize_lang(lang)
    valid_sections=set(SECTIONS)|{"all"}
    section=section if section in valid_sections else "all"
    return [_activity(a,lang) for a in RAW if section=="all" or a[1]==section]

def _session_pool(base,lang):
    section=base[1]
    same_section=[a for a in RAW if a[1]==section and a[0]!=base[0]]
    random.SystemRandom().shuffle(same_section)
    selected=[base]+same_section[:6]
    pool=[]
    for raw in selected:
        activity=_activity(raw,lang)
        for index,phrase in enumerate(activity["steps"]):
            pool.append({
                "text":phrase,
                "activity_id":raw[0],
                "activity_title":activity["title"],
                "prompt_number":index+1
            })
    unique={}
    for prompt in pool:
        key=" ".join(prompt["text"].casefold().split())
        if key not in unique:
            unique[key]=prompt
    result=list(unique.values())
    random.SystemRandom().shuffle(result)
    return result,selected

def get_session(lang="es",kind="pause",minutes=3):
    lang=_normalize_lang(lang)
    minutes=_normalize_minutes(minutes)
    mapping={
        "pause":"c01","energy":"m01","calm":"c02",
        "nature":"p01","coach":"w01","program":"w02"
    }
    base=RAW_BY_ID[mapping.get(kind,"c01")]
    pool,selected=_session_pool(base,lang)
    target=max(1,math.ceil(minutes*60/PROMPT_INTERVAL_SECONDS))
    steps=[p["text"] for p in pool[:target]]
    if len(steps)<target:
        used=set(steps)
        remaining=[p["text"] for p in pool if p["text"] not in used]
        steps.extend(remaining[:target-len(steps)])
    activity=_activity(base,lang)
    activity.update({
        "minutes":minutes,
        "steps":steps,
        "step_count":len(steps),
        "prompt_interval_seconds":PROMPT_INTERVAL_SECONDS,
        "unique_prompts":len(set(steps))==len(steps),
        "session_activities":[
            {"id":a[0],"title":a[2] if lang=="es" else a[3]}
            for a in selected
        ],
        "session_mode":"guided",
        "measurement":{
            "tracks_active_time":True,
            "tracks_completed_sessions":True,
            "tracks_prompt_count":True,
            "tracks_user_rating":True,
            "uses_physical_sensors":False
        }
    })
    return activity

PLANTS={
"mint":{
"es":("Menta","Mentha spp.","Hierba aromática utilizada en alimentos e infusiones.","Observa la forma y el aroma sin ingerirla.","Puede empeorar el reflujo en algunas personas. No ingieras aceites esenciales."),
"en":("Mint","Mentha spp.","An aromatic herb used in foods and infusions.","Observe its shape and scent without ingesting it.","It may worsen reflux for some people. Do not ingest essential oils.")
},
"chamomile":{
"es":("Manzanilla","Matricaria chamomilla","Se consume tradicionalmente como infusión.","Observa los detalles de una flor.","Puede provocar alergias, especialmente en personas sensibles a la familia Asteraceae."),
"en":("Chamomile","Matricaria chamomilla","Traditionally consumed as an infusion.","Notice the details of a flower.","It may cause allergies, especially in people sensitive to Asteraceae plants.")
},
"rosemary":{
"es":("Romero","Salvia rosmarinus","Hierba aromática utilizada en cocina y jardinería.","Observa sus hojas y su forma.","No ingieras aceite esencial y evita el contacto con los ojos."),
"en":("Rosemary","Salvia rosmarinus","An aromatic herb used in cooking and gardening.","Observe its leaves and shape.","Do not ingest essential oil and avoid eye contact.")
}}

def get_plant(plant_id,lang="es"):
    lang=_normalize_lang(lang)
    if plant_id not in PLANTS:
        return None
    p=PLANTS[plant_id][lang]
    return {
        "id":plant_id,
        "name":p[0],
        "scientific":p[1],
        "traditional":p[2],
        "activity":p[3],
        "caution":p[4],
        "language":lang
    }

PROGRAM=[
("Comienza con una pausa","Begin with a pause","c01",3),
("Observa la naturaleza","Observe nature","p03",5),
("Mueve el cuerpo con suavidad","Move gently","m01",3),
("Vuelve al presente","Return to the present","c02",5),
("Descubre una planta","Discover a plant","p02",5),
("Elige una prioridad","Choose a priority","w01",3),
("Repasa lo que te resultó útil","Review what helped","w02",5)
]

def get_program_day(lang="es",day=1):
    lang=_normalize_lang(lang)
    try:
        day=int(day)
    except (TypeError,ValueError,OverflowError):
        day=1
    day=max(1,min(7,day))
    title_es,title_en,activity_id,minutes=PROGRAM[day-1]
    activity=_activity(RAW_BY_ID[activity_id],lang)
    activity["minutes"]=minutes
    return {
        "day":day,
        "title":title_es if lang=="es" else title_en,
        "goal":activity["description"],
        "kind":activity["kind"],
        "minutes":minutes,
        "activity":activity
    }

def get_metrics():
    return {
        "engine_version":VERSION,
        "total_activities":len(RAW),
        "activities_by_section":{
            section:sum(1 for item in RAW if item[1]==section)
            for section in SECTIONS
        },
        "languages":["es","en"],
        "steps_per_activity":20,
        "prompt_interval_seconds":PROMPT_INTERVAL_SECONDS,
        "max_session_minutes":MINUTES_MAX
    }
