import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.main import app as real_app
from app.config.database import Base, get_db
from app.config.settings import TEST_DATABASE_URL
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
import asyncio

engine = create_async_engine(TEST_DATABASE_URL, echo=False,
    pool_size=20,
    max_overflow=40,)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

@pytest_asyncio.fixture(scope="module", autouse=True)
async def async_db_engine():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield conn
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def app():
  
    async def override_get_db():
      async with TestingSessionLocal() as session:
        yield session
        
    real_app.dependency_overrides[get_db] = override_get_db

    async with LifespanManager(real_app) as manager:
        yield manager.app

@pytest_asyncio.fixture
async def client(app):
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver/api/") as client:
        yield client

@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
