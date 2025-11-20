import json
import os
from typing import List, Optional
from models import Libro

DB_FILE = "libros.json"

def cargar_libros() -> tuple[List[Libro], int]:
    if not os.path.exists(DB_FILE):
        return [], 1

    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            libros = [Libro(**libro) for libro in data.get('libros', [])]
            contador = data.get('contador_id', 1)
            return libros, contador
    except (json.JSONDecodeError, FileNotFoundError):
        return [], 1

def guardar_libros(libros: List[Libro], contador_id: int):
    data = {
        'libros': [libro.model_dump() for libro in libros],
        'contador_id': contador_id
    }
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def buscar_por_isbn(libros: List[Libro], isbn: str) -> Optional[Libro]:
    for libro in libros:
        if libro.ISBN == isbn:
            return libro
    return None

def buscar_por_titulo(libros: List[Libro], titulo: str) -> Optional[Libro]:
    titulo_lower = titulo.lower()
    for libro in libros:
        if libro.titulo.lower() == titulo_lower:
            return libro
    return None

def buscar_libros(libros: List[Libro], query: str) -> List[Libro]:
    query_lower = query.lower()
    resultados = []
    
    for libro in libros:
        if (str(libro.id) == query or
            query_lower in libro.titulo.lower() or
            query_lower in libro.autor.lower() or
            query_lower in libro.ISBN.lower()):
            resultados.append(libro)
    
    return resultados