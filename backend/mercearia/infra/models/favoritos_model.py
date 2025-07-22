import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from mercearia.domain.entities.favorito import Favorito
from mercearia.infra.database import Base
import uuid


class FavoritoModel(Base):
    __tablename__ = "favoritos"

    id: Mapped[str] = mapped_column(
        sa.String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(sa.String, sa.ForeignKey("users.id"), nullable=False)
    produto_id: Mapped[str] = mapped_column(sa.String,sa.ForeignKey("produtos.id"), nullable=False)

    produto = relationship("ProdutoModel", back_populates="favoritado")
    user = relationship("UserModel", back_populates="favoritos")

    @classmethod
    def from_entity(cls, entity: Favorito) -> "FavoritoModel":
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            produto_id=entity.produto_id,
            produto=entity.produto
        )

    def to_entity(self) -> Favorito:
        return Favorito(
            id=self.id,
            user_id=self.user_id,
            produto_id=self.produto_id,

            produto=self.produto
        )
