from __future__ import annotations
import random,time,datetime,hashlib,threading
from copy import deepcopy

VERSION="9.0.0"
APP_NAME="WELLNESS COACH"
COMPANY="May Roga LLC"
AUDIENCE="40+"
PROMPT_INTERVAL_SECONDS=10
MINUTES_ALLOWED=(3,5,10)
LANGUAGES=("es","en","pt")
SECTIONS=("calm","movement","focus","routines")
_LOCK=threading.RLock()
_HISTORY=[]
_MAX_HISTORY=500

_TEXT={
"es":{
"app":"WELLNESS COACH",
"subtitle":"Pequeños pasos para tu bienestar cotidiano",
"sections":{
"calm":"Calma y atención",
"movement":"Movimiento suave",
"focus":"Organización y enfoque",
"routines":"Rutinas de bienestar"
},
"section_descriptions":{
"calm":"Pausas breves para bajar el ritmo, respirar con naturalidad y dirigir tu atención al presente.",
"movement":"Movimientos cotidianos suaves que puedes adaptar a tu comodidad y espacio.",
"focus":"Pequeños pasos para ordenar tus ideas, tus prioridades y tu entorno.",
"routines":"Hábitos sencillos para cuidar tu tiempo, tus descansos y tu día."
},
"start":"Comienza sin prisa. Adapta cada paso a tu comodidad.",
"finish":"Has completado esta actividad. Gracias por dedicarte este momento.",
"safety":"Adapta los movimientos a tu comodidad. Detente si sientes dolor, mareo, falta de aire o cualquier malestar. Esta aplicación ofrece orientación general de bienestar, no atención médica.",
"minutes":"minutos",
"step":"Paso",
"of":"de",
"today":"Hoy",
"day":"Día",
"program":"Programa de 7 días",
"no_repeat":"Evitar repetir actividades recientes",
"rating_question":"¿Cómo te resultó esta actividad?",
"rating_before":"Antes",
"rating_after":"Después",
"rating_low":"Necesito algo más sencillo",
"rating_ok":"Me resultó adecuada",
"rating_high":"Me sentí muy bien",
"saved":"Progreso guardado en este dispositivo.",
"not_found":"No se encontró la actividad.",
"choose":"Elige una actividad",
"duration":"Duración",
"complete":"Actividad completada",
"step_intro":"Haz este paso a tu propio ritmo.",
"rest":"Puedes descansar cuando lo necesites.",
"focus":"Enfoque",
"calm":"Calma",
"movement":"Movimiento",
"routines":"Rutinas",
"week_done":"Has llegado al final del programa semanal. Puedes repetirlo o elegir una actividad."
},
"en":{
"app":"WELLNESS COACH",
"subtitle":"Small steps for everyday well-being",
"sections":{
"calm":"Calm and attention",
"movement":"Gentle movement",
"focus":"Organization and focus",
"routines":"Everyday wellness routines"
},
"section_descriptions":{
"calm":"Short pauses to slow down, breathe naturally, and bring your attention to the present.",
"movement":"Gentle everyday movements that you can adapt to your comfort and space.",
"focus":"Small steps to organize your thoughts, priorities, and surroundings.",
"routines":"Simple habits to care for your time, breaks, and daily rhythm."
},
"start":"Begin without rushing. Adapt each step to your comfort.",
"finish":"You have completed this activity. Thank you for taking this moment for yourself.",
"safety":"Adapt movements to your comfort. Stop if you feel pain, dizziness, shortness of breath, or any discomfort. This app provides general wellness guidance, not medical care.",
"minutes":"minutes",
"step":"Step",
"of":"of",
"today":"Today",
"day":"Day",
"program":"7-day program",
"no_repeat":"Avoid repeating recent activities",
"rating_question":"How did this activity feel?",
"rating_before":"Before",
"rating_after":"After",
"rating_low":"I need something simpler",
"rating_ok":"It felt suitable",
"rating_high":"I felt very good",
"saved":"Progress saved on this device.",
"not_found":"Activity not found.",
"choose":"Choose an activity",
"duration":"Duration",
"complete":"Activity completed",
"step_intro":"Do this step at your own pace.",
"rest":"You can rest whenever you need to.",
"focus":"Focus",
"calm":"Calm",
"movement":"Movement",
"routines":"Routines",
"week_done":"You have reached the end of the weekly program. You can repeat it or choose an activity."
},
"pt":{
"app":"WELLNESS COACH",
"subtitle":"Pequenos passos para o bem-estar diário",
"sections":{
"calm":"Calma e atenção",
"movement":"Movimento suave",
"focus":"Organização e foco",
"routines":"Rotinas de bem-estar"
},
"section_descriptions":{
"calm":"Pausas curtas para desacelerar, respirar naturalmente e trazer a atenção para o presente.",
"movement":"Movimentos suaves do dia a dia que você pode adaptar ao seu conforto e espaço.",
"focus":"Pequenos passos para organizar seus pensamentos, prioridades e ambiente.",
"routines":"Hábitos simples para cuidar do seu tempo, das pausas e do ritmo diário."
},
"start":"Comece sem pressa. Adapte cada passo ao seu conforto.",
"finish":"Você concluiu esta atividade. Obrigado por reservar este momento para si.",
"safety":"Adapte os movimentos ao seu conforto. Pare se sentir dor, tontura, falta de ar ou qualquer desconforto. Este aplicativo oferece orientações gerais de bem-estar, não atendimento médico.",
"minutes":"minutos",
"step":"Etapa",
"of":"de",
"today":"Hoje",
"day":"Dia",
"program":"Programa de 7 dias",
"no_repeat":"Evitar repetir atividades recentes",
"rating_question":"Como foi esta atividade para você?",
"rating_before":"Antes",
"rating_after":"Depois",
"rating_low":"Preciso de algo mais simples",
"rating_ok":"Foi adequada para mim",
"rating_high":"Senti-me muito bem",
"saved":"Progresso salvo neste dispositivo.",
"not_found":"Atividade não encontrada.",
"choose":"Escolha uma atividade",
"duration":"Duração",
"complete":"Atividade concluída",
"step_intro":"Faça esta etapa no seu próprio ritmo.",
"rest":"Você pode descansar sempre que precisar.",
"focus":"Foco",
"calm":"Calma",
"movement":"Movimento",
"routines":"Rotinas",
"week_done":"Você chegou ao fim do programa semanal. Pode repeti-lo ou escolher uma atividade."
}
}

# Cada passo tem instrução completa, pronta para ser exibida e lida pela voz.
# As atividades são gerais e não prometem resultados médicos.
_ACTIVITY_ROWS=[
("calm","calm_breath","Respirar sem pressa","Breathe without rushing","Respirar sem pressa",
[
("Senta-te ou fica de pé numa posição confortável.","Sit or stand in a comfortable position.","Sente-se ou fique em pé em uma posição confortável."),
("Solta os ombros sem forçar o pescoço.","Let your shoulders relax without straining your neck.","Relaxe os ombros sem forçar o pescoço."),
("Inspira de forma natural e tranquila.","Breathe in naturally and gently.","Inspire de forma natural e tranquila."),
("Deixa o aire salir sin intentar controlarlo demasiado.","Let the air out without trying to control it too much.","Deixe o ar sair sem tentar controlá-lo demais."),
("Repite a tu ritmo, sin aguantar la respiración.","Repeat at your own pace without holding your breath.","Repita no seu ritmo, sem prender a respiração."),
("Observa cómo te sientes y termina cuando quieras.","Notice how you feel and finish whenever you wish.","Observe como você se sente e termine quando quiser.")]),
("calm","calm_senses","Volver al momento presente","Return to the present moment","Voltar ao momento presente",
[
("Busca una postura cómoda y deja las manos descansar.","Find a comfortable position and let your hands rest.","Encontre uma posição confortável e deixe as mãos descansarem."),
("Nombra mentalmente tres cosas que puedes ver.","Silently name three things you can see.","Nomeie mentalmente três coisas que você consegue ver."),
("Observa dos sonidos que estén a tu alrededor.","Notice two sounds around you.","Perceba dois sons ao seu redor."),
("Siente el apoyo de tus pies o de tu asiento.","Notice the support beneath your feet or seat.","Perceba o apoio sob os pés ou no assento."),
("Lleva tu atención a una cosa sencilla que agradeces hoy.","Bring your attention to one simple thing you appreciate today.","Volte a atenção para uma coisa simples pela qual agradece hoje."),
("Termina mirando a tu alrededor con calma.","Finish by calmly looking around you.","Termine olhando ao redor com tranquilidade.")]),
("calm","calm_shoulders","Soltar hombros y manos","Relax shoulders and hands","Relaxar ombros e mãos",
[
("Colócate en una posición estable y cómoda.","Settle into a stable, comfortable position.","Fique em uma posição estável e confortável."),
("Eleva suavemente los hombros solo si te resulta cómodo.","Gently raise your shoulders only if comfortable.","Eleve suavemente os ombros somente se for confortável."),
("Déjalos bajar sin empujarlos.","Let them lower without forcing them.","Deixe-os baixar sem forçar."),
("Abre las manos y vuelve a relajarlas.","Open your hands and relax them again.","Abra as mãos e relaxe-as novamente."),
("Mueve los dedos lentamente, sin tensión.","Move your fingers slowly, without tension.","Movimente os dedos lentamente, sem tensão."),
("Respira con naturalidad y nota cómo estás.","Breathe naturally and notice how you feel.","Respire naturalmente e observe como está.")]),
("calm","calm_pause","Pausa consciente","Mindful pause","Pausa consciente",
[
("Deja por un momento lo que estés haciendo.","Set aside what you are doing for a moment.","Deixe por um momento o que estiver fazendo."),
("Apoya los pies o encuentra una postura estable.","Place your feet down or find a stable position.","Apoie os pés ou encontre uma posição estável."),
("Relaja la mandíbula sin abrir demasiado la boca.","Relax your jaw without opening your mouth too far.","Relaxe a mandíbula sem abrir demais a boca."),
("Respira como lo haces normalmente.","Breathe as you normally do.","Respire como costuma respirar."),
("Elige una sola cosa a la que prestar atención.","Choose one thing to pay attention to.","Escolha uma única coisa para observar."),
("Vuelve a tu actividad cuando te sientas preparado.","Return to your activity when you feel ready.","Volte à sua atividade quando se sentir preparado.")]),
("calm","calm_visual","Mirar con tranquilidad","Look around calmly","Olhar com tranquilidade",
[
("Elige un punto agradable y seguro para mirar.","Choose a pleasant and safe point to look at.","Escolha um ponto agradável e seguro para olhar."),
("Observa sus formas sin tener que describirlas perfectamente.","Notice its shapes without needing to describe them perfectly.","Observe as formas sem precisar descrevê-las perfeitamente."),
("Fíjate en un color que destaque.","Notice one color that stands out.","Observe uma cor que se destaque."),
("Mira un poco más lejos si eso resulta cómodo.","Look a little farther away if that feels comfortable.","Olhe um pouco mais longe se isso for confortável."),
("Deja que tu mirada descanse unos instantes.","Let your gaze rest for a few moments.","Deixe o olhar descansar por alguns instantes."),
("Parpadea con naturalidad y continúa cuando quieras.","Blink naturally and continue whenever you wish.","Pisque naturalmente e continue quando quiser.")]),
("calm","calm_kindness","Hablarte con amabilidad","Speak to yourself kindly","Falar consigo com gentileza",
[
("Haz una pausa y nota cómo te encuentras.","Pause and notice how you are feeling.","Faça uma pausa e observe como está se sentindo."),
("Recuerda que no tienes que resolverlo todo ahora.","Remember that you do not have to solve everything now.","Lembre-se de que você não precisa resolver tudo agora."),
("Piensa qué le dirías a alguien a quien aprecias.","Think about what you would say to someone you care about.","Pense no que diria a alguém de quem gosta."),
("Prueba a dirigirte esas mismas palabras amables.","Try offering yourself those same kind words.","Experimente dizer a si mesmo essas mesmas palavras gentis."),
("Elige un pequeño paso posible para este momento.","Choose one small step that is possible right now.","Escolha um pequeno passo possível para este momento."),
("Termina sin juzgar cómo te ha salido.","Finish without judging how it went.","Termine sem julgar como foi.")]),
("calm","calm_release","Cambiar de ritmo","Change your pace","Mudar o ritmo",
[
("Detén una tarea si puedes hacerlo sin problema.","Pause a task if you can do so easily.","Interrompa uma tarefa se puder fazer isso sem problema."),
("Apoya las manos y suelta los hombros.","Rest your hands and relax your shoulders.","Apoie as mãos e relaxe os ombros."),
("Haz una respiración natural y cómoda.","Take one natural, comfortable breath.","Faça uma respiração natural e confortável."),
("Mira a tu alrededor sin buscar nada en particular.","Look around without searching for anything in particular.","Olhe ao redor sem procurar nada em particular."),
("Decide si necesitas continuar o hacer otra pausa.","Decide whether to continue or take another break.","Decida se precisa continuar ou fazer outra pausa."),
("Retoma el día a tu propio ritmo.","Return to your day at your own pace.","Retome o dia no seu próprio ritmo.")]),
("calm","calm_gratitude","Un detalle positivo","One positive detail","Um detalhe positivo",
[
("Piensa en algo sencillo que haya salido bien hoy.","Think of one simple thing that went well today.","Pense em algo simples que deu certo hoje."),
("Puede ser un gesto, una conversación o un momento tranquilo.","It may be a gesture, a conversation, or a quiet moment.","Pode ser um gesto, uma conversa ou um momento tranquilo."),
("Recuerda el detalle sin exagerar su importancia.","Recall the detail without overstating its importance.","Lembre-se do detalhe sem exagerar sua importância."),
("Observa qué valor tuvo para ti.","Notice what it meant to you.","Observe o que isso significou para você."),
("Si no encuentras uno, elige algo pequeño del presente.","If none comes to mind, choose something small in the present.","Se não lembrar de um, escolha algo pequeno do presente."),
("Continúa con una actitud abierta y realista.","Continue with an open and realistic attitude.","Continue com uma atitude aberta e realista.")]),
("movement","move_neck","Movilidad suave del cuello","Gentle neck mobility","Mobilidade suave do pescoço",
[
("Siéntate o ponte de pie con estabilidad.","Sit or stand with a stable posture.","Sente-se ou fique em pé com estabilidade."),
("Mira al frente sin empujar la cabeza hacia atrás.","Look ahead without pushing your head backward.","Olhe para a frente sem empurrar a cabeça para trás."),
("Gira un poco la cabeza hacia un lado, solo si es cómodo.","Turn your head slightly to one side, only if comfortable.","Vire a cabeça um pouco para um lado, somente se for confortável."),
("Vuelve al centro lentamente.","Return to the center slowly.","Volte lentamente ao centro."),
("Repite hacia el otro lado dentro de un rango cómodo.","Repeat on the other side within a comfortable range.","Repita para o outro lado dentro de um alcance confortável."),
("Deja el cuello quieto y descansa si lo necesitas.","Keep your neck still and rest if needed.","Deixe o pescoço parado e descanse se precisar.")]),
("movement","move_hands","Manos y muñecas","Hands and wrists","Mãos e punhos",
[
("Siéntate cómodamente y deja los hombros relajados.","Sit comfortably and keep your shoulders relaxed.","Sente-se confortavelmente e mantenha os ombros relaxados."),
("Abre las manos lentamente.","Open your hands slowly.","Abra as mãos lentamente."),
("Cierra los dedos suavemente, sin apretar.","Gently close your fingers without squeezing.","Feche os dedos suavemente, sem apertar."),
("Haz círculos pequeños con las muñecas si te resulta cómodo.","Make small wrist circles if comfortable.","Faça pequenos círculos com os punhos se for confortável."),
("Sacude las manos suavemente para soltarlas.","Gently shake your hands to loosen them.","Balance as mãos suavemente para relaxá-las."),
("Apoya las manos y descansa.","Rest your hands and relax.","Apoie as mãos e descanse.")]),
("movement","move_ankles","Tobillos y pies sentado","Seated ankles and feet","Tornozelos e pés sentado",
[
("Siéntate en una silla estable con los pies apoyados.","Sit in a stable chair with your feet supported.","Sente-se em uma cadeira estável com os pés apoiados."),
("Levanta ligeramente la punta de un pie si puedes.","Lift the front of one foot slightly if you can.","Levante ligeiramente a ponta de um pé, se puder."),
("Vuelve a apoyar todo el pie.","Place the whole foot down again.","Apoie novamente todo o pé."),
("Repite con el otro pie, sin forzar.","Repeat with the other foot, without forcing.","Repita com o outro pé, sem forçar."),
("Haz pequeños círculos con los tobillos si resulta cómodo.","Make small ankle circles if comfortable.","Faça pequenos círculos com os tornozelos se for confortável."),
("Mantén los pies apoyados y termina descansando.","Keep your feet supported and finish by resting.","Mantenha os pés apoiados e termine descansando.")]),
("movement","move_stand","Levantarse con apoyo opcional","Standing with optional support","Levantar-se com apoio opcional",
[
("Acércate a una silla estable o quédate sentado si lo prefieres.","Move near a stable chair, or remain seated if you prefer.","Aproxime-se de uma cadeira estável ou permaneça sentado, se preferir."),
("Coloca los pies en una posición cómoda y firme.","Place your feet in a comfortable, steady position.","Coloque os pés em uma posição confortável e firme."),
("Usa las manos como apoyo si lo necesitas.","Use your hands for support if needed.","Use as mãos como apoio se precisar."),
("Ponte de pie despacio solo si es seguro para ti.","Stand up slowly only if it is safe for you.","Levante-se devagar somente se for seguro para você."),
("Quédate quieto un momento y comprueba cómo te sientes.","Stand still for a moment and notice how you feel.","Fique parado por um momento e observe como se sente."),
("Vuelve a sentarte si lo necesitas; no hay obligación de continuar.","Sit back down if needed; there is no need to continue.","Volte a sentar se precisar; não é necessário continuar.")]),
("movement","move_walk","Caminar con atención","Mindful walking","Caminhar com atenção",
[
("Elige un lugar despejado y seguro, o imagina los pasos sentado.","Choose a clear, safe place, or imagine the steps while seated.","Escolha um local livre e seguro ou imagine os passos sentado."),
("Empieza con un ritmo cómodo.","Begin at a comfortable pace.","Comece em um ritmo confortável."),
("Observa cómo se apoyan los pies.","Notice how your feet meet the ground.","Observe como os pés tocam o chão."),
("Mantén la mirada en un punto seguro delante de ti.","Keep your gaze on a safe point ahead.","Mantenha o olhar em um ponto seguro à frente."),
("Reduce el ritmo o detente cuando lo desees.","Slow down or stop whenever you wish.","Diminua o ritmo ou pare quando quiser."),
("Termina con una pausa estable y cómoda.","Finish with a steady, comfortable pause.","Termine com uma pausa estável e confortável.")]),
("movement","move_arms","Brazos en movimiento suave","Gentle arm movement","Movimento suave dos braços",
[
("Siéntate o ponte de pie con estabilidad.","Sit or stand steadily.","Sente-se ou fique em pé com estabilidade."),
("Deja los brazos relajados junto al cuerpo.","Let your arms rest loosely by your sides.","Deixe os braços relaxados ao lado do corpo."),
("Levanta una mano solo hasta una altura cómoda.","Raise one hand only to a comfortable height.","Levante uma mão somente até uma altura confortável."),
("Baja lentamente y repite con la otra mano.","Lower it slowly and repeat with the other hand.","Abaixe lentamente e repita com a outra mão."),
("Mueve los brazos hacia delante solo si no causa molestias.","Move your arms forward only if it causes no discomfort.","Mova os braços para a frente somente se não causar desconforto."),
("Relaja los brazos y descansa.","Relax your arms and rest.","Relaxe os braços e descanse.")]),
("movement","move_posture","Revisar la postura","Check your posture","Revisar a postura",
[
("Encuentra una posición cómoda, sentado o de pie.","Find a comfortable position, sitting or standing.","Encontre uma posição confortável, sentado ou em pé."),
("Nota dónde se apoyan los pies o el cuerpo.","Notice where your feet or body are supported.","Observe onde os pés ou o corpo estão apoiados."),
("Deja que los hombros descansen sin empujarlos hacia atrás.","Let your shoulders rest without pulling them backward.","Deixe os ombros descansarem sem puxá-los para trás."),
("Permite que la cabeza quede en una posición natural.","Allow your head to rest in a natural position.","Deixe a cabeça em uma posição natural."),
("Cambia de posición si algo se siente incómodo.","Change position if anything feels uncomfortable.","Mude de posição se algo parecer desconfortável."),
("Elige la postura que puedas mantener con comodidad.","Choose a posture you can maintain comfortably.","Escolha a postura que consiga manter confortavelmente.")]),
("movement","move_break","Pausa de movimiento","Movement break","Pausa para movimento",
[
("Deja espacio suficiente para moverte con seguridad.","Make enough space to move safely.","Deixe espaço suficiente para se movimentar com segurança."),
("Empieza moviendo los dedos de las manos.","Begin by moving your fingers.","Comece movimentando os dedos das mãos."),
("Mueve los hombros suavemente dentro de un rango cómodo.","Move your shoulders gently within a comfortable range.","Movimente os ombros suavemente dentro de um alcance confortável."),
("Si te resulta seguro, cambia el peso de un pie al otro.","If safe, shift your weight from one foot to the other.","Se for seguro, transfira o peso de um pé para o outro."),
("También puedes hacer estos pasos sentado.","You can also do these steps while seated.","Você também pode fazer estas etapas sentado."),
("Termina en una posición estable y descansa.","Finish in a stable position and rest.","Termine em uma posição estável e descanse.")]),
("focus","focus_one","Una cosa cada vez","One thing at a time","Uma coisa de cada vez",
[
("Piensa en lo que estás intentando hacer ahora.","Think about what you are trying to do now.","Pense no que está tentando fazer agora."),
("Nombra la tarea en una frase sencilla.","Name the task in one simple sentence.","Nomeie a tarefa em uma frase simples."),
("Aparta una distracción que puedas controlar.","Set aside one distraction you can control.","Afaste uma distração que possa controlar."),
("Decide cuál es el primer paso pequeño.","Decide on the first small step.","Decida qual é o primeiro pequeno passo."),
("Dedica un momento a ese paso, sin exigir perfección.","Spend a moment on that step without demanding perfection.","Dedique um momento a essa etapa, sem exigir perfeição."),
("Anota qué sigue si no puedes terminar ahora.","Write down what comes next if you cannot finish now.","Anote o próximo passo se não puder terminar agora.")]),
("focus","focus_three","Elegir tres prioridades","Choose three priorities","Escolher três prioridades",
[
("Piensa en las cosas que te gustaría atender hoy.","Think about the things you would like to handle today.","Pense nas coisas que gostaria de resolver hoje."),
("Elige una que sea importante y posible.","Choose one that is important and achievable.","Escolha uma que seja importante e possível."),
("Elige una segunda tarea más pequeña.","Choose a second, smaller task.","Escolha uma segunda tarefa menor."),
("Elige una tercera solo si tienes tiempo y energía.","Choose a third only if you have time and energy.","Escolha uma terceira somente se tiver tempo e energia."),
("Decide cuál harás primero.","Decide which one you will do first.","Decida qual fará primeiro."),
("Recuerda que puedes ajustar la lista durante el día.","Remember that you can adjust the list during the day.","Lembre-se de que pode ajustar a lista durante o dia.")]),
("focus","focus_clear","Ordenar un espacio pequeño","Tidy one small space","Organizar um pequeno espaço",
[
("Elige una superficie pequeña, no toda la habitación.","Choose one small surface, not the whole room.","Escolha uma pequena superfície, não o cômodo inteiro."),
("Retira solo los objetos que claramente no pertenecen allí.","Remove only items that clearly do not belong there.","Retire apenas os objetos que claramente não pertencem ali."),
("Agrupa los objetos parecidos si resulta práctico.","Group similar items if practical.","Agrupe objetos semelhantes, se for prático."),
("Deja accesible lo que uses con frecuencia.","Keep frequently used items accessible.","Deixe acessível o que usa com frequência."),
("Detente cuando el espacio sea más útil, aunque no esté perfecto.","Stop when the space is more useful, even if not perfect.","Pare quando o espaço estiver mais útil, mesmo que não esteja perfeito."),
("Elige otro momento para continuar, si lo deseas.","Choose another time to continue if you wish.","Escolha outro momento para continuar, se desejar.")]),
("focus","focus_remember","Recordar sin sobrecargarte","Remember without overload","Lembrar sem sobrecarga",
[
("Piensa en una cosa que necesites recordar.","Think of one thing you need to remember.","Pense em algo de que precisa se lembrar."),
("Escríbela en un lugar que suelas consultar.","Write it somewhere you usually check.","Anote em um lugar que costuma consultar."),
("Añade una fecha u hora solo si es necesaria.","Add a date or time only if needed.","Acrescente uma data ou horário somente se necessário."),
("Si requiere varios pasos, escribe solo el siguiente.","If it requires several steps, write only the next one.","Se exigir várias etapas, anote apenas a próxima."),
("Comprueba que la nota sea fácil de entender.","Check that the note is easy to understand.","Verifique se a anotação é fácil de entender."),
("Vuelve a tu actividad sin intentar memorizarlo todo.","Return to your activity without trying to memorize everything.","Volte à sua atividade sem tentar memorizar tudo.")]),
("focus","focus_decide","Tomar una decisión pequeña","Make one small decision","Tomar uma pequena decisão",
[
("Describe la decisión en pocas palabras.","Describe the decision in a few words.","Descreva a decisão em poucas palavras."),
("Piensa en dos opciones realistas.","Think of two realistic options.","Pense em duas opções realistas."),
("Considera qué opción es más sencilla de realizar.","Consider which option is easier to carry out.","Considere qual opção é mais fácil de realizar."),
("Identifica si necesitas algún dato más antes de elegir.","Identify whether you need more information before choosing.","Identifique se precisa de mais alguma informação antes de escolher."),
("Elige el próximo paso, no necesariamente toda la solución.","Choose the next step, not necessarily the whole solution.","Escolha o próximo passo, não necessariamente toda a solução."),
("Revisa la decisión si cambian las circunstancias.","Review the decision if circumstances change.","Reavalie a decisão se as circunstâncias mudarem.")]),
("focus","focus_digital","Pausa de distracciones digitales","Digital distraction break","Pausa das distrações digitais",
[
("Observa si alguna notificación puede esperar.","Notice whether any notification can wait.","Observe se alguma notificação pode esperar."),
("Silencia o aparta el dispositivo durante unos minutos si puedes.","Mute or set aside your device for a few minutes if possible.","Silencie ou afaste o dispositivo por alguns minutos, se puder."),
("Elige la tarea que quieres atender primero.","Choose the task you want to handle first.","Escolha a tarefa que deseja realizar primeiro."),
("Deja a la vista solo lo que necesitas para empezar.","Keep only what you need to begin in view.","Deixe visível apenas o que precisa para começar."),
("Trabaja a tu ritmo durante un momento breve.","Work at your own pace for a short while.","Trabalhe no seu ritmo por um breve momento."),
("Revisa tus mensajes cuando hayas terminado ese paso.","Check your messages when you have finished that step.","Confira as mensagens quando terminar essa etapa.")]),
("focus","focus_plan","Plan sencillo para hoy","A simple plan for today","Plano simples para hoje",
[
("Piensa en el tiempo disponible que tienes hoy.","Think about the time you have available today.","Pense no tempo disponível que tem hoje."),
("Elige una tarea importante y concreta.","Choose one important, specific task.","Escolha uma tarefa importante e concreta."),
("Decide cuándo sería razonable empezar.","Decide when it would be reasonable to start.","Decida quando seria razoável começar."),
("Reserva espacio para comer, descansar y cambiar de tarea.","Leave room for meals, rest, and transitions.","Reserve espaço para comer, descansar e mudar de tarefa."),
("Reduce el plan si parece demasiado exigente.","Reduce the plan if it seems too demanding.","Reduza o plano se parecer exigente demais."),
("Conserva solo el siguiente paso necesario.","Keep only the next necessary step.","Mantenha apenas o próximo passo necessário.")]),
("focus","focus_finish","Cerrar una tarea","Close out a task","Concluir uma tarefa",
[
("Elige una tarea que esté casi terminada.","Choose a task that is nearly finished.","Escolha uma tarefa quase concluída."),
("Identifica qué falta realmente para darla por terminada.","Identify what is actually missing to finish it.","Identifique o que realmente falta para concluí-la."),
("Haz solo ese pequeño paso si puedes.","Do only that small step if you can.","Faça apenas essa pequena etapa, se puder."),
("Guarda los materiales o la información que necesites.","Put away the materials or information you need.","Guarde os materiais ou as informações de que precisa."),
("Anota el siguiente paso si todavía queda algo pendiente.","Write down the next step if anything remains.","Anote a próxima etapa se ainda houver algo pendente."),
("Reconoce el avance sin exigirte hacerlo todo hoy.","Acknowledge the progress without requiring yourself to do everything today.","Reconheça o progresso sem exigir fazer tudo hoje.")]),
("routines","routine_water","Pausa para beber agua","A water break","Pausa para beber água",
[
("Haz una pausa y comprueba si tienes agua a mano.","Pause and check whether you have water nearby.","Faça uma pausa e veja se há água por perto."),
("Si puedes beber agua con seguridad, sírvete una cantidad cómoda.","If you can drink water safely, pour a comfortable amount.","Se puder beber água com segurança, sirva uma quantidade confortável."),
("Bebe despacio según tus necesidades habituales.","Drink slowly according to your usual needs.","Beba devagar conforme suas necessidades habituais."),
("No te obligues a beber más de lo que necesitas.","Do not force yourself to drink more than you need.","Não se obrigue a beber mais do que precisa."),
("Guarda el vaso en un lugar seguro.","Put the glass in a safe place.","Coloque o copo em um local seguro."),
("Vuelve a tu actividad cuando estés listo.","Return to your activity when you are ready.","Volte à sua atividade quando estiver pronto.")]),
("routines","routine_break","Preparar una pausa","Plan a break","Preparar uma pausa",
[
("Piensa en la actividad que estás realizando.","Think about the activity you are doing.","Pense na atividade que está realizando."),
("Elige un momento razonable para hacer una pausa.","Choose a reasonable time to take a break.","Escolha um momento razoável para fazer uma pausa."),
("Decide qué harás durante la pausa: sentarte, estirarte suavemente o mirar al exterior.","Decide what to do during the break: sit, move gently, or look outside.","Decida o que fará na pausa: sentar, movimentar-se suavemente ou olhar para fora."),
("Deja preparado lo necesario para volver con facilidad.","Prepare what you need to return easily.","Deixe preparado o necessário para voltar com facilidade."),
("Haz la pausa sin convertirla en otra obligación.","Take the break without turning it into another obligation.","Faça a pausa sem transformá-la em mais uma obrigação."),
("Retoma la tarea cuando te resulte adecuado.","Return to the task when it feels right.","Retome a tarefa quando for adequado.")]),
("routines","routine_evening","Cerrar el día con calma","End the day calmly","Encerrar o dia com calma",
[
("Piensa en una cosa que hayas atendido hoy.","Think of one thing you took care of today.","Pense em algo de que cuidou hoje."),
("Reconoce un esfuerzo, por pequeño que haya sido.","Acknowledge an effort, however small.","Reconheça um esforço, por menor que tenha sido."),
("Anota una tarea que pueda esperar hasta mañana.","Write down one task that can wait until tomorrow.","Anote uma tarefa que possa esperar até amanhã."),
("Deja preparado algo sencillo para el día siguiente, si te ayuda.","Prepare one simple thing for tomorrow if it helps.","Deixe algo simples preparado para o dia seguinte, se ajudar."),
("Reduce las pantallas o las tareas si eso encaja en tu rutina.","Reduce screens or tasks if that fits your routine.","Reduza telas ou tarefas se isso combinar com sua rotina."),
("Elige una actividad tranquila para cerrar este momento.","Choose a calm activity to close this moment.","Escolha uma atividade tranquila para encerrar este momento.")]),
("routines","routine_morning","Empezar el día paso a paso","Start the day step by step","Começar o dia passo a passo",
[
("Antes de empezar, observa cómo te encuentras hoy.","Before starting, notice how you feel today.","Antes de começar, observe como está hoje."),
("Elige una necesidad básica que quieras atender primero.","Choose one basic need to address first.","Escolha uma necessidade básica para atender primeiro."),
("Piensa en una prioridad realista para el día.","Think of one realistic priority for the day.","Pense em uma prioridade realista para o dia."),
("Decide un primer paso pequeño.","Choose one small first step.","Escolha um primeiro passo pequeno."),
("Deja margen para imprevistos y descanso.","Leave room for unexpected events and rest.","Deixe espaço para imprevistos e descanso."),
("Empieza sin exigirte resolverlo todo de inmediato.","Begin without expecting yourself to solve everything immediately.","Comece sem exigir resolver tudo imediatamente.")]),
("routines","routine_sleep","Preparar un descanso","Prepare for rest","Preparar-se para descansar",
[
("Piensa qué suele ayudarte a pasar a un ritmo más tranquilo.","Think about what usually helps you slow down.","Pense no que costuma ajudar a desacelerar."),
("Elige una acción sencilla que encaje con tu rutina.","Choose one simple action that fits your routine.","Escolha uma ação simples que combine com sua rotina."),
("Prepara el espacio para que resulte cómodo y seguro.","Prepare the space so it feels comfortable and safe.","Prepare o espaço para que seja confortável e seguro."),
("Deja anotado lo que no necesitas resolver ahora.","Write down anything you do not need to solve now.","Anote o que não precisa resolver agora."),
("Permite que la actividad sea flexible, no una regla rígida.","Let the activity stay flexible, not a strict rule.","Permita que a atividade seja flexível, não uma regra rígida."),
("Termina eligiendo cómo quieres continuar tu noche.","Finish by choosing how you want to continue your evening.","Termine escolhendo como deseja continuar sua noite.")]),
("routines","routine_connection","Un contacto significativo","A meaningful connection","Um contato significativo",
[
("Piensa en alguien con quien te resulte agradable hablar.","Think of someone you enjoy talking with.","Pense em alguém com quem gosta de conversar."),
("Decide si te gustaría enviar un mensaje breve o llamar.","Decide whether you would like to send a short message or call.","Decida se gostaria de enviar uma mensagem breve ou telefonar."),
("Elige palabras sencillas y auténticas.","Choose simple and genuine words.","Escolha palavras simples e sinceras."),
("Respeta tu tiempo y el de la otra persona.","Respect your time and the other person's time.","Respeite seu tempo e o da outra pessoa."),
("Si hoy no es posible, puedes elegir otro momento.","If today is not possible, you can choose another time.","Se hoje não for possível, você pode escolher outro momento."),
("Reconoce que mantener vínculos puede empezar con un gesto pequeño.","Recognize that maintaining connections can begin with a small gesture.","Reconheça que manter vínculos pode começar com um pequeno gesto.")]),
("routines","routine_meal","Preparar una comida sin prisa","Prepare a meal without rushing","Preparar uma refeição sem pressa",
[
("Piensa en la próxima comida o merienda que te corresponda.","Think about your next meal or snack.","Pense na próxima refeição ou lanche."),
("Comprueba qué tienes disponible y qué necesitas.","Check what you have available and what you need.","Confira o que tem disponível e do que precisa."),
("Elige una opción práctica acorde con tus necesidades habituales.","Choose a practical option that fits your usual needs.","Escolha uma opção prática de acordo com suas necessidades habituais."),
("Organiza solo los elementos necesarios para empezar.","Arrange only what you need to begin.","Organize apenas o necessário para começar."),
("Tómate el tiempo que puedas, sin buscar una preparación perfecta.","Take the time you can, without aiming for a perfect preparation.","Use o tempo disponível, sem buscar uma preparação perfeita."),
("Deja el espacio seguro y ordenado al terminar.","Leave the space safe and tidy when finished.","Deixe o espaço seguro e organizado ao terminar.")]),
("routines","routine_transition","Cambiar de una tarea a otra","Transition between tasks","Passar de uma tarefa para outra",
[
("Termina o pausa la tarea actual en un punto razonable.","Finish or pause the current task at a reasonable point.","Termine ou pause a tarefa atual em um ponto razoável."),
("Guarda lo necesario para retomarla después.","Put away what you need to resume it later.","Guarde o necessário para retomá-la depois."),
("Levántate o cambia de postura solo si es cómodo y seguro.","Stand or change posture only if comfortable and safe.","Levante-se ou mude de postura somente se for confortável e seguro."),
("Haz una pausa breve antes de empezar lo siguiente.","Take a short pause before starting the next thing.","Faça uma breve pausa antes de começar a próxima atividade."),
("Identifica el primer paso de la siguiente tarea.","Identify the first step of the next task.","Identifique a primeira etapa da próxima tarefa."),
("Empieza cuando estés listo, sin correr.","Begin when ready, without rushing.","Comece quando estiver pronto, sem pressa.")]),
("routines","routine_weekly","Revisar la semana","Review the week","Revisar a semana",
[
("Piensa en una cosa útil que hayas hecho esta semana.","Think of one useful thing you did this week.","Pense em algo útil que fez nesta semana."),
("Elige una dificultad que quieras abordar poco a poco.","Choose one difficulty you want to address gradually.","Escolha uma dificuldade que queira abordar aos poucos."),
("Anota una prioridad para los próximos días.","Write down one priority for the coming days.","Anote uma prioridade para os próximos dias."),
("Elige un hábito sencillo que te gustaría mantener.","Choose one simple habit you would like to maintain.","Escolha um hábito simples que gostaria de manter."),
("Deja espacio para cambiar el plan si lo necesitas.","Leave room to change the plan if needed.","Deixe espaço para mudar o plano se precisar."),
("Cierra la revisión reconociendo lo que ya has avanzado.","End the review by acknowledging the progress you have made.","Encerre a revisão reconhecendo o progresso que já fez.")])
]

def _norm_lang(lang="es"):
    value=str(lang or "es").strip().lower()
    if value.startswith("en"):return "en"
    if value.startswith("pt"):return "pt"
    return "es"

def _norm_section(section):
    value=str(section or "all").strip().lower()
    aliases={"pause":"calm","energy":"movement","nature":"routines","coach":"focus","program":"routines","plants":"all","all":"all"}
    value=aliases.get(value,value)
    return value if value in SECTIONS or value=="all" else "all"

def _triple(es,en,pt,lang):
    return {"es":es,"en":en,"pt":pt}[_norm_lang(lang)]

def _build_catalog():
    records=[]
    for row in _ACTIVITY_ROWS:
        section,aid,title_es,title_en,title_pt,steps=row
        localized_steps=[]
        for i,step in enumerate(steps,1):
            localized_steps.append({
                "id":f"{aid}_s{i}",
                "text":{"es":step[0],"en":step[1],"pt":step[2]},
                "seconds":10,
                "order":i
            })
        records.append({
            "id":aid,
            "section":section,
            "kind":section,
            "title":{"es":title_es,"en":title_en,"pt":title_pt},
            "description":{
                "es":_TEXT["es"]["section_descriptions"][section],
                "en":_TEXT["en"]["section_descriptions"][section],
                "pt":_TEXT["pt"]["section_descriptions"][section]
            },
            "steps":localized_steps,
            "tags":[section,"everyday","40+"]
        })
    return records

_CATALOG=_build_catalog()
_BY_ID={item["id"]:item for item in _CATALOG}
_RECENT_IDS=[]
_PROGRAM_SECTIONS=("calm","movement","focus","routines","calm","movement","focus")

def _localized_activity(record,lang="es",minutes=3):
    lang=_norm_lang(lang)
    out=deepcopy(record)
    out["title"]=record["title"][lang]
    out["description"]=record["description"][lang]
    out["lang"]=lang
    out["language"]=lang
    out["minutes"]=_duration(minutes)
    out["duration_seconds"]=_duration(minutes)*60
    out["prompt_interval_seconds"]=PROMPT_INTERVAL_SECONDS
    out["total_steps"]=len(record["steps"])
    out["steps"]=[
        {"id":s["id"],"text":s["text"][lang],"seconds":s.get("seconds",10),"order":s["order"]}
        for s in record["steps"]
    ]
    out["instructions"]=[s["text"] for s in out["steps"]]
    out["safety"]=_TEXT[lang]["safety"]
    return out

def _duration(minutes=3):
    try:
        value=int(minutes)
    except (TypeError,ValueError):
        value=3
    return min(MINUTES_ALLOWED,key=lambda allowed:abs(allowed-value))

def _section_info(lang="es"):
    lang=_norm_lang(lang)
    return [
        {
            "id":section,
            "key":section,
            "name":_TEXT[lang]["sections"][section],
            "title":_TEXT[lang]["sections"][section],
            "description":_TEXT[lang]["section_descriptions"][section],
            "count":sum(1 for a in _CATALOG if a["section"]==section)
        }
        for section in SECTIONS
    ]

def get_catalog(lang="es"):
    return _section_info(lang)

def get_activities(lang="es",section="all"):
    # Compatibilidad con llamadas antiguas: get_activities("calm") o get_activities("es","movement").
    if str(lang).lower() in SECTIONS or str(lang).lower() in ("all","plants","pause","energy","nature","coach","program"):
        if section=="all":
            section,lang=lang,"es"
    normalized=_norm_section(section)
    selected=[a for a in _CATALOG if normalized=="all" or a["section"]==normalized]
    return [_localized_activity(a,lang,3) for a in selected]

def get_activity(activity_id,lang="es"):
    if isinstance(activity_id,dict):
        activity_id=activity_id.get("id") or activity_id.get("activity_id")
    record=_BY_ID.get(str(activity_id or "").strip())
    return _localized_activity(record,lang,3) if record else None

def get_plant(plant_id,lang="es"):
    # Ruta heredada: se conserva para evitar errores de importación, pero el catálogo botánico se ha retirado.
    return None

def _section_for_kind(kind):
    value=str(kind or "calm").strip().lower()
    aliases={
        "pause":"calm","calm":"calm","breathing":"calm","relax":"calm",
        "energy":"movement","move":"movement","movement":"movement",
        "focus":"focus","coach":"focus","organization":"focus","organize":"focus",
        "nature":"routines","routine":"routines","routines":"routines","program":"routines",
        "plants":"routines","all":"all"
    }
    return aliases.get(value,"calm")

def _choose_activity(section="all",avoid_ids=None,allow_repeat=False):
    normalized=_norm_section(section)
    avoid=set(str(x) for x in (avoid_ids or []))
    candidates=[a for a in _CATALOG if normalized=="all" or a["section"]==normalized]
    if not candidates:
        candidates=list(_CATALOG)
    if not allow_repeat:
        candidates=[a for a in candidates if a["id"] not in avoid]
    if not candidates:
        candidates=[a for a in _CATALOG if normalized=="all" or a["section"]==normalized]
    if not candidates:
        candidates=list(_CATALOG)
    return random.choice(candidates)

def create_session_id():
    seed=f"{time.time_ns()}:{random.random()}:{threading.get_ident()}"
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:20]

def get_session(activity_id=None,minutes=3,lang="es",activity=None,kind=None,allow_repeat=False,avoid_ids=None):
    # Admite la llamada nueva get_session(activity_id=..., minutes=..., lang=...)
    # y la antigua get_session(lang, kind, minutes) usada por main.py.
    if isinstance(activity_id,str) and activity_id.lower() in LANGUAGES and isinstance(minutes,str):
        old_lang=activity_id
        old_kind=minutes
        old_minutes=lang if isinstance(lang,(int,float)) else 3
        lang=old_lang
        minutes=old_minutes
        kind=kind or old_kind
        activity_id=None
    elif isinstance(activity_id,str) and activity_id.lower() in LANGUAGES and kind is None and activity is None:
        # Firma antigua get_session("es", "calm", 3) ya gestionada arriba;
        # get_session("es") se interpreta como idioma.
        lang=activity_id
        activity_id=None
    if activity is not None and activity_id is None:
        activity_id=activity.get("id") if isinstance(activity,dict) else activity
    lang=_norm_lang(lang)
    duration=_duration(minutes)
    selected=None
    if isinstance(activity_id,dict):
        activity_id=activity_id.get("id")
    if activity_id:
        selected=_BY_ID.get(str(activity_id))
    if selected is None:
        section=_section_for_kind(kind or "calm")
        if section=="all":
            section="all"
        selected=_choose_activity(section,avoid_ids=avoid_ids,allow_repeat=allow_repeat)
    result=_localized_activity(selected,lang,duration)
    sid=create_session_id()
    result.update({
        "session_id":sid,
        "id":selected["id"],
        "activity_id":selected["id"],
        "session_minutes":duration,
        "duration":duration,
        "duration_label":f'{duration} {_TEXT[lang]["minutes"]}',
        "status":"ready",
        "safety_notice":_TEXT[lang]["safety"],
        "completion_message":_TEXT[lang]["finish"],
        "step_intro":_TEXT[lang]["step_intro"],
        "rest_message":_TEXT[lang]["rest"],
        "allow_repeat":bool(allow_repeat)
    })
    with _LOCK:
        _HISTORY.append({"session_id":sid,"activity_id":selected["id"],"section":selected["section"],"lang":lang,"minutes":duration,"created_at":datetime.datetime.now(datetime.timezone.utc).isoformat()})
        if len(_HISTORY)>_MAX_HISTORY:
            del _HISTORY[:-_MAX_HISTORY]
        _RECENT_IDS.append(selected["id"])
        if len(_RECENT_IDS)>20:
            del _RECENT_IDS[:-20]
    return result

def get_program_day(lang="es",day=1):
    # También acepta get_program_day(day) para compatibilidad.
    if isinstance(lang,(int,float)):
        day,lang=int(lang),"es"
    lang=_norm_lang(lang)
    try:
        day=max(1,min(7,int(day)))
    except (TypeError,ValueError):
        day=1
    section=_PROGRAM_SECTIONS[day-1]
    candidates=[a for a in _CATALOG if a["section"]==section]
    # La selección diaria es determinista: la misma fecha del programa muestra la misma actividad.
    record=candidates[(day*3+day//2)%len(candidates)]
    activity_data=_localized_activity(record,lang,3)
    return {
        "day":day,
        "day_number":day,
        "lang":lang,
        "language":lang,
        "title":f'{_TEXT[lang]["day"]} {day}: {activity_data["title"]}',
        "program_title":_TEXT[lang]["program"],
        "section":section,
        "activity":activity_data,
        "activity_id":record["id"],
        "minutes":3,
        "duration_seconds":180,
        "instructions":activity_data["instructions"],
        "safety":_TEXT[lang]["safety"],
        "next_day":day+1 if day<7 else None,
        "complete":day==7,
        "completion_message":_TEXT[lang]["week_done"] if day==7 else None
    }

def get_program(lang="es"):
    lang=_norm_lang(lang)
    return {
        "title":_TEXT[lang]["program"],
        "language":lang,
        "days":[get_program_day(lang,day) for day in range(1,8)]
    }

def get_health():
    return {
        "status":"ok",
        "app":APP_NAME,
        "company":COMPANY,
        "version":VERSION,
        "audience":AUDIENCE,
        "languages":list(LANGUAGES),
        "sections":list(SECTIONS),
        "activities":len(_CATALOG),
        "plant_catalog":False,
        "durations":list(MINUTES_ALLOWED)
    }

def get_config():
    return {
        "name":APP_NAME,
        "app":APP_NAME,
        "company":COMPANY,
        "version":VERSION,
        "audience":AUDIENCE,
        "languages":list(LANGUAGES),
        "default_language":"es",
        "durations":list(MINUTES_ALLOWED),
        "program_days":7,
        "sections":get_catalog("es"),
        "activity_count":len(_CATALOG),
        "prompt_interval_seconds":PROMPT_INTERVAL_SECONDS,
        "local_data_only":True,
        "medical_service":False,
        "plant_catalog":False,
        "safety":{
            "es":_TEXT["es"]["safety"],
            "en":_TEXT["en"]["safety"],
            "pt":_TEXT["pt"]["safety"]
        }
    }

def get_recent_sessions(limit=20):
    try:
        limit=max(1,min(100,int(limit)))
    except (TypeError,ValueError):
        limit=20
    with _LOCK:
        return deepcopy(_HISTORY[-limit:][::-1])

def clear_session_history():
    with _LOCK:
        _HISTORY.clear()
        _RECENT_IDS.clear()
    return {"ok":True,"cleared":True}

def get_text(key,lang="es"):
    return _TEXT[_norm_lang(lang)].get(key,key)

def get_section_text(section,lang="es"):
    lang=_norm_lang(lang)
    section=_norm_section(section)
    if section=="all":
        return _TEXT[lang]["subtitle"]
    return _TEXT[lang]["sections"].get(section,_TEXT[lang]["subtitle"])

def legacy_id(value):
    value=str(value or "").strip()
    if value in _BY_ID:
        return value
    aliases={
        "breathing":"calm_breath","pause":"calm_pause","mindfulness":"calm_senses",
        "energy":"move_break","stretch":"move_arms","coach":"focus_one",
        "nature":"routine_break","plants":"routine_break"
    }
    return aliases.get(value.lower())

# Aliases públicos para compatibilidad con importaciones antiguas.
catalog=get_catalog
activities=get_activities
session=get_session
plant=get_plant
program_day=get_program_day
health=get_health
config=get_config
activity=get_activity
program=get_program
recent_sessions=get_recent_sessions
