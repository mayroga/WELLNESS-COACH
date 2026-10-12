
from __future__ import annotations
import random,time,datetime,hashlib,threading
from copy import deepcopy

VERSION="9.0.0"
APP_NAME="WELLNESS COACH"
COMPANY="May Roga LLC"
PROMPT_INTERVAL_SECONDS=10
MINUTES_ALLOWED=(3,5,10)
LANGUAGES=("es","en","pt")
SECTIONS=("movement","calm","coach")
_LOCK=threading.RLock()
_RNG=random.SystemRandom()
_HISTORY={}
_MAX_HISTORY=5000

_NAMES={
"movement":[
("Movimiento cómodo","Comfortable movement","Movimento confortável"),
("Despertar los hombros","Wake up your shoulders","Despertar os ombros"),
("Pausa para las manos","A pause for your hands","Pausa para as mãos"),
("Estirar con suavidad","Gentle stretching","Alongamento suave"),
("Movilidad sentado","Seated mobility","Mobilidade sentado"),
("Caminar con atención","Mindful walking","Caminhada consciente"),
("Descanso para el cuello","Neck relaxation","Relaxamento do pescoço"),
("Soltar las muñecas","Release your wrists","Soltar os pulsos"),
("Respirar y moverse","Breathe and move","Respirar e movimentar"),
("Pausa de postura","Posture break","Pausa para a postura"),
("Mover los tobillos","Move your ankles","Movimentar os tornozelos"),
("Activar las piernas","Wake up your legs","Ativar as pernas"),
("Equilibrio con apoyo","Supported balance","Equilíbrio com apoio"),
("Movimientos de brazos","Arm movements","Movimentos dos braços"),
("Pausa después de sentarse","A break after sitting","Pausa depois de estar sentado"),
("Movimiento lento","Slow movement","Movimento lento"),
("Relajar la mandíbula","Relax your jaw","Relaxar a mandíbula"),
("Descanso visual","Rest your eyes","Descanso para os olhos"),
("Movimiento a tu ritmo","Move at your own pace","Movimente-se no seu ritmo"),
("Cerrar con suavidad","Finish gently","Terminar suavemente")],
"calm":[
("Respiración tranquila","Calm breathing","Respiração tranquila"),
("Atención al presente","Attention to the present","Atenção ao presente"),
("Pausa consciente","Mindful pause","Pausa consciente"),
("Escuchar el entorno","Listen to your surroundings","Ouvir o ambiente"),
("Observar sin juzgar","Observe without judging","Observar sem julgar"),
("Soltar la tensión","Release tension","Soltar a tensão"),
("Un minuto de silencio","One minute of quiet","Um minuto de silêncio"),
("Reconocer los sentidos","Notice your senses","Perceber os sentidos"),
("Pausa entre tareas","Pause between tasks","Pausa entre tarefas"),
("Respirar sin prisa","Breathe without rushing","Respirar sem pressa"),
("Atención a los sonidos","Notice the sounds","Atenção aos sons"),
("Descanso mental breve","A brief mental rest","Breve descanso mental"),
("Volver al momento","Return to the moment","Voltar ao momento"),
("Mirar con curiosidad","Look with curiosity","Olhar com curiosidade"),
("Soltar una preocupación","Set aside a worry","Deixar uma preocupação de lado"),
("Pausa de gratitud","A gratitude pause","Pausa de gratidão"),
("Reconocer cómo estás","Notice how you feel","Perceber como se sente"),
("Dar espacio a los pensamientos","Make room for thoughts","Dar espaço aos pensamentos"),
("Calma antes de continuar","Calm before continuing","Calma antes de continuar"),
("Cerrar la pausa","Finish the pause","Terminar a pausa")],
"coach":[
("Elegir un paso pequeño","Choose one small step","Escolher um pequeno passo"),
("Ordenar una prioridad","Organize one priority","Organizar uma prioridade"),
("Preparar el día","Prepare your day","Preparar o dia"),
("Dividir una tarea","Break down a task","Dividir uma tarefa"),
("Hacer una lista breve","Make a short list","Fazer uma lista curta"),
("Preparar un espacio","Prepare a space","Preparar um espaço"),
("Planificar una pausa","Plan a break","Planear uma pausa"),
("Retomar una tarea","Return to a task","Retomar uma tarefa"),
("Reducir distracciones","Reduce distractions","Reduzir distrações"),
("Organizar lo inmediato","Organize what is immediate","Organizar o que é imediato"),
("Elegir qué puede esperar","Choose what can wait","Escolher o que pode esperar"),
("Preparar lo necesario","Prepare what you need","Preparar o necessário"),
("Reconocer un avance","Notice one achievement","Reconhecer um progresso"),
("Definir un límite sencillo","Set a simple boundary","Definir um limite simples"),
("Crear una rutina breve","Create a short routine","Criar uma rotina breve"),
("Hacer espacio en la agenda","Make room in your schedule","Abrir espaço na agenda"),
("Resolver el siguiente paso","Work out the next step","Definir o próximo passo"),
("Cerrar una tarea pendiente","Close one pending task","Concluir uma tarefa pendente"),
("Elegir con calma","Choose calmly","Escolher com calma"),
("Revisar y terminar","Review and finish","Rever e terminar")]
}

_DESC={
"movement":{
"es":"Actividad general de movimiento suave. Adapta cada paso a tu comodidad y omite cualquier movimiento que no te resulte adecuado.",
"en":"A general gentle-movement activity. Adapt each step to your comfort and skip any movement that does not feel right.",
"pt":"Atividade geral de movimento suave. Adapte cada passo ao seu conforto e omita qualquer movimento que não seja adequado."},
"calm":{
"es":"Una pausa sencilla para dirigir la atención al momento presente, sin exigirte sentirte de una manera determinada.",
"en":"A simple pause to bring attention to the present moment, without requiring yourself to feel a particular way.",
"pt":"Uma pausa simples para dirigir a atenção ao momento presente, sem exigir que se sinta de uma maneira específica."},
"coach":{
"es":"Una actividad práctica para organizar una idea o elegir un siguiente paso pequeño y realista.",
"en":"A practical activity to organize an idea or choose a small, realistic next step.",
"pt":"Uma atividade prática para organizar uma ideia ou escolher um próximo passo pequeno e realista."}
}

_STEPS={
"movement":[
("Busca una posición cómoda, sentado o de pie, con apoyo si lo necesitas.","Find a comfortable position, seated or standing, using support if needed.","Encontre uma posição confortável, sentado ou em pé, usando apoio se necessário."),
("Afloja los hombros y deja los brazos en una posición natural.","Relax your shoulders and let your arms rest naturally.","Relaxe os ombros e deixe os braços numa posição natural."),
("Haz un movimiento pequeño y lento que te resulte cómodo.","Make a small, slow movement that feels comfortable.","Faça um movimento pequeno e lento que seja confortável."),
("Regresa a una posición cómoda y nota cómo te sientes.","Return to a comfortable position and notice how you feel.","Volte a uma posição confortável e perceba como se sente."),
("Repite suavemente si te resulta agradable; no fuerces el cuerpo.","Repeat gently if it feels pleasant; do not force your body.","Repita suavemente se for agradável; não force o corpo."),
("Termina despacio y continúa con tu día a tu ritmo.","Finish slowly and continue your day at your own pace.","Termine devagar e continue o dia no seu ritmo.")],
"calm":[
("Adopta una postura cómoda y permite que la atención se asiente.","Choose a comfortable posture and let your attention settle.","Adote uma postura confortável e deixe a atenção assentar."),
("Observa la respiración tal como ocurre, sin intentar cambiarla.","Notice your breathing as it is, without trying to change it.","Observe a respiração como acontece, sem tentar alterá-la."),
("Identifica un sonido, una forma o una sensación cercana.","Notice a sound, a shape, or a nearby sensation.","Perceba um som, uma forma ou uma sensação próxima."),
("Cuando la mente se distraiga, vuelve con amabilidad a este momento.","When your mind wanders, gently return to this moment.","Quando a mente se distrair, volte gentilmente a este momento."),
("Permite que los pensamientos estén presentes sin tener que resolverlos ahora.","Let thoughts be present without needing to solve them now.","Permita que os pensamentos estejam presentes sem precisar resolvê-los agora."),
("Mira a tu alrededor y termina la pausa sin prisa.","Look around and finish the pause without rushing.","Olhe ao redor e termine a pausa sem pressa.")],
"coach":[
("Haz una pausa y piensa qué te gustaría ordenar o resolver.","Pause and consider what you would like to organize or resolve.","Faça uma pausa e pense no que gostaria de organizar ou resolver."),
("Describe el asunto en una frase sencilla.","Describe the matter in one simple sentence.","Descreva o assunto numa frase simples."),
("Elige una parte pequeña que dependa de ti.","Choose one small part that is within your control.","Escolha uma pequena parte que dependa de si."),
("Decide cuál sería el primer paso concreto y realista.","Decide on the first concrete, realistic step.","Decida qual seria o primeiro passo concreto e realista."),
("Piensa qué necesitas preparar y cuándo podrías hacerlo.","Consider what you need to prepare and when you could do it.","Pense no que precisa preparar e quando poderia fazê-lo."),
("Revisa tu elección y termina con una intención clara.","Review your choice and finish with a clear intention.","Reveja a sua escolha e termine com uma intenção clara.")],
}

def _lang(lang):
    return lang if lang in LANGUAGES else "es"

def _localized(row,lang):
    return row[LANGUAGES.index(_lang(lang))]

def _make_catalog():
    out=[]
    for section,names in _NAMES.items():
        for i,name in enumerate(names,1):
            aid=f"{section}_{i:02d}"
            out.append({
                "id":aid,"section":section,
                "title":dict(zip(LANGUAGES,name)),
                "description":dict(zip(LANGUAGES,[_DESC[section][x] for x in LANGUAGES])),
                "steps":[dict(zip(LANGUAGES,row)) for row in _STEPS[section]],
                "step_count":len(_STEPS[section]),"plant_id":None
            })
    return out

_CATALOG=_make_catalog()
_BY_ID={a["id"]:a for a in _CATALOG}

def _public_activity(item,lang="es",minutes=None):
    lang=_lang(lang)
    out={
        "id":item["id"],"section":item["section"],
        "title":item["title"][lang],
        "description":item["description"][lang],
        "steps":[x[lang] for x in item["steps"]],
        "step_count":len(item["steps"]),"plant_id":None
    }
    if minutes is not None:out["minutes"]=minutes
    return out

def get_catalog(lang="es"):
    lang=_lang(lang)
    return [{"id":s,"name":{"es":{"movement":"Movimiento suave","calm":"Calma y atención","coach":"Organización y planificación"}[s],"en":{"movement":"Gentle movement","calm":"Calm and attention","coach":"Organization and planning"}[s],"pt":{"movement":"Movimento suave","calm":"Calma e atenção","coach":"Organização e planeamento"}[s]}[lang],"count":sum(1 for a in _CATALOG if a["section"]==s)} for s in SECTIONS]

def get_activities(lang="es",section="all"):
    lang=_lang(lang)
    if section not in ("all",*SECTIONS):section="all"
    return [_public_activity(a,lang) for a in _CATALOG if section=="all" or a["section"]==section]

def get_activity(activity_id,lang="es"):
    item=_BY_ID.get(str(activity_id))
    return _public_activity(item,lang) if item else None

def get_plant(plant_id,lang="es"):
    return None

def _section_for_kind(kind):
    return {"pause":"calm","energy":"movement","calm":"calm","nature":"calm","coach":"coach","program":"coach","movement":"movement"}.get(kind,"calm")

def _duration(minutes):
    try:n=int(minutes)
    except (TypeError,ValueError):n=3
    return min(MINUTES_ALLOWED,key=lambda x:abs(x-n))

def _choose_activity(section,allow_repeat=False):
    pool=[a for a in _CATALOG if a["section"]==section]
    if not pool:pool=[a for a in _CATALOG if a["section"]=="calm"]
    if not allow_repeat:
        now=time.time()
        with _LOCK:
            recent={aid for aid,t in _HISTORY.items() if now-t<1800}
        fresh=[a for a in pool if a["id"] not in recent]
        if fresh:pool=fresh
    item=_RNG.choice(pool)
    with _LOCK:
        _HISTORY[item["id"]]=time.time()
        if len(_HISTORY)>_MAX_HISTORY:
            for k in sorted(_HISTORY,key=_HISTORY.get)[:len(_HISTORY)//4]:_HISTORY.pop(k,None)
    return item

def create_session_id(activity_id="",lang="es",minutes=3):
    seed=f"{activity_id}|{_lang(lang)}|{_duration(minutes)}|{time.time_ns()}|{_RNG.random()}"
    return hashlib.sha256(seed.encode()).hexdigest()[:20]

def get_session(lang="es",kind="pause",minutes=3,allow_repeat=False,section=None,activity_id=None):
    lang=_lang(lang);minutes=_duration(minutes)
    section=section if section in SECTIONS else _section_for_kind(kind)
    item=_BY_ID.get(str(activity_id)) if activity_id else None
    if item is None or item["section"]!=section:item=_choose_activity(section,allow_repeat)
    result=_public_activity(item,lang,minutes)
    result.update({
        "app":APP_NAME,"version":VERSION,"language":lang,
        "duration_seconds":minutes*60,
        "prompt_interval_seconds":PROMPT_INTERVAL_SECONDS,
        "session_id":create_session_id(item["id"],lang,minutes),
        "instructions":result["steps"],"total_steps":len(result["steps"]),
        "allow_repeat":bool(allow_repeat),"can_clear":True
    })
    return result

_PROGRAM=[
("calm","Comenzar con calma","Begin calmly","Começar com calma","Dedica unos minutos a observar el presente.","Spend a few minutes noticing the present.","Dedique alguns minutos a observar o presente."),
("coach","Elegir una prioridad","Choose a priority","Escolher uma prioridade","Identifica una prioridad pequeña y un primer paso.","Identify one small priority and a first step.","Identifique uma pequena prioridade e um primeiro passo."),
("movement","Moverse suavemente","Move gently","Movimentar-se suavemente","Prueba movimientos cómodos sin forzar el cuerpo.","Try comfortable movements without forcing your body.","Experimente movimentos confortáveis sem forçar o corpo."),
("calm","Hacer una pausa","Take a pause","Fazer uma pausa","Haz una pausa breve y vuelve a tu ritmo.","Take a short pause and return at your own pace.","Faça uma pausa breve e retome o seu ritmo."),
("coach","Preparar el siguiente paso","Prepare the next step","Preparar o próximo passo","Organiza algo concreto que te ayude a continuar.","Organize one concrete thing that helps you continue.","Organize algo concreto que ajude a continuar."),
("movement","Recuperar comodidad","Restore comfort","Recuperar o conforto","Elige movimientos suaves que te resulten cómodos.","Choose gentle movements that feel comfortable.","Escolha movimentos suaves que sejam confortáveis."),
("calm","Cerrar la semana","Close the week","Concluir a semana","Reconoce lo que probaste y elige qué te gustaría repetir.","Notice what you tried and choose what you would like to repeat.","Reconheça o que experimentou e escolha o que gostaria de repetir.")
]

def get_program_day(lang="es",day=1):
    lang=_lang(lang)
    try:day=max(1,min(7,int(day)))
    except (TypeError,ValueError):day=1
    row=_PROGRAM[day-1];section=row[0]
    item=_choose_activity(section,allow_repeat=True)
    return {
        "day":day,"language":lang,"minutes":5,
        "title":row[1+LANGUAGES.index(lang)],
        "goal":row[4+LANGUAGES.index(lang)],
        "description":row[4+LANGUAGES.index(lang)],
        "activity":_public_activity(item,lang,5)
    }

def get_health():
    return {"status":"ok","app":APP_NAME,"version":VERSION,"languages":list(LANGUAGES),"sections":list(SECTIONS),"activity_count":len(_CATALOG)}

def get_config():
    return {"name":APP_NAME,"company":COMPANY,"version":VERSION,"languages":list(LANGUAGES),"durations":list(MINUTES_ALLOWED),"program_days":7,"sections":get_catalog(),"activity_count":len(_CATALOG),"prompt_interval_seconds":PROMPT_INTERVAL_SECONDS}

catalog=get_catalog
activities=get_activities
activity=get_activity
session=get_session
plant=get_plant
program_day=get_program_day
health=get_health
config=get_config
