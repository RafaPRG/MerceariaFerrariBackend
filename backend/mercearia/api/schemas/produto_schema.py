from pydantic import BaseModel, Field


class ProdutoResponse(BaseModel):
    id: str = Field(..., description="ID do produto")
    nome: str = Field(..., description="Nome do produto")
    descricao: str = Field(..., description="Descrição do produto")
    preco: float = Field(..., gt=0, description="Preço do produto")
    imagem: str = Field(..., description="URL da foto do produto")

    @classmethod
    def from_entity(cls, produto):
        return cls(id=produto.id, nome=produto.nome, descricao=produto.descricao, preco=produto.preco, imagem=produto.imagem)
