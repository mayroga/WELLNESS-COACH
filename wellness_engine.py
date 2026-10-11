from __future__ import annotations
import os,random,time,datetime,hashlib,threading
from copy import deepcopy

VERSION="6.0.0"
APP_NAME="WELLNESS COACH"
COMPANY="May Roga LLC"
PROMPT_INTERVAL_SECONDS=10
MINUTES_ALLOWED=(3,5,10)
LANGUAGES=("es","en")
SECTIONS=("plants","movement","calm","coach")
_LOCK=threading.RLock()
_RNG=random.SystemRandom()

def _b(es,en,lang="es"):
    return en if lang=="en" else es

# PLANTAS: información botánica general y actividades de observación.
# Las precauciones no sustituyen la identificación profesional de una planta.
_PLANT_ROWS=[
("Manzanilla","Chamomile","Matricaria chamomilla","aromatic","Flores pequeñas blancas y centro amarillo; aroma suave.","Small white flowers with yellow centers; gentle aroma.","Observar los pétalos, el centro y el contraste de colores.","Observe the petals, center and color contrast.","No ingerir ni usar preparados sin revisar alergias e interacciones; puede causar alergia en personas sensibles a las asteráceas.","Do not ingest or use preparations without checking allergies and interactions; may trigger allergies in people sensitive to Asteraceae."),
("Menta","Mint","Mentha spicata","aromatic","Hojas verdes aromáticas y tallos que se extienden con facilidad.","Aromatic green leaves and spreading stems.","Comparar la forma, el borde y la disposición de las hojas.","Compare leaf shape, edges and arrangement.","No confundir especies; el aceite concentrado no equivale a una hoja y puede ser peligroso.","Do not confuse species; concentrated oil is not equivalent to a leaf and may be hazardous."),
("Lavanda","Lavender","Lavandula angustifolia","aromatic","Hojas estrechas y espigas de flores generalmente violetas.","Narrow leaves and spikes of usually purple flowers.","Mirar las espigas y contar lentamente sus grupos de flores.","Look at the flower spikes and slowly count their clusters.","El aroma puede molestar a personas sensibles; no ingerir aceites esenciales.","The scent may bother sensitive people; do not ingest essential oils."),
("Romero","Rosemary","Salvia rosmarinus","aromatic","Arbusto de hojas estrechas, firmes y muy aromáticas.","Shrub with narrow, firm, strongly aromatic leaves.","Observar cómo las hojas estrechas se distribuyen sobre el tallo.","Notice how narrow leaves are arranged along the stem.","No ingerir preparados concentrados sin orientación profesional; evitar aceites esenciales por vía oral.","Do not ingest concentrated preparations without professional guidance; avoid oral essential oils."),
("Albahaca","Basil","Ocimum basilicum","herb","Hojas suaves y verdes; planta aromática de clima cálido.","Soft green leaves; an aromatic warm-weather plant.","Comparar dos hojas y describir sus diferencias visibles.","Compare two leaves and describe visible differences.","Identificar correctamente la especie; no usar aceites concentrados como alimento o remedio.","Identify the species correctly; do not use concentrated oils as food or remedies."),
("Sábila o aloe vera","Aloe vera","Aloe vera","succulent","Hojas carnosas en roseta con bordes dentados.","Fleshy rosette leaves with toothed edges.","Observar la roseta y el patrón de los bordes sin cortar la hoja.","Observe the rosette and leaf-edge pattern without cutting the leaf.","El látex amarillo puede ser irritante y peligroso si se ingiere; no consumir productos caseros.","Yellow latex can be irritating and dangerous if swallowed; do not consume homemade products."),
("Helecho","Fern","Nephrolepis exaltata","fern","Frondas divididas en numerosos foliolos; suele preferir humedad.","Divided fronds with many leaflets; often prefers humidity.","Seguir visualmente una fronda desde la base hasta la punta.","Trace one frond visually from base to tip.","Las especies varían; no ingerir ni asumir que una planta silvestre es segura.","Species vary; do not ingest or assume a wild plant is safe."),
("Suculenta","Succulent","Echeveria elegans","succulent","Hojas gruesas que suelen formar una roseta compacta.","Thick leaves that often form a compact rosette.","Contar las capas visibles de la roseta.","Count the visible layers of the rosette.","Confirmar la especie antes de tocar o ingerir; algunas suculentas ornamentales son tóxicas.","Confirm the species before touching or ingesting; some ornamental succulents are toxic."),
("Girasol","Sunflower","Helianthus annuus","flower","Flor grande con centro prominente y hojas ásperas.","Large flower with a prominent center and rough leaves.","Observar el centro y la disposición de los pétalos.","Observe the center and arrangement of the petals.","Puede provocar alergias; no consumir semillas de plantas tratadas con químicos no aptos para alimentos.","May cause allergies; do not eat seeds from plants treated with non-food chemicals."),
("Caléndula","Calendula","Calendula officinalis","flower","Flores amarillas o anaranjadas con numerosos pétalos.","Yellow or orange flowers with many petals.","Comparar tonos, pétalos y simetría de la flor.","Compare shades, petals and flower symmetry.","Puede causar reacciones alérgicas; no sustituye tratamientos médicos.","May cause allergic reactions; it does not replace medical treatment."),
("Tomillo","Thyme","Thymus vulgaris","aromatic","Planta baja con hojas pequeñas y tallos leñosos.","Low-growing plant with small leaves and woody stems.","Observar el tamaño de las hojas y la estructura del tallo.","Observe leaf size and stem structure.","No ingerir aceites concentrados; las preparaciones pueden interactuar con medicamentos.","Do not ingest concentrated oils; preparations may interact with medicines."),
("Cilantro","Cilantro","Coriandrum sativum","herb","Hojas finamente divididas y flores pequeñas en grupos.","Finely divided leaves and small clustered flowers.","Comparar hojas jóvenes y maduras si ambas están presentes.","Compare young and mature leaves if both are present.","Puede causar alergias; identifica la planta antes de usarla como alimento.","May cause allergies; identify the plant before using it as food."),
("Poto","Golden pothos","Epipremnum aureum","toxic","Enredadera de hojas brillantes, a menudo con manchas amarillas.","Vining plant with glossy leaves, often marked with yellow.","Seguir visualmente la dirección de crecimiento de una hoja a otra.","Trace the growth direction visually from leaf to leaf.","Tóxica si se ingiere y puede irritar la boca y la piel; mantener lejos de niños y mascotas.","Toxic if swallowed and may irritate the mouth and skin; keep away from children and pets."),
("Costilla de Adán","Monstera","Monstera deliciosa","toxic","Hojas grandes que desarrollan cortes y perforaciones.","Large leaves that develop splits and holes.","Observar las perforaciones sin arrancar ninguna hoja.","Observe the holes without removing any leaves.","Contiene cristales irritantes; no ingerir hojas ni frutos sin identificación y preparación especializada.","Contains irritating crystals; do not eat leaves or fruit without expert identification and preparation."),
("Orquídea","Orchid","Phalaenopsis spp.","flower","Flores simétricas y raíces adaptadas a su modo de crecimiento.","Symmetrical flowers and roots adapted to their growing conditions.","Observar la simetría de la flor y la forma de sus pétalos.","Observe the flower symmetry and petal shapes.","Las necesidades cambian por especie; no aplicar productos concentrados sin comprobar su seguridad.","Needs vary by species; do not apply concentrated products without checking safety."),
("Cactus","Cactus","Cactaceae","succulent","Tallo adaptado a almacenar agua; muchas especies tienen espinas.","Water-storing stem; many species have spines.","Observar las espinas desde una distancia segura.","Observe the spines from a safe distance.","Las espinas pueden causar lesiones; no tocar ni ingerir especies desconocidas.","Spines can injure; do not touch or ingest unknown species."),
("Hiedra común","English ivy","Hedera helix","toxic","Enredadera con hojas lobuladas y crecimiento trepador.","Climbing vine with lobed leaves.","Identificar visualmente la forma de las hojas y su patrón.","Identify the leaf shape and pattern visually.","Puede ser tóxica si se ingiere y causar irritación; evitar contacto con savia.","May be toxic if swallowed and cause irritation; avoid contact with sap."),
("Pino","Pine","Pinus spp.","tree","Árbol con hojas aciculares y, en muchas especies, conos.","Tree with needle-like leaves and, in many species, cones.","Distinguir agujas, ramas y conos sin recoger material desconocido.","Distinguish needles, branches and cones without collecting unknown material.","No preparar infusiones con pinos no identificados; existen especies parecidas con riesgos distintos.","Do not make infusions from unidentified pines; similar-looking species can carry different risks."),
("Bambú","Bamboo","Bambusoideae","foliage","Tallos segmentados y hojas estrechas de crecimiento variable.","Segmented stems and narrow leaves with varied growth patterns.","Contar los segmentos visibles del tallo.","Count the visible stem segments.","La seguridad depende de la especie y del procesamiento; no consumir brotes silvestres sin identificación.","Safety depends on species and processing; do not eat wild shoots without identification."),
("Planta de interior","Houseplant","Planta ornamental diversa","foliage","La forma, el color y la textura dependen de la especie.","Shape, color and texture depend on the species.","Elegir tres rasgos visibles y describirlos sin juzgarlos.","Choose three visible traits and describe them without judgment.","Identificar la especie antes de tocar, podar o ingerir cualquier parte.","Identify the species before touching, pruning or ingesting any part."),
("Jazmín","Jasmine","Jasminum spp.","flower","Enredadera o arbusto con flores claras en muchas especies.","Vine or shrub with pale flowers in many species.","Observar la forma de la flor y su ubicación en la planta.","Observe flower shape and where it grows on the plant.","No todas las especies tienen el mismo uso; no ingerir flores de identificación incierta.","Not all species have the same uses; do not eat flowers of uncertain identity."),
("Rosa","Rose","Rosa spp.","flower","Flores de numerosos pétalos y tallos que pueden tener espinas.","Flowers with many petals and stems that may have thorns.","Comparar el número y la disposición de los pétalos.","Compare petal count and arrangement.","Las espinas pueden pinchar; flores comerciales pueden llevar pesticidas.","Thorns can prick; commercial flowers may carry pesticides."),
("Hibisco","Hibiscus","Hibiscus rosa-sinensis","flower","Flor grande con estambres destacados y colores vivos.","Large flower with prominent stamens and vivid colors.","Observar el centro de la flor y los cambios de color.","Observe the flower center and color variations.","Las especies y preparaciones varían; no consumir sin identificar la planta y revisar seguridad.","Species and preparations vary; do not consume without identification and safety checks."),
("Gardenia","Gardenia","Gardenia jasminoides","flower","Hojas verdes brillantes y flores blancas perfumadas.","Glossy green leaves and fragrant white flowers.","Comparar el brillo de las hojas con la textura de la flor.","Compare leaf gloss with flower texture.","Puede causar irritación en personas sensibles; no ingerir plantas ornamentales.","May irritate sensitive people; do not ingest ornamental plants."),
("Violeta africana","African violet","Streptocarpus ionanthus","flower","Hojas suaves y redondeadas con flores de varios tonos.","Soft rounded leaves with flowers in varied shades.","Observar la textura de las hojas sin frotarlas.","Observe leaf texture without rubbing them.","Evitar tratamientos químicos no etiquetados para plantas de interior.","Avoid chemical treatments not labeled for houseplants."),
("Begonia","Begonia","Begonia spp.","flower","Hojas asimétricas y flores que varían según la especie.","Asymmetrical leaves and flowers that vary by species.","Buscar la asimetría de las hojas y comparar sus bordes.","Look for leaf asymmetry and compare edges.","Muchas begonias son irritantes o tóxicas al ingerirse, especialmente para mascotas.","Many begonias are irritating or toxic if swallowed, especially for pets."),
("Geranio","Geranium","Pelargonium spp.","flower","Hojas redondeadas y flores agrupadas en tonos diversos.","Rounded leaves and clustered flowers in varied colors.","Observar cómo se agrupan las flores en el tallo.","Notice how flowers cluster along the stem.","Puede provocar sensibilidad cutánea; no ingerir aceites ni preparados caseros.","May cause skin sensitivity; do not ingest oils or homemade preparations."),
("Petunia","Petunia","Petunia × hybrida","flower","Flores en forma de embudo con amplia variedad de colores.","Funnel-shaped flowers in a wide range of colors.","Observar la transición del color hacia el centro de la flor.","Observe how color changes toward the flower center.","No consumir plantas ornamentales ni productos tratados con pesticidas.","Do not eat ornamental plants or plants treated with pesticides."),
("Dalia","Dahlia","Dahlia spp.","flower","Flores con múltiples capas y formas variadas.","Flowers with multiple layers and varied forms.","Contar las capas de pétalos visibles sin arrancarlos.","Count visible petal layers without removing them.","Identificar la especie y evitar ingerir partes ornamentales.","Identify the species and avoid eating ornamental parts."),
("Zinnia","Zinnia","Zinnia elegans","flower","Flores coloridas con discos centrales y pétalos ordenados.","Colorful flowers with central disks and orderly petals.","Buscar patrones repetidos entre pétalos.","Look for repeated patterns among petals.","Puede causar sensibilidad en algunas personas; no ingerir plantas de jardín sin confirmar su identidad.","May cause sensitivity in some people; do not eat garden plants without confirming identity."),
("Lirio de la paz","Peace lily","Spathiphyllum spp.","toxic","Hojas alargadas y una estructura blanca que rodea la espádice.","Long leaves and a white structure surrounding the spadix.","Observar la diferencia entre la hoja y la estructura floral blanca.","Observe the difference between the leaf and the white flower-like structure.","Contiene cristales irritantes; tóxico para mascotas y personas si se ingiere.","Contains irritating crystals; toxic to pets and people if swallowed."),
("Sansevieria","Snake plant","Dracaena trifasciata","succulent","Hojas verticales y firmes con bandas o bordes contrastantes.","Upright firm leaves with bands or contrasting edges.","Seguir las líneas y bandas de una hoja.","Trace the lines and bands on one leaf.","Puede causar molestias digestivas si se ingiere; mantener fuera del alcance de mascotas.","May cause digestive upset if swallowed; keep away from pets."),
("Árbol de jade","Jade plant","Crassula ovata","succulent","Hojas gruesas y ovaladas en tallos ramificados.","Thick oval leaves on branching stems.","Observar la forma ovalada y la distribución de las hojas.","Observe the oval shape and leaf arrangement.","Puede ser tóxico para mascotas si se ingiere; no consumir.","May be toxic to pets if swallowed; do not eat."),
("Echeveria","Echeveria","Echeveria spp.","succulent","Rosetas geométricas de hojas carnosas.","Geometric rosettes of fleshy leaves.","Observar la simetría radial de la roseta.","Observe the radial symmetry of the rosette.","Identificar la especie antes de tocar o ingerir; evitar productos no etiquetados.","Identify the species before touching or ingesting; avoid unlabeled products."),
("Haworthia","Haworthia","Haworthiopsis attenuata","succulent","Hojas cortas agrupadas en rosetas, a veces con bandas blancas.","Short rosette leaves, sometimes with white bands.","Comparar las marcas y las puntas de las hojas.","Compare leaf markings and tips.","No asumir que una suculenta es comestible; identificar antes de usar.","Do not assume a succulent is edible; identify it before use."),
("Árbol del dinero","Money tree","Pachira aquatica","foliage","Hojas palmeadas que parten de un punto común.","Palmate leaves that radiate from one point.","Contar los foliolos que salen de un mismo punto.","Count the leaflets that radiate from one point.","Evitar ingerir partes de plantas ornamentales sin identificación segura.","Avoid eating parts of ornamental plants without reliable identification."),
("Ficus","Rubber fig","Ficus elastica","foliage","Hojas grandes, brillantes y de textura firme.","Large glossy leaves with a firm texture.","Observar reflejos y nervaduras principales.","Observe reflections and main veins.","La savia puede irritar la piel y los ojos; mantener lejos de mascotas que mordisquean plantas.","Sap may irritate skin and eyes; keep away from pets that chew plants."),
("Filodendro","Philodendron","Philodendron spp.","toxic","Hojas de formas variadas y crecimiento trepador o erguido.","Leaves of varied shapes and climbing or upright growth.","Comparar el contorno de las hojas de una misma planta.","Compare leaf outlines on the same plant.","Muchas especies contienen cristales irritantes; no ingerir y mantener fuera del alcance de niños y mascotas.","Many species contain irritating crystals; do not ingest and keep away from children and pets."),
("Calatea","Calathea","Goeppertia spp.","foliage","Hojas con dibujos, franjas y contrastes visibles.","Leaves with visible patterns, stripes and contrasts.","Describir el patrón de una hoja en tres palabras.","Describe one leaf pattern in three words.","Las necesidades de cuidado varían; evita pesticidas sin instrucciones claras.","Care needs vary; avoid pesticides without clear instructions."),
("Maranta","Prayer plant","Maranta leuconeura","foliage","Hojas estampadas que pueden cambiar de posición a lo largo del día.","Patterned leaves that may change position through the day.","Observar la posición de las hojas sin intentar moverlas.","Observe leaf positions without trying to move them.","No ingerir preparados caseros; comprobar la identidad de cualquier planta.","Do not ingest homemade preparations; verify any plant's identity."),
("Drácena","Dracaena","Dracaena spp.","foliage","Hojas alargadas y crecimiento vertical o en roseta.","Long leaves with upright or rosette growth.","Comparar hojas altas y bajas, si las hay.","Compare upper and lower leaves, if present.","Varias especies son tóxicas para mascotas; no ingerir.","Several species are toxic to pets; do not ingest."),
("Palmera areca","Areca palm","Dypsis lutescens","foliage","Frondas arqueadas con numerosos foliolos estrechos.","Arching fronds with many narrow leaflets.","Seguir una fronda y observar cómo se divide.","Follow a frond and notice how it branches.","No consumir partes de plantas ornamentales sin identificación y evaluación de seguridad.","Do not eat ornamental plant parts without identification and safety assessment."),
("Palma de salón","Parlor palm","Chamaedorea elegans","foliage","Palma compacta con frondas finas y arqueadas.","Compact palm with fine arching fronds.","Observar el ritmo de las hojas que salen del tallo.","Notice the rhythm of leaves emerging from the stem.","Evitar el uso de productos químicos no etiquetados en interiores.","Avoid using chemicals not labeled for indoor plants."),
("Árbol de caucho","Rubber tree","Hevea brasiliensis","tree","Árbol tropical asociado a la producción de látex.","Tropical tree associated with latex production.","Comparar la forma del árbol con otras plantas de hoja ancha.","Compare the tree's form with other broad-leaved plants.","El látex puede provocar reacciones alérgicas; no tocar la savia.","Latex can trigger allergic reactions; do not touch sap."),
("Olivo","Olive tree","Olea europaea","tree","Hojas estrechas, verde grisáceas, con envés más claro.","Narrow gray-green leaves with a lighter underside.","Comparar la cara superior e inferior de una hoja caída.","Compare the upper and lower sides of a fallen leaf.","No ingerir hojas ni extractos como tratamiento sin orientación profesional.","Do not ingest leaves or extracts as treatment without professional guidance."),
("Limón","Lemon tree","Citrus limon","tree","Hojas aromáticas, flores claras y frutos amarillos cuando madura.","Aromatic leaves, pale flowers and yellow fruit when ripe.","Observar hojas, flores o frutos según la estación.","Observe leaves, flowers or fruit depending on the season.","La savia y algunos aceites cítricos pueden irritar la piel; el contacto con ciertos cítricos y sol puede causar reacciones.","Sap and some citrus oils may irritate skin; contact with some citrus plants and sunlight can cause reactions."),
("Naranjo","Orange tree","Citrus sinensis","tree","Hojas verdes y brillantes, flores blancas y frutos anaranjados.","Glossy green leaves, white flowers and orange fruit.","Buscar el contraste entre hojas y frutos si están presentes.","Look for contrast between leaves and fruit if present.","No consumir plantas tratadas con productos no aptos para alimentos.","Do not eat plants treated with products not approved for food."),
("Mango","Mango tree","Mangifera indica","tree","Hojas largas que pueden cambiar de color al crecer.","Long leaves that may change color as they mature.","Observar diferencias de color entre hojas nuevas y maduras.","Observe color differences between new and mature leaves.","La savia y la piel del fruto pueden irritar a personas sensibles; evitar contacto si existe alergia.","Sap and fruit skin may irritate sensitive people; avoid contact if allergic."),
("Guayaba","Guava tree","Psidium guajava","tree","Hojas con nervaduras marcadas y textura algo rugosa.","Leaves with pronounced veins and a somewhat rough texture.","Seguir una nervadura principal desde la base hacia la punta.","Trace a main vein from base to tip.","No utilizar extractos caseros como sustituto de atención médica.","Do not use homemade extracts as a substitute for medical care."),
("Aguacate","Avocado tree","Persea americana","tree","Hojas elípticas y copa frondosa en árboles maduros.","Elliptical leaves and a leafy crown on mature trees.","Observar el contorno elíptico y el tamaño de las hojas.","Observe the elliptical outline and leaf size.","Partes de la planta pueden ser tóxicas para algunos animales; no usar semillas ni hojas como remedio casero.","Parts of the plant can be toxic to some animals; do not use seeds or leaves as home remedies."),
("Plátano","Banana plant","Musa spp.","foliage","Hojas muy grandes que se despliegan desde un tallo aparente.","Very large leaves unfurling from a pseudostem.","Observar las líneas paralelas y la anchura de la hoja.","Observe the parallel lines and width of the leaf.","Las hojas pueden rasgarse con facilidad; no trepar ni manipular tallos inestables.","Leaves tear easily; do not climb or handle unstable stems."),
("Bambú de la suerte","Lucky bamboo","Dracaena sanderiana","foliage","Tallos verdes segmentados, a menudo cultivados en agua.","Green segmented stems, often grown in water.","Contar los segmentos visibles y observar su dirección.","Count visible segments and observe their direction.","No es bambú verdadero y puede ser tóxico para mascotas si se ingiere.","It is not true bamboo and may be toxic to pets if swallowed."),
("Hiedra sueca","Swedish ivy","Plectranthus verticillatus","foliage","Hojas redondeadas y tallos que cuelgan o se extienden.","Rounded leaves and stems that trail or spread.","Observar el patrón repetido de hojas a lo largo del tallo.","Observe the repeating leaf pattern along the stem.","No ingerir; identificar la especie antes de aplicar preparados.","Do not ingest; identify the species before applying preparations."),
("Tradescantia","Spiderwort","Tradescantia zebrina","foliage","Hojas con bandas de colores y tallos rastreros.","Striped leaves and trailing stems.","Comparar las bandas de color entre hojas.","Compare color bands between leaves.","La savia puede irritar la piel de algunas personas; mantener fuera del alcance de mascotas.","Sap may irritate some people's skin; keep away from pets."),
("Coleo","Coleus","Coleus scutellarioides","foliage","Hojas muy coloridas con bordes y patrones variables.","Highly colorful leaves with varied edges and patterns.","Identificar dos colores y un patrón de una hoja.","Identify two colors and one pattern on a leaf.","No ingerir plantas ornamentales; algunas variedades pueden ser tóxicas para mascotas.","Do not eat ornamental plants; some varieties may be toxic to pets."),
("Croton","Croton","Codiaeum variegatum","toxic","Hojas firmes con combinaciones de verde, amarillo, rojo o naranja.","Firm leaves combining green, yellow, red or orange.","Observar las combinaciones de color sin tocar la savia.","Observe color combinations without touching the sap.","La savia es irritante y la planta puede ser tóxica si se ingiere.","Sap is irritating and the plant may be toxic if swallowed."),
("Poinsettia","Poinsettia","Euphorbia pulcherrima","toxic","Brácteas coloridas rodean pequeñas flores centrales.","Colorful bracts surround small central flowers.","Distinguir las brácteas de las flores pequeñas.","Distinguish the bracts from the small flowers.","La savia puede irritar; no ingerir y mantener fuera del alcance de niños y mascotas.","Sap may irritate; do not ingest and keep away from children and pets."),
("Narciso","Daffodil","Narcissus spp.","toxic","Flores con una corona central característica.","Flowers with a distinctive central trumpet.","Observar la corona central y la simetría de la flor.","Observe the central trumpet and flower symmetry.","Todas las partes pueden ser tóxicas si se ingieren, especialmente el bulbo.","All parts may be toxic if swallowed, especially the bulb."),
("Tulipán","Tulip","Tulipa spp.","flower","Flores en forma de copa y hojas alargadas.","Cup-shaped flowers and long leaves.","Observar la forma de copa y el contorno de las hojas.","Observe the cup shape and leaf outlines.","Los bulbos son tóxicos si se ingieren; pueden irritar la piel.","Bulbs are toxic if swallowed and may irritate skin."),
("Crisantemo","Chrysanthemum","Chrysanthemum spp.","flower","Flores con numerosas capas y formas diversas.","Flowers with many layers and varied forms.","Observar la repetición de pétalos alrededor del centro.","Observe petal repetition around the center.","Puede causar alergia; algunas especies son tóxicas para mascotas.","May cause allergies; some species are toxic to pets."),
("Diente de león","Dandelion","Taraxacum officinale","flower","Flor amarilla que puede formar una esfera de semillas.","Yellow flower that may form a spherical seed head.","Comparar la flor amarilla con la esfera de semillas si existe.","Compare the yellow flower with the seed head if present.","No consumir plantas silvestres de áreas tratadas o contaminadas; confirmar identidad.","Do not eat wild plants from treated or contaminated areas; confirm identity."),
("Trébol","Clover","Trifolium spp.","herb","Hojas que suelen aparecer en grupos de tres foliolos.","Leaves that often appear in groups of three leaflets.","Contar los foliolos y observar su forma.","Count the leaflets and observe their shape.","No ingerir plantas silvestres sin identificación y revisión de seguridad.","Do not eat wild plants without identification and safety review."),
("Hierbabuena","Spearmint","Mentha spicata","aromatic","Hojas dentadas y aroma fresco característico.","Toothed leaves and a characteristic fresh aroma.","Comparar la forma de las hojas con las de otras plantas aromáticas.","Compare leaf shape with other aromatic plants.","Identificar la especie; los aceites concentrados no deben ingerirse sin indicación profesional.","Identify the species; concentrated oils should not be ingested without professional guidance."),
("Salvia","Sage","Salvia officinalis","aromatic","Hojas gris verdosas con textura aterciopelada.","Gray-green leaves with a velvety texture.","Observar la textura y el tono mate de las hojas.","Observe leaf texture and muted color.","Algunas preparaciones concentradas pueden ser riesgosas; evitar aceites esenciales por vía oral.","Some concentrated preparations can be risky; avoid oral essential oils."),
("Orégano","Oregano","Origanum vulgare","aromatic","Hojas pequeñas y tallos ramificados con aroma intenso.","Small leaves and branching stems with a strong aroma.","Observar las hojas en pares y el patrón de ramificación.","Observe paired leaves and branching patterns.","No ingerir aceites esenciales; las plantas ornamentales pueden haber recibido químicos.","Do not ingest essential oils; ornamental plants may have been treated with chemicals."),
("Toronjil","Lemon balm","Melissa officinalis","aromatic","Hojas verdes dentadas con aroma cítrico suave.","Toothed green leaves with a mild citrus aroma.","Describir el borde de la hoja y observar el tallo.","Describe the leaf edge and observe the stem.","Puede interactuar con medicamentos; no usar preparados como tratamiento sin orientación profesional.","May interact with medicines; do not use preparations as treatment without professional guidance."),
("Hierba limón","Lemongrass","Cymbopogon citratus","aromatic","Hojas largas, estrechas y arqueadas, con aroma cítrico.","Long narrow arching leaves with a citrus scent.","Seguir la dirección de las hojas largas desde la base.","Trace the long leaves from the base.","Puede irritar la piel; los aceites concentrados no deben ingerirse.","May irritate skin; concentrated oils should not be ingested."),
("Jengibre","Ginger","Zingiber officinale","herb","Hojas largas; la parte subterránea forma un rizoma.","Long leaves; the underground part forms a rhizome.","Observar la disposición de las hojas y aprender qué es un rizoma.","Observe leaf arrangement and learn what a rhizome is.","Los suplementos pueden interactuar con medicamentos; no usar para sustituir atención médica.","Supplements may interact with medicines; do not use to replace medical care."),
("Cúrcuma","Turmeric","Curcuma longa","herb","Hojas amplias y rizoma de color intenso.","Broad leaves and a strongly colored rhizome.","Observar el tamaño de las hojas y la forma de crecimiento.","Observe leaf size and growth pattern.","Los suplementos concentrados pueden tener riesgos e interacciones; no aplicar polvo en ojos o heridas.","Concentrated supplements may carry risks and interactions; do not apply powder to eyes or wounds."),
("Perejil","Parsley","Petroselinum crispum","herb","Hojas verdes divididas y tallos finos.","Divided green leaves and slender stems.","Comparar la división de las hojas con una hoja simple.","Compare divided leaves with a simple leaf.","No confundir con especies silvestres parecidas; las cantidades culinarias no equivalen a extractos concentrados.","Do not confuse it with similar wild species; culinary amounts are not equivalent to concentrated extracts."),
("Eneldo","Dill","Anethum graveolens","herb","Hojas muy finas y plumosas; flores agrupadas en umbelas.","Very fine feathery leaves; flowers clustered in umbels.","Observar el aspecto plumoso y la estructura de las agrupaciones.","Observe the feathery appearance and cluster structure.","Puede causar alergia; identificar la planta antes de consumirla.","May cause allergies; identify the plant before consuming it."),
("Hinojo","Fennel","Foeniculum vulgare","herb","Hojas finamente divididas y tallos erectos.","Finely divided leaves and upright stems.","Comparar la estructura de las hojas con un pequeño abanico.","Compare leaf structure with a small fan.","Puede causar alergias e interacciones; no consumir plantas silvestres de identidad incierta.","May cause allergies and interactions; do not eat wild plants of uncertain identity."),
("Flor de pascua silvestre","Wild poinsettia","Euphorbia heterophylla","toxic","Hojas de forma variable y pequeñas estructuras florales.","Variable-shaped leaves and small floral structures.","Observar diferencias entre hojas de una misma planta.","Observe differences between leaves on the same plant.","La savia de muchas euforbias es irritante; no tocar ni ingerir.","Sap from many spurges is irritating; do not touch or ingest."),
("Ave del paraíso","Bird of paradise","Strelitzia reginae","flower","Hojas grandes y flores de aspecto escultórico.","Large leaves and sculptural-looking flowers.","Observar la forma de las hojas y la estructura de la flor.","Observe leaf shapes and the flower structure.","Puede ser tóxica para mascotas si se ingiere; no consumir partes ornamentales.","May be toxic to pets if swallowed; do not eat ornamental parts."),
("Anturio","Anthurium","Anthurium andraeanum","toxic","Bráctea brillante y espádice central, con hojas lustrosas.","Glossy spathe and central spadix, with shiny leaves.","Distinguir la bráctea coloreada del espádice central.","Distinguish the colored spathe from the central spadix.","Contiene cristales irritantes; tóxico si se ingiere.","Contains irritating crystals; toxic if swallowed."),
("Vinca","Periwinkle","Catharanthus roseus","toxic","Flores simples de cinco pétalos y hojas brillantes.","Simple five-petaled flowers and glossy leaves.","Contar los pétalos visibles y observar la forma de la flor.","Count visible petals and observe flower shape.","Contiene alcaloides potentes; no ingerir ni preparar remedios caseros.","Contains potent alkaloids; do not ingest or make home remedies."),
("Adelfa","Oleander","Nerium oleander","toxic","Arbusto con hojas estrechas y flores agrupadas.","Shrub with narrow leaves and clustered flowers.","Observar desde lejos la forma de las hojas y flores.","Observe leaf and flower shapes from a distance.","Extremadamente tóxica si se ingiere; no tocar, quemar ni usar como remedio.","Extremely toxic if swallowed; do not touch, burn or use as a remedy."),
("Dedalera","Foxglove","Digitalis purpurea","toxic","Espigas florales con flores tubulares colgantes.","Flower spikes with hanging tubular flowers.","Observar la forma tubular desde una distancia segura.","Observe the tubular shape from a safe distance.","Extremadamente tóxica y puede afectar el corazón; no tocar ni ingerir.","Extremely toxic and can affect the heart; do not touch or ingest."),
("Cala","Calla lily","Zantedeschia aethiopica","toxic","Estructura floral en forma de embudo y hojas anchas.","Funnel-shaped floral structure and broad leaves.","Observar la curva de la estructura floral blanca.","Observe the curve of the white floral structure.","Contiene cristales irritantes; no ingerir ni manipular la savia.","Contains irritating crystals; do not ingest or handle sap."),
("Cinta o mala madre","Spider plant","Chlorophytum comosum","foliage","Hojas arqueadas con franjas y brotes colgantes.","Arching striped leaves and hanging plantlets.","Seguir una hoja hasta donde nace y observar los brotes.","Trace a leaf to its base and observe the plantlets.","Generalmente se cultiva como ornamental; no consumir plantas tratadas con químicos.","Commonly grown as an ornamental; do not eat plants treated with chemicals."),
("Aspidistra","Cast-iron plant","Aspidistra elatior","foliage","Hojas largas y firmes que nacen desde la base.","Long firm leaves emerging from the base.","Observar cómo las hojas salen directamente del suelo.","Observe how leaves emerge directly from the soil.","No ingerir plantas ornamentales sin identificación y revisión de seguridad.","Do not eat ornamental plants without identification and safety review."),
("Árbol de magnolia","Magnolia","Magnolia grandiflora","tree","Hojas coriáceas y flores grandes en algunas estaciones.","Leathery leaves and large flowers in some seasons.","Observar la textura y el contorno de las hojas.","Observe leaf texture and outlines.","No usar corteza, hojas o flores como remedio sin orientación profesional.","Do not use bark, leaves or flowers as remedies without professional guidance."),
("Jacaranda","Jacaranda","Jacaranda mimosifolia","tree","Hojas finamente divididas y floración violeta llamativa.","Finely divided leaves and striking violet blooms.","Observar el patrón de las hojas y el contraste de color.","Observe leaf patterns and color contrast.","No ingerir partes del árbol; observar desde una distancia segura.","Do not ingest tree parts; observe from a safe distance.")
]

def _plant_records():
    records={}
    for i,row in enumerate(_PLANT_ROWS,1):
        es,en,scientific,group,feature_es,feature_en,observe_es,observe_en,caution_es,caution_en=row
        pid=f"p{i:02d}"
        records[pid]={"id":pid,"name":{"es":es,"en":en},"scientific_name":scientific,"group":group,"characteristics":{"es":feature_es,"en":feature_en},"wellness_relation":{"es":"Actividad de atención plena: observar la forma, los colores y los detalles sin necesidad de hacer nada más.","en":"Mindful observation: notice shape, colors and details without needing to do anything else."},"observation":{"es":observe_es,"en":observe_en},"precautions":{"es":caution_es,"en":caution_en},"activity":{"es":f"Observa {es.lower()} durante unos minutos","en":f"Observe {en.lower()} for a few minutes"}}
    return records

PLANTS=_plant_records()
# DESCRIPCIONES BOTANICAS COMPLETAS PARA TODAS LAS FICHAS.
# Se agregan sin modificar los registros, funciones ni API existentes.
_PLANT_DESCRIPTIONS={
"es":{
"p01":"La manzanilla es una planta herbácea aromática conocida por sus pequeñas flores con pétalos blancos y un centro amarillo. Su aspecto delicado y su aroma característico permiten observar fácilmente la estructura de sus flores.",
"p02":"La menta es una planta aromática de hojas verdes, generalmente dentadas, y tallos que pueden extenderse y ramificarse. Existen distintas especies y variedades, por lo que la identificación exacta es importante.",
"p03":"La lavanda es una planta aromática que suele crecer como un pequeño arbusto. Presenta hojas estrechas y espigas florales que habitualmente tienen tonos violetas, aunque el color puede variar según la variedad.",
"p04":"El romero es un arbusto aromático de tallos leñosos y hojas estrechas, firmes y alargadas. Sus hojas suelen ser verdes por la parte superior y más claras por debajo, y desprenden un aroma característico.",
"p05":"La albahaca es una planta aromática de clima cálido, con hojas generalmente verdes, suaves y ovaladas. La forma, el tamaño y el aroma pueden variar entre sus numerosas variedades.",
"p06":"La sábila o aloe vera es una planta suculenta que forma una roseta de hojas gruesas y carnosas, habitualmente con bordes dentados. La apariencia exterior no permite determinar por sí sola la composición ni la seguridad de sus preparados.",
"p07":"Los helechos son plantas que no producen flores ni semillas. Se reproducen mediante esporas y suelen presentar frondas divididas en numerosos foliolos; sus formas y necesidades de humedad varían entre especies.",
"p08":"Las suculentas son plantas que almacenan agua en hojas, tallos o raíces. La especie de referencia, Echeveria elegans, suele formar una roseta compacta de hojas carnosas; otras suculentas pueden tener formas muy diferentes.",
"p09":"El girasol es una planta de tallo generalmente erguido, hojas anchas y ásperas y una inflorescencia grande con numerosas flores pequeñas agrupadas en el centro. Los pétalos exteriores suelen ser amarillos, aunque existen variedades de otros tonos.",
"p10":"La caléndula es una planta herbácea que produce flores habitualmente amarillas o anaranjadas. Sus inflorescencias están compuestas por numerosos elementos florales y sus hojas pueden presentar formas diferentes según su posición.",
"p11":"El tomillo es una planta aromática de porte bajo, con tallos que pueden volverse leñosos y hojas pequeñas. Sus flores suelen agruparse cerca de los extremos de las ramas y su aspecto depende de la variedad y las condiciones de cultivo.",
"p12":"El cilantro es una planta herbácea cuyas hojas pueden cambiar considerablemente de forma a medida que crece. Produce pequeñas flores agrupadas en umbelas y frutos redondeados que se utilizan como especia cuando corresponden a una planta correctamente identificada.",
"p13":"El poto es una planta ornamental trepadora o colgante con hojas brillantes, generalmente acorazonadas y a menudo salpicadas de amarillo o crema. Puede desarrollar raíces aéreas y crecer a lo largo de soportes o superficies.",
"p14":"La costilla de Adán o Monstera deliciosa es una planta tropical de hojas grandes que, al madurar, suelen desarrollar cortes y perforaciones. Su estructura foliar es una de sus características más reconocibles y puede cambiar con la edad de la planta.",
"p15":"Las orquídeas constituyen una familia muy diversa de plantas con flores. La referencia Phalaenopsis incluye especies e híbridos con flores duraderas, simétricas y raíces adaptadas a sus condiciones de crecimiento; sus necesidades varían según el ejemplar.",
"p16":"Los cactus son plantas adaptadas a almacenar agua, generalmente en tallos carnosos. Muchas especies presentan espinas y otras estructuras especializadas; sus tamaños, flores y formas varían ampliamente.",
"p17":"La hiedra común es una planta trepadora o rastrera que puede adherirse a superficies mediante raíces especializadas. Sus hojas suelen ser lobuladas en tallos jóvenes y pueden adoptar formas distintas en ramas maduras.",
"p18":"Los pinos son árboles o arbustos del género Pinus que presentan hojas en forma de aguja, a menudo agrupadas, y producen conos. La apariencia y las características de las agujas cambian entre especies.",
"p19":"El bambú pertenece a un grupo de gramíneas que suele formar tallos segmentados y hojas estrechas. Algunas especies crecen en grupos compactos y otras se extienden mediante rizomas; la forma y el tamaño varían considerablemente.",
"p20":"La expresión planta de interior describe numerosas especies cultivadas dentro de viviendas u otros edificios. Sin identificar la especie concreta no es posible establecer una descripción botánica específica, porque el tamaño, las hojas y las necesidades pueden ser muy diferentes.",
"p21":"El jazmín es el nombre común de diversas especies de arbustos y plantas trepadoras. Muchas presentan flores claras y aromáticas, pero la forma de las hojas, el crecimiento y las características de las flores dependen de la especie.",
"p22":"Las rosas pertenecen al género Rosa y pueden crecer como arbustos o trepadoras. Sus flores presentan numerosos pétalos en distintas formas y colores, y muchos tallos tienen espinas o estructuras similares.",
"p23":"Hibiscus rosa-sinensis es un arbusto ornamental tropical conocido por sus flores grandes y vistosas. La flor suele presentar cinco pétalos y una columna central de estambres; existen variedades de numerosos colores.",
"p24":"La gardenia es un arbusto de hojas verdes, firmes y brillantes que produce flores generalmente blancas y perfumadas. La apariencia y la floración dependen de la especie, la variedad y las condiciones de cultivo.",
"p25":"La violeta africana es una planta ornamental compacta, con hojas redondeadas y suaves que suelen formar una roseta. Sus flores pueden ser violetas, azules, rosadas o blancas, según la variedad.",
"p26":"Las begonias comprenden numerosas especies ornamentales con hojas de formas, colores y patrones variados. Sus flores también presentan diferencias importantes, por lo que el nombre común no identifica por sí solo una especie concreta.",
"p27":"Los geranios ornamentales que se cultivan habitualmente en macetas suelen pertenecer al género Pelargonium. Presentan hojas de formas diversas y flores agrupadas que pueden tener varios colores.",
"p28":"La petunia es una planta ornamental que produce flores con forma de embudo y una amplia variedad de colores. Se cultiva con frecuencia en jardines, jardineras y macetas, y puede presentar un crecimiento compacto o extendido.",
"p29":"Las dalias son plantas conocidas por sus flores compuestas de numerosas estructuras dispuestas en patrones variados. Existen variedades de distintos tamaños, colores y formas, desde flores sencillas hasta otras con muchas capas aparentes.",
"p30":"Las zinnias son plantas ornamentales que producen flores vistosas y coloridas. Sus inflorescencias pueden presentar un centro diferenciado y varias filas de flores periféricas; las variedades difieren en altura, tamaño y color.",
"p31":"El lirio de la paz es una planta tropical de hojas alargadas y verdes. Su estructura floral característica incluye una espata generalmente blanca que rodea un espádice central, y suele cultivarse como planta de interior.",
"p32":"La sansevieria, actualmente clasificada en el género Dracaena, presenta hojas rígidas y erguidas, a menudo con bandas o bordes de colores contrastantes. Su forma y altura dependen de la variedad.",
"p33":"El árbol de jade es una planta suculenta de tallos ramificados y hojas gruesas, carnosas y generalmente ovaladas. Con el tiempo puede adquirir aspecto de pequeño arbusto y desarrollar una estructura leñosa.",
"p34":"Las echeverias son plantas suculentas que suelen formar rosetas simétricas de hojas carnosas. Sus colores, tamaños y formas varían entre especies y cultivares, y algunas producen tallos florales elevados.",
"p35":"Las haworthias y plantas afines son pequeñas suculentas que suelen crecer en rosetas. Algunas presentan bandas blancas, puntos o superficies translúcidas en las hojas, características que ayudan a distinguir determinadas especies.",
"p36":"El árbol del dinero, Pachira aquatica, es un árbol tropical que puede cultivarse como ornamental. Sus hojas compuestas tienen varios foliolos que parten de un mismo punto y su tronco puede engrosarse con el crecimiento.",
"p37":"Ficus elastica es un árbol tropical conocido por sus hojas grandes, ovaladas, gruesas y brillantes. Las hojas nuevas pueden aparecer protegidas por una estructura envolvente, y la planta produce una savia característica.",
"p38":"Los filodendros forman un grupo diverso de plantas tropicales, muchas de ellas trepadoras o de crecimiento erguido. Sus hojas varían mucho en tamaño y forma, y algunas especies desarrollan raíces aéreas.",
"p39":"Las calateas y plantas relacionadas son ornamentales apreciadas por sus hojas decoradas con líneas, franjas y contrastes de color. La forma de las hojas y sus patrones dependen de la especie y la variedad.",
"p40":"La maranta es una planta tropical de porte bajo con hojas decoradas por patrones contrastantes. Sus hojas pueden cambiar de posición durante el día y suelen cultivarse en ambientes con luz indirecta.",
"p41":"Las drácenas son plantas ornamentales que pueden tener hojas estrechas o anchas, dispuestas en rosetas o sobre tallos erguidos. La apariencia cambia mucho entre especies y variedades comercializadas.",
"p42":"La palmera areca es una palmera tropical que forma grupos de tallos y frondas arqueadas compuestas por numerosos foliolos estrechos. Se cultiva con frecuencia en interiores luminosos y jardines cálidos.",
"p43":"La palma de salón es una palmera pequeña con tallos delgados y frondas finas que se arquean suavemente. Es común como planta ornamental de interior y crece relativamente despacio.",
"p44":"Hevea brasiliensis es un árbol tropical relacionado con la producción comercial de caucho natural. Sus hojas son compuestas y su tronco contiene látex, una sustancia que requiere precauciones de contacto.",
"p45":"El olivo es un árbol de hojas estrechas, persistentes y verde grisáceas, cuyo envés suele ser más claro. Produce flores pequeñas y frutos que se desarrollan en condiciones adecuadas de clima y cultivo.",
"p46":"El limonero es un árbol o arbusto cítrico de hojas verdes y aromáticas, flores claras y frutos amarillos al madurar. Las ramas pueden presentar espinas y la forma del árbol depende de la variedad y la poda.",
"p47":"El naranjo es un árbol cítrico de hojas verdes y brillantes que puede producir flores blancas y frutos anaranjados. Su crecimiento, tamaño y fructificación dependen de la variedad, el clima y el cultivo.",
"p48":"El mango es un árbol tropical de copa amplia y hojas largas, que pueden mostrar tonos rojizos o bronceados cuando son jóvenes. Produce frutos cuya forma, color y tamaño cambian según la variedad.",
"p49":"La guayaba es un árbol o arbusto tropical con hojas opuestas, nervaduras visibles y textura algo rugosa. Puede producir flores claras y frutos redondeados, aunque las características concretas varían con el cultivo.",
"p50":"El aguacate es un árbol de hoja perenne que puede desarrollar una copa amplia y hojas elípticas. Produce flores pequeñas y frutos cuya forma y piel varían entre variedades; las hojas y otras partes no deben confundirse con alimentos seguros para animales.",
"p51":"Las plantas de plátano pertenecen al género Musa y presentan hojas muy grandes que se despliegan desde un pseudotallo formado por las bases foliares. Las hojas pueden rasgarse con el viento y la planta produce racimos de frutos en condiciones adecuadas.",
"p52":"El bambú de la suerte es una planta ornamental de tallos verdes segmentados que se comercializa con frecuencia en recipientes con agua. Aunque su nombre popular incluye la palabra bambú, botánicamente pertenece al género Dracaena.",
"p53":"La hiedra sueca es una planta ornamental de tallos flexibles, hojas redondeadas y crecimiento extendido o colgante. El nombre común puede aplicarse a plantas de aspecto parecido, por lo que la identificación botánica es importante.",
"p54":"Tradescantia zebrina es una planta de tallos rastreros y hojas ovaladas que suelen mostrar bandas verdes, plateadas o violáceas. Crece y se propaga con facilidad en condiciones adecuadas.",
"p55":"El coleo es una planta ornamental apreciada por sus hojas de colores intensos, con combinaciones de verde, amarillo, rojo, rosa o púrpura. Los patrones y bordes cambian según la variedad y las condiciones de crecimiento.",
"p56":"El croton es una planta tropical ornamental con hojas firmes y brillantes que pueden combinar verde, amarillo, naranja y rojo. La forma de las hojas y sus patrones de color varían entre variedades.",
"p57":"La poinsettia o flor de Pascua es una planta ornamental cuyas partes coloreadas más llamativas son brácteas que rodean pequeñas flores centrales. Las brácteas suelen ser rojas, aunque existen variedades blancas, rosadas y de otros tonos.",
"p58":"Los narcisos son plantas bulbosas que producen hojas alargadas y flores con una corona central característica. La forma y el color varían entre especies y cultivares, y el bulbo debe tratarse como una parte potencialmente tóxica.",
"p59":"Los tulipanes son plantas bulbosas conocidas por sus flores generalmente solitarias, con forma de copa, y sus hojas alargadas. Existen numerosas variedades de diferentes colores y formas de flor.",
"p60":"Los crisantemos son plantas con flores compuestas que pueden presentar numerosas capas y una gran diversidad de formas y colores. Se cultivan como ornamentales y sus características dependen de la especie y el cultivar.",
"p61":"El diente de león es una planta herbácea con hojas que suelen formar una roseta basal y flores amarillas. Después de la floración puede producir una esfera de frutos con estructuras plumosas que facilitan su dispersión por el viento.",
"p62":"Los tréboles pertenecen al género Trifolium y suelen presentar hojas compuestas por tres foliolos. Sus flores aparecen agrupadas en cabezuelas y pueden variar en color según la especie.",
"p63":"La hierbabuena, Mentha spicata, es una planta aromática de hojas verdes y dentadas que puede extenderse mediante tallos subterráneos o rastreros. Se parece a otras mentas, por lo que conviene confirmar la especie antes de utilizarla.",
"p64":"La salvia común es una planta aromática de hojas gris verdosas, alargadas y algo aterciopeladas. Puede formar un pequeño arbusto y produce flores agrupadas en tallos florales.",
"p65":"El orégano es una planta aromática con hojas pequeñas y tallos ramificados que pueden volverse leñosos en la base. Sus flores pequeñas suelen agruparse en las partes superiores de los tallos.",
"p66":"El toronjil o melisa es una planta aromática de hojas verdes con bordes dentados y aroma cítrico suave. Sus tallos son ramificados y puede producir pequeñas flores claras durante la temporada de floración.",
"p67":"La hierba limón es una gramínea aromática de hojas largas, estrechas y arqueadas. Forma grupos densos y desprende un aroma cítrico característico cuando sus hojas se rozan, aunque no es necesario tocarlas para observar su forma.",
"p68":"El jengibre es una planta herbácea tropical con hojas largas y estrechas que nacen de tallos aéreos. Su estructura subterránea es un rizoma, es decir, un tallo modificado que crece horizontalmente.",
"p69":"La cúrcuma es una planta tropical de hojas amplias y alargadas que crece a partir de rizomas subterráneos, generalmente de color amarillo anaranjado intenso. La apariencia de la planta varía según la etapa de crecimiento y la variedad.",
"p70":"El perejil es una planta herbácea con hojas verdes divididas y tallos finos. Las hojas pueden ser lisas o rizadas según la variedad y su identificación debe distinguirse de otras plantas de aspecto similar.",
"p71":"El eneldo es una planta herbácea de hojas muy finas y plumosas. Produce flores pequeñas agrupadas en umbelas, una estructura en la que varios radios parten de un punto común.",
"p72":"El hinojo es una planta de tallos erguidos y hojas finamente divididas, de aspecto plumoso. Puede producir umbelas de flores amarillas y desarrollar una base engrosada en ciertas variedades cultivadas.",
"p73":"Euphorbia heterophylla es una planta herbácea cuyas hojas pueden variar mucho de forma a lo largo del tallo. Como otras euforbias, puede producir una savia irritante y no debe manipularse sin identificación y precauciones adecuadas.",
"p74":"El ave del paraíso es una planta ornamental de hojas grandes y firmes, con flores de estructura llamativa que recuerdan la silueta de un ave. Se cultiva en climas cálidos y su floración depende de la especie y las condiciones.",
"p75":"El anturio es una planta tropical ornamental con hojas brillantes y una inflorescencia formada por un espádice central rodeado de una espata, que suele ser roja o de otro color intenso. Su aspecto varía entre especies e híbridos.",
"p76":"Catharanthus roseus, conocida como vinca de Madagascar, es una planta de hojas brillantes y flores con cinco pétalos. Contiene alcaloides potentes, por lo que no debe ingerirse ni utilizarse para preparar remedios caseros.",
"p77":"La adelfa es un arbusto ornamental de hojas estrechas y alargadas que produce flores agrupadas de diversos colores. Todas sus partes son altamente tóxicas, por lo que debe observarse sin tocarla ni manipular sus restos.",
"p78":"La dedalera es una planta que puede formar altas espigas con flores tubulares colgantes. Su aspecto es reconocible, pero contiene sustancias que pueden afectar gravemente al corazón y debe evitarse todo contacto o ingestión.",
"p79":"La cala es una planta ornamental con hojas anchas y una estructura floral en forma de embudo, llamada espata, que rodea un espádice. Contiene cristales irritantes y no debe ingerirse ni manipularse la savia.",
"p80":"La cinta o mala madre es una planta ornamental con hojas largas y arqueadas, a menudo con franjas claras. Puede producir tallos colgantes con pequeñas plantas nuevas que permiten su propagación.",
"p81":"La aspidistra es una planta de hojas largas, firmes y verdes que emergen directamente desde la base. Se cultiva como ornamental por su resistencia y su capacidad de adaptarse a condiciones de interior.",
"p82":"La magnolia es un árbol o arbusto que puede presentar hojas firmes y flores grandes y llamativas. Algunas especies tienen hojas persistentes y otras las pierden por temporada; la apariencia depende de la especie.",
"p83":"La jacaranda es un árbol ornamental que destaca por sus hojas compuestas muy divididas y sus flores violetas o azuladas, agrupadas en racimos. Su floración y aspecto cambian con el clima, la estación y la edad del árbol."
},
"en":{
"p01":"Chamomile is an aromatic herb known for its small flowers with white petals and yellow centers. Its delicate appearance and characteristic scent make the structure of its flowers easy to observe.",
"p02":"Mint is an aromatic plant with green, usually toothed leaves and stems that can spread and branch. Several species and varieties exist, so accurate identification matters.",
"p03":"Lavender is an aromatic plant that often grows as a small shrub. It has narrow leaves and flower spikes that are usually purple, although color varies by variety.",
"p04":"Rosemary is an aromatic shrub with woody stems and narrow, firm leaves. The leaves are often green above and lighter underneath, with a characteristic scent.",
"p05":"Basil is a warm-weather aromatic plant with generally green, soft, oval leaves. Leaf shape, size and aroma vary among its many varieties.",
"p06":"Aloe vera is a succulent that forms a rosette of thick, fleshy leaves, usually with toothed edges. Appearance alone cannot establish the composition or safety of aloe preparations.",
"p07":"Ferns are plants that do not produce flowers or seeds. They reproduce by spores and often have fronds divided into many leaflets; their shapes and moisture needs vary by species.",
"p08":"Succulents store water in leaves, stems or roots. The reference species, Echeveria elegans, usually forms a compact rosette of fleshy leaves; other succulents can look very different.",
"p09":"The sunflower is an upright-stemmed plant with broad, rough leaves and a large flower head containing many small flowers at its center. The outer florets are often yellow, though other colors exist.",
"p10":"Calendula is an herbaceous plant that produces usually yellow or orange flower heads. Each head contains many floral structures, and leaf shape may differ by position.",
"p11":"Thyme is a low-growing aromatic plant with small leaves and stems that may become woody. Its flowers often cluster near branch tips, and its appearance depends on variety and growing conditions.",
"p12":"Cilantro is an herb whose leaves can change considerably in shape as it grows. It produces small flowers in umbels and rounded fruits used as a spice when correctly identified.",
"p13":"Golden pothos is a climbing or trailing ornamental plant with glossy, usually heart-shaped leaves often marked with yellow or cream. It can develop aerial roots and grow along supports.",
"p14":"Monstera deliciosa is a tropical plant with large leaves that often develop splits and holes as they mature. Its distinctive leaf structure changes as the plant grows.",
"p15":"Orchids are a diverse family of flowering plants. Phalaenopsis species and hybrids often have symmetrical, long-lasting flowers and roots adapted to their growing conditions; care needs vary.",
"p16":"Cacti are plants adapted to storing water, generally in fleshy stems. Many species have spines and other specialized structures, and their sizes, flowers and shapes vary widely.",
"p17":"English ivy is a climbing or trailing plant that can attach to surfaces using specialized roots. Its leaves are often lobed on young stems and may look different on mature branches.",
"p18":"Pines are trees or shrubs in the genus Pinus. They have needle-like leaves, often grouped together, and produce cones; needle appearance varies among species.",
"p19":"Bamboo belongs to a group of grasses that commonly have segmented stems and narrow leaves. Some species form compact clumps while others spread by rhizomes; size and form vary widely.",
"p20":"Houseplant is a general term for many species grown inside homes or buildings. Without identifying the specific species, a precise botanical description is not possible because appearance and care needs differ greatly.",
"p21":"Jasmine is a common name for several shrub and climbing-plant species. Many have pale, fragrant flowers, but leaf shape, growth and floral characteristics depend on the species.",
"p22":"Roses belong to the genus Rosa and may grow as shrubs or climbers. Their flowers have numerous petals in varied forms and colors, and many stems bear thorns or similar structures.",
"p23":"Hibiscus rosa-sinensis is a tropical ornamental shrub known for large, showy flowers. A flower typically has five petals and a central column of stamens; varieties come in many colors.",
"p24":"Gardenia is a shrub with firm, glossy green leaves and generally white, fragrant flowers. Its appearance and flowering depend on species, variety and growing conditions.",
"p25":"African violet is a compact ornamental plant with rounded, soft leaves that often form a rosette. Flowers may be purple, blue, pink or white depending on variety.",
"p26":"Begonias include many ornamental species with leaves of varied shapes, colors and patterns. Flowers also differ substantially, so the common name alone does not identify one specific species.",
"p27":"Ornamental geraniums commonly grown in pots often belong to the genus Pelargonium. They have leaves of varied shapes and clustered flowers in many colors.",
"p28":"Petunia is an ornamental plant that produces funnel-shaped flowers in a wide range of colors. It is commonly grown in gardens, planters and pots, with compact or spreading growth.",
"p29":"Dahlias are known for flower heads with many structures arranged in varied patterns. Varieties differ in size, color and form, from simple blooms to flowers with many apparent layers.",
"p30":"Zinnias are ornamental plants that produce colorful, showy flower heads. Their heads may have a distinct center and rows of outer florets; varieties differ in height, size and color.",
"p31":"Peace lily is a tropical plant with long green leaves. Its distinctive flower structure includes a usually white spathe surrounding a central spadix, and it is commonly grown indoors.",
"p32":"The snake plant, now classified in the genus Dracaena, has stiff upright leaves, often with contrasting bands or edges. Its height and shape depend on the variety.",
"p33":"The jade plant is a succulent with branching stems and thick, fleshy, usually oval leaves. Over time it can develop a small-shrub appearance and woody structure.",
"p34":"Echeverias are succulents that usually form symmetrical rosettes of fleshy leaves. Colors, sizes and shapes vary by species and cultivar, and some produce raised flower stalks.",
"p35":"Haworthias and related plants are small succulents that often grow in rosettes. Some have white bands, spots or translucent leaf surfaces that help distinguish certain species.",
"p36":"The money tree, Pachira aquatica, is a tropical tree that can be grown ornamentally. Its compound leaves have several leaflets radiating from one point, and its trunk may thicken with age.",
"p37":"Ficus elastica is a tropical tree known for large, oval, thick and glossy leaves. New leaves may emerge enclosed in a protective structure, and the plant produces characteristic sap.",
"p38":"Philodendrons are a diverse group of tropical plants, many climbing or growing upright. Their leaves vary greatly in size and shape, and some species develop aerial roots.",
"p39":"Calatheas and related plants are ornamental plants valued for leaves marked with lines, stripes and contrasting colors. Leaf shape and patterns depend on species and variety.",
"p40":"Prayer plant is a low-growing tropical plant with leaves marked by contrasting patterns. Its leaves may change position throughout the day, and it is often grown in indirect light.",
"p41":"Dracaenas are ornamental plants with narrow or broad leaves arranged in rosettes or along upright stems. Appearance varies considerably among species and commercial varieties.",
"p42":"The areca palm is a tropical palm that forms clusters of stems and arching fronds made up of many narrow leaflets. It is often grown indoors in bright conditions and in warm gardens.",
"p43":"The parlor palm is a small palm with slender stems and fine, gently arching fronds. It is a common indoor ornamental and grows relatively slowly.",
"p44":"Hevea brasiliensis is a tropical tree associated with commercial natural-rubber production. Its leaves are compound, and its trunk contains latex, which requires contact precautions.",
"p45":"The olive tree is an evergreen tree with narrow, gray-green leaves whose undersides are usually lighter. It produces small flowers and fruits under suitable climate and growing conditions.",
"p46":"The lemon tree is a citrus tree or shrub with aromatic green leaves, pale flowers and yellow fruit when ripe. Branches may have thorns, and shape depends on variety and pruning.",
"p47":"The orange tree is a citrus tree with glossy green leaves that may produce white flowers and orange-colored fruit. Growth and fruiting depend on variety, climate and cultivation.",
"p48":"Mango is a tropical tree with a broad crown and long leaves that may be reddish or bronze when young. Its fruit shape, color and size vary by variety.",
"p49":"Guava is a tropical tree or shrub with opposite leaves, visible veins and a somewhat rough texture. It may produce pale flowers and rounded fruits, with traits varying by cultivar.",
"p50":"Avocado is an evergreen tree that can develop a broad crown and elliptical leaves. It produces small flowers and fruits whose shape and skin vary by variety; leaves and other parts should not be assumed safe for animals.",
"p51":"Banana plants belong to the genus Musa and have very large leaves emerging from a pseudostem formed by leaf bases. Leaves may split in wind, and the plant can produce fruit bunches under suitable conditions.",
"p52":"Lucky bamboo is an ornamental plant with green segmented stems, often sold in containers of water. Despite its common name, it is botanically a member of the genus Dracaena, not true bamboo.",
"p53":"Swedish ivy is an ornamental plant with flexible stems, rounded leaves and trailing or spreading growth. The common name can be applied to similar-looking plants, so botanical identification matters.",
"p54":"Tradescantia zebrina is a trailing plant with oval leaves that often show green, silver or purple stripes. It grows and propagates readily under suitable conditions.",
"p55":"Coleus is an ornamental plant valued for intensely colored leaves combining green, yellow, red, pink or purple. Patterns and edges vary by variety and growing conditions.",
"p56":"Croton is a tropical ornamental plant with firm, glossy leaves that may combine green, yellow, orange and red. Leaf shape and color patterns vary among varieties.",
"p57":"Poinsettia is an ornamental plant whose most striking colored parts are bracts surrounding small central flowers. Bracts are often red, though white, pink and other varieties exist.",
"p58":"Daffodils are bulbous plants with long leaves and flowers featuring a distinctive central trumpet. Shape and color vary among species and cultivars, and bulbs should be treated as potentially toxic.",
"p59":"Tulips are bulbous plants known for usually solitary, cup-shaped flowers and long leaves. Many varieties have different colors and flower shapes.",
"p60":"Chrysanthemums are plants with composite flower heads that may have many layers and a wide range of shapes and colors. They are grown ornamentally, and traits depend on species and cultivar.",
"p61":"Dandelion is an herbaceous plant whose leaves often form a basal rosette and whose flowers are yellow. After flowering, it may form a spherical seed head with feathery structures that help wind dispersal.",
"p62":"Clovers belong to the genus Trifolium and usually have leaves composed of three leaflets. Their flowers grow in rounded heads and vary in color by species.",
"p63":"Spearmint, Mentha spicata, is an aromatic plant with green toothed leaves that may spread through underground or trailing stems. It resembles other mints, so confirm the species before use.",
"p64":"Common sage is an aromatic plant with gray-green, elongated and somewhat velvety leaves. It can form a small shrub and produces flowers on upright flowering stems.",
"p65":"Oregano is an aromatic plant with small leaves and branching stems that may become woody at the base. Its small flowers often cluster near the upper parts of the stems.",
"p66":"Lemon balm is an aromatic plant with green toothed leaves and a mild citrus scent. Its stems branch and may produce small pale flowers during the flowering season.",
"p67":"Lemongrass is an aromatic grass with long, narrow, arching leaves. It forms dense clumps and has a characteristic citrus scent, although touching the leaves is not necessary for observation.",
"p68":"Ginger is a tropical herb with long, narrow leaves growing from above-ground shoots. Its underground structure is a rhizome, a modified stem that grows horizontally.",
"p69":"Turmeric is a tropical plant with broad, elongated leaves that grows from underground rhizomes, usually deep yellow-orange in color. Appearance varies with growth stage and variety.",
"p70":"Parsley is an herbaceous plant with divided green leaves and slender stems. Leaves may be flat or curly depending on variety, and identification should distinguish it from similar-looking plants.",
"p71":"Dill is an herbaceous plant with very fine, feathery leaves. It produces small flowers grouped in umbels, where several rays originate from a common point.",
"p72":"Fennel is a plant with upright stems and finely divided, feathery leaves. It may produce yellow umbels and develop a swollen base in certain cultivated varieties.",
"p73":"Euphorbia heterophylla is an herbaceous plant whose leaves may vary considerably in shape along the stem. Like other spurges, it may produce irritating sap and should not be handled without proper identification and precautions.",
"p74":"Bird of paradise is an ornamental plant with large, firm leaves and striking flowers whose structure resembles a bird. It is grown in warm climates, and flowering depends on species and conditions.",
"p75":"Anthurium is a tropical ornamental plant with glossy leaves and an inflorescence made up of a central spadix surrounded by a spathe, often red or another vivid color. Appearance varies among species and hybrids.",
"p76":"Catharanthus roseus, known as Madagascar periwinkle, is a plant with glossy leaves and five-petaled flowers. It contains potent alkaloids and must not be ingested or used for homemade remedies.",
"p77":"Oleander is an ornamental shrub with narrow, elongated leaves and clusters of flowers in various colors. All parts are highly toxic, so observe it without touching or handling its remains.",
"p78":"Foxglove is a plant that may produce tall spikes of hanging, tubular flowers. It is recognizable, but contains substances that can seriously affect the heart, so contact and ingestion must be avoided.",
"p79":"Calla lily is an ornamental plant with broad leaves and a funnel-shaped floral structure called a spathe surrounding a spadix. It contains irritating crystals and must not be eaten or handled by its sap.",
"p80":"The spider plant is an ornamental plant with long, arching leaves, often striped with pale colors. It can produce hanging stems bearing small plantlets that allow propagation.",
"p81":"Cast-iron plant has long, firm green leaves that emerge directly from the base. It is grown ornamentally for its resilience and ability to adapt to indoor conditions.",
"p82":"Magnolia is a tree or shrub that may have firm leaves and large, showy flowers. Some species are evergreen and others are deciduous; appearance depends on the species.",
"p83":"Jacaranda is an ornamental tree known for finely divided compound leaves and violet or bluish flowers arranged in clusters. Flowering and appearance vary with climate, season and tree age."
}}

for _pid,_plant in PLANTS.items():
    _plant["description"]={
        "es":_PLANT_DESCRIPTIONS["es"].get(_pid,"Descripción botánica específica pendiente de verificación."),
        "en":_PLANT_DESCRIPTIONS["en"].get(_pid,"Specific botanical description pending verification.")
    }

# Veinte guiones por categoría. Cada actividad obtiene una secuencia propia
# de veinte instrucciones, en ambos idiomas.
_STEPS={
"calm":[
("Apoya los pies y nota el contacto con el suelo.","Place your feet down and notice their contact with the floor."),
("Mira un punto cómodo delante de ti.","Look at a comfortable point in front of you."),
("Suelta los hombros solo hasta donde resulte natural.","Let your shoulders soften only as much as feels natural."),
("Inhala con suavidad, sin forzar el aire.","Breathe in gently without forcing the air."),
("Deja que la exhalación siga su propio ritmo.","Let the exhale follow its own rhythm."),
("Nota tres cosas que puedes ver.","Notice three things you can see."),
("Escucha un sonido cercano y otro lejano.","Listen for one nearby sound and one distant sound."),
("Relaja las manos si te resulta cómodo.","Relax your hands if comfortable."),
("Observa el apoyo de la espalda o del asiento.","Notice the support of your back or seat."),
("Permite que la respiración sea normal.","Allow your breathing to remain natural."),
("Mira cómo cambia la luz en tu entorno.","Notice how light changes in your surroundings."),
("Nombra mentalmente un detalle agradable o neutral.","Silently name one pleasant or neutral detail."),
("Afloja la mandíbula sin apretar los dientes.","Unclench your jaw without pressing your teeth together."),
("Nota la temperatura del aire en la piel.","Notice the air temperature on your skin."),
("Deja pasar un pensamiento sin tener que resolverlo ahora.","Let a thought pass without needing to solve it now."),
("Vuelve con atención a los pies.","Bring your attention back to your feet."),
("Elige una palabra sencilla para este momento.","Choose a simple word for this moment."),
("Haz una pausa breve antes del siguiente movimiento.","Pause briefly before your next movement."),
("Observa cómo te encuentras sin juzgarte.","Notice how you feel without judging yourself."),
("Decide cuál será tu siguiente paso pequeño.","Choose your next small step.")
],
"movement":[
("Siéntate o ponte de pie de forma estable.","Sit or stand in a stable position."),
("Comprueba que tienes espacio a tu alrededor.","Check that you have space around you."),
("Mueve lentamente los dedos de las manos.","Slowly move your fingers."),
("Haz círculos pequeños con los hombros si te resulta cómodo.","Make small shoulder circles if comfortable."),
("Mira a un lado y luego al centro, sin forzar el cuello.","Look to one side and then center without straining your neck."),
("Abre y cierra las manos con suavidad.","Gently open and close your hands."),
("Estira los dedos y después suéltalos.","Stretch your fingers and then release."),
("Mueve los tobillos dentro de un rango cómodo.","Move your ankles within a comfortable range."),
("Si estás sentado, cambia suavemente el apoyo de los pies.","If seated, gently shift how your feet rest."),
("Si estás de pie, reparte el peso sin perder estabilidad.","If standing, distribute your weight while staying stable."),
("Alarga la columna sin arquear la espalda.","Lengthen your spine without arching your back."),
("Deja que los brazos descansen antes del siguiente movimiento.","Let your arms rest before the next movement."),
("Realiza una elevación pequeña de talones si es seguro.","Raise your heels slightly if safe."),
("Vuelve a una postura cómoda.","Return to a comfortable posture."),
("Haz un movimiento lento que te resulte fácil.","Make one slow movement that feels easy."),
("Detente si aparece dolor, mareo o malestar.","Stop if pain, dizziness or discomfort appears."),
("Comprueba que puedes respirar con normalidad.","Check that you can breathe normally."),
("Reduce el recorrido si lo necesitas.","Reduce the range if needed."),
("Relaja las partes del cuerpo que no estás moviendo.","Relax body parts you are not moving."),
("Termina con una postura estable y cómoda.","Finish in a stable, comfortable posture.")
],
"plants":[
("Mira la planta completa antes de elegir un detalle.","Look at the whole plant before choosing one detail."),
("Observa la forma general de sus hojas.","Notice the overall shape of its leaves."),
("Busca un borde, una línea o una curva.","Find an edge, line or curve."),
("Compara dos tonos visibles.","Compare two visible shades."),
("Fíjate en cómo se distribuyen las hojas.","Notice how the leaves are arranged."),
("Observa la dirección en la que crece el tallo.","Notice the direction in which the stem grows."),
("Busca un patrón que se repita.","Look for a repeating pattern."),
("Observa las zonas iluminadas y las zonas en sombra.","Notice the lit areas and the shaded areas."),
("Mira una textura sin tocarla.","Notice a texture without touching it."),
("Cuenta lentamente tres detalles de la planta.","Slowly count three details of the plant."),
("Compara una hoja grande con una pequeña, si las hay.","Compare a large leaf with a small one, if present."),
("Observa cómo se relaciona la planta con su maceta o entorno.","Notice how the plant relates to its pot or surroundings."),
("Busca un detalle que no habías notado al principio.","Find a detail you did not notice at first."),
("Describe mentalmente la planta con tres palabras.","Describe the plant silently in three words."),
("Observa sin arrancar hojas ni flores.","Observe without removing leaves or flowers."),
("Recuerda que la identificación importa antes de tocar una planta desconocida.","Remember that identification matters before touching an unknown plant."),
("Mira el conjunto una vez más.","Look at the whole plant once more."),
("Elige el detalle que más llamó tu atención.","Choose the detail that caught your attention most."),
("Haz una respiración natural mientras observas.","Breathe naturally as you observe."),
("Termina agradeciendo este momento de atención.","Finish by appreciating this moment of attention.")
],
"coach":[
("Elige una sola cosa que quieras atender ahora.","Choose one thing you want to focus on now."),
("Describe el objetivo con palabras sencillas.","Describe the goal in simple words."),
("Distingue lo que puedes hacer de lo que no controlas.","Separate what you can do from what you cannot control."),
("Divide la tarea en un paso pequeño.","Break the task into one small step."),
("Piensa qué necesitas tener a mano.","Consider what you need to have ready."),
("Calcula un tiempo realista para empezar.","Estimate a realistic time to begin."),
("Retira una distracción si está a tu alcance.","Remove one distraction if you can."),
("Decide qué significa terminar ese primer paso.","Decide what finishing the first step means."),
("Piensa en una dificultad posible sin anticipar todas las demás.","Consider one possible difficulty without anticipating every other one."),
("Elige una alternativa sencilla si aparece esa dificultad.","Choose a simple alternative if that difficulty appears."),
("Haz una pausa para revisar tu plan.","Pause to review your plan."),
("Comprueba si tu primer paso sigue siendo realista.","Check whether your first step is still realistic."),
("Reduce el objetivo si ahora parece demasiado grande.","Scale down the goal if it feels too large now."),
("Piensa qué información necesitas y dónde verificarla.","Consider what information you need and where to verify it."),
("Elige cuándo comenzar, aunque sea por poco tiempo.","Choose when to begin, even briefly."),
("Decide cómo recordarás el siguiente paso.","Decide how you will remember the next step."),
("Reconoce el esfuerzo de organizarte.","Acknowledge the effort of getting organized."),
("Evita exigirte resolverlo todo en este momento.","Avoid demanding that you solve everything right now."),
("Resume tu plan en una frase.","Summarize your plan in one sentence."),
("Elige una acción concreta para después de esta sesión.","Choose one concrete action for after this session.")
]}

_TITLES={
"calm":[("Pausa consciente","Mindful pause"),("Respirar sin prisa","Unhurried breathing"),("Atención al presente","Attention to the present"),("Un minuto de quietud","A moment of stillness"),("Escucha tranquila","Quiet listening"),("Soltar tensión cotidiana","Release everyday tension"),("Volver al momento","Return to the moment"),("Pausa de los sentidos","Sensory pause"),("Descanso de atención","Attention break"),("Un espacio de calma","A space for calm"),("Respiración natural","Natural breathing"),("Observar sin juzgar","Observe without judgment"),("Pausa de los hombros","Shoulder pause"),("Escucha del entorno","Listening to your surroundings"),("Atención amable","Gentle attention"),("Descanso breve","Short rest"),("Punto de apoyo","A point of support"),("Pausa entre tareas","Pause between tasks"),("Un momento para ti","A moment for yourself"),("Cerrar con calma","Finish calmly")],
"movement":[("Movimiento suave","Gentle movement"),("Despertar las manos","Wake up your hands"),("Hombros cómodos","Comfortable shoulders"),("Movilidad de tobillos","Ankle mobility"),("Pausa activa","Active break"),("Cambiar de postura","Change posture"),("Estiramiento ligero","Light stretching"),("Movimiento sentado","Seated movement"),("Movimiento de pie","Standing movement"),("Soltar las manos","Release your hands"),("Postura estable","Stable posture"),("Pequeños movimientos","Small movements"),("Activar el cuerpo con suavidad","Gently activate your body"),("Descanso del escritorio","Desk break"),("Movimiento consciente","Mindful movement"),("Movilidad sin prisa","Unhurried mobility"),("Pausa para el cuerpo","A pause for your body"),("Movimiento accesible","Accessible movement"),("Volver a una postura cómoda","Return to a comfortable posture"),("Terminar con equilibrio","Finish with balance")],
"plants":[("Mirar con atención","Observe with attention"),("Detalles de la naturaleza","Nature's details"),("Pausa verde","Green pause"),("Observar formas","Observe shapes"),("Colores naturales","Natural colors"),("Patrones de hojas","Leaf patterns"),("Pequeños detalles","Small details"),("Un momento con una planta","A moment with a plant"),("Texturas a la vista","Textures to notice"),("La forma de crecer","The shape of growth"),("Observar sin prisa","Observe unhurriedly"),("Luz y sombra","Light and shadow"),("Una mirada nueva","A fresh look"),("Geometría natural","Natural geometry"),("Atención al entorno","Attention to surroundings"),("La planta y su espacio","The plant and its space"),("Detalles que se repiten","Repeating details"),("Mirada tranquila","Quiet observation"),("Un detalle diferente","A different detail"),("Cerrar observando","Finish by observing")],
"coach":[("Plan de un paso","One-step plan"),("Organizar sin prisa","Organize without rushing"),("Elegir una prioridad","Choose a priority"),("Preparar el siguiente paso","Prepare the next step"),("Reducir una tarea","Make a task smaller"),("Claridad para empezar","Clarity to begin"),("Resolver una cosa","Handle one thing"),("Tiempo realista","Realistic timing"),("Plan sencillo","Simple plan"),("Preparación práctica","Practical preparation"),("Enfoque amable","Gentle focus"),("Revisar opciones","Review options"),("Un objetivo posible","An achievable goal"),("Pausa para decidir","Pause to decide"),("Ordenar las ideas","Organize your thoughts"),("Preparar el entorno","Prepare your surroundings"),("Elegir qué sigue","Choose what comes next"),("Menos pasos, más claridad","Fewer steps, more clarity"),("Un comienzo concreto","A concrete start"),("Cerrar con una decisión","Finish with a decision")]}

_DESCRIPTIONS={
"plants":{"es":"Actividad de observación de la naturaleza. No requiere tocar, cortar ni ingerir la planta.","en":"A nature-observation activity. No touching, cutting or eating the plant is required."},
"movement":{"es":"Movimiento cotidiano suave y adaptable. Haz solo lo que resulte cómodo y seguro.","en":"Gentle, adaptable everyday movement. Do only what feels comfortable and safe."},
"calm":{"es":"Una pausa general de atención al presente, sin promesas médicas ni necesidad de cambiar la respiración.","en":"A general present-moment pause, with no medical promises or need to change your breathing."},
"coach":{"es":"Una actividad sencilla para organizar prioridades y elegir un siguiente paso práctico.","en":"A simple activity to organize priorities and choose a practical next step."}}


def _steps_for(section,index,lang=None,plant=None):
    base=_STEPS[section]
    shift=(index*3)%len(base)
    ordered=base[shift:]+base[:shift]
    if section=="plants" and plant:
        ordered=list(ordered)
        ordered[0]=(plant["observation"]["es"],plant["observation"]["en"])
        ordered[1]=(plant["characteristics"]["es"],plant["characteristics"]["en"])
        ordered[2]=(plant["wellness_relation"]["es"],plant["wellness_relation"]["en"])
        ordered[3]=(plant["precautions"]["es"],plant["precautions"]["en"])
    if lang is None:
        return list(ordered)
    lang=_valid_lang(lang)
    return [_b(es,en,lang) for es,en in ordered]

def _build_catalog():
    catalog=[]
    for section in ("movement","calm","coach"):
        for i,(title_es,title_en) in enumerate(_TITLES[section]):
            aid=f"{section}_{i+1:02d}"
            catalog.append({"id":aid,"section":section,"title":{"es":title_es,"en":title_en},"description":_DESCRIPTIONS[section],"steps":_steps_for(section,i),"plant_id":None,"index":i})
    for i,(pid,plant) in enumerate(PLANTS.items()):
        catalog.append({"id":f"plant_{pid}","section":"plants","title":{"es":plant["activity"]["es"],"en":plant["activity"]["en"]},"description":_DESCRIPTIONS["plants"],"steps":_steps_for("plants",i,plant=plant),"plant_id":pid,"index":i})
    return catalog

_CATALOG=_build_catalog()
_BY_ID={item["id"]:item for item in _CATALOG}

def _valid_lang(lang):
    return lang if lang in LANGUAGES else "es"

def _public_activity(item,lang="es",minutes=None):
    lang=_valid_lang(lang)
    localized_steps=[]
    for step in item.get("steps",[]):
        if isinstance(step,(tuple,list)) and len(step)>=2:
            localized_steps.append(_b(str(step[0]),str(step[1]),lang))
        elif isinstance(step,dict):
            localized_steps.append(str(step.get(lang) or step.get("es") or step.get("en") or ""))
        else:
            localized_steps.append(str(step))
    data={"id":item["id"],"section":item["section"],"title":_b(item["title"]["es"],item["title"]["en"],lang),"description":_b(item["description"]["es"],item["description"]["en"],lang),"steps":localized_steps,"plant_id":item.get("plant_id"),"step_count":len(localized_steps)}
    if minutes is not None:
        data["minutes"]=int(minutes)
    if item.get("plant_id") in PLANTS:
        p=PLANTS[item["plant_id"]]
        data["plant"]={"id":p["id"],"name":_b(p["name"]["es"],p["name"]["en"],lang),"scientific_name":p["scientific_name"],"characteristics":_b(p["characteristics"]["es"],p["characteristics"]["en"],lang),"wellness_relation":_b(p["wellness_relation"]["es"],p["wellness_relation"]["en"],lang),"observation":_b(p["observation"]["es"],p["observation"]["en"],lang),"precautions":_b(p["precautions"]["es"],p["precautions"]["en"],lang)}
    return data

def get_catalog(lang="es"):
    lang=_valid_lang(lang)
    counts={s:len([a for a in _CATALOG if a["section"]==s]) for s in SECTIONS}
    return {"app":APP_NAME,"version":VERSION,"language":lang,"sections":[{"id":s,"name":_b({"plants":"Plantas y naturaleza","movement":"Movimiento suave","calm":"Calma y atención","coach":"Coach y planificación"}[s],{"plants":"Plants and nature","movement":"Gentle movement","calm":"Calm and attention","coach":"Coaching and planning"}[s],lang),"count":counts[s]} for s in SECTIONS],"activities":[_public_activity(a,lang) for a in _CATALOG],"plant_count":len(PLANTS),"durations":list(MINUTES_ALLOWED)}

def get_activities(lang="es",section="all"):
    lang=_valid_lang(lang)
    section=section if section in (*SECTIONS,"all") else "all"
    return [_public_activity(a,lang) for a in _CATALOG if section=="all" or a["section"]==section]

def get_activity(activity_id,lang="es"):
    if not activity_id:return None
    item=_BY_ID.get(str(activity_id))
    if not item:return None
    return _public_activity(item,_valid_lang(lang))

def get_plant(plant_id,lang="es"):
    lang=_valid_lang(lang)
    p=PLANTS.get(str(plant_id))
    if not p:return None
    return {"id":p["id"],"name":_b(p["name"]["es"],p["name"]["en"],lang),"scientific_name":p["scientific_name"],"group":p["group"],"characteristics":_b(p["characteristics"]["es"],p["characteristics"]["en"],lang),"wellness_relation":_b(p["wellness_relation"]["es"],p["wellness_relation"]["en"],lang),"observation":_b(p["observation"]["es"],p["observation"]["en"],lang),"precautions":_b(p["precautions"]["es"],p["precautions"]["en"],lang),"activity":_b(p["activity"]["es"],p["activity"]["en"],lang),"disclaimer":_b("Información botánica general y actividad de observación; no es consejo médico ni recomendación para ingerir o aplicar plantas.","General botanical information and an observation activity; not medical advice or a recommendation to ingest or apply plants.",lang)}

def _section_for_kind(kind):
    kind=str(kind or "pause").lower()
    return {"pause":"calm","energy":"movement","calm":"calm","nature":"plants","plants":"plants","movement":"movement","coach":"coach","program":"all"}.get(kind,"calm")

def _duration(value):
    try:value=int(value)
    except (TypeError,ValueError):value=3
    return value if value in MINUTES_ALLOWED else min(MINUTES_ALLOWED,key=lambda x:abs(x-value))

def get_session(activity_id=None,minutes=3,lang="es",activity=None,kind=None):
    # Compatibilidad con la llamada antigua main.py:
    # get_session(lang, kind, minutes)
    if activity_id in LANGUAGES and isinstance(minutes,str) and str(lang).isdigit():
        old_lang=activity_id
        old_kind=minutes
        old_minutes=int(lang)
        lang=old_lang
        minutes=old_minutes
        activity_id=None
        kind=old_kind
    lang=_valid_lang(lang)
    minutes=_duration(minutes)
    if isinstance(activity,dict):
        activity_id=activity.get("id",activity_id)
    item=_BY_ID.get(str(activity_id)) if activity_id else None
    if item is None:
        section=_section_for_kind(kind or activity_id)
        pool=[x for x in _CATALOG if section=="all" or x["section"]==section]
        if not pool:pool=[x for x in _CATALOG if x["section"]=="calm"]
        item=_RNG.choice(pool)
    result=_public_activity(item,lang,minutes)
    result.update({"app":APP_NAME,"version":VERSION,"language":lang,"duration_seconds":minutes*60,"prompt_interval_seconds":PROMPT_INTERVAL_SECONDS,"session_id":create_session_id(item["id"],minutes),"instructions":result["steps"],"total_steps":len(result["steps"])})
    return result

def get_program_day(lang="es",day=1):
    lang=_valid_lang(lang)
    try:day=int(day)
    except (TypeError,ValueError):day=1
    day=max(1,min(7,day))
    sequence=("calm","plants","movement","coach","calm","plants","coach")
    section=sequence[day-1]
    pool=[x for x in _CATALOG if x["section"]==section]
    item=pool[(day*7-7)%len(pool)]
    titles_es=["Comenzar con calma","Observar la naturaleza","Moverse suavemente","Organizar un paso","Volver al presente","Descubrir detalles verdes","Elegir el siguiente paso"]
    titles_en=["Begin calmly","Observe nature","Move gently","Organize one step","Return to the present","Discover green details","Choose the next step"]
    descriptions_es=["Una pausa sencilla para empezar.","Observa detalles naturales con curiosidad.","Prueba movimientos suaves y cómodos.","Elige una prioridad pequeña y realista.","Dedica unos minutos a notar tu entorno.","Observa una planta sin prisa.","Termina la semana con una acción concreta."]
    descriptions_en=["A simple pause to begin.","Notice natural details with curiosity.","Try gentle, comfortable movements.","Choose one small, realistic priority.","Spend a few minutes noticing your surroundings.","Observe a plant without rushing.","Finish the week with one concrete action."]
    mins=(3,5,3,5,10,5,10)[day-1]
    return {"day":day,"title":_b(titles_es[day-1],titles_en[day-1],lang),"description":_b(descriptions_es[day-1],descriptions_en[day-1],lang),"minutes":mins,"activity":_public_activity(item,lang,mins),"section":section,"prompt_interval_seconds":PROMPT_INTERVAL_SECONDS}

def get_health():
    return {"status":"ok","app":APP_NAME,"version":VERSION,"activities":len(_CATALOG),"plants":len(PLANTS),"durations":list(MINUTES_ALLOWED),"languages":list(LANGUAGES)}

def get_config():
    return {"name":APP_NAME,"company":COMPANY,"version":VERSION,"languages":list(LANGUAGES),"durations":list(MINUTES_ALLOWED),"sections":list(SECTIONS),"activity_count":len(_CATALOG),"plant_count":len(PLANTS),"program_days":7,"prompt_interval_seconds":PROMPT_INTERVAL_SECONDS}

def create_session_id(activity_id="",minutes=3):
    raw=f"{activity_id}|{minutes}|{time.time_ns()}|{_RNG.random()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]

# Alias de compatibilidad para otros módulos.
catalog=get_catalog
activities=get_activities
session=get_session
plant=get_plant
program_day=get_program_day
health=get_health
config=get_config
