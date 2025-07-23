import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from mercearia.domain.entities.produto import Produto
from mercearia.infra.database import Base
import uuid


class ProdutoModel(Base):
    __tablename__ = "produtos"

    id: Mapped[str] = mapped_column(
        sa.String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    nome: Mapped[str] = mapped_column(sa.String, nullable=False)
    descricao: Mapped[str] = mapped_column(sa.String, nullable=False)
    preco: Mapped[float] = mapped_column(sa.Float, nullable=False)
    imagem: Mapped[str] = mapped_column(sa.String, nullable=False)

    favoritado = relationship(
        "FavoritoModel", back_populates="produto", lazy="selectin"
    )

    @classmethod
    def from_entity(cls, entity: Produto) -> "ProdutoModel":
        return cls(
            id=entity.id,
            nome=entity.nome,
            descricao=entity.descricao,
            preco=entity.preco,
            imagem=entity.imagem,
        )

    def to_entity(self) -> Produto:
        return Produto(
            id=self.id,
            nome=self.nome,
            descricao=self.descricao,
            preco=self.preco,
            imagem=self.imagem,
        )
