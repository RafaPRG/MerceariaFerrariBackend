from fastapi import APIRouter, HTTPException
from mercearia.api.schemas.favorito_schema import FavoritoRequest, FavoritoResponse
from mercearia.domain.entities.favorito import Favorito
from mercearia.domain.entities.user import User
from mercearia.domain.entities.produto import Produto
from mercearia.domain.value_objects.email_vo import Email
from mercearia.domain.value_objects.password_vo import Password
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
        user = User("temp", "Temp User", Email(email), Password("Fake1234"), "user")
        favoritos = usecase.execute(user.id)
        return [
            FavoritoResponse(email=email, produto=f.produto_id)
            for f in favoritos
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", summary="Adicionar favorito")
def adicionar_favorito(data: FavoritoRequest):
    try:
        usecase = AddFavorito(repo)
        user = User("temp", "Temp User", Email(data.email), Password("Fake1234"), "user")
        produto = Produto(data.produto, "Produto X", "Descrição do produto", 10.0, "imagem.png")
        usecase.execute(user.id, produto.id)
        return {"message": "Favorito adicionado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/", summary="Remover favorito")
def remover_favorito(data: FavoritoRequest):
    try:
        usecase = RemoveFavorito(repo)
        user = User("temp", "Temp User", Email(data.email), Password("Fake1234"), "user")
        produto = Produto(data.produto, "Produto X", "Descrição do produto", 10.0, "imagem.png")
        usecase.execute(user.id, produto.id)
        return {"message": "Favorito removido com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
