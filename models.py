from pydantic import BaseModel, Field
from typing import Optional

class Libro(BaseModel):
    id: Optional[int] = None
    titulo: str = Field(..., min_length=1, max_length=200)
    autor: str = Field(..., min_length=1, max_length=100)
    año: int = Field(..., ge=1000, le=9999)
    ISBN: str = Field(..., min_length=10, max_length=17)

class LibroCreate(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200)
    autor: str = Field(..., min_length=1, max_length=100)
    año: int = Field(..., ge=1000, le=9999)
    ISBN: str = Field(..., min_length=10, max_length=17)

class LibroUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=200)
    autor: Optional[str] = Field(None, min_length=1, max_length=100)
    año: Optional[int] = Field(None, ge=1000, le=9999)
    ISBN: Optional[str] = Field(None, min_length=10, max_length=17)