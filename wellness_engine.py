from __future__ import annotations
import random,time,hashlib,threading
VERSION="6.2.0"
APP_NAME="WELLNESS COACH"
COMPANY="May Roga LLC"
PROMPT_INTERVAL_SECONDS=6
MINUTES_ALLOWED=(3,5,10)
LANGUAGES=("es","en","pt")
SECTIONS=("movement","calm","coach")
_LOCK=threading.RLock()
_RNG=random.SystemRandom()

def _b(es,en,lang="es",pt=None):
    if lang=="pt":return pt or en
    return en if lang=="en" else es

_STEPS={
"calm":[
('Apoya los pies y nota el contacto con el suelo.','Place your feet down and notice their contact with the floor.'),
('Mira un punto cómodo delante de ti.','Look at a comfortable point in front of you.'),
('Suelta los hombros solo hasta donde resulte natural.','Let your shoulders soften only as much as feels natural.'),
('Inhala con suavidad, sin forzar el aire.','Breathe in gently without forcing the air.'),
('Deja que la exhalación siga su propio ritmo.','Let the exhale follow its own rhythm.'),
('Nota tres cosas que puedes ver.','Notice three things you can see.'),
('Escucha un sonido cercano y otro lejano.','Listen for one nearby sound and one distant sound.'),
('Relaja las manos si te resulta cómodo.','Relax your hands if comfortable.'),
('Observa el apoyo de la espalda o del asiento.','Notice the support of your back or seat.'),
('Permite que la respiración sea normal.','Allow your breathing to remain natural.'),
('Mira cómo cambia la luz en tu entorno.','Notice how light changes in your surroundings.'),
('Nombra mentalmente un detalle agradable o neutral.','Silently name one pleasant or neutral detail.'),
('Afloja la mandíbula sin apretar los dientes.','Unclench your jaw without pressing your teeth together.'),
('Nota la temperatura del aire en la piel.','Notice the air temperature on your skin.'),
('Deja pasar un pensamiento sin tener que resolverlo ahora.','Let a thought pass without needing to solve it now.'),
('Vuelve con atención a los pies.','Bring your attention back to your feet.'),
('Elige una palabra sencilla para este momento.','Choose a simple word for this moment.'),
('Haz una pausa breve antes del siguiente movimiento.','Pause briefly before your next movement.'),
('Observa cómo te encuentras sin juzgarte.','Notice how you feel without judging yourself.'),
('Decide cuál será tu siguiente paso pequeño.','Choose your next small step.')
],
"movement":[
('Siéntate o ponte de pie de forma estable.','Sit or stand in a stable position.'),
('Comprueba que tienes espacio a tu alrededor.','Check that you have space around you.'),
('Mueve lentamente los dedos de las manos.','Slowly move your fingers.'),
('Haz círculos pequeños con los hombros si te resulta cómodo.','Make small shoulder circles if comfortable.'),
('Mira a un lado y luego al centro, sin forzar el cuello.','Look to one side and then center without straining your neck.'),
('Abre y cierra las manos con suavidad.','Gently open and close your hands.'),
('Estira los dedos y después suéltalos.','Stretch your fingers and then release.'),
('Mueve los tobillos dentro de un rango cómodo.','Move your ankles within a comfortable range.'),
('Si estás sentado, cambia suavemente el apoyo de los pies.','If seated, gently shift how your feet rest.'),
('Si estás de pie, reparte el peso sin perder estabilidad.','If standing, distribute your weight while staying stable.'),
('Alarga la columna sin arquear la espalda.','Lengthen your spine without arching your back.'),
('Deja que los brazos descansen antes del siguiente movimiento.','Let your arms rest before the next movement.'),
('Realiza una elevación pequeña de talones si es seguro.','Raise your heels slightly if safe.'),
('Vuelve a una postura cómoda.','Return to a comfortable posture.'),
('Haz un movimiento lento que te resulte fácil.','Make one slow movement that feels easy.'),
('Detente si aparece dolor, mareo o malestar.','Stop if pain, dizziness or discomfort appears.'),
('Comprueba que puedes respirar con normalidad.','Check that you can breathe normally.'),
('Reduce el recorrido si lo necesitas.','Reduce the range if needed.'),
('Relaja las partes del cuerpo que no estás moviendo.','Relax body parts you are not moving.'),
('Termina con una postura estable y cómoda.','Finish in a stable, comfortable posture.')
],
"coach":[
('Elige una sola cosa que quieras atender ahora.','Choose one thing you want to focus on now.'),
('Describe el objetivo con palabras sencillas.','Describe the goal in simple words.'),
('Distingue lo que puedes hacer de lo que no controlas.','Separate what you can do from what you cannot control.'),
('Divide la tarea en un paso pequeño.','Break the task into one small step.'),
('Piensa qué necesitas tener a mano.','Consider what you need to have ready.'),
('Calcula un tiempo realista para empezar.','Estimate a realistic time to begin.'),
('Retira una distracción si está a tu alcance.','Remove one distraction if you can.'),
('Decide qué significa terminar ese primer paso.','Decide what finishing the first step means.'),
('Piensa en una dificultad posible sin anticipar todas las demás.','Consider one possible difficulty without anticipating every other one.'),
('Elige una alternativa sencilla si aparece esa dificultad.','Choose a simple alternative if that difficulty appears.'),
('Haz una pausa para revisar tu plan.','Pause to review your plan.'),
('Comprueba si tu primer paso sigue siendo realista.','Check whether your first step is still realistic.'),
('Reduce el objetivo si ahora parece demasiado grande.','Scale down the goal if it feels too large now.'),
('Piensa qué información necesitas y dónde verificarla.','Consider what information you need and where to verify it.'),
('Elige cuándo comenzar, aunque sea por poco tiempo.','Choose when to begin, even briefly.'),
('Decide cómo recordarás el siguiente paso.','Decide how you will remember the next step.'),
('Reconoce el esfuerzo de organizarte.','Acknowledge the effort of getting organized.'),
('Evita exigirte resolverlo todo en este momento.','Avoid demanding that you solve everything right now.'),
('Resume tu plan en una frase.','Summarize your plan in one sentence.'),
('Elige una acción concreta para después de esta sesión.','Choose one concrete action for after this session.')
]}

_TITLES={
"calm":[('Pausa consciente','Mindful pause'),('Respirar sin prisa','Unhurried breathing'),('Atención al presente','Attention to the present'),('Un minuto de quietud','A moment of stillness'),('Escucha tranquila','Quiet listening'),('Soltar tensión cotidiana','Release everyday tension'),('Volver al momento','Return to the moment'),('Pausa de los sentidos','Sensory pause'),('Descanso de atención','Attention break'),('Un espacio de calma','A space for calm'),('Respiración natural','Natural breathing'),('Observar sin juzgar','Observe without judgment'),('Pausa de los hombros','Shoulder pause'),('Escucha del entorno','Listening to your surroundings'),('Atención amable','Gentle attention'),('Descanso breve','Short rest'),('Punto de apoyo','A point of support'),('Pausa entre tareas','Pause between tasks'),('Un momento para ti','A moment for yourself'),('Cerrar con calma','Finish calmly')],
"movement":[('Movimiento suave','Gentle movement'),('Despertar las manos','Wake up your hands'),('Hombros cómodos','Comfortable shoulders'),('Movilidad de tobillos','Ankle mobility'),('Pausa activa','Active break'),('Cambiar de postura','Change posture'),('Estiramiento ligero','Light stretching'),('Movimiento sentado','Seated movement'),('Movimiento de pie','Standing movement'),('Soltar las manos','Release your hands'),('Postura estable','Stable posture'),('Pequeños movimientos','Small movements'),('Activar el cuerpo con suavidad','Gently activate your body'),('Descanso del escritorio','Desk break'),('Movimiento consciente','Mindful movement'),('Movilidad sin prisa','Unhurried mobility'),('Pausa para el cuerpo','A pause for your body'),('Movimiento accesible','Accessible movement'),('Volver a una postura cómoda','Return to a comfortable posture'),('Terminar con equilibrio','Finish with balance')],
"coach":[('Plan de un paso','One-step plan'),('Organizar sin prisa','Organize without rushing'),('Elegir una prioridad','Choose a priority'),('Preparar el siguiente paso','Prepare the next step'),('Reducir una tarea','Make a task smaller'),('Claridad para empezar','Clarity to begin'),('Resolver una cosa','Handle one thing'),('Tiempo realista','Realistic timing'),('Plan sencillo','Simple plan'),('Preparación práctica','Practical preparation'),('Enfoque amable','Gentle focus'),('Revisar opciones','Review options'),('Un objetivo posible','An achievable goal'),('Pausa para decidir','Pause to decide'),('Ordenar las ideas','Organize your thoughts'),('Preparar el entorno','Prepare your surroundings'),('Elegir qué sigue','Choose what comes next'),('Menos pasos, más claridad','Fewer steps, more clarity'),('Un comienzo concreto','A concrete start'),('Cerrar con una decisión','Finish with a decision')]
}

_STEPS_PT={
"calm":[
'Apoie os pés e perceba o contato com o chão.','Olhe para um ponto confortável à sua frente.','Relaxe os ombros apenas até onde for natural.','Inspire suavemente, sem forçar o ar.','Deixe a expiração seguir seu próprio ritmo.','Perceba três coisas que você consegue ver.','Escute um som próximo e outro distante.','Relaxe as mãos, se isso for confortável.','Perceba o apoio das costas ou do assento.','Permita que a respiração permaneça natural.','Observe como a luz muda ao seu redor.','Nomeie mentalmente um detalhe agradável ou neutro.','Relaxe a mandíbula sem apertar os dentes.','Perceba a temperatura do ar na pele.','Deixe um pensamento passar sem precisar resolvê-lo agora.','Volte a atenção para os pés.','Escolha uma palavra simples para este momento.','Faça uma breve pausa antes do próximo movimento.','Perceba como você está, sem se julgar.','Escolha qual será seu próximo pequeno passo.'],
"movement":[
'Sente-se ou fique em pé de forma estável.','Confira se há espaço ao seu redor.','Mova lentamente os dedos das mãos.','Faça pequenos círculos com os ombros, se for confortável.','Olhe para um lado e depois volte ao centro, sem forçar o pescoço.','Abra e feche as mãos suavemente.','Alongue os dedos e depois relaxe.','Movimente os tornozelos dentro de um limite confortável.','Se estiver sentado, mude suavemente o apoio dos pés.','Se estiver em pé, distribua o peso sem perder a estabilidade.','Alongue a coluna sem arquear as costas.','Deixe os braços descansarem antes do próximo movimento.','Eleve um pouco os calcanhares, se for seguro.','Volte a uma posição confortável.','Faça um movimento lento que seja fácil para você.','Pare se sentir dor, tontura ou desconforto.','Confira se consegue respirar normalmente.','Diminua a amplitude do movimento, se necessário.','Relaxe as partes do corpo que não estão se movendo.','Termine em uma posição estável e confortável.'],
"coach":[
'Escolha uma coisa em que queira se concentrar agora.','Descreva o objetivo com palavras simples.','Separe o que você pode fazer daquilo que não controla.','Divida a tarefa em uma pequena etapa.','Pense no que precisa ter à mão.','Estime um tempo realista para começar.','Afaste uma distração, se puder.','Defina o que significa concluir essa primeira etapa.','Pense em uma possível dificuldade sem antecipar todas as outras.','Escolha uma alternativa simples caso essa dificuldade apareça.','Faça uma pausa para revisar seu plano.','Confira se sua primeira etapa continua realista.','Reduza o objetivo se ele parecer grande demais agora.','Pense de que informação precisa e onde pode verificá-la.','Escolha quando começar, mesmo que seja por pouco tempo.','Decida como vai se lembrar da próxima etapa.','Reconheça o esforço que está fazendo para se organizar.','Não exija resolver tudo neste momento.','Resuma seu plano em uma frase.','Escolha uma ação concreta para depois desta sessão.']
}

_TITLES_PT={
"calm":['Pausa consciente','Respirar sem pressa','Atenção ao presente','Um momento de quietude','Escuta tranquila','Soltar a tensão cotidiana','Voltar ao momento','Pausa dos sentidos','Pausa para a atenção','Um espaço de calma','Respiração natural','Observar sem julgar','Pausa para os ombros','Escutar o ambiente','Atenção gentil','Descanso breve','Um ponto de apoio','Pausa entre tarefas','Um momento para você','Terminar com calma'],
"movement":['Movimento suave','Despertar as mãos','Ombros confortáveis','Mobilidade dos tornozelos','Pausa ativa','Mudar de postura','Alongamento leve','Movimento sentado','Movimento em pé','Relaxar as mãos','Postura estável','Pequenos movimentos','Ativar o corpo suavemente','Pausa da mesa de trabalho','Movimento consciente','Mobilidade sem pressa','Uma pausa para o corpo','Movimento acessível','Voltar a uma postura confortável','Terminar com equilíbrio'],
"coach":['Plano de uma etapa','Organizar sem pressa','Escolher uma prioridade','Preparar a próxima etapa','Simplificar uma tarefa','Clareza para começar','Resolver uma coisa','Tempo realista','Plano simples','Preparação prática','Foco gentil','Revisar opções','Um objetivo possível','Pausa para decidir','Organizar as ideias','Preparar o ambiente','Escolher o próximo passo','Menos etapas, mais clareza','Um começo concreto','Terminar com uma decisão']
}

_DESCRIPTIONS={
"calm":{"es":"Una pausa general de atención al presente, sin promesas médicas ni necesidad de cambiar la respiración.","en":"A general present-moment pause, with no medical promises or need to change your breathing.","pt":"Uma pausa geral para prestar atenção ao momento presente, sem promessas médicas nem necessidade de mudar a respiração."},
"movement":{"es":"Movimiento cotidiano suave y adaptable. Haz solo lo que resulte cómodo y seguro.","en":"Gentle, adaptable everyday movement. Do only what feels comfortable and safe.","pt":"Movimento cotidiano suave e adaptável. Faça apenas o que for confortável e seguro."},
"coach":{"es":"Una actividad sencilla para organizar prioridades y elegir un siguiente paso práctico.","en":"A simple activity to organize priorities and choose a practical next step.","pt":"Uma atividade simples para organizar prioridades e escolher o próximo passo prático."}
}

def _valid_lang(lang):
    lang=str(lang or "es").strip().lower()
    return lang if lang in LANGUAGES else "es"

def _valid_section(section):
    section=str(section or "all").strip().lower()
    return section if section in (*SECTIONS,"all") else "all"

def _duration(value):
    try:value=int(value)
    except (TypeError,ValueError):value=3
    return value if value in MINUTES_ALLOWED else min(MINUTES_ALLOWED,key=lambda x:abs(x-value))

def _steps_for(section,index,lang=None,plant=None):
    base=_STEPS[section]
    shift=(index*3)%len(base)
    ordered=base[shift:]+base[:shift]
    pt_base=_STEPS_PT[section]
    pt_ordered=pt_base[shift:]+pt_base[:shift]
    steps=[(pair[0],pair[1],pt) for pair,pt in zip(ordered,pt_ordered)]
    if lang is None:return steps
    lang=_valid_lang(lang)
    return [step[2] if lang=="pt" else step[1] if lang=="en" else step[0] for step in steps]

def _build_catalog():
    catalog=[]
    for section in ("movement","calm","coach"):
        for i,(title_es,title_en) in enumerate(_TITLES[section]):
            aid=f"{section}_{i+1:02d}"
            catalog.append({"id":aid,"section":section,"title":{"es":title_es,"en":title_en,"pt":_TITLES_PT[section][i]},"description":_DESCRIPTIONS[section],"steps":_steps_for(section,i),"plant_id":None,"index":i})
    return catalog

_CATALOG=_build_catalog()
_BY_ID={item["id"]:item for item in _CATALOG}

def _public_activity(item,lang="es",minutes=None):
    lang=_valid_lang(lang)
    localized_steps=[]
    for step in item.get("steps",[]):
        if isinstance(step,(tuple,list)) and len(step)>=3:
            localized_steps.append(step[2] if lang=="pt" else step[1] if lang=="en" else step[0])
        elif isinstance(step,(tuple,list)) and len(step)>=2:
            localized_steps.append(step[1] if lang=="en" else step[0])
        elif isinstance(step,dict):
            localized_steps.append(str(step.get(lang) or step.get("es") or step.get("en") or ""))
        else:
            localized_steps.append(str(step))
    data={"id":item["id"],"section":item["section"],"title":item["title"].get(lang,item["title"]["es"]),"description":item["description"].get(lang,item["description"]["es"]),"steps":localized_steps,"plant_id":None,"step_count":len(localized_steps)}
    if minutes is not None:data["minutes"]=_duration(minutes)
    return data

def get_catalog(lang="es"):
    lang=_valid_lang(lang)
    names={"calm":{"es":"Calma y atención","en":"Calm and attention","pt":"Calma e atenção"},"movement":{"es":"Movimiento suave","en":"Gentle movement","pt":"Movimento suave"},"coach":{"es":"Coach y planificación","en":"Coaching and planning","pt":"Rotinas cotidianas"}}
    counts={s:sum(1 for a in _CATALOG if a["section"]==s) for s in SECTIONS}
    return {"app":APP_NAME,"company":COMPANY,"version":VERSION,"language":lang,"languages":list(LANGUAGES),"sections":[{"id":s,"name":names[s][lang],"count":counts[s]} for s in SECTIONS],"activities":[_public_activity(a,lang) for a in _CATALOG],"plant_count":0,"durations":list(MINUTES_ALLOWED),"prompt_interval_seconds":PROMPT_INTERVAL_SECONDS}

def get_activities(lang="es",section="all"):
    lang=_valid_lang(lang)
    raw_section=str(section or "all").strip().lower()
    if raw_section in ("plants","nature"):return []
    section=_valid_section(raw_section)
    return [_public_activity(a,lang) for a in _CATALOG if section=="all" or a["section"]==section]

def get_activity(activity_id,lang="es"):
    if not activity_id:return None
    item=_BY_ID.get(str(activity_id))
    return _public_activity(item,lang) if item else None

def get_plant(plant_id,lang="es"):
    return None

def _section_for_kind(kind):
    kind=str(kind or "pause").lower().strip()
    return {"pause":"calm","energy":"movement","calm":"calm","nature":"calm","plants":"calm","movement":"movement","coach":"coach","routine":"coach","daily":"coach","program":"all"}.get(kind,"calm")

def create_session_id(activity_id="",minutes=3):
    raw=f"{activity_id}|{minutes}|{time.time_ns()}|{_RNG.random()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]

def get_session(activity_id=None,minutes=3,lang="es",activity=None,kind=None):
    if activity_id in LANGUAGES and isinstance(minutes,str) and str(lang).isdigit():
        old_lang,old_kind,old_minutes=activity_id,minutes,int(lang)
        activity_id=None;kind=old_kind;minutes=old_minutes;lang=old_lang
    lang=_valid_lang(lang);minutes=_duration(minutes)
    if isinstance(activity,dict):activity_id=activity.get("id",activity_id)
    item=_BY_ID.get(str(activity_id)) if activity_id else None
    if item is None:
        section=_section_for_kind(kind or activity_id)
        pool=[x for x in _CATALOG if section=="all" or x["section"]==section]
        if not pool:pool=[x for x in _CATALOG if x["section"]=="calm"]
        item=_RNG.choice(pool)
    result=_public_activity(item,lang,minutes)
    result.update({"app":APP_NAME,"version":VERSION,"language":lang,"duration_seconds":minutes*60,"prompt_interval_seconds":PROMPT_INTERVAL_SECONDS,"session_id":create_session_id(item["id"],minutes),"instructions":list(result["steps"]),"total_steps":len(result["steps"]),"voice_order":"show_text_then_speak_same_text"})
    return result

def get_program_day(lang="es",day=1):
    lang=_valid_lang(lang)
    try:day=int(day)
    except (TypeError,ValueError):day=1
    day=max(1,min(7,day))
    sequence=("calm","movement","coach","calm","movement","coach","coach")
    section=sequence[day-1]
    pool=[x for x in _CATALOG if x["section"]==section]
    item=pool[(day*7-7)%len(pool)]
    titles={"es":["Comenzar con calma","Moverse suavemente","Organizar un paso","Volver al presente","Moverse con comodidad","Elegir el siguiente paso","Cerrar con una decisión"],"en":["Begin calmly","Move gently","Organize one step","Return to the present","Move comfortably","Choose the next step","Finish with a decision"],"pt":["Começar com calma","Movimentar-se suavemente","Organizar uma etapa","Voltar ao presente","Movimentar-se com conforto","Escolher o próximo passo","Terminar com uma decisão"]}
    descriptions={"es":["Una pausa sencilla para empezar.","Prueba movimientos suaves y cómodos.","Elige una prioridad pequeña y realista.","Dedica unos minutos a notar tu entorno.","Prueba movimientos suaves sin forzar.","Elige un siguiente paso posible.","Termina la semana con una acción concreta."],"en":["A simple pause to begin.","Try gentle, comfortable movements.","Choose one small, realistic priority.","Spend a few minutes noticing your surroundings.","Try gentle movement without strain.","Choose one possible next step.","Finish the week with one concrete action."],"pt":["Uma pausa simples para começar.","Experimente movimentos suaves e confortáveis.","Escolha uma prioridade pequena e realista.","Dedique alguns minutos a perceber o ambiente.","Faça movimentos suaves sem forçar.","Escolha um próximo passo possível.","Termine a semana com uma ação concreta."]}
    mins=(3,5,3,5,10,5,10)[day-1]
    return {"day":day,"title":titles[lang][day-1],"description":descriptions[lang][day-1],"minutes":mins,"activity":_public_activity(item,lang,mins),"section":section,"prompt_interval_seconds":PROMPT_INTERVAL_SECONDS}

def get_health():
    return {"status":"ok","app":APP_NAME,"version":VERSION,"activities":len(_CATALOG),"plants":0,"plant_count":0,"durations":list(MINUTES_ALLOWED),"languages":list(LANGUAGES)}

def get_config():
    return {"name":APP_NAME,"company":COMPANY,"version":VERSION,"languages":list(LANGUAGES),"durations":list(MINUTES_ALLOWED),"sections":list(SECTIONS),"activity_count":len(_CATALOG),"plant_count":0,"program_days":7,"prompt_interval_seconds":PROMPT_INTERVAL_SECONDS,"voice_order":"show_text_then_speak_same_text"}

catalog=get_catalog
activities=get_activities
session=get_session
plant=get_plant
program_day=get_program_day
health=get_health
config=get_config
