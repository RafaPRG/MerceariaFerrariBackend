from mercearia.infra.repositories.in_memory_favorito_repository import InMemoryFavoritoRepository
from mercearia.usecases.favorito.add_favorito import AddFavorito
from mercearia.usecases.favorito.remove_favorito import RemoveFavorito
from mercearia.usecases.favorito.get_user_favoritos import GetUserFavoritos

def test_add_and_list_favorito_usecase():
    repo = InMemoryFavoritoRepository()
    add = AddFavorito(repo)
    get = GetUserFavoritos(repo)

    add.execute(user_id="1", produto_id="10")
    favoritos = get.execute(user_id="1")

    assert len(favoritos) == 1
    assert favoritos[0].produto_id == "10"

def test_add_duplicate_favorito_usecase():
    repo = InMemoryFavoritoRepository()
    add = AddFavorito(repo)
    get = GetUserFavoritos(repo)

    add.execute("1", "10")
    add.execute("1", "10")  # tentativa duplicada
    favoritos = get.execute("1")

    assert len(favoritos) == 1

def test_remove_favorito_usecase():
    repo = InMemoryFavoritoRepository()
    add = AddFavorito(repo)
    remove = RemoveFavorito(repo)
    get = GetUserFavoritos(repo)

    add.execute("1", "10")
    remove.execute("1", "10")
    favoritos = get.execute("1")

    assert len(favoritos) == 0
