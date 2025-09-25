# Backend de los Juegos de Química

## Descripción

Este es el backend de los juegos de química, un proyecto que tiene como objetivo ayudar a los estudiantes a aprender química de una manera divertida y entretenida. El backend está construido con Node.js y Express, y utiliza MongoDB como base de datos.

### Instalación

Para instalar las dependencias del proyecto, ejecute el siguiente comando:

```bash
pip install -r requirements.txt
```

### Ejecución en Desarrollo

Para ejecutar el servidor, utilice el siguiente comando:

```bash
fastapi dev app/main.py
```

## producción

Para ejecutar el servidor en producción, utilice el siguiente comando:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Módulos

- Lotería: Este módulo contiene la lógica del juego de lotería. Permite a los jugadores jugar al juego de lotería y verificar si han ganado o no.
- Tabla Periódica: Este módulo proporciona información sobre los elementos químicos y sus propiedades.
- Quiz: Este módulo permite a los jugadores responder preguntas de opción múltiple sobre química. Los jugadores pueden ganar puntos por cada respuesta correcta.
