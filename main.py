from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"

movies = [
    {
		"id": 1,
		"title": "En busca de la Felicidad",
		"overview": "La vida es una lucha para Chris Gardner. Expulsado de su apartamento, él y su joven hijo se encuentran solos sin ningún lugar a donde ir. A pesar de que Chris ocasionalmente consigue trabajo como interno en una prestigiada firma financiera, la posición no le da dinero. El dúo debe vivir en un albergue y enfrentar muchas dificultades, pero Chris no se da por vencido y lucha por conseguir una vida mejor para él y su hijo. Al final logra convertirse en un hombre multimillonario",
		"year": "2006",
		"rating": 7.8,
		"category": "Drama"
	}
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

@app.get('/movies', tags=['movies'])
def get_movies():
    return movies