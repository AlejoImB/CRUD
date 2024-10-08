from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

# Definir el modelo de datos para las tareas
class Tarea(BaseModel):
    id: int
    titulo: str

# Inicializar la aplicación de FastAPI
app = FastAPI()

# Configuración para usar plantillas Jinja2
templates = Jinja2Templates(directory="templates")

# Lista de tareas simulando una base de datos en memoria
tareas_db: List[Tarea] = []

# Endpoint de bienvenida (index) que renderiza un archivo HTML
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Obtener todas las tareas
@app.get("/tareas/", response_model=List[Tarea])
async def obtener_tareas():
    return tareas_db

# Crear una nueva tarea
@app.post("/tareas/", response_model=Tarea)
async def crear_tarea(tarea: Tarea):
    tareas_db.append(tarea)
    return tarea

# Obtener una tarea por ID
@app.get("/tareas/{tarea_id}", response_model=Tarea)
async def obtener_tarea(tarea_id: int):
    for tarea in tareas_db:
        if tarea.id == tarea_id:
            return tarea
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

# Actualizar una tarea
@app.put("/tareas/{tarea_id}", response_model=Tarea)
async def actualizar_tarea(tarea_id: int, tarea_actualizada: Tarea):
    for index, tarea in enumerate(tareas_db):
        if tarea.id == tarea_id:
            tareas_db[index] = tarea_actualizada
            return tarea_actualizada
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

# Eliminar una tarea
@app.delete("/tareas/{tarea_id}")
async def eliminar_tarea(tarea_id: int):
    for index, tarea in enumerate(tareas_db):
        if tarea.id == tarea_id:
            tareas_db.pop(index)
            return {"message": "Tarea eliminada"}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")
