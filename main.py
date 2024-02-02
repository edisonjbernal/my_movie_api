from fastapi import FastAPI, Body, Path, Query, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Any, Coroutine, Optional, List

from starlette.requests import Request
from jwt_manager import create_token,validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel

# Security

class JWTBeater(HTTPBearer):
    async def __call__(self, request: Request):
         auth: HTTPAuthorizationCredentials = await  super().__call__(request)
         data = validate_token(auth.credentials)
         if data['email'] != "admin@gmail.com":
             raise HTTPException(status_code=403, detail="Credenciales inválidas")
         return auth.credentials
    


# Model
    
app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)

class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int] = None
    #title: str = Field(default="Mi Película", min_length=1, max_length=100)
    #overview: str = Field(default="Mi descripción", min_length=1, max_length=100)
    title: str = Field( min_length=1, max_length=100)
    overview: str = Field( min_length=1, max_length=100)
    year: int = Field( ge=1900, le=2022)
    rating: float
    category: str

    class Config:
        schema_extra = {
            "example": {
                "title": "Mi Película",
                "overview": "Mi descripción",
                "year": 2022,
                "rating": 9.5,
                "category": "Drama"
            }
        }

# App


movies = [
    {
		"id": 1,
		"title": "En busca de la Felicidad",
		"overview": "La vida es una lucha para Chris Gardner. Expulsado de su apartamento, él y su joven hijo se encuentran solos sin ningún lugar a donde ir. A pesar de que Chris ocasionalmente consigue trabajo como interno en una prestigiada firma financiera, la posición no le da dinero. El dúo debe vivir en un albergue y enfrentar muchas dificultades, pero Chris no se da por vencido y lucha por conseguir una vida mejor para él y su hijo. Al final logra convertirse en un hombre multimillonario",
		"year": "2006",
		"rating": 9.2,
		"category": "Drama"
	},
    {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token : str = create_token(user.dict())
        return JSONResponse(content={"token": token})
    return JSONResponse(status_code=401, content={"message":"Credenciales incorrectas"})

# Parámetro Path

@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBeater())])
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies)

@app.get('/movies/{id}', tags=['movies'] , response_model=Movie , status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(status_code=404, content=[])

# Parámetro Query Se le agregar una barra al final, para diferenciarlo de get_movies
@app.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length=1, max_length=100)) -> List[Movie]:
    data = [ item for item in movies if item['category'] == category ]
    return JSONResponse(content=data)

# Parámetro Body)

@app.post('/movies', tags=['movies'] , response_model=dict , status_code=201)
def create_movie(movie : Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    movies.append(movie)
    return JSONResponse(status_code=201, content={"message":"Se ha creado la película"})

@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
	for item in movies:
		if item["id"] == id:
			item['title'] = movie.title
			item['overview'] = movie.overview
			item['year'] = movie.year
			item['rating'] = movie.rating
			item['category'] = movie.category
			return JSONResponse(status_code=200, content={"message":"Se ha modificado la película"})

@app.delete('/movies/{id}', tags=['movies'] , response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={"message":"Se ha eliminado"})