from fastapi import APIRouter, HTTPException, Depends
from mercearia.api.schemas.favorito_schema import FavoritoRequest, FavoritoResponse
from mercearia.domain.entities.produto import Produto
from mercearia.infra.repositories.sqlalchemy.sqlalchemy_favorito_repository import SQLAlchemyFavoritoRepository
from mercearia.infra.repositories.sqlalchemy.sqlalchemy_user_repository import SQLAlchemyUserRepository
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
        # Busca usuário no banco
        user_repo = SQLAlchemyUserRepository(session)
        user = await user_repo.login(email)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

        repo = SQLAlchemyFavoritoRepository(session)
        usecase = GetUserFavoritos(repo)

        favoritos = await usecase.execute(user.id)
        return [
            FavoritoResponse(email=email, produto=f.Produto)
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
        user_repo = SQLAlchemyUserRepository(session)
        user = await user_repo.login(data.email)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

        repo = SQLAlchemyFavoritoRepository(session)
        usecase = AddFavorito(repo)

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
        user_repo = SQLAlchemyUserRepository(session)
        user = await user_repo.login(data.email)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

        repo = SQLAlchemyFavoritoRepository(session)
        usecase = RemoveFavorito(repo)

        produto = Produto(data.produto, "Produto X", "Descrição do produto", 10.0, "imagem.png")
        await usecase.execute(user.id, produto.id)
        return {"message": "Favorito removido com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
