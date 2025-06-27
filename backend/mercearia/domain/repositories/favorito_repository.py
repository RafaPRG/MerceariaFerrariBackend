from abc import ABC, abstractmethod
from mercearia.domain.entities.favorito import Favorito
from typing import List

class FavoritoRepository(ABC):
    @abstractmethod
    def add(self, favorito: Favorito) -> None:
        """Adds a product to the user's favorites"""
        ...

    @abstractmethod
    def remove(self, favorito: Favorito) -> None:
        """Removes a product from the user's favorites"""
        ...

    @abstractmethod
    def list_by_user(self, user_id: str) -> List[Favorito]:
        """Returns all favorites for a given user"""
        ...

    @abstractmethod
    def exists(self, user_id: str, produto_id: str) -> bool:
        """Checks if a specific product is already favorited by the user"""
        ...
