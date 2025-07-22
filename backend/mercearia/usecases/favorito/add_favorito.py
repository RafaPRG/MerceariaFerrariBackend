from mercearia.domain.repositories.favorito_repository import FavoritoRepository
from mercearia.domain.entities.favorito import Favorito


class AddFavorito:
    def __init__(self, favorito_repository: FavoritoRepository):
        self.favorito_repository = favorito_repository

    async def execute(self, user_id: str, produto_id: str) -> None:
        favorito = Favorito(user_id=user_id, produto_id=produto_id)
        await self.favorito_repository.add(favorito)
