Querying Perplexity AI using sonar-pro for: What are the best practices for setting up PostgreSQL with Docker Compose for FastAPI, specifically focusing on development and test database separation?
Here are some best practices for setting up PostgreSQL with Docker Compose for FastAPI, focusing on development and test database separation:

1. Use separate services for development and test databases[1][5]:

```yaml
services:
  db_dev:
    image: postgres:13
    environment:
      POSTGRES_DB: dev_db
      POSTGRES_USER: dev_user
      POSTGRES_PASSWORD: dev_password

  db_test:
    image: postgres:13  
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_password
```

2. Use environment variables for database connection settings[3]:

```python
class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI")
    def assemble_db_connection(cls, v: str | None, values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_SERVER"),
            path=values.data.get("POSTGRES_DB"),
        ).unicode_string()
```

3. Use Docker networks to isolate development and test environments[5]:

```yaml
networks:
  development:
  test:

services:
  db_dev:
    networks:
      - development
  
  db_test:
    networks:
      - test
```

4. Use volumes for persistent data storage[1]:

```yaml
volumes:
  postgres_data_dev:
  postgres_data_test:

services:
  db_dev:
    volumes:
      - postgres_data_dev:/var/lib/postgresql/data
  
  db_test:
    volumes:
      - postgres_data_test:/var/lib/postgresql/data
```

5. Use Docker Compose profiles to manage different environments[8]:

```yaml
services:
  db_dev:
    profiles: ["dev"]
  
  db_test:
    profiles: ["test"]
```

6. Use wait-for-it scripts to ensure database is ready before starting the application[5]:

```yaml
services:
  web:
    command: ["./wait-for-it.sh", "db:5432", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

7. Use separate configuration files for different environments[3]:

```python
from pydantic_settings import BaseSettings

class DevSettings(BaseSettings):
    DATABASE_URL: str = "postgresql://dev_user:dev_password@db_dev/dev_db"

class TestSettings(BaseSettings):
    DATABASE_URL: str = "postgresql://test_user:test_password@db_test/test_db"
```

8. Use pytest fixtures for database setup and teardown in tests[9]:

```python
@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
```