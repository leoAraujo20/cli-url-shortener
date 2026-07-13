import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.api.core.database import get_session
from src.api.server.server import app


@pytest.fixture(scope="session", name="engine")
def engine_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    yield engine
    engine.dispose()


@pytest.fixture(scope="function", name="session")
def session_fixture(engine):
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function", name="client")
def get_session_override(session):
    def _get_session_override():
        yield session

    app.dependency_overrides[get_session] = _get_session_override
    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()
