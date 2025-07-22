from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from mercearia.domain.entities.favorito import Favorito
from mercearia.domain.repositories.favorito_repository import FavoritoRepository
from mercearia.infra.models.favoritos_model import FavoritoModel


class SQLAlchemyFavoritoRepository(FavoritoRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, favorito: Favorito) -> None:

        if not await self.exists(favorito.user_id, favorito.produto_id):
            db_favorito = FavoritoModel.from_entity(favorito)
            print(f"{db_favorito.user_id} : {db_favorito.produto_id}")

            self._session.add(db_favorito)
            await self._session.commit()

    async def remove(self, favorito: Favorito) -> None:
        print(f"{favorito.user_id} : {favorito.produto_id}")
        stmt = delete(FavoritoModel).where(
            FavoritoModel.user_id == favorito.user_id,
            FavoritoModel.produto_id == favorito.produto_id
        )
        await self._session.execute(stmt)
        await self._session.commit()

    async def list_by_user(self, user_id: str) -> List[Favorito]:
        stmt = select(FavoritoModel).options(joinedload(FavoritoModel.produto)).where(FavoritoModel.user_id == user_id)
        result = await self._session.execute(stmt)
        return [f.to_entity() for f in result.scalars().all()]

    async def exists(self, user_id: str, produto_id: str) -> bool:
        print(f"{user_id} : {produto_id}")
        stmt = select(FavoritoModel).where(
            FavoritoModel.user_id == user_id,
            FavoritoModel.produto_id == produto_id
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None
