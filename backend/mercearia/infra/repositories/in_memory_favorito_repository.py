from mercearia.domain.repositories.favorito_repository import FavoritoRepository
from mercearia.domain.entities.favorito import Favorito
from typing import List


class InMemoryFavoritoRepository(FavoritoRepository):
    def __init__(self):
        self._favoritos: List[Favorito] = []

    async def add(self, favorito: Favorito) -> None:
        if favorito not in self._favoritos:
            self._favoritos.append(favorito)

    async def remove(self, favorito: Favorito) -> None:
        if favorito in self._favoritos:
            self._favoritos.remove(favorito)

    async def list_by_user(self, user_id: str) -> List[Favorito]:
        return [f for f in self._favoritos if f.user_id == user_id]

    async def exists(self, user_id: str, produto_id: str) -> bool:
        return any(
            f.user_id == user_id and f.produto_id == produto_id for f in self._favoritos
        )
