from fastapi import APIRouter, HTTPException, Depends
from mercearia.api.schemas.favorito_schema import FavoritoRequest, FavoritoResponse
from mercearia.domain.entities.favorito import Favorito
from mercearia.domain.entities.user import User
from mercearia.domain.entities.produto import Produto
from mercearia.domain.value_objects.email_vo import Email
from mercearia.domain.value_objects.password_vo import Password
from mercearia.infra.repositories.sqlalchemy.sqlalchemy_favorito_repository import SQLAlchemyFavoritoRepository
from mercearia.usecases.favorito.add_favorito import AddFavorito
from mercearia.usecases.favorito.get_user_favoritos import GetUserFavoritos
from mercearia.usecases.favorito.remove_favorito import RemoveFavorito
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from mercearia.api.deps import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
security = HTTPBearer()

@router.get("/", response_model=list[FavoritoResponse], summary="Listar favoritos")
async def listar_favoritos(
    email: str,
    session: AsyncSession = Depends(get_db_session),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        repo = SQLAlchemyFavoritoRepository(session)
        usecase = GetUserFavoritos(repo)
        user = User("temp", "Temp User", Email(email), Password("Fake1234"), "user")
        favoritos = await usecase.execute(user.id)
        return [
            FavoritoResponse(email=email, produto=f.produto_id)
            for f in favoritos
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", summary="Adicionar favorito")
async def adicionar_favorito(
    data: FavoritoRequest,
    session: AsyncSession = Depends(get_db_session),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        repo = SQLAlchemyFavoritoRepository(session)
        usecase = AddFavorito(repo)
        user = User("temp", "Temp User", Email(data.email), Password("Fake1234"), "user")
        produto = Produto(data.produto, "Produto X", "Descrição do produto", 10.0, "imagem.png")
        await usecase.execute(user.id, produto.id)
        return {"message": "Favorito adicionado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/", summary="Remover favorito")
async def remover_favorito(
    data: FavoritoRequest,
    session: AsyncSession = Depends(get_db_session),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        repo = SQLAlchemyFavoritoRepository(session)
        usecase = RemoveFavorito(repo)
        user = User("temp", "Temp User", Email(data.email), Password("Fake1234"), "user")
        produto = Produto(data.produto, "Produto X", "Descrição do produto", 10.0, "imagem.png")
        await usecase.execute(user.id, produto.id)
        return {"message": "Favorito removido com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
