from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mercearia.api.routes import user_route, produto_route, favorito_route
from mercearia.api.openapi_tags import openapi_tags
from mercearia.api.security import get_password_hash

from contextlib import asynccontextmanager
from datetime import datetime
import uuid
import sqlalchemy as sa
from mercearia.infra.database import engine, async_session, Base
from mercearia.infra.models.produto_model import ProdutoModel
from mercearia.infra.models.user_model import UserModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Criar tabelas no startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tabelas do banco criadas/verificadas.")

    # Popular dados
    async with async_session() as db:
        try:
            # Verificar e popular produtos
            total_produtos = await db.execute(
                sa.select(sa.func.count()).select_from(ProdutoModel)
            )
            qtd_produtos = total_produtos.scalar_one()

            if qtd_produtos == 0:
                print("Populando produtos iniciais...")
                produtos_mock = [
                    { "nome": "Arroz Coripil Tipo 1 5kg", "preco": 26.30, "imagem": "arroz.png", "descricao": "Pacote de arroz de 5kg" },
                    { "nome": "Feijão Camil 1kg", "preco": 7.00, "imagem": "feijao.png", "descricao": "Feijão carioca tipo 1" },
                    { "nome": "Milho Verde em Lata OLÉ", "preco": 4.69, "imagem": "milho.png", "descricao": "Milho verde em conserva" },
                    { "nome": "Leite Condensado Italac 395g", "preco": 7.71, "imagem": "leite.png", "descricao": "Leite condensado cremoso" },
                    { "nome": "Requeijão Vigor 200g", "preco": 6.99, "imagem": "requeijao.png", "descricao": "Requeijão cremoso tradicional" },
                    { "nome": "Latão Brahma Chopp 473ml", "preco": 5.99, "imagem": "brahma.png", "descricao": "Latão de cerveja Brahma" },
                    { "nome": "Long Neck Heineken 330ml", "preco": 7.00, "imagem": "heineken.png", "descricao": "Cerveja Heineken Long Neck" },
                ]

                for p in produtos_mock:
                    await db.execute(
                        sa.insert(ProdutoModel).values(
                            id=str(uuid.uuid4()),
                            nome=p["nome"],
                            preco=p["preco"],
                            imagem=p["imagem"],
                            descricao=p["descricao"]
                        )
                    )
                print("Produtos inseridos com sucesso.")

            # Verificar e popular usuários
            total_users = await db.execute(
                sa.select(sa.func.count()).select_from(UserModel)
            )
            qtd_users = total_users.scalar_one()

            if qtd_users == 0:
                print("Populando usuários iniciais...")
                users_mock = [
                    {
                        "name": "Miguel Ferrari",
                        "email": "admin@merceariaferrari.com",
                        "password": "Admin@123",
                        "role": "admin"
                    },
                    {
                        "name": "Jucelino Freitas",
                        "email": "jucelinofreitas@gmail.com",
                        "password": "Juce@123",
                        "role": "user"
                    },
                ]

                for u in users_mock:
                    hashed_password = get_password_hash(u["password"])
                    await db.execute(
                        sa.insert(UserModel).values(
                            id=str(uuid.uuid4()),
                            name=u["name"],
                            email=u["email"],
                            password=hashed_password,
                            role=u["role"]
                        )
                    )
                print("Usuários inseridos com sucesso.")

            await db.commit()

        except Exception as e:
            print(f"Erro ao popular dados iniciais: {e}")
            await db.rollback()

    yield  # Permite que a aplicação FastAPI inicie normalmente

    # Finalização: dispose do engine
    await engine.dispose()
    print("Engine do banco desconectado no shutdown.")

# Inicialização da aplicação FastAPI
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
    lifespan=lifespan
)

# Origens confiáveis (frontend local e produção)
origins = [
    "http://localhost:5173",  # Vite dev
    "https://frontmercearia.vercel.app",  # Produção
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

# Rotas principais
app.include_router(user_route.router, prefix="/user", tags=["Usuários"])
app.include_router(produto_route.router, prefix="/produtos", tags=["Produtos"])
app.include_router(favorito_route.router, prefix="/favoritos", tags=["Favoritos"])
