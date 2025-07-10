from fastapi import APIRouter
from mercearia.api.schemas.produto_schema import ProdutoResponse
from mercearia.domain.entities.produto import Produto
from mercearia.infra.repositories.in_memory_produto_repository import InMemoryProdutoRepository
from mercearia.usecases.produto.get_all_produtos import GetAllProdutos

router = APIRouter()
repo = InMemoryProdutoRepository()

@router.get("/", response_model=list[ProdutoResponse], summary="Listar produtos")
def listar_produtos():
    usecase = GetAllProdutos(repo)
    produtos: list[Produto] = usecase.execute()
    return [
        ProdutoResponse(
            nome=p.nome,
            descricao=p.descricao,
            preco=p.preco,
            imagem=p.imagem
        ) for p in produtos
    ]
