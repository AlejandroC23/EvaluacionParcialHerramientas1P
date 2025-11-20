from fastapi import FastAPI, HTTPException, status, Query
from models import Libro, LibroCreate, LibroUpdate
from database import cargar_libros, guardar_libros, buscar_por_isbn, buscar_por_titulo, buscar_libros
from isbn_generator import generar_isbn13, generar_isbn10
from typing import List

app = FastAPI(title="API de Gestión de Libros")

libros_db, contador_id = cargar_libros()

@app.get("/")
def root():
    return {"mensaje": "API de Gestión de Libros"}

@app.get("/generar-isbn13")
def obtener_isbn13():
    return {"ISBN": generar_isbn13()}

@app.get("/generar-isbn10")
def obtener_isbn10():
    return {"ISBN": generar_isbn10()}

@app.post("/libros", response_model=Libro, status_code=status.HTTP_201_CREATED)
def crear_libro(libro: LibroCreate):
    global contador_id
    
    libro_existente_isbn = buscar_por_isbn(libros_db, libro.ISBN)
    if libro_existente_isbn:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un libro con el ISBN {libro.ISBN}"
        )
    
    libro_existente_titulo = buscar_por_titulo(libros_db, libro.titulo)
    if libro_existente_titulo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un libro con el título '{libro.titulo}'"
        )
    
    nuevo_libro = Libro(
        id=contador_id,
        titulo=libro.titulo,
        autor=libro.autor,
        año=libro.año,
        ISBN=libro.ISBN
    )
    libros_db.append(nuevo_libro)
    contador_id += 1
    guardar_libros(libros_db, contador_id)
    return nuevo_libro

@app.get("/libros", response_model=List[Libro])
def obtener_libros():
    return libros_db

@app.get("/libros/buscar", response_model=List[Libro])
def buscar(b: str = Query(..., description="Buscar por ID, título, autor, ISBN")):
    resultados = buscar_libros(libros_db, b)
    if not resultados:
        raise HTTPException(status_code=404, detail="No se encontraron libros")
    return resultados

@app.post("/libros/{libro_id}/actualizar", response_model=Libro)
def actualizar_libro(libro_id: int, libro_actualizado: LibroUpdate):
    global contador_id
    for i, libro in enumerate(libros_db):
        if libro.id == libro_id:
            datos_actualizados = libro_actualizado.model_dump(exclude_unset=True)
            
            if 'ISBN' in datos_actualizados:
                libro_existente = buscar_por_isbn(libros_db, datos_actualizados['ISBN'])
                if libro_existente and libro_existente.id != libro_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Ya existe un libro con el ISBN {datos_actualizados['ISBN']}"
                    )
            
            if 'titulo' in datos_actualizados:
                libro_existente = buscar_por_titulo(libros_db, datos_actualizados['titulo'])
                if libro_existente and libro_existente.id != libro_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Ya existe un libro con el título '{datos_actualizados['titulo']}'"
                    )
            
            libro_modificado = libro.model_copy(update=datos_actualizados)
            libros_db[i] = libro_modificado
            guardar_libros(libros_db, contador_id)
            return libro_modificado
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.post("/libros/{libro_id}/eliminar", status_code=status.HTTP_200_OK)
def eliminar_libro(libro_id: int):
    global contador_id
    for i, libro in enumerate(libros_db):
        if libro.id == libro_id:
            libros_db.pop(i)
            guardar_libros(libros_db, contador_id)
            return {"mensaje": "Libro eliminado exitosamente"}
    raise HTTPException(status_code=404, detail="Libro no encontrado")