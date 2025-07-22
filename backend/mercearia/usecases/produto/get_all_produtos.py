from mercearia.domain.repositories.produto_repository import ProdutoRepository
from mercearia.domain.entities.produto import Produto
from typing import List


class GetAllProdutos:
    def __init__(self, produto_repository: ProdutoRepository):
        self._produto_repository = produto_repository

    async def execute(self) -> List[Produto]:
        return await self._produto_repository.get_all()
