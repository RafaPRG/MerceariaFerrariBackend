from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from mercearia.domain.entities.produto import Produto
from mercearia.domain.repositories.produto_repository import ProdutoRepository
from mercearia.infra.models.produto_model import ProdutoModel


class SQLAlchemyProdutoRepository(ProdutoRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> List[Produto]:
        stmt = select(ProdutoModel)
        result = await self._session.execute(stmt)
        return [produto.to_entity() for produto in result.scalars().all()]
