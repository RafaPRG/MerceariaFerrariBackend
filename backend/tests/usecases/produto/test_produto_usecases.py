from mercearia.usecases.produto.get_all_produtos import GetAllProdutos
from mercearia.infra.repositories.in_memory_produto_repository import (
    InMemoryProdutoRepository,
)


def test_get_all_produtos_returns_produtos():
    repo = InMemoryProdutoRepository()
    usecase = GetAllProdutos(produto_repository=repo)

    produtos = usecase.execute()

    assert len(produtos) > 0
    assert all(p.id and p.nome for p in produtos)
