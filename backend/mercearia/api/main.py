from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mercearia.api.routes import user_route, produto_route, favorito_route
from mercearia.api.openapi_tags import openapi_tags

app = FastAPI(
    title="Mercearia API",
    description="API backend do Mercearia com Clean Architecture, FastAPI e PostgreSQL",
    version="1.0.0",
    contact={
        "name": "Miguel Ferrari e Rafael Ponce",
        "email": "mercearia@exemplo.com",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    openapi_tags=openapi_tags,
)

# Origens confiáveis (frontend local e produção)
origins = [
    "http://localhost:5173",  # Vite dev
    "https://frontmercearia.vercel.app",  # Substitua com o domínio real
]

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rota de teste
@app.get("/")
def root():
    return {"mensagem": "Bem-vindo à API da Mercearia!"}


# Inclusão das rotas
app.include_router(user_route.router, prefix="/user", tags=["Usuários"])
app.include_router(produto_route.router, prefix="/produtos", tags=["Produtos"])
app.include_router(favorito_route.router, prefix="/favoritos", tags=["Favoritos"])
