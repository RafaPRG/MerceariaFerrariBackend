from mercearia.domain.repositories.favorito_repository import FavoritoRepository
from mercearia.domain.entities.favorito import Favorito
from typing import List

class GetUserFavoritos:
    def __init__(self, favorito_repository: FavoritoRepository):
        self.favorito_repository = favorito_repository

    def execute(self, user_id: str) -> List[Favorito]:
        return self.favorito_repository.list_by_user(user_id)
