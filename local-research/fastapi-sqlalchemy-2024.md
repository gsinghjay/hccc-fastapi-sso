Querying Perplexity AI using sonar-pro for: What are the latest FastAPI best practices for SQLAlchemy integration and database session management in 2024? Focus on async SQLAlchemy and production readiness.
Based on the latest best practices for FastAPI and SQLAlchemy integration in 2024, here are the key recommendations:

1. Use async SQLAlchemy for improved performance:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
```

2. Implement dependency injection for database sessions:

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db():
    async with AsyncSession(engine) as session:
        yield session

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    return user
```

3. Use connection pooling to optimize database connections:

```python
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=0
)
```

4. Implement proper error handling for database operations:

```python
from sqlalchemy.exc import SQLAlchemyError

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        user = await db.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")
```

5. Use async context managers for transaction management:

```python
async def create_user(db: AsyncSession, user: UserCreate):
    async with db.begin():
        db_user = User(**user.dict())
        db.add(db_user)
        await db.flush()
        return db_user
```

6. Implement database migrations using Alembic:

```
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

7. Use SQLAlchemy 2.0-style queries for better type checking and performance:

```python
from sqlalchemy import select

async def get_users(db: AsyncSession):
    stmt = select(User)
    result = await db.execute(stmt)
    return result.scalars().all()
```

8. Implement proper indexing for frequently queried columns:

```python
from sqlalchemy import Index

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    
    __table_args__ = (Index("ix_users_email", "email"),)
```

These practices focus on async SQLAlchemy usage and production readiness, emphasizing performance, error handling, and maintainability[1][2][4][5][7].