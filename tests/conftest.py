from src import create_app
from pytest import fixture

@fixture
def app():
    app = create_app()
    return app