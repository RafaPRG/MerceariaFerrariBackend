from pydantic import BaseModel, Field


class ProdutoResponse(BaseModel):
    nome: str = Field(..., description="Nome do produto")
    descricao: str = Field(..., description="Descrição do produto")
    preco: float = Field(..., gt=0, description="Preço do produto")

    @classmethod
    def from_entity(cls, produto):
        return cls(nome=produto.nome, descricao=produto.descricao, preco=produto.preco)
