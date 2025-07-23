from pydantic import BaseModel, Field
from mercearia.api.schemas.produto_schema import ProdutoResponse
from mercearia.domain.entities.favorito import Favorito


class FavoritoRequest(BaseModel):
    produto_id: str = Field(..., description="Nome do produto favoritado")


class FavoritoResponse(BaseModel):
    id: str = Field(..., description="id do usuario")
    produto: ProdutoResponse = Field(..., description="Nome do produto favoritado")

    @classmethod
    def from_entity(cls, favorito: Favorito):
        return cls(
            id=favorito.user_id, produto=ProdutoResponse.from_entity(favorito.produto)
        )
