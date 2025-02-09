Querying Perplexity AI using sonar-pro for: What are the latest FastAPI best practices for async testing with SQLAlchemy and database sessions in 2024? Include examples from FastAPI's official documentation.
Here are the latest FastAPI best practices for async testing with SQLAlchemy and database sessions in 2024:

1. Use SQLAlchemy 2.0+ with async support:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
async_session = AsyncSession(engine)
```

2. Create an async database dependency:

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db():
    async with AsyncSession(engine) as session:
        yield session

@app.get("/items")
async def get_items(db: AsyncSession = Depends(get_db)):
    # Use db for queries
```

3. Use pytest-asyncio for async tests:

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_items(async_client: AsyncClient):
    response = await async_client.get("/items")
    assert response.status_code == 200
```

4. Create an async test client fixture:

```python
import pytest
from httpx import AsyncClient
from main import app

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
```

5. Use async context managers for database operations in tests:

```python
async def test_create_item(async_client, async_session):
    async with async_session.begin():
        # Perform test database setup
    
    response = await async_client.post("/items", json={"name": "Test Item"})
    assert response.status_code == 201
```

6. Mock database calls in unit tests:

```python
from unittest.mock import AsyncMock

async def test_get_item(mocker):
    mock_db = AsyncMock()
    mock_db.execute.return_value.scalar_one_or_none.return_value = {"id": 1, "name": "Test"}
    
    result = await get_item(1, db=mock_db)
    assert result == {"id": 1, "name": "Test"}
```

These practices are based on FastAPI's documentation and recent community recommendations for async testing with SQLAlchemy in 2024[1][3][5].