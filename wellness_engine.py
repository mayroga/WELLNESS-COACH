import hashlib,random,time,threading
APP_NAME="WELLNESS COACH"
COMPANY="May Roga LLC"
VERSION="11.0.0"
LANGUAGES=("es","en","pt")
MINUTES_ALLOWED=(3,5,10)
SECTIONS=("all","calm","movement","coach")
PROMPT_INTERVAL_SECONDS=12
_RNG=random.Random()
_LOCK=threading.RLock()
_DAY_SECTIONS=("calm","movement","coach","calm","movement","coach","calm")
_DAY_MINUTES=(3,5,3,5,10,5,10)
_TITLES={
"calm":[
("Respirar con tranquilidad","Breathe with ease","Respire com tranquilidade"),
("Soltar la tensión del día","Release the day's tension","Solte a tensão do dia"),
("Hacer una pausa consciente","Take a mindful pause","Faça uma pausa consciente"),
("Descansar los hombros","Relax your shoulders","Relaxe os ombros"),
("Encontrar un ritmo sereno","Find a calm rhythm","Encontre um ritmo tranquilo"),
("Volver al momento presente","Return to the present","Volte ao momento presente"),
("Dar espacio a la calma","Make room for calm","Dê espaço à calma"),
("Relajar el rostro","Relax your face","Relaxe o rosto"),
("Respirar sin prisa","Breathe without rushing","Respire sem pressa"),
("Hacer una pausa amable","Take a gentle pause","Faça uma pausa gentil"),
("Reconocer cómo se siente el cuerpo","Notice how your body feels","Perceba como seu corpo se sente"),
("Dejar ir la tensión innecesaria","Release unnecessary tension","Solte a tensão desnecessária"),
("Descansar la mente unos minutos","Give your mind a short rest","Descanse a mente por alguns minutos"),
("Recuperar la atención con suavidad","Gently regain your attention","Recupere a atenção com suavidade"),
("Crear un momento de quietud","Create a moment of stillness","Crie um momento de tranquilidade"),
("Respirar con comodidad","Breathe comfortably","Respire com conforto"),
("Bajar el ritmo por un momento","Slow down for a moment","Diminua o ritmo por um momento"),
("Practicar una pausa tranquila","Practice a calm pause","Pratique uma pausa tranquila"),
("Notar el apoyo de los pies","Notice the support beneath your feet","Perceba o apoio sob os pés"),
("Terminar con serenidad","Finish with serenity","Termine com serenidade")],
"movement":[
("Mover el cuerpo con suavidad","Move your body gently","Movimente o corpo suavemente"),
("Despertar los hombros","Wake up your shoulders","Desperte os ombros"),
("Estirar los brazos cómodamente","Stretch your arms comfortably","Alongue os braços com conforto"),
("Soltar las manos y las muñecas","Relax your hands and wrists","Relaxe as mãos e os pulsos"),
("Movilidad suave sentado","Gentle seated mobility","Mobilidade suave sentado"),
("Dar unos pasos conscientes","Take a few mindful steps","Dê alguns passos com atenção"),
("Activar los tobillos","Move your ankles","Movimente os tornozelos"),
("Estirar la espalda sin forzar","Stretch your back without strain","Alongue as costas sem forçar"),
("Mover el cuello con cuidado","Move your neck carefully","Movimente o pescoço com cuidado"),
("Cambiar de postura con comodidad","Change position comfortably","Mude de posição com conforto"),
("Despertar el cuerpo poco a poco","Gently wake up your body","Desperte o corpo aos poucos"),
("Coordinar brazos y respiración","Coordinate your arms and breathing","Coordene braços e respiração"),
("Pausar el tiempo sentado","Take a seated movement break","Faça uma pausa de movimento sentado"),
("Aflojar las piernas","Loosen your legs","Relaxe as pernas"),
("Practicar equilibrio con apoyo","Practice balance with support","Pratique equilíbrio com apoio"),
("Mover las manos con intención","Move your hands with intention","Movimente as mãos com intenção"),
("Hacer una pausa activa","Take an active break","Faça uma pausa ativa"),
("Recuperar movilidad cotidiana","Support everyday mobility","Estimule a mobilidade cotidiana"),
("Estirar sin llegar al dolor","Stretch without reaching pain","Alongue sem chegar à dor"),
("Terminar con movimientos suaves","Finish with gentle movements","Termine com movimentos suaves")],
"coach":[
("Preparar el día con claridad","Prepare your day with clarity","Prepare o dia com clareza"),
("Elegir una prioridad realista","Choose one realistic priority","Escolha uma prioridade realista"),
("Organizar el próximo paso","Organize the next step","Organize o próximo passo"),
("Crear una pausa en la rutina","Make room for a routine break","Crie uma pausa na rotina"),
("Dividir una tarea en pasos","Break a task into steps","Divida uma tarefa em etapas"),
("Ordenar el espacio inmediato","Organize your immediate space","Organize o espaço ao seu redor"),
("Planificar un descanso breve","Plan a short rest","Planeje um breve descanso"),
("Reconocer lo que ya está hecho","Notice what is already done","Reconheça o que já foi feito"),
("Elegir un ritmo sostenible","Choose a sustainable pace","Escolha um ritmo sustentável"),
("Simplificar una tarea cotidiana","Simplify an everyday task","Simplifique uma tarefa cotidiana"),
("Prepararse para una transición","Prepare for a transition","Prepare-se para uma mudança de atividade"),
("Hacer una cosa a la vez","Do one thing at a time","Faça uma coisa de cada vez"),
("Crear un hábito pequeño","Build a small habit","Crie um pequeno hábito"),
("Recordar una pausa necesaria","Remember to take a needed break","Lembre-se de fazer uma pausa necessária"),
("Revisar el día sin juzgarse","Review the day without judgment","Revise o dia sem se julgar"),
("Poner límites al ritmo diario","Set limits on your daily pace","Estabeleça limites para o ritmo diário"),
("Elegir qué puede esperar","Choose what can wait","Escolha o que pode esperar"),
("Preparar un cierre tranquilo","Prepare a calm ending","Prepare um encerramento tranquilo"),
("Dar valor a un pequeño avance","Value a small step forward","Valorize um pequeno avanço"),
("Elegir el siguiente paso posible","Choose the next possible step","Escolha o próximo passo possível")]
}
_DESCRIPTIONS={
"calm":{"es":"Una pausa sencilla para recuperar tranquilidad, sin exigencias ni prisa.","en":"A simple pause to regain calm, without pressure or rushing.","pt":"Uma pausa simples para recuperar a tranquilidade, sem pressão nem pressa."},
"movement":{"es":"Movimientos cotidianos suaves. Haz solo lo que te resulte cómodo y estable.","en":"Gentle everyday movements. Do only what feels comfortable and steady.","pt":"Movimentos suaves do dia a dia. Faça apenas o que for confortável e estável."},
"coach":{"es":"Una guía práctica para organizar el día y elegir un siguiente paso realista.","en":"Practical guidance to organize your day and choose a realistic next step.","pt":"Orientação prática para organizar o dia e escolher o próximo passo realista."}
}
_STEP_TEXT={
"calm":{
"es":[
"Adopta una postura cómoda y estable. Puedes permanecer sentado.",
"Lee esta indicación y permite que tu respiración siga su ritmo natural.",
"Afloja suavemente la mandíbula, las manos y los hombros, sin forzar.",
"Quédate con una sola sensación cómoda. No necesitas conseguir nada especial.",
"Nota cómo estás ahora y prepárate para continuar a tu propio ritmo."],
"en":[
"Choose a comfortable, stable position. You may remain seated.",
"Read this instruction and let your breathing keep its natural rhythm.",
"Softly relax your jaw, hands, and shoulders without forcing them.",
"Stay with one comfortable sensation. You do not need to achieve anything special.",
"Notice how you feel now and prepare to continue at your own pace."],
"pt":[
"Escolha uma posição confortável e estável. Você pode permanecer sentado.",
"Leia esta instrução e deixe a respiração seguir seu ritmo natural.",
"Relaxe suavemente a mandíbula, as mãos e os ombros, sem forçar.",
"Permaneça com uma sensação confortável. Você não precisa alcançar nada especial.",
"Perceba como você está agora e prepare-se para continuar no seu ritmo."]},
"movement":{
"es":[
"Colócate en una posición estable. Si lo necesitas, permanece sentado.",
"Comienza con un movimiento pequeño y lento, sin rebotes ni esfuerzo.",
"Continúa solo dentro de un rango cómodo. Respira con naturalidad.",
"Reduce el movimiento o descansa si notas dolor, mareo o falta de estabilidad.",
"Detén el movimiento con calma y vuelve a una posición cómoda."],
"en":[
"Get into a stable position. Remain seated if that helps.",
"Begin with a small, slow movement, without bouncing or straining.",
"Continue only within a comfortable range. Breathe naturally.",
"Reduce the movement or rest if you notice pain, dizziness, or instability.",
"Stop the movement calmly and return to a comfortable position."],
"pt":[
"Fique em uma posição estável. Permaneça sentado se isso ajudar.",
"Comece com um movimento pequeno e lento, sem impulsos nem esforço.",
"Continue apenas dentro de uma amplitude confortável. Respire naturalmente.",
"Reduza o movimento ou descanse se sentir dor, tontura ou falta de estabilidade.",
"Interrompa o movimento com calma e volte a uma posição confortável."]},
"coach":{
"es":[
"Observa qué necesitas atender ahora, sin intentar resolverlo todo a la vez.",
"Elige una sola tarea o intención que sea realista para este momento.",
"Divídela mentalmente en un paso pequeño y concreto.",
"Decide cuándo o cómo darás ese paso, dejando margen para descansar.",
"Resume tu próximo paso en una frase sencilla y termina sin exigirte más."],
"en":[
"Notice what needs your attention now, without trying to solve everything at once.",
"Choose one task or intention that is realistic for this moment.",
"Break it down mentally into one small, concrete step.",
"Decide when or how to take that step, leaving room to rest.",
"Summarize your next step in one simple sentence and finish without demanding more of yourself."],
"pt":[
"Perceba o que precisa da sua atenção agora, sem tentar resolver tudo de uma vez.",
"Escolha uma tarefa ou intenção realista para este momento.",
"Divida-a mentalmente em uma etapa pequena e concreta.",
"Decida quando ou como dará esse passo, deixando espaço para descansar.",
"Resuma o próximo passo em uma frase simples e termine sem exigir demais de si."]
}}
def _valid_lang(lang):
    lang=str(lang or "es").lower().strip()
    return lang if lang in LANGUAGES else "es"
def _valid_section(section):
    section=str(section or "all").lower().strip()
    return section if section in SECTIONS else "all"
def _duration(value):
    try: value=int(value)
    except (TypeError,ValueError): value=3
    return min(MINUTES_ALLOWED,key=lambda n:abs(n-value))
def _make_catalog():
    out=[]
    for section,titles in _TITLES.items():
        for i,title in enumerate(titles,1):
            out.append({"id":f"{section}_{i:02d}","section":section,"title":dict(zip(LANGUAGES,title)),"description":_DESCRIPTIONS[section],"steps":_STEP_TEXT[section],"plant_id":None,"step_count":5})
    return out
_CATALOG=_make_catalog()
_BY_ID={x["id"]:x for x in _CATALOG}
def _public_activity(item,lang="es",minutes=None):
    lang=_valid_lang(lang)
    result={"id":item["id"],"section":item["section"],"title":item["title"][lang],"description":item["description"][lang],"steps":list(item["steps"][lang]),"instructions":list(item["steps"][lang]),"step_count":len(item["steps"][lang]),"plant_id":None,"language":lang}
    if minutes is not None:
        duration=_duration(minutes)
        result.update({"minutes":duration,"duration_minutes":duration,"duration_seconds":duration*60,"step_interval_seconds":duration*60/len(result["steps"]),"prompt_interval_seconds":duration*60/len(result["steps"])})
    return result
def get_catalog(lang="es"):
    lang=_valid_lang(lang)
    return {"app":APP_NAME,"company":COMPANY,"version":VERSION,"language":lang,"languages":list(LANGUAGES),"sections":[{"id":"calm","name":{"es":"Calma","en":"Calm","pt":"Calma"}[lang]},{"id":"movement","name":{"es":"Movimiento suave","en":"Gentle movement","pt":"Movimento suave"}[lang]},{"id":"coach","name":{"es":"Rutinas cotidianas","en":"Everyday routines","pt":"Rotinas cotidianas"}[lang]}],"activities":[_public_activity(x,lang) for x in _CATALOG],"activity_count":len(_CATALOG),"plant_count":0,"durations":list(MINUTES_ALLOWED),"program_days":7,"prompt_interval_seconds":PROMPT_INTERVAL_SECONDS}
def get_activities(lang="es",section="all"):
    lang=_valid_lang(lang); section=_valid_section(section)
    return [_public_activity(x,lang) for x in _CATALOG if section=="all" or x["section"]==section]
def get_activity(activity_id,lang="es"):
    item=_BY_ID.get(str(activity_id or ""))
    return _public_activity(item,lang) if item else None
def get_plant(plant_id,lang="es"):
    return None
def _section_for_kind(kind):
    kind=str(kind or "calm").lower().strip()
    mapping={"pause":"calm","energy":"movement","calm":"calm","movement":"movement","coach":"coach","routine":"coach","daily":"coach","program":"all"}
    return mapping.get(kind,kind if kind in SECTIONS else "calm")
def create_session_id(activity_id="",minutes=3):
    raw=f"{activity_id}|{minutes}|{time.time_ns()}|{random.random()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]
def get_session(activity_id=None,minutes=3,lang="es",activity=None,kind=None,**kwargs):
    # Compatible with older positional calls: get_session(lang,kind,minutes)
    if activity_id in LANGUAGES and isinstance(minutes,str) and str(lang).isdigit():
        old_lang,old_kind,old_minutes=activity_id,minutes,int(lang)
        activity_id=None; kind=old_kind; minutes=old_minutes; lang=old_lang
    lang=_valid_lang(lang); duration=_duration(minutes)
    if isinstance(activity,dict) and activity.get("id"):
        activity_id=activity["id"]
    item=_BY_ID.get(str(activity_id or ""))
    if item is None:
        section=_section_for_kind(kind or activity_id)
        pool=[x for x in _CATALOG if section=="all" or x["section"]==section]
        if not pool: pool=[x for x in _CATALOG if x["section"]=="calm"]
        with _LOCK: item=_RNG.choice(pool)
    result=_public_activity(item,lang,duration)
    result.update({"app":APP_NAME,"version":VERSION,"session_id":create_session_id(item["id"],duration),"total_steps":len(result["steps"]),"instructions":list(result["steps"]),"duration_seconds":duration*60,"step_interval_seconds":duration*60/len(result["steps"]),"prompt_interval_seconds":duration*60/len(result["steps"]),"timing_mode":"duration_divided_equally_between_visible_steps","voice_order":"show_text_then_speak_same_text"})
    return result
def get_program_day(lang="es",day=1):
    lang=_valid_lang(lang)
    try: day=max(1,min(7,int(day)))
    except (TypeError,ValueError): day=1
    section=_DAY_SECTIONS[day-1]; duration=_DAY_MINUTES[day-1]
    pool=[x for x in _CATALOG if x["section"]==section]
    item=pool[(day*3-3)%len(pool)]
    labels={"es":f"Día {day} de 7","en":f"Day {day} of 7","pt":f"Dia {day} de 7"}
    descriptions={"es":"Una propuesta breve y flexible. Adáptala a tu comodidad.","en":"A short, flexible suggestion. Adapt it to your comfort.","pt":"Uma proposta breve e flexível. Adapte-a ao seu conforto."}
    return {"app":APP_NAME,"version":VERSION,"language":lang,"day":day,"total_days":7,"title":labels[lang],"description":descriptions[lang],"section":section,"minutes":duration,"duration_minutes":duration,"duration_seconds":duration*60,"prompt_interval_seconds":duration*60/5,"activity":_public_activity(item,lang,duration)}
def get_health():
    return {"status":"ok","app":APP_NAME,"company":COMPANY,"version":VERSION,"activity_count":len(_CATALOG),"plant_count":0,"durations":list(MINUTES_ALLOWED),"languages":list(LANGUAGES),"sections":list(SECTIONS[1:])}
def get_config():
    return {"name":APP_NAME,"company":COMPANY,"version":VERSION,"languages":list(LANGUAGES),"durations":list(MINUTES_ALLOWED),"sections":list(SECTIONS),"activity_count":len(_CATALOG),"plant_count":0,"program_days":7,"prompt_interval_seconds":PROMPT_INTERVAL_SECONDS,"voice_order":"show_text_then_speak_same_text"}
catalog=get_catalog
activities=get_activities
session=get_session
plant=get_plant
program_day=get_program_day
health=get_health
config=get_config
