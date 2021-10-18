# Polenes Bot

Bot de telegram que responde con el nivel de polen en Santiago, obtenido de
[polenes.cl](http://polenes.cl).

## Cómo usar

Enviar un mensaje con el tipo de polen por el que se quiere consultar –total,
árboles, platano oriental o pastos– a @PolenesBot. O alternativamente, correr
una versión propia como se detalla en la sección siguiente.

## Cómo correr

1. Clonar el repositorio
2. Crear un ambiente virtual con `python -m venv .venv` y activarlo con
   `source .venv/bin/activate` (aunque puede variar dependiando de la
   plataforma)
3. Instalar las dependencias con `python -m pip install -r requirements.txt`
4. Generar una credencial con @BotFather y guardarla en `credenciales.txt`
5. Ejecutar con `python polenesbot.py`
