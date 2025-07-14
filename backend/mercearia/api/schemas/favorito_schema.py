from pydantic import BaseModel, EmailStr, Field


class FavoritoRequest(BaseModel):
    email: EmailStr = Field(..., description="Email do usuário")
    produto: str = Field(..., description="Nome do produto favoritado")


class FavoritoResponse(BaseModel):
    email: EmailStr = Field(..., description="Email do usuário")
    produto: str = Field(..., description="Nome do produto favoritado")

    @classmethod
    def from_entity(cls, favorito):
        return cls(email=favorito.email, produto=favorito.produto)
