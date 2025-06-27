from mercearia.domain.repositories.produto_repository import ProdutoRepository
from mercearia.domain.entities.produto import Produto
from typing import List

class InMemoryProdutoRepository(ProdutoRepository):
    def __init__(self):
        self._produtos: List[Produto] = [
            Produto(id="1", nome="Arroz", descricao="Arroz branco tipo 1", preco=5.99, imagem="arroz.jpg"),
            Produto(id="2", nome="Feijão", descricao="Feijão carioca", preco=6.49, imagem="feijao.jpg"),
            Produto(id="3", nome="Macarrão", descricao="Macarrão espaguete", preco=4.99, imagem="macarrao.jpg"),
            Produto(id="4", nome="Café", descricao="Café torrado e moído", preco=10.99, imagem="cafe.jpg"),
        ]

    def get_all(self) -> List[Produto]:
        return self._produtos
