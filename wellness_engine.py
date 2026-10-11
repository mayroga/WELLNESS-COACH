from __future__ import annotations
import copy
import random

VERSION="4.0.0"
LANGUAGES=("es","en")
SECTIONS=("plants","movement","calm","coach")
DURATIONS=(3,5,10)

CATALOG={
"es":[
{"id":"plants","title":"Plantas y naturaleza","description":"Observación, curiosidad y conexión con el entorno."},
{"id":"movement","title":"Energía y movimiento","description":"Pausas adaptables y movimientos suaves."},
{"id":"calm","title":"Calma y atención","description":"Observación del presente y pausas cotidianas."},
{"id":"coach","title":"Mi coach de bienestar","description":"Organización práctica y pequeños pasos para el día."}
],
"en":[
{"id":"plants","title":"Plants and nature","description":"Observation, curiosity, and connection with your surroundings."},
{"id":"movement","title":"Energy and movement","description":"Adaptable breaks and gentle movement."},
{"id":"calm","title":"Calm and mindfulness","description":"Noticing the present and taking everyday pauses."},
{"id":"coach","title":"My wellness coach","description":"Practical planning and small steps for the day."}
]}

PLANTS={
"p01":{
"es":{"id":"p01","name":"Manzanilla","scientific_name":"Matricaria chamomilla","traditional_use":"Se consume tradicionalmente como infusión.","observation":"Observa los detalles de una flor y sus formas.","precautions":"Puede provocar alergias, especialmente en personas sensibles a plantas de la familia Asteraceae. Si tomas medicamentos, estás embarazada o tienes dudas, consulta a un profesional sanitario antes de consumirla."},
"en":{"id":"p01","name":"Chamomile","scientific_name":"Matricaria chamomilla","traditional_use":"Traditionally consumed as an infusion.","observation":"Notice the details and shapes of a flower.","precautions":"It may cause allergies, especially in people sensitive to Asteraceae plants. If you take medication, are pregnant, or have concerns, consult a healthcare professional before consuming it."}},
"p02":{
"es":{"id":"p02","name":"Menta","scientific_name":"Mentha spp.","traditional_use":"Hierba aromática utilizada en alimentos e infusiones.","observation":"Observa la forma de sus hojas y, si lo deseas, percibe suavemente su aroma.","precautions":"Puede empeorar el reflujo en algunas personas. No ingieras aceites esenciales ni utilices preparados concentrados sin orientación profesional."},
"en":{"id":"p02","name":"Mint","scientific_name":"Mentha spp.","traditional_use":"An aromatic herb used in foods and infusions.","observation":"Notice the shape of its leaves and, if you wish, gently notice its scent.","precautions":"It may worsen reflux in some people. Do not ingest essential oils or use concentrated preparations without professional guidance."}},
"p03":{
"es":{"id":"p03","name":"Albahaca","scientific_name":"Ocimum basilicum","traditional_use":"Hierba aromática utilizada en la cocina y en jardines.","observation":"Observa el color, la forma y la disposición de sus hojas.","precautions":"No consumas una planta silvestre si no puedes identificarla con seguridad. Lava las hierbas destinadas a la alimentación."},
"en":{"id":"p03","name":"Basil","scientific_name":"Ocimum basilicum","traditional_use":"An aromatic herb used in cooking and gardens.","observation":"Notice the color, shape, and arrangement of its leaves.","precautions":"Do not consume a wild plant unless you can identify it with certainty. Wash herbs intended for food."}},
"p04":{
"es":{"id":"p04","name":"Romero","scientific_name":"Salvia rosmarinus","traditional_use":"Hierba aromática utilizada en cocina y jardinería.","observation":"Observa sus hojas estrechas, su color y la forma de sus ramas.","precautions":"No ingieras aceite esencial de romero. Evita el contacto de aceites concentrados con los ojos y consulta a un profesional antes de usar preparados medicinales."},
"en":{"id":"p04","name":"Rosemary","scientific_name":"Salvia rosmarinus","traditional_use":"An aromatic herb used in cooking and gardening.","observation":"Notice its narrow leaves, color, and branch shapes.","precautions":"Do not ingest rosemary essential oil. Avoid contact between concentrated oils and your eyes, and consult a professional before using medicinal preparations."}}
}

RAW=[
{"id":"p01","section":"plants","es":{"title":"Observar una flor","description":"Una práctica de observación natural que puedes hacer en casa o al aire libre.","steps":["Busca una flor, una fotografía o una planta que puedas observar cómodamente.","Mira sus formas y sus colores sin necesidad de identificarla.","Observa un detalle pequeño que no habías notado antes.","Si te resulta agradable, dedica un momento a observar sus hojas o pétalos.","Termina eligiendo un detalle natural que te gustaría volver a observar." ]},"en":{"title":"Notice a flower","description":"A nature observation practice you can do at home or outdoors.","steps":["Find a flower, a photograph, or a plant you can observe comfortably.","Look at its shapes and colors without needing to identify it.","Notice one small detail you had not seen before.","If you enjoy it, spend a moment looking at its leaves or petals.","Finish by choosing one natural detail you would like to notice again."]}},
{"id":"p02","section":"plants","es":{"title":"Explorar la menta","description":"Observa una hierba aromática sin necesidad de consumirla.","steps":["Busca una planta de menta o una fotografía clara de sus hojas.","Observa la forma y el borde de una hoja.","Fíjate en las diferencias de color entre las hojas.","Si tienes una planta segura y te apetece, percibe suavemente su aroma sin ingerirla.","Termina recordando que observar la naturaleza también puede ser una actividad sencilla." ]},"en":{"title":"Explore mint","description":"Observe an aromatic herb without needing to consume it.","steps":["Find a mint plant or a clear photograph of its leaves.","Notice the shape and edge of one leaf.","Look for differences in color between leaves.","If you have a safe plant and wish to, gently notice its scent without ingesting it.","Finish by remembering that observing nature can be a simple activity."]}},
{"id":"p03","section":"plants","es":{"title":"Una pequeña hoja","description":"Descubre detalles de una hoja y de su entorno.","steps":["Elige una hoja de una planta conocida o una fotografía.","Observa su tamaño y su forma general.","Fíjate en las líneas que recorren la hoja.","Mira cómo cambia la luz sobre su superficie.","Cierra la práctica escogiendo el detalle que más te llamó la atención." ]},"en":{"title":"A small leaf","description":"Discover details in a leaf and its surroundings.","steps":["Choose a leaf from a known plant or a photograph.","Notice its size and overall shape.","Look at the lines running across the leaf.","Notice how light changes across its surface.","Finish by choosing the detail that caught your attention most."]}},
{"id":"p04","section":"plants","es":{"title":"Descubrir el romero","description":"Una actividad de observación de una hierba aromática común.","steps":["Busca una planta de romero o una fotografía.","Observa sus hojas estrechas y la disposición de sus ramas.","Compara dos hojas y encuentra una semejanza.","Observa su color y la textura visible sin tocarla si no lo deseas.","Termina identificando un detalle que puedas describir con tus propias palabras." ]},"en":{"title":"Discover rosemary","description":"An observation activity featuring a common aromatic herb.","steps":["Find a rosemary plant or a photograph.","Notice its narrow leaves and the arrangement of its branches.","Compare two leaves and find one similarity.","Notice its color and visible texture without touching it if you prefer.","Finish by identifying one detail you can describe in your own words."]}},
{"id":"m01","section":"movement","es":{"title":"Movimiento sentado","description":"Movimientos suaves que puedes adaptar o realizar sentado.","steps":["Busca una posición estable y cómoda, con los pies apoyados si es posible.","Mueve lentamente los dedos de las manos y después relájalos.","Rota suavemente los hombros solo hasta donde te resulte cómodo.","Estira una pierna ligeramente si puedes hacerlo sin dolor; después cambia de lado.","Termina quedándote en una postura cómoda y observa cómo te encuentras." ]},"en":{"title":"Seated movement","description":"Gentle movements you can adapt or do while seated.","steps":["Find a stable, comfortable position, with your feet supported if possible.","Slowly move your fingers and then relax them.","Gently roll your shoulders only as far as feels comfortable.","Slightly extend one leg if you can do so without pain; then switch sides.","Finish in a comfortable position and notice how you feel."]}},
{"id":"m02","section":"movement","es":{"title":"Pausa para cambiar de postura","description":"Una pausa para interrumpir un periodo prolongado en la misma posición.","steps":["Observa cuánto tiempo llevas en la misma postura.","Si es seguro, cambia suavemente la posición de los pies y la espalda.","Mueve las manos y los brazos sin hacer fuerza.","Si te resulta cómodo y estable, ponte de pie lentamente; también puedes permanecer sentado.","Elige una postura cómoda para continuar con tu día." ]},"en":{"title":"A posture break","description":"A short break from staying in the same position for a long time.","steps":["Notice how long you have been in the same position.","If safe, gently adjust the position of your feet and back.","Move your hands and arms without straining.","If comfortable and stable, stand up slowly; you may also remain seated.","Choose a comfortable posture for the rest of your day."]}},
{"id":"m03","section":"movement","es":{"title":"Despertar las manos","description":"Una actividad sencilla para mover las manos y los dedos sin forzarlos.","steps":["Apoya las manos en una superficie o déjalas descansar cómodamente.","Abre los dedos suavemente y después relájalos.","Mueve cada muñeca despacio dentro de un rango cómodo.","Acerca y separa los dedos sin apretar ni provocar dolor.","Descansa las manos y continúa solo si te resulta agradable." ]},"en":{"title":"Wake up your hands","description":"A simple activity for moving your hands and fingers without straining.","steps":["Rest your hands on a surface or let them sit comfortably.","Gently spread your fingers and then relax them.","Slowly move each wrist within a comfortable range.","Bring your fingers together and apart without squeezing or causing pain.","Rest your hands and continue only if it feels comfortable."]}},
{"id":"c01","section":"calm","es":{"title":"Volver al presente","description":"Observa lo que te rodea sin intentar cambiar nada.","steps":["Busca una posición cómoda y permite que tus hombros descansen.","Nombra mentalmente tres cosas que puedes ver.","Identifica dos sonidos que puedas escuchar sin buscarlos con esfuerzo.","Nota el contacto de tus pies con el suelo o de tu cuerpo con el asiento.","Elige una cosa sencilla de tu entorno a la que quieras prestar atención." ]},"en":{"title":"Return to the present","description":"Notice your surroundings without trying to change anything.","steps":["Find a comfortable position and let your shoulders rest.","Silently name three things you can see.","Notice two sounds you can hear without searching for them.","Notice the contact of your feet with the floor or your body with the seat.","Choose one simple thing around you to pay attention to."]}},
{"id":"c02","section":"calm","es":{"title":"Un minuto de atención","description":"Una práctica breve de observación que no requiere controlar la respiración.","steps":["Elige un objeto cercano que puedas mirar cómodamente.","Observa su color y su forma.","Fíjate en una parte del objeto que normalmente pasas por alto.","Si aparecen otras ideas, puedes dejarlas pasar y volver a mirar el objeto.","Termina cuando quieras y continúa con tu día sin exigirte nada." ]},"en":{"title":"A moment of attention","description":"A brief observation practice that does not require controlling your breathing.","steps":["Choose a nearby object you can look at comfortably.","Notice its color and shape.","Look for one part of the object you might usually overlook.","If other thoughts appear, let them pass and return your attention to the object.","Finish whenever you wish and continue your day without putting pressure on yourself."]}},
{"id":"c03","section":"calm","es":{"title":"Pausa con los sentidos","description":"Utiliza los sentidos para observar tu entorno a tu propio ritmo.","steps":["Mira a tu alrededor y elige un color que te agrade.","Escucha los sonidos cercanos sin intentar clasificarlos.","Observa si percibes una textura a través de tus manos o de la ropa.","Nota la temperatura del ambiente sin tener que cambiarla.","Escoge el detalle más agradable o interesante de esta pausa." ]},"en":{"title":"A pause for the senses","description":"Use your senses to notice your surroundings at your own pace.","steps":["Look around and choose a color you enjoy.","Listen to nearby sounds without trying to classify them.","Notice a texture through your hands or clothing if you wish.","Notice the temperature of the surroundings without needing to change it.","Choose the most pleasant or interesting detail from this pause."]}},
{"id":"w01","section":"coach","es":{"title":"Elegir una prioridad","description":"Organiza el siguiente paso de tu día sin intentar resolverlo todo a la vez.","steps":["Piensa en las tareas que tienes delante, sin necesidad de escribirlas todas.","Elige una tarea pequeña que sea útil atender hoy.","Divide esa tarea en un primer paso que puedas explicar en una frase.","Decide cuándo o dónde podrías comenzar ese paso.","Termina recordando que avanzar una cosa cada vez también es avanzar." ]},"en":{"title":"Choose one priority","description":"Plan your next step without trying to solve everything at once.","steps":["Think about the tasks ahead without needing to write them all down.","Choose one small task that would be useful to address today.","Break it into a first step you can describe in one sentence.","Decide when or where you could begin that step.","Finish by remembering that doing one thing at a time is still progress."]}},
{"id":"w02","section":"coach","es":{"title":"Preparar una pausa","description":"Encuentra un momento realista para una actividad breve de bienestar general.","steps":["Piensa en una parte de tu día en la que suelas tener unos minutos libres.","Elige una actividad sencilla que puedas hacer en ese momento.","Comprueba que el lugar sea cómodo y seguro para esa actividad.","Decide cuánto tiempo quieres dedicarle, sin convertirlo en una obligación.","Termina eligiendo una señal sencilla que te recuerde hacer la pausa." ]},"en":{"title":"Plan a short break","description":"Find a realistic moment for a brief general wellness activity.","steps":["Think of a part of your day when you usually have a few free minutes.","Choose a simple activity you could do then.","Make sure the place is comfortable and safe for that activity.","Choose how much time you would like to spend, without turning it into an obligation.","Finish by choosing a simple reminder for your break."]}}
]

PROGRAM=[
{"day":1,"activity_id":"c01","minutes":3},
{"day":2,"activity_id":"p01","minutes":5},
{"day":3,"activity_id":"m01","minutes":3},
{"day":4,"activity_id":"c03","minutes":5},
{"day":5,"activity_id":"p04","minutes":5},
{"day":6,"activity_id":"w01","minutes":3},
{"day":7,"activity_id":"c02","minutes":5}
]

def _language(lang:str)->str:
    return lang if lang in LANGUAGES else "es"

def _duration(minutes:int)->int:
    try:
        n=int(minutes)
    except (TypeError,ValueError):
        n=3
    return n if n in DURATIONS else min(DURATIONS,key=lambda x:abs(x-n))

def _raw_activity(activity_id:str,lang:str="es")->dict|None:
    language=_language(lang)
    for item in RAW:
        if item["id"]==activity_id:
            text=item[language]
            return {
                "id":item["id"],
                "section":item["section"],
                "title":text["title"],
                "description":text["description"],
                "steps":list(text["steps"]),
                "language":language
            }
    return None

def get_catalog(lang:str="es")->list:
    return copy.deepcopy(CATALOG[_language(lang)])

def get_activities(lang:str="es",section:str="all")->list:
    language=_language(lang)
    selected=section if section in (*SECTIONS,"all") else "all"
    result=[]
    for item in RAW:
        if selected!="all" and item["section"]!=selected:
            continue
        activity=_raw_activity(item["id"],language)
        if activity:
            result.append(activity)
    return copy.deepcopy(result)

def get_activity(activity_id:str,lang:str="es")->dict|None:
    activity=_raw_activity(str(activity_id),lang)
    return copy.deepcopy(activity) if activity else None

def get_session(lang:str="es",kind:str="pause",minutes:int=3)->dict:
    language=_language(lang)
    duration=_duration(minutes)
    kinds={
        "pause":("calm","c01"),
        "energy":("movement","m01"),
        "calm":("calm","c02"),
        "nature":("plants","p01"),
        "coach":("coach","w01"),
        "program":("calm","c01")
    }
    section,default_id=kinds.get(kind,("calm","c01"))
    candidates=[x for x in RAW if x["section"]==section]
    item=next((x for x in candidates if x["id"]==default_id),None)
    if item is None and candidates:
        item=candidates[0]
    activity=_raw_activity(item["id"],language) if item else None
    return {
        "language":language,
        "kind":kind if kind in kinds else "pause",
        "minutes":duration,
        "activity":activity,
        "title":activity["title"] if activity else "",
        "description":activity["description"] if activity else "",
        "steps":activity["steps"] if activity else []
    }

def get_plant(plant_id:str,lang:str="es")->dict|None:
    language=_language(lang)
    item=PLANTS.get(str(plant_id).lower())
    if not item:
        return None
    return copy.deepcopy(item[language])

def get_program_day(lang:str="es",day:int=1)->dict:
    language=_language(lang)
    try:
        number=int(day)
    except (TypeError,ValueError):
        number=1
    number=max(1,min(7,number))
    plan=PROGRAM[number-1]
    activity=_raw_activity(plan["activity_id"],language)
    names={
        "es":[
            "Comienza con una pausa",
            "Observa la naturaleza",
            "Muévete suavemente",
            "Vuelve al presente",
            "Descubre una planta",
            "Elige una prioridad",
            "Repasa lo que te ayudó"
        ],
        "en":[
            "Begin with a pause",
            "Observe nature",
            "Move gently",
            "Return to the present",
            "Discover a plant",
            "Choose a priority",
            "Review what helped"
        ]
    }
    descriptions={
        "es":[
            "Empieza con una pausa y descubre qué práctica te resulta útil.",
            "Dedica unos minutos a observar un detalle natural.",
            "Prueba movimientos pequeños dentro de tus posibilidades.",
            "Utiliza los sentidos para observar tu entorno.",
            "Observa una hierba aromática y conoce sus precauciones.",
            "Convierte una tarea en un primer paso manejable.",
            "Repasa una práctica y decide qué quieres mantener."
        ],
        "en":[
            "Start with a pause and discover which practice is useful to you.",
            "Spend a few minutes noticing a natural detail.",
            "Try small movements within your abilities.",
            "Use your senses to notice your surroundings.",
            "Observe an aromatic herb and learn about its precautions.",
            "Turn a task into one manageable first step.",
            "Review one practice and decide what to keep."
        ]
    }
    return {
        "day":number,
        "total_days":7,
        "language":language,
        "title":names[language][number-1],
        "description":descriptions[language][number-1],
        "minutes":plan["minutes"],
        "activity":copy.deepcopy(activity)
    }

def health_check()->dict:
    return {
        "status":"ok",
        "version":VERSION,
        "languages":list(LANGUAGES),
        "sections":list(SECTIONS),
        "activities":len(RAW),
        "plants":len(PLANTS),
        "program_days":len(PROGRAM)
    }
