import re
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from mercearia.domain.entities.user import User
from mercearia.domain.value_objects.email_vo import Email
from mercearia.domain.value_objects.password_vo import Password
from mercearia.infra.database import Base
import uuid


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        sa.String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    email: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    role: Mapped[str] = mapped_column(sa.String, default="user")

    favoritos = relationship("FavoritoModel", lazy="selectin", back_populates="user")

    @classmethod
    def from_entity(cls, entity: User) -> "UserModel":
        return cls(
            id=entity.id,
            name=entity.name,
            email=str(entity.email),
            password=str(entity.password),
            role=entity.role,
        )

    def to_entity(self) -> User:
        return User(
            id=self.id,
            name=self.name,
            email=Email(self.email),
            password=Password(self.password),
            role=self.role,
        )
