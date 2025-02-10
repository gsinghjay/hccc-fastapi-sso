"""
Test configuration and fixtures.
"""

from typing import AsyncGenerator, Generator
import asyncio

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
)

from app.main import app
from app.core.config import Settings, get_settings
from app.db.base import get_db


def get_settings_override() -> Settings:
    """Override settings for testing"""
    return Settings(
        DEBUG=True,
        POSTGRES_SERVER="postgres_test",
        POSTGRES_USER="postgres",
        POSTGRES_PASSWORD=SecretStr("change-in-production"),
        POSTGRES_DB="test_user_management",
        POSTGRES_PORT=5432,
        SECRET_KEY=SecretStr("x" * 32),
    )


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test case."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Create a test database engine."""
    settings = get_settings_override()
    engine = create_async_engine(
        str(settings.SQLALCHEMY_DATABASE_URI),
        echo=settings.DEBUG,
        pool_pre_ping=True,
    )
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def test_db(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """
    Fixture that creates a nested transaction, recreates it when the application
    code calls session.commit and rolls it back at the end.
    """
    connection = await test_engine.connect()
    trans = await connection.begin()

    # Create a new session with the connection
    test_session_maker = async_sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
    session = test_session_maker()

    # Override the get_db dependency
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        try:
            yield session
        finally:
            await session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield session

    await session.close()
    await trans.rollback()
    await connection.close()


@pytest.fixture
def client(test_db: AsyncSession) -> Generator[TestClient, None, None]:
    """
    Test client fixture that can be used across all tests.

    Returns:
        TestClient: A test client configured to make requests to the test app
    """
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_settings() -> Settings:
    """Fixture to provide test Settings instance."""
    return get_settings_override()
