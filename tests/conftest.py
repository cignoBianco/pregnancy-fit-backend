import pytest
from sqlmodel import SQLModel, Session, create_engine
from app.models.user import User
from app.core.database import get_session


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="session")
def create_db(engine):
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture()
def session(engine, create_db):
    with Session(engine) as session:
        yield session
