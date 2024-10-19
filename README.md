# ASISTENTE DE DOCUMENTACION
## Video Funcionamiento
[Link al video]()
## Que hace este proyecto?
Lo que hace es primero almacenar toda la data del documento en una base vectorial en Pinecone.
Despues se le hace una consulta al LLM y en base a los chumks relacionados con la informacion que se obtuvo , los consume y da una respuesta con tu historial y solo lo que se encuentre en la base vectorial. Esto en base a All Tomorrows, una novela de evolucion especulativa

## Funcionamiento


## Ejecucion
Dirigete a la carpeta del proyecto
```
cd ASISTENTE_DOCUMENTACION
``` 

Activa el entorno con
```
.\proyecto1\Scripts\activate
``` 

instalar las librerias con
```
pip install -r requirements.txt
``` 
Ahora ejecuta el main usando streamlit
```
streamlit run main.py
``` 

## Preguntas que puedes hacer? 
Acontinuacion se detallan una serie de preguntas que le puedes hacer al LLM 
ojo en orden
```
Que es all tomorrows?
``
```
Que especies humanos,posthumanos y alienigenas hay en all tomorrows
``
```
Dime la historia de all tomorrows
``
```
Que le hicieron los Qu a la humanidad?
``
```
Que hizo la humanidad despues de los Qu?
``