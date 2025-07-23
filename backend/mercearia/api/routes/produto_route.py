from fastapi import APIRouter, Depends
from mercearia.api.schemas.produto_schema import ProdutoResponse
from mercearia.domain.entities.produto import Produto
from mercearia.infra.repositories.sqlalchemy.sqlalchemy_produto_repository import (
    SQLAlchemyProdutoRepository,
)
from mercearia.usecases.produto.get_all_produtos import GetAllProdutos
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from mercearia.api.deps import get_db_session
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
security = HTTPBearer()


@router.get("/", response_model=list[ProdutoResponse], summary="Listar produtos")
async def listar_produtos(
    session: AsyncSession = Depends(get_db_session),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    repo = SQLAlchemyProdutoRepository(session)
    usecase = GetAllProdutos(repo)
    produtos = await usecase.execute()
    return [
        ProdutoResponse(
            id=p.id, nome=p.nome, descricao=p.descricao, preco=p.preco, imagem=p.imagem
        )
        for p in produtos
    ]
