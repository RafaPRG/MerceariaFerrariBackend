from mercearia.domain.repositories.favorito_repository import FavoritoRepository
from mercearia.domain.entities.favorito import Favorito


class RemoveFavorito:
    def __init__(self, favorito_repository: FavoritoRepository):
        self.favorito_repository = favorito_repository

    async def execute(self, user_id: str, produto_id: str) -> None:
        favorito = Favorito(user_id=user_id, produto_id=produto_id)

        if await self.favorito_repository.exists(user_id, produto_id):
          return await self.favorito_repository.remove(favorito)
        
        raise ValueError("Favorito não existente")
