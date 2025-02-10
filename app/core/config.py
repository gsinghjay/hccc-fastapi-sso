from functools import lru_cache
from pydantic import (
    PostgresDsn,
    SecretStr,
    Field,
    field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings management using pydantic v2.

    Environment variables take precedence over values defined in .env file.
    All sensitive values are handled as SecretStr for security.

    Attributes:
        PROJECT_NAME (str): Name of the project
        API_PREFIX (str): Global API prefix (e.g., /api)
        API_V1_STR (str): API version 1 path component (e.g., v1)
        SECRET_KEY (SecretStr): Secret key for JWT token generation
        ACCESS_TOKEN_EXPIRE_MINUTES (int): JWT token expiration time in minutes
        BACKEND_CORS_ORIGINS (list[str]): List of allowed CORS origins
        POSTGRES_SERVER (str): PostgreSQL server hostname
        POSTGRES_USER (str): PostgreSQL username
        POSTGRES_PASSWORD (SecretStr): PostgreSQL password
        POSTGRES_DB (str): PostgreSQL database name
        SQLALCHEMY_DATABASE_URI (PostgresDsn): Constructed database URI
        DEBUG (bool): Enable debug mode (should be False in production)
    """

    # Application
    PROJECT_NAME: str = Field(
        default="FastAPI User Management", description="Name of the project"
    )
    API_PREFIX: str = Field(default="/api", description="Global API prefix")
    API_V1_STR: str = Field(default="v1", description="API version 1 path component")
    DEBUG: bool = Field(
        default=False, description="Enable debug mode (should be False in production)"
    )

    # Security
    SECRET_KEY: SecretStr = Field(
        default_factory=lambda: SecretStr(
            "your-super-secret-key-here-at-least-32-chars"
        ),
        description="Secret key for JWT token generation (min 32 characters)",
        examples=["your-super-secret-key-here-at-least-32-chars"],
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=11520,  # 8 days (60 * 24 * 8)
        ge=1,
        description="JWT token expiration time in minutes (default: 8 days)",
    )

    # CORS
    BACKEND_CORS_ORIGINS: str | list[str] = Field(
        default=["http://localhost:8000", "http://localhost:3000"],
        description="List of origins that can access the API. Can be a comma-separated string or a list.",
        examples=[
            ["http://localhost:8000", "http://localhost:3000"],
            "http://localhost:8000,http://localhost:3000",
        ],
    )

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(
        default=60, ge=1, description="Number of requests allowed per minute per client"
    )

    # PostgreSQL
    POSTGRES_SERVER: str = Field(
        default="localhost",
        description="PostgreSQL server hostname",
        examples=["localhost"],
    )
    POSTGRES_USER: str = Field(
        default="postgres", description="PostgreSQL username", examples=["postgres"]
    )
    POSTGRES_PASSWORD: SecretStr = Field(
        default_factory=lambda: SecretStr("your-secure-password"),
        description="PostgreSQL password",
        examples=["your-secure-password"],
    )
    POSTGRES_DB: str = Field(
        default="user_management",
        description="PostgreSQL database name",
        examples=["user_management"],
    )
    POSTGRES_PORT: int = Field(default=5432, description="PostgreSQL port")

    @property
    def API_V1_PATH(self) -> str:
        """
        Constructs the full API v1 path prefix.

        Returns:
            str: The complete path prefix for API v1 endpoints (e.g., /api/v1)
        """
        return f"{self.API_PREFIX}/{self.API_V1_STR}"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        """
        Constructs the PostgreSQL database URI from individual components.

        Returns:
            PostgresDsn: The constructed database URI
        """
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=f"/{self.POSTGRES_DB}",
        )

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        """
        Validates and processes CORS origins configuration.

        Args:
            v: String or list of strings representing allowed origins

        Returns:
            list[str]: List of processed CORS origins

        Raises:
            ValueError: If the origin URL is invalid
        """
        if isinstance(v, str):
            if not v.startswith("["):
                return [i.strip() for i in v.split(",")]
            raise ValueError("String input should be comma-separated URLs")
        elif isinstance(v, (list, tuple)):
            # Ensure all items are strings
            if not all(isinstance(x, str) for x in v):
                raise ValueError("All CORS origins must be strings")
            return list(v)
        raise ValueError(
            "BACKEND_CORS_ORIGINS should be a comma separated string or a list of strings"
        )

    @field_validator("SECRET_KEY", mode="before")
    @classmethod
    def validate_secret_key(cls, v: str | SecretStr) -> str | SecretStr:
        """
        Validates that the secret key meets minimum security requirements.

        Args:
            v: Secret key string or SecretStr

        Returns:
            str | SecretStr: Validated secret key

        Raises:
            ValueError: If the secret key is too short
        """
        if isinstance(v, SecretStr):
            if len(v.get_secret_value()) < 32:
                raise ValueError("SECRET_KEY must be at least 32 characters long")
            return v
        elif isinstance(v, str):
            if len(v) < 32:
                raise ValueError("SECRET_KEY must be at least 32 characters long")
            return v
        raise ValueError("SECRET_KEY must be a string or SecretStr")

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        json_schema_extra={
            "examples": [
                {
                    "PROJECT_NAME": "FastAPI User Management",
                    "API_PREFIX": "/api",
                    "API_V1_STR": "v1",
                    "DEBUG": False,
                    "SECRET_KEY": "your-super-secret-key-here-at-least-32-chars",
                    "ACCESS_TOKEN_EXPIRE_MINUTES": 11520,
                    "BACKEND_CORS_ORIGINS": [
                        "http://localhost:8000",
                        "http://localhost:3000",
                    ],
                    "RATE_LIMIT_PER_MINUTE": 60,
                    "POSTGRES_SERVER": "localhost",
                    "POSTGRES_USER": "postgres",
                    "POSTGRES_PASSWORD": "your-secure-password",
                    "POSTGRES_DB": "user_management",
                    "POSTGRES_PORT": 5432,
                }
            ]
        },
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Creates and returns a cached Settings instance.

    The settings are cached to avoid reading the environment variables
    on every request. The cache is invalidated when the environment
    variables change.

    Returns:
        Settings: Application settings loaded from environment variables
    """
    return Settings()
