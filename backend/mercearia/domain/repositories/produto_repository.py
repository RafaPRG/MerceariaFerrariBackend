from abc import ABC, abstractmethod
from mercearia.domain.entities.produto import Produto
from typing import List

class ProdutoRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Produto]: ...