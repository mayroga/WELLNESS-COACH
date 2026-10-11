from __future__ import annotations
import os,random,time,datetime,hashlib,threading
from copy import deepcopy

VERSION="5.0.0"
APP_NAME="WELLNESS COACH"
COMPANY="May Roga LLC"
PROMPT_INTERVAL_SECONDS=4.5
MINUTES_ALLOWED=(3,5,10)
LANGUAGES=("es","en")
SECTIONS=("plants","movement","calm","coach")
_lock=threading.RLock()
_rng=random.SystemRandom()

# Actividades de bienestar general. No son tratamientos ni diagnósticos.
PLANTS={
"p01":{"name":{"es":"Manzanilla","en":"Chamomile"},"scientific":"Matricaria chamomilla","use":{"es":"Planta aromática utilizada tradicionalmente en infusiones.","en":"An aromatic plant traditionally used in infusions."},"observation":{"es":"Observa los detalles de una flor sin arrancarla.","en":"Notice the details of a flower without picking it."},"precautions":{"es":"Puede causar alergias. No ingieras aceites esenciales.","en":"It may cause allergies. Do not ingest essential oils."}},
"p02":{"name":{"es":"Menta","en":"Mint"},"scientific":"Mentha spp.","use":{"es":"Hierba aromática utilizada en alimentos y jardinería.","en":"An aromatic herb used in food and gardening."},"observation":{"es":"Observa la forma de sus hojas y, si es apropiado, su aroma.","en":"Notice the shape of its leaves and, if appropriate, its scent."},"precautions":{"es":"Puede empeorar el reflujo en algunas personas. No ingieras aceites esenciales.","en":"It may worsen reflux for some people. Do not ingest essential oils."}},
"p03":{"name":{"es":"Lavanda","en":"Lavender"},"scientific":"Lavandula spp.","use":{"es":"Planta aromática cultivada en jardines.","en":"An aromatic plant grown in gardens."},"observation":{"es":"Observa el color y la disposición de sus flores.","en":"Notice the color and arrangement of its flowers."},"precautions":{"es":"Evita el contacto con los ojos y no ingieras aceites esenciales.","en":"Avoid eye contact and do not ingest essential oils."}},
"p04":{"name":{"es":"Romero","en":"Rosemary"},"scientific":"Salvia rosmarinus","use":{"es":"Hierba aromática utilizada en cocina y jardinería.","en":"An aromatic herb used in cooking and gardening."},"observation":{"es":"Observa sus hojas estrechas y su estructura.","en":"Notice its narrow leaves and structure."},"precautions":{"es":"No ingieras aceite esencial y evita el contacto con los ojos.","en":"Do not ingest essential oil and avoid eye contact."}},
"p05":{"name":{"es":"Albahaca","en":"Basil"},"scientific":"Ocimum basilicum","use":{"es":"Hierba aromática común en huertos y cocinas.","en":"An aromatic herb commonly grown in gardens and kitchens."},"observation":{"es":"Compara el tamaño y la forma de dos hojas.","en":"Compare the size and shape of two leaves."},"precautions":{"es":"No ingieras aceites esenciales sin indicación profesional.","en":"Do not ingest essential oils without professional guidance."}},
"p06":{"name":{"es":"Aloe vera","en":"Aloe vera"},"scientific":"Aloe vera","use":{"es":"Planta suculenta cultivada en interiores y exteriores.","en":"A succulent plant grown indoors and outdoors."},"observation":{"es":"Observa sus hojas carnosas sin cortarlas.","en":"Notice its fleshy leaves without cutting them."},"precautions":{"es":"No ingieras la planta ni apliques productos sin conocer su seguridad.","en":"Do not ingest the plant or apply products without knowing their safety."}},
"p07":{"name":{"es":"Helecho","en":"Fern"},"scientific":"Polypodiopsida","use":{"es":"Grupo de plantas ornamentales de ambientes diversos.","en":"A group of ornamental plants found in varied environments."},"observation":{"es":"Sigue con la mirada la forma de una fronda.","en":"Follow the shape of a frond with your eyes."},"precautions":{"es":"No consumas plantas silvestres o desconocidas.","en":"Do not consume wild or unidentified plants."}},
"p08":{"name":{"es":"Suculenta","en":"Succulent"},"scientific":"Succulentae","use":{"es":"Plantas que almacenan agua en sus tejidos.","en":"Plants that store water in their tissues."},"observation":{"es":"Observa cómo se distribuyen sus hojas.","en":"Notice how its leaves are arranged."},"precautions":{"es":"Comprueba las necesidades de cuidado de cada especie.","en":"Check the care requirements of each species."}},
"p09":{"name":{"es":"Girasol","en":"Sunflower"},"scientific":"Helianthus annuus","use":{"es":"Planta conocida por sus flores grandes.","en":"A plant known for its large flowers."},"observation":{"es":"Observa los patrones del centro de la flor.","en":"Notice the patterns at the center of the flower."},"precautions":{"es":"Evita consumir semillas si tienes alergias relevantes.","en":"Avoid eating seeds if you have relevant allergies."}},
"p10":{"name":{"es":"Caléndula","en":"Calendula"},"scientific":"Calendula officinalis","use":{"es":"Planta ornamental de flores amarillas o anaranjadas.","en":"An ornamental plant with yellow or orange flowers."},"observation":{"es":"Compara los tonos de sus pétalos.","en":"Compare the shades of its petals."},"precautions":{"es":"Puede causar reacciones alérgicas en algunas personas.","en":"It may cause allergic reactions in some people."}},
"p11":{"name":{"es":"Tomillo","en":"Thyme"},"scientific":"Thymus vulgaris","use":{"es":"Hierba aromática utilizada en cocina.","en":"An aromatic herb used in cooking."},"observation":{"es":"Observa el tamaño de sus hojas pequeñas.","en":"Notice the size of its small leaves."},"precautions":{"es":"No ingieras aceites esenciales ni preparados desconocidos.","en":"Do not ingest essential oils or unknown preparations."}},
"p12":{"name":{"es":"Cilantro","en":"Cilantro"},"scientific":"Coriandrum sativum","use":{"es":"Hierba comestible utilizada en distintas cocinas.","en":"An edible herb used in different cuisines."},"observation":{"es":"Observa la forma de sus hojas.","en":"Notice the shape of its leaves."},"precautions":{"es":"Lava adecuadamente las hierbas destinadas al consumo.","en":"Wash herbs intended for consumption properly."}},
"p13":{"name":{"es":"Poto","en":"Pothos"},"scientific":"Epipremnum aureum","use":{"es":"Planta ornamental común en interiores.","en":"An ornamental plant commonly grown indoors."},"observation":{"es":"Sigue con la mirada el recorrido de una hoja.","en":"Follow the outline of a leaf with your eyes."},"precautions":{"es":"Puede ser tóxica si la ingieren mascotas o personas; mantenla fuera de su alcance.","en":"It may be toxic if eaten by people or pets; keep it out of reach."}},
"p14":{"name":{"es":"Monstera","en":"Monstera"},"scientific":"Monstera deliciosa","use":{"es":"Planta ornamental de hojas grandes.","en":"An ornamental plant with large leaves."},"observation":{"es":"Observa las divisiones y el contorno de sus hojas.","en":"Notice the divisions and outline of its leaves."},"precautions":{"es":"No ingieras sus hojas; mantenlas fuera del alcance de niños y mascotas.","en":"Do not eat its leaves; keep them away from children and pets."}},
"p15":{"name":{"es":"Orquídea","en":"Orchid"},"scientific":"Orchidaceae","use":{"es":"Familia de plantas con flores muy variadas.","en":"A family of plants with varied flowers."},"observation":{"es":"Identifica dos formas diferentes en una flor.","en":"Identify two different shapes in a flower."},"precautions":{"es":"Respeta las necesidades específicas de cada especie.","en":"Respect the specific needs of each species."}},
"p16":{"name":{"es":"Cactus","en":"Cactus"},"scientific":"Cactaceae","use":{"es":"Grupo de plantas adaptadas a almacenar agua.","en":"A group of plants adapted to storing water."},"observation":{"es":"Observa su forma sin tocar las espinas.","en":"Notice its shape without touching its spines."},"precautions":{"es":"Mantén distancia de las espinas y usa protección al manipularlo.","en":"Keep clear of spines and use protection when handling it."}},
"p17":{"name":{"es":"Hiedra","en":"Ivy"},"scientific":"Hedera spp.","use":{"es":"Planta trepadora utilizada como ornamental.","en":"A climbing plant used ornamentally."},"observation":{"es":"Observa cómo se extienden sus tallos.","en":"Notice how its stems spread."},"precautions":{"es":"Puede ser tóxica al ingerirse y causar irritación.","en":"It may be toxic if eaten and may cause irritation."}},
"p18":{"name":{"es":"Pino","en":"Pine"},"scientific":"Pinus spp.","use":{"es":"Árbol perenne presente en muchos paisajes.","en":"An evergreen tree found in many landscapes."},"observation":{"es":"Observa la disposición de sus agujas o ramas.","en":"Notice the arrangement of its needles or branches."},"precautions":{"es":"No consumas agujas, resinas ni preparados de especie desconocida.","en":"Do not consume needles, resin, or preparations from unidentified species."}},
"p19":{"name":{"es":"Bambú","en":"Bamboo"},"scientific":"Bambusoideae","use":{"es":"Grupo de plantas de tallos característicos.","en":"A group of plants with distinctive stems."},"observation":{"es":"Observa los segmentos y líneas del tallo.","en":"Notice the segments and lines along the stem."},"precautions":{"es":"No consumas una planta sin identificarla correctamente.","en":"Do not consume a plant without identifying it correctly."}},
"p20":{"name":{"es":"Planta de interior","en":"Houseplant"},"scientific":"Planta ornamental","use":{"es":"Una planta puede servir como objeto de observación cotidiana.","en":"A plant can serve as an everyday object for observation."},"observation":{"es":"Elige una hoja y observa tres detalles diferentes.","en":"Choose a leaf and notice three different details."},"precautions":{"es":"Evita ingerir plantas desconocidas y lávate las manos tras manipularlas.","en":"Avoid eating unknown plants and wash your hands after handling them."}}
}

# Cada banco tiene 20 indicaciones distintas por idioma.
STEPS={
"calm":{
"es":[
"Apoya los pies donde te resulte cómodo.",
"Observa tres objetos que estén cerca.",
"Nota un color que no habías mirado.",
"Relaja las manos sin forzarlas.",
"Escucha un sonido del entorno.",
"Deja que los hombros encuentren una posición cómoda.",
"Mira un punto fijo durante unos segundos.",
"Identifica una superficie lisa o rugosa.",
"Permite que la respiración siga su ritmo natural.",
"Observa la luz que hay en la habitación.",
"Nombra mentalmente algo que ves.",
"Nota el apoyo de la silla o del suelo.",
"Deja pasar un pensamiento sin resolverlo ahora.",
"Mira algo que tenga una forma interesante.",
"Comprueba si puedes aflojar la mandíbula.",
"Escucha si hay un sonido cercano y otro lejano.",
"Elige un detalle del entorno y descríbelo mentalmente.",
"Date permiso para hacer esta pausa a tu ritmo.",
"Vuelve la atención a los pies y las manos.",
"Decide qué pequeño paso te gustaría dar después."
],
"en":[
"Place your feet in a comfortable position.",
"Notice three objects nearby.",
"Notice a color you had not looked at.",
"Relax your hands without forcing them.",
"Listen to a sound in your surroundings.",
"Let your shoulders settle comfortably.",
"Look at one steady point for a few seconds.",
"Notice a smooth or rough surface.",
"Let your breathing keep its natural rhythm.",
"Notice the light in the room.",
"Silently name something you can see.",
"Notice the support of your chair or the floor.",
"Let one thought pass without solving it now.",
"Look at something with an interesting shape.",
"Check whether you can soften your jaw.",
"Listen for one nearby sound and one distant sound.",
"Choose a detail and describe it silently.",
"Allow yourself to take this pause at your own pace.",
"Bring your attention back to your feet and hands.",
"Choose one small step you would like to take next."
]},
"movement":{
"es":[
"Comprueba que tienes espacio suficiente para moverte.",
"Siéntate o ponte de pie en una posición estable.",
"Mueve lentamente los dedos de las manos.",
"Abre y cierra las manos sin apretar.",
"Haz un círculo pequeño con los hombros si te resulta cómodo.",
"Vuelve los hombros a una posición natural.",
"Mueve los tobillos suavemente si puedes hacerlo con comodidad.",
"Alterna el apoyo de los pies sin perder estabilidad.",
"Estira los dedos de las manos sin llegar al dolor.",
"Deja los brazos descansar a los lados.",
"Gira la cabeza solo un poco si no causa molestias.",
"Regresa la cabeza al centro con suavidad.",
"Estira la espalda sin arquearla en exceso.",
"Cambia de postura lentamente si lo necesitas.",
"Relaja las manos y los antebrazos.",
"Nota qué movimiento te resulta más cómodo.",
"Descansa si aparece dolor, mareo o malestar.",
"Comprueba que puedes mantener una postura estable.",
"Deja que el cuerpo vuelva a una posición cómoda.",
"Elige un movimiento pequeño para repetir más tarde."
],
"en":[
"Check that you have enough room to move.",
"Sit or stand in a stable position.",
"Slowly move your fingers.",
"Open and close your hands without squeezing.",
"Make a small shoulder circle if comfortable.",
"Return your shoulders to a natural position.",
"Gently move your ankles if comfortable.",
"Shift your foot support without losing stability.",
"Stretch your fingers without reaching pain.",
"Let your arms rest at your sides.",
"Turn your head slightly only if comfortable.",
"Gently bring your head back to center.",
"Lengthen your back without over-arching.",
"Change position slowly if needed.",
"Relax your hands and forearms.",
"Notice which movement feels most comfortable.",
"Rest if you experience pain, dizziness, or discomfort.",
"Check that you can maintain a stable posture.",
"Let your body return to a comfortable position.",
"Choose one small movement to repeat later."
]},
"plants":{
"es":[
"Elige una planta o una imagen de una planta.",
"Observa su forma general antes de mirar los detalles.",
"Busca una diferencia entre dos hojas.",
"Fíjate en un tono claro y otro oscuro.",
"Observa si los bordes son lisos o irregulares.",
"Sigue visualmente una línea o una nervadura.",
"Compara el tamaño de dos partes.",
"Busca dónde termina una hoja y comienza otra.",
"Observa cómo la luz cambia su apariencia.",
"Nota si la planta crece hacia arriba o hacia los lados.",
"Busca una sombra cercana a la planta.",
"Observa la textura sin tocar si no estás seguro.",
"Cuenta mentalmente tres detalles visibles.",
"Identifica una parte que no habías observado.",
"Compara la planta con el fondo que la rodea.",
"Busca una forma repetida en sus hojas.",
"Observa si hay partes nuevas o antiguas.",
"Describe mentalmente la planta con tres palabras.",
"Recuerda que observar no requiere arrancar ni probar nada.",
"Elige un detalle natural que quieras volver a mirar."
],
"en":[
"Choose a plant or an image of a plant.",
"Notice its overall shape before looking at details.",
"Find one difference between two leaves.",
"Notice one light shade and one dark shade.",
"Notice whether the edges are smooth or uneven.",
"Follow a line or vein with your eyes.",
"Compare the size of two parts.",
"Notice where one leaf ends and another begins.",
"Notice how light changes its appearance.",
"Notice whether the plant grows upward or sideways.",
"Look for a shadow near the plant.",
"Notice the texture without touching if unsure.",
"Silently count three visible details.",
"Identify one part you had not noticed before.",
"Compare the plant with its background.",
"Look for a repeated shape among its leaves.",
"Notice whether some parts look newer or older.",
"Describe the plant silently using three words.",
"Remember that observing does not require picking or tasting anything.",
"Choose one natural detail to look at again."
]},
"coach":{
"es":[
"Piensa en una sola tarea que tengas pendiente.",
"Define qué significaría avanzar un poco.",
"Divide la tarea en un primer paso pequeño.",
"Comprueba si necesitas algún material antes de empezar.",
"Elige un momento realista para comenzar.",
"Retira una distracción que puedas controlar.",
"Decide qué puede esperar hasta otro momento.",
"Escribe mentalmente la acción más sencilla.",
"Comprueba si el paso elegido cabe en unos minutos.",
"Piensa qué ayuda práctica podrías necesitar.",
"Elige entre empezar ahora o programarlo.",
"Si no puedes hacerlo hoy, decide cuándo revisarlo.",
"Reduce el objetivo si te parece demasiado grande.",
"Identifica una cosa que ya esté resuelta.",
"Deja espacio para imprevistos razonables.",
"Comprueba que tu plan depende de acciones posibles.",
"Elige una señal que te recuerde el siguiente paso.",
"Decide qué harás si aparece un obstáculo.",
"Resume tu plan en una frase sencilla.",
"Elige cuándo revisarás tu avance."
],
"en":[
"Think of one task you need to do.",
"Define what making a little progress would mean.",
"Break the task into one small first step.",
"Check whether you need any materials before starting.",
"Choose a realistic time to begin.",
"Remove one distraction you can control.",
"Decide what can wait until later.",
"Silently name the simplest action.",
"Check whether the step fits into a few minutes.",
"Think of practical help you might need.",
"Choose whether to start now or schedule it.",
"If today is not possible, decide when to revisit it.",
"Reduce the goal if it feels too large.",
"Identify one thing that is already handled.",
"Leave room for reasonable interruptions.",
"Check that your plan depends on possible actions.",
"Choose a reminder for your next step.",
"Decide what you will do if an obstacle appears.",
"Summarize your plan in one simple sentence.",
"Choose when you will review your progress."
]}
}

# Variaciones de títulos y descripciones para crear 20 actividades por sección.
TITLES={
"calm":{"es":["Pausa consciente","Atención a los sentidos","Un momento de quietud","Escucha tu entorno","Descanso visual","Pausa entre tareas","Atención tranquila","Observar sin prisa","Regresar al presente","Un minuto para ti","Mirada serena","Pausa de manos","Escucha cercana","Pausa en tu espacio","Atención a los detalles","Descanso cotidiano","Un momento sencillo","Pausa al mediodía","Atención sin presión","Cierre tranquilo"],"en":["Mindful pause","Notice your senses","A quiet moment","Listen to your surroundings","Visual rest","Pause between tasks","Quiet attention","Observe without rushing","Return to the present","A moment for yourself","A calm gaze","Hand pause","Nearby sounds","Pause in your space","Notice the details","Everyday rest","A simple moment","Midday pause","Pressure-free attention","A calm finish"]},
"movement":{"es":["Movimiento amable","Pausa de hombros","Manos en movimiento","Cambiar de postura","Movimiento sentado","Pausa de tobillos","Estiramiento suave","Despertar las manos","Postura cómoda","Pequeños movimientos","Pausa corporal","Movimiento consciente","Descanso de brazos","Equilibrio y apoyo","Pausa de espalda","Movilidad tranquila","Movimiento a tu ritmo","Soltar tensión postural","Pausa activa","Cierre corporal"],"en":["Gentle movement","Shoulder pause","Hands in motion","Change position","Seated movement","Ankle pause","Gentle stretch","Wake up your hands","Comfortable posture","Small movements","Body pause","Mindful movement","Arm rest","Balance and support","Back pause","Easy mobility","Movement at your pace","Release postural strain","Active pause","Body reset"]},
"plants":{"es":["Mirar una planta","Detalles de hojas","Colores naturales","Formas en la naturaleza","Observación botánica","Luz y hojas","Pequeños patrones","Una pausa verde","Curiosidad natural","Mirada de jardinero","Formas y texturas","Descubrir un detalle","Observar sin tocar","Hojas y sombras","Una planta cercana","Patrones repetidos","Naturaleza cotidiana","Mirar con curiosidad","Tres detalles verdes","Cierre en la naturaleza"],"en":["Look at a plant","Leaf details","Natural colors","Shapes in nature","Botanical observation","Light and leaves","Small patterns","A green pause","Natural curiosity","A gardener's gaze","Shapes and textures","Discover a detail","Observe without touching","Leaves and shadows","A nearby plant","Repeated patterns","Everyday nature","Look with curiosity","Three natural details","Finish with nature"]},
"coach":{"es":["Un paso posible","Ordena tu prioridad","Plan sencillo","Preparar el comienzo","Decidir con calma","Una tarea a la vez","Pequeños avances","Organizar el día","Elegir qué importa","Reducir una tarea","Plan de pocos minutos","Preparación práctica","Una decisión útil","Retomar una tarea","Plan realista","Orden sin presión","Definir el siguiente paso","Preparar una pausa","Revisar el día","Cierre y continuidad"],"en":["One possible step","Set your priority","A simple plan","Prepare to begin","Decide calmly","One task at a time","Small progress","Organize your day","Choose what matters","Make a task smaller","A few-minute plan","Practical preparation","One useful decision","Return to a task","A realistic plan","Order without pressure","Define the next step","Plan a pause","Review your day","Finish and continue"]}
}
DESCRIPTIONS={
"es":{
"plants":"Observación sencilla de plantas y detalles naturales, sin necesidad de experiencia.",
"movement":"Movimientos opcionales y adaptables. Haz solo lo que te resulte cómodo.",
"calm":"Una práctica cotidiana para observar el entorno y hacer una pausa sin forzar la respiración.",
"coach":"Organiza una acción cotidiana en pasos pequeños y realistas."
},
"en":{
"plants":"Simple observation of plants and natural details, with no experience required.",
"movement":"Optional, adaptable movements. Do only what feels comfortable.",
"calm":"An everyday practice to notice your surroundings and pause without forcing your breathing.",
"coach":"Organize an everyday action into small, realistic steps."
}}

def _lang(value):
    return "en" if str(value or "es").lower().startswith("en") else "es"

def _section(value):
    value=str(value or "all").strip().lower()
    aliases={"plant":"plants","nature":"plants","energía":"movement","energia":"movement","movimiento":"movement","calma":"calm","atencion":"calm","atención":"calm","coach":"coach","all":"all","todos":"all","todas":"all"}
    value=aliases.get(value,value)
    return value if value in SECTIONS or value=="all" else "all"

def _build_catalog():
    result=[]
    for section in SECTIONS:
        for i in range(20):
            if section=="plants":
                pid=list(PLANTS.keys())[i]
                plant=PLANTS[pid]
                title={l:plant["name"][l] if i<3 else TITLES[section][l][i] for l in LANGUAGES}
                title["es"]="Naturaleza: "+title["es"]
                title["en"]="Nature: "+title["en"]
                steps={l:list(STEPS[section][l]) for l in LANGUAGES}
                if i<3:
                    steps["es"][0]="Observa la planta: "+plant["name"]["es"]+"."
                    steps["en"][0]="Observe the plant: "+plant["name"]["en"]+"."
                item={"id":pid,"section":section,"plant_id":pid,"title":title,"description":{l:DESCRIPTIONS[l][section] for l in LANGUAGES},"steps":steps}
            else:
                aid={"movement":"m","calm":"c","coach":"w"}[section]+str(i+1).zfill(2)
                item={"id":aid,"section":section,"title":{l:TITLES[section][l][i] for l in LANGUAGES},"description":{l:DESCRIPTIONS[l][section] for l in LANGUAGES},"steps":{l:list(STEPS[section][l]) for l in LANGUAGES}}
            result.append(item)
    return result

_CATALOG=_build_catalog()
_BY_ID={a["id"]:a for a in _CATALOG}

def _public_activity(item,lang="es",minutes=None):
    language=_lang(lang)
    out={"id":item["id"],"section":item["section"],"title":item["title"][language],"description":item["description"][language],"steps":list(item["steps"][language])}
    if item.get("plant_id"):
        out["plant_id"]=item["plant_id"]
    if minutes is not None:
        out["minutes"]=max(1,min(10,int(minutes)))
    return out

def get_catalog(lang="es"):
    language=_lang(lang)
    return {"version":VERSION,"name":APP_NAME,"company":COMPANY,"languages":list(LANGUAGES),"sections":list(SECTIONS),"prompt_interval_seconds":PROMPT_INTERVAL_SECONDS,"activities":[_public_activity(a,language) for a in _CATALOG]}

def get_activities(lang="es",section="all"):
    language=_lang(lang)
    wanted=_section(section)
    return [_public_activity(a,language) for a in _CATALOG if wanted=="all" or a["section"]==wanted]

def get_activity(activity_id,lang="es",minutes=None):
    item=_BY_ID.get(str(activity_id or "").strip())
    if not item:
        return None
    return _public_activity(item,lang,minutes)

def get_session(activity_id=None,minutes=3,lang="es",activity=None):
    language=_lang(lang)
    try:
        duration=int(minutes)
    except (ValueError,TypeError):
        duration=3
    if duration not in MINUTES_ALLOWED:
        duration=3
    item=activity if isinstance(activity,dict) else _BY_ID.get(str(activity_id or ""))
    if not item:
        item=_rng.choice(_CATALOG)
    out=_public_activity(item,language,duration)
    out.update({"duration_seconds":duration*60,"prompt_interval_seconds":PROMPT_INTERVAL_SECONDS,"steps_count":len(out["steps"]),"generated_at":datetime.datetime.now(datetime.timezone.utc).isoformat()})
    return out

def get_plant(plant_id,lang="es"):
    language=_lang(lang)
    pid=str(plant_id or "").strip()
    p=PLANTS.get(pid)
    if not p:
        return None
    return {"id":pid,"name":p["name"][language],"scientific_name":p["scientific"],"traditional_use":p["use"][language],"observation":p["observation"][language],"precautions":p["precautions"][language],"disclaimer":{"es":"Información general; no sustituye orientación profesional. No ingieras plantas desconocidas ni aceites esenciales.","en":"General information; not a substitute for professional guidance. Do not ingest unknown plants or essential oils."}[language]}

def get_program_day(lang="es",day=1):
    language=_lang(lang)
    try:
        number=int(day)
    except (ValueError,TypeError):
        number=1
    number=max(1,min(7,number))
    plan=[
        ("calm",1,3),("plants",0,5),("movement",2,3),("calm",8,5),
        ("plants",3,5),("coach",5,3),("coach",18,5)
    ]
    section,index,mins=plan[number-1]
    pool=[a for a in _CATALOG if a["section"]==section]
    item=pool[index%len(pool)]
    names={"es":["Comienza con una pausa","Observa la naturaleza","Muévete suavemente","Vuelve al presente","Descubre una planta","Elige una prioridad","Repasa lo que te ayudó"],"en":["Begin with a pause","Observe nature","Move gently","Return to the present","Discover a plant","Choose a priority","Review what helped"]}
    desc={"es":["Empieza con una pausa y descubre qué práctica te resulta útil.","Dedica unos minutos a observar un detalle natural.","Prueba movimientos pequeños dentro de tus posibilidades.","Utiliza los sentidos para observar tu entorno.","Conoce una planta y respeta sus precauciones.","Convierte una tarea en un primer paso manejable.","Repasa una práctica y decide qué quieres mantener."],"en":["Start with a pause and notice which practice is useful to you.","Spend a few minutes noticing a natural detail.","Try small movements within your abilities.","Use your senses to notice your surroundings.","Learn about a plant and respect its precautions.","Turn a task into one manageable first step.","Review one practice and decide what to keep."]}
    return {"day":number,"title":names[language][number-1],"description":desc[language][number-1],"minutes":mins,"activity":_public_activity(item,language,mins),"prompt_interval_seconds":PROMPT_INTERVAL_SECONDS}

def get_health():
    return {"status":"ok","engine":APP_NAME,"version":VERSION,"activities":len(_CATALOG),"activities_per_section":{s:sum(1 for a in _CATALOG if a["section"]==s) for s in SECTIONS},"languages":list(LANGUAGES),"prompt_interval_seconds":PROMPT_INTERVAL_SECONDS}

def get_config(lang="es"):
    language=_lang(lang)
    return {"name":APP_NAME,"company":COMPANY,"version":VERSION,"language":language,"languages":list(LANGUAGES),"sections":list(SECTIONS),"minutes":list(MINUTES_ALLOWED),"prompt_interval_seconds":PROMPT_INTERVAL_SECONDS,"disclaimer":{"es":"Actividades generales de bienestar, no tratamientos ni diagnósticos.","en":"General wellness activities, not treatments or diagnoses."}[language]}

def create_session_id(activity_id,minutes=3):
    raw=f"{activity_id}|{minutes}|{time.time_ns()}|{_rng.random()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]

# Alias para mantener compatibilidad con llamadas anteriores.
catalog=get_catalog
activities=get_activities
session=get_session
plant=get_plant
program_day=get_program_day
health=get_health
config=get_config
