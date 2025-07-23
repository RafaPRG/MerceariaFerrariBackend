from fastapi import APIRouter, HTTPException, Depends
from mercearia.api.schemas.favorito_schema import FavoritoRequest, FavoritoResponse
from mercearia.domain.entities.produto import Produto
from mercearia.infra.repositories.sqlalchemy.sqlalchemy_favorito_repository import (
    SQLAlchemyFavoritoRepository,
)
from mercearia.infra.repositories.sqlalchemy.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from mercearia.usecases.favorito.add_favorito import AddFavorito
from mercearia.usecases.favorito.get_user_favoritos import GetUserFavoritos
from mercearia.usecases.favorito.remove_favorito import RemoveFavorito
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from mercearia.api.deps import get_db_session, get_current_user, get_favorito_repository
from sqlalchemy.ext.asyncio import AsyncSession
from mercearia.domain.repositories.favorito_repository import FavoritoRepository
from mercearia.api.schemas.produto_schema import ProdutoResponse

router = APIRouter()
security = HTTPBearer()


@router.get("/", response_model=list[FavoritoResponse], summary="Listar favoritos")
async def listar_favoritos(
    session: AsyncSession = Depends(get_db_session),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user=Depends(get_current_user),
    repo: FavoritoRepository = Depends(get_favorito_repository),
):
    try:
        usecase = GetUserFavoritos(repo)

        favoritos = await usecase.execute(user.id)
        return [FavoritoResponse.from_entity(f) for f in favoritos]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", summary="Adicionar favorito")
async def adicionar_favorito(
    data: FavoritoRequest,
    session: AsyncSession = Depends(get_db_session),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user=Depends(get_current_user),
    repo: FavoritoRepository = Depends(get_favorito_repository),
):
    try:
        usecase = AddFavorito(repo)
        await usecase.execute(user.id, data.produto_id)
        return {"message": "Favorito adicionado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/", summary="Remover favorito")
async def remover_favorito(
    data: FavoritoRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user=Depends(get_current_user),
    repo: FavoritoRepository = Depends(get_favorito_repository),
):
    try:
        usecase = RemoveFavorito(repo)
        await usecase.execute(user.id, data.produto_id)
        return {"message": "Favorito removido com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
