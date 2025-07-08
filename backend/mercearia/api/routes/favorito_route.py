from fastapi import APIRouter, HTTPException
from mercearia.api.schemas.favorito_schema import FavoritoRequest, FavoritoResponse
from mercearia.domain.entities.favorito import Favorito
from mercearia.domain.entities.user import User
from mercearia.domain.entities.produto import Produto
from mercearia.infra.repositories.in_memory_favorito_repository import InMemoryFavoritoRepository
from mercearia.usecases.favorito.add_favorito import AddFavorito
from mercearia.usecases.favorito.get_user_favoritos import GetUserFavoritos
from mercearia.usecases.favorito.remove_favorito import RemoveFavorito

router = APIRouter()
repo = InMemoryFavoritoRepository()

@router.get("/", response_model=list[FavoritoResponse], summary="Listar favoritos")
def listar_favoritos(email: str):
    try:
        usecase = GetUserFavoritos(repo)
        user = User("temporário", email, "senha", "user")
        favoritos = usecase.execute(user)
        return [FavoritoResponse(email=f.email, produto=f.produto) for f in favoritos]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/", summary="Adicionar favorito")
def adicionar_favorito(data: FavoritoRequest):
    try:
        usecase = AddFavorito(repo)
        user = User("temporário", data.email, "senha", "user")
        produto = Produto(data.produto, "desc", 0.0)
        usecase.execute(user, produto)
        return {"message": "Favorito adicionado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/", summary="Remover favorito")
def remover_favorito(data: FavoritoRequest):
    try:
        usecase = RemoveFavorito(repo)
        user = User("temporário", data.email, "senha", "user")
        produto = Produto(data.produto, "desc", 0.0)
        usecase.execute(user, produto)
        return {"message": "Favorito removido com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
