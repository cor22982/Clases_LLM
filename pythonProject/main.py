#nos sirve para poder hacer chiang en los modelos
#chain es una parte de nuestro agente que hace una determinada accion
from langchain.chains.llm import LLMChain
#Ahora usaremos otro paquete para hacer templates, son las consultas para openia.
#Un template lo que hace es poder tomar ese propmt ponerlo en una estructura y mandarlo a openia
from langchain.prompts.prompt import PromptTemplate
from langchain_core.prompts import PipelinePromptTemplate

#ahora vamos a importar la libreria que nos va a ayudar para crear ese chat con open ia
from langchain_openai import ChatOpenAI
#luego tenemos que importar la libereria que nos va a servir para poder tomar las api key
from dotenv import load_dotenv
import os #manejo de las request, o tener funciones del sistema operativo.

#DESCRIPCION
#TOmarme cierta informaicon que yo le pongo a el codigo, y va a hacer que se le pida a
#CHATPGT y que haga un resumen de esa biografia y que le de datos interesantes de esa biografica

#Esta es la autobiografia
informacion = """
    Ángel David Revilla Lenoci nació el 16 de julio de 1982 en la ciudad de Caracas, Venezuela,3​4​ Su padre era piloto y su madre era una empresaria orientada a la gastronomía.5​6​ su ascendencia proviene de España6​Estados Unidos e Italia.7​ Estudió comunicación social en la Universidad Santa María, ubicada en Caracas6​ y trabajó como periodista para una revista médica.3​4​
    En 1998 creó el blog titulado El Diario de Dross6​ cuyo nombre de usuario "Dross", se origina, según él, en el luchador Darren Drozdov, exluchador de la WWE erróneamente conocido como «Warren Droz».4​8​9​ De donde tomó el nombre Dross mal escrito porque le falló la memoria.10​ Revilla comenzó en el año 2000 escribiendo críticas mordaces de juegos para sitios web como MeriStation o Vandal,11​ también hizo algunas publicaciones en el foro GameFAQs.12​
    A los 25 años decidió mudarse a la ciudad de Buenos Aires, Argentina, donde continuó su carrera como bloguero.3​4​ Un año antes, en 2006, Revilla había decidido crear un canal en YouTube con el nombre de DrossRotzank. Añadiendo Rotzank al nombre de Dross, que es el apellido de un criador del que su familia adquirió un perro cuando era un niño.10​
    
    En sus inicios en YouTube, Revilla realizó «reseñas» de videojuegos y gameplays. Estos vídeos se caracterizaban por su humor negro, que venían acompañados de videojuegos con temáticas de terror o incluso de serie B.
    Su primer vídeo importante de este estilo fue Dross juega I wanna be the guy, donde marca su característico estilo en los gameplays. Otro contenido habitual en su canal de YouTube, en esta primera etapa, eran las vídeo-reacciones, donde Dross se grababa viendo algún vídeo grotesco (sin mostrarlo en su vídeo), siendo este tipo de contenido una insignia de su canal.
    También se caracterizó por crear sketches con múltiples personajes, donde se mostraba a él (Dross) interactuando junto a El Troll, Fuyito Kokoyama, Estela Conchaseca, además de integrar personajes que, si bien no aparecían en sus videos, formaban parte de su canon, tales como La gorda (supuesta novia de Dross) y Morzat (descrito como un Dios intergaláctico el cual su comunidad adoptó como un meme). También destacó por sus videos Dross responde preguntas estúpidas, que no era sino una sección donde respondía de forma irónica y mordaz a diversas preguntas absurdas que le dejaban sus seguidores.
    Finalmente, un sello de su canal, fueron los Dross-O-Rama, que consistían en transmisiones en vivo mediante YouTube. Cabe mencionar que, si bien esto ya es muy normal actualmente, las transmisiones en vivo antes eran algo menos común, por lo que cuando un youtuber hacía una, era un momento especial para la comunidad. Dross en estos espacios interactuaba con su comunidad. Este formato sería recuperado más tarde en Los Vlogs de Dross, canal secundario Dross, y hasta 2022 volvería a llamarse Dross-O-Rama. Para octubre de 2013, debido a su interés en lo paranormal, Revilla decidió empezar a subir contenido de terror y relacionado con conspiraciones, siendo este el contenido que se quedaría en su canal desde entonces. Su audiencia bautizó este cambio como el octubre eterno, esto debido a que Dross solamente traía contenido paranormal a su canal durante octubre.
    En esta nueva etapa, su contenido insignia fueron los top 7, y fue tanto el éxito de sus tops que ayudó a popularizarlos en la comunidad hispana. Incluso, su estética y forma de narrar sería de gran influencia para toda una legión de youtubers enfocados al terror que surgieron en aquellos años.9​ En 2020, Revilla superó los veinte millones de suscriptores.13​ Revilla posee dos canales secundarios: Los Vlogs de Dross,6​14​ en el que sube material secundario y clips de sus streams, y Mi Querido Mussolini, canal en el que graba a su pez mascota llamado Mussolini.6​
"""

if __name__ == "__main__":
    load_dotenv()#vamos a cargar las variables de ambiente que tengamos.
    summary_template = f"""
    Given the information {informacion} about that pearson I want to create: 
        1. A little summary
        2. Two intersting facts about him.
    Give me that information in the same language of information
    """

    #crearemos nuestro objeto promt template. Esa nos iba a servir par el esquema del prompt

    summary_template_prompt = PromptTemplate(
        input_variables=[informacion],
        template=summary_template
    )

    #ahora vamos a crear nuestro objeto que es el chatgpt y vamos a agregar nuestro llm

    #la temperatura es una variable que indica que tan creativa es la respuesta.
    #Que tan creativa es la respuesta.
    #La temperatura va de 0 a 1.

    #Los steps lo que hacen es varias consultas a la inteligencia aritficial para iterar sobre una misa respuesta
    #Es otra forma de hacer few shoots prompting.

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    #creamos una chain y metemos el promt y el llm
    chain = summary_template_prompt | llm

    #ahora creamos nuestra consulta
    # le estoy diciento que informacion sea la variable de entrada. a GPT.
    res = chain.invoke(input={"informacion": informacion})
    print(res.content)
