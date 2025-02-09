# CHANGELOG


## v1.0.0 (2025-02-09)

### Bug Fixes

- Resolve Ruff linting issues
  ([`de6a83b`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/de6a83b255f5bf6d1f0945319108f4ee69f63ebd))

### Build System

- **deps**: Update dependencies and add Gunicorn
  ([`cdf9ccb`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/cdf9ccb7afc49cf86cceb7e6129338f5c13582b8))

### Chores

- Add cursor-tools generated directories to gitignore
  ([`b9056f1`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/b9056f11a2637032a10a251551c41ea04d857116))

- Add local-docs/ for generated documentation - Add local-research/ for research notes

- Fixed typo with adding repomix file to .gitignore
  ([`46e615d`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/46e615d34159b7e7a09333f4a638e013e8e3fd00))

- Reanaylzed project with Giga
  ([`201a75d`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/201a75d6cbc67274da860407c303a70d5633dd7f))

- Update gitignore for Python, Docker, and development files
  ([`93e5188`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/93e518823b802d877650cecd3786a1bb20bb816b))

- **config**: Update project configuration
  ([`6353766`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/6353766f6a36c33b3aa49e247da59ab6102bd814))

- Add pydantic mypy plugin configuration - Update dependencies in poetry.lock - Add configuration
  testing rules - Update FastAPI core rules

- **deps**: Add Playwright dependencies
  ([`292c625`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/292c625f624b74b23a56729ad14c1ee33ac934fc))

- Add Playwright for browser automation - Add pytest-playwright for test integration - Configure
  test dependencies

- **dev**: Add development guidelines and rules
  ([`3399af8`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/3399af89457128a7b953a847abc4d77c7a8a51da))

- **env**: Remove inline comments from environment variables
  ([`c091459`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/c091459d832d09e58f41ddf6dcd734a42f90d4eb))

- **tools**: Implement cursor-tools global installation
  ([`5e17de5`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/5e17de535e2174839f0d1c53f30795f98c87e616))

- Update FastAPI core rules for production-first approach - Update global development standards -
  Update init files conventions - Add local research documentation - Ignore repomix output file

- **traefik**: Add certificates directory for SSL
  ([`0a10ee9`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/0a10ee9c12e4729c74fbbaece71562bddd379656))

### Documentation

- Add environment configuration examples and update README
  ([`dc69b02`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/dc69b0262c42a1932f057646be7097538fd07538))

- Add .env.example with all configuration variables - Document configuration variables with
  descriptions - Update README with completed core configuration features - Add checkmarks for
  completed TDD steps - Add implementation details and test coverage stats

- Update documentation with deployment instructions
  ([`49b34bc`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/49b34bc4ae691c82a43c44128ccd1fc71bc39a74))

- **rules**: Update configuration rules to reflect production-first approach
  ([`1a210eb`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/1a210ebae0f87719e85ad4edad14cbb3724de2fd))

- Remove environment-specific configuration references - Add DEBUG flag guidelines - Update testing
  requirements for simplified config - Emphasize production-safe defaults

- **rules**: Update project rules for e2e testing
  ([`daafc26`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/daafc268465853155d8b82a91b33b44a39c3f9e2))

- Add e2e testing standards and best practices - Define page object model requirements - Document
  test organization structure - Update API layer test coverage requirements

- **testing**: Update testing standards to follow FastAPI best practices
  ([`90555b9`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/90555b911299527343341f7fb5b374521e90b9fb))

### Features

- Added python semantic versioning
  ([`21fb526`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/21fb526616d8290d66f07c3483c10fec9a0e782f))

- **app**: Configure FastAPI application with settings
  ([`58e0879`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/58e087919f13889725e02d52c55fdf6d5bc293b2))

- Use settings for application title and debug mode - Configure OpenAPI docs URL with API prefix -
  Enable debug reload based on settings

- **core**: Implement settings management with pydantic
  ([`1ee0922`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/1ee0922463552d203ab6f6e3285ec0b456202270))

- Add Settings class with environment variable support - Implement secure handling of sensitive data
  using SecretStr - Add validation for SECRET_KEY and CORS origins - Add computed properties for API
  paths and database URI - Cache settings with lru_cache for performance

- **db**: Add async database session management
  ([`7c9f0d6`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/7c9f0d6d96a490295ff05932425a1c59487b3d7b))

- Configure async SQLAlchemy engine with settings - Add async session factory - Implement database
  dependency with proper cleanup - Add type hints and documentation

- **db**: Initialize alembic for database migrations
  ([`efcd23f`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/efcd23fe04724586b827daca65e47d0aae28fe1f))

- Add alembic initialization with async SQLAlchemy support - Configure env.py to use project's Base
  metadata and settings - Set up both online and offline migration modes - Enable async migration
  support with SQLAlchemy

- **docker**: Add development and production docker-compose configurations
  ([`25878b0`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/25878b064132329ce55d859d04cb8e4e16a72627))

- **docker**: Add multi-stage Dockerfile with Poetry and Gunicorn setup
  ([`622aa8e`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/622aa8e358c14b4aaaf7d9f9bf464e3647494d83))

- **middleware**: Configure CORS using settings
  ([`a9db343`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/a9db34381e2e4f7ba3410e25e872eac36a5e5319))

- Replace hardcoded CORS origins with settings - Add placeholder for rate limiting middleware -
  Improve middleware documentation

- **scripts**: Add e2e test runner using FastAPI CLI
  ([`b3958d1`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/b3958d16944b019681368f54c2a771292fcfec8f))

- Use FastAPI CLI for development server - Manage server lifecycle for tests - Configure test
  environment

- **testing**: Add e2e testing infrastructure with Playwright
  ([`5bd3ca3`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/5bd3ca36408e8b20a02fbf82a51925e5882ef713))

- Add e2e test configuration with fixtures - Implement base page object model - Share test settings
  with unit tests - Configure browser and page management

- **traefik**: Add development traefik configuration
  ([`95a108c`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/95a108c75d867b6e838309b8993f5e4981925f3d))

- **traefik**: Add dynamic configuration for security headers
  ([`4faf504`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/4faf50406b18b829f1fcc0b660cdfb6d0d622301))

- **traefik**: Add production traefik configuration with SSL
  ([`13d7e5b`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/13d7e5b96b936dc12f781dcf57b7f4bd133d15f9))

### Refactoring

- **api**: Use settings for API versioning
  ([`ae26e75`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/ae26e7506a4d333da6fc6b8b9c4a11c39c15176b))

- Use settings for API version prefix - Update health check test to use settings - Improve route
  organization

- **config**: Improve settings validation and documentation
  ([`9c1a16e`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/9c1a16e1590b139798cd17823c61c6af4c241f28))

- **config**: Remove environment setting in favor of DEBUG flag
  ([`548e7e1`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/548e7e170775d4892b617a52bf636f2addf6cb67))

- Removed ENVIRONMENT setting to simplify configuration - Enhanced DEBUG field documentation -
  Maintains production-first mindset with DEBUG=False by default

BREAKING CHANGE: Removed ENVIRONMENT setting. Use DEBUG=True for development when needed.

- **main**: Move docs to root level while keeping API endpoints prefixed
  ([`251a1c5`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/251a1c5d90892c26b99b040247be79fac0f61a4e))

- Changed docs_url from '/api/docs' to '/docs' for better discoverability - Changed openapi_url from
  '/api/openapi.json' to '/openapi.json' - Maintained API prefix for all other endpoints via router

### Testing

- **config**: Improve type safety and test organization
  ([`e27b34d`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/e27b34d602c2c014daee6100b1a04cd8b6032036))

- **core**: Add comprehensive tests for settings management
  ([`0903e31`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/0903e318ceed152f8f0c7f500e506c7461666a89))

- Add tests for default values and environment variables - Test validation rules for SECRET_KEY and
  CORS origins - Test computed properties for API paths and database URI - Verify settings caching
  behavior - Add test fixtures for reusability

- **e2e**: Implement health endpoint e2e test
  ([`91ef870`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/91ef8708ae72d8fd0efff70067490d1411709d38))

- Add health endpoint test using page object model - Verify API response in browser context - Add
  e2e test marker

- **fixtures**: Standardize test fixtures and settings override
  ([`e649f3e`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/e649f3e964cb86ac231f6006ae02c0d9126f0fce))

- **health**: Refactor health check tests to use TestClient
  ([`613ffce`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/613ffce0db52f0bee26cd9fc10f07b813416b5e0))

### BREAKING CHANGES

- **config**: Removed ENVIRONMENT setting. Use DEBUG=True for development when needed.
