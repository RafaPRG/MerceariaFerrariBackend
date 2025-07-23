import uuid
from mercearia.domain.entities.produto import Produto


class Favorito:
    def __init__(
        self,
        user_id: str,
        produto_id: str,
        id: str | None = None,
        produto: Produto | None = None,
    ):
        self.id = id or str(uuid.uuid4())
        self.user_id = user_id
        self.produto_id = produto_id
        self.produto = produto

    def __eq__(self, other):
        return (
            isinstance(other, Favorito)
            and self.user_id == other.user_id
            and self.produto_id == other.produto_id
        )

    def __hash__(self):
        return hash((self.user_id, self.produto_id))
