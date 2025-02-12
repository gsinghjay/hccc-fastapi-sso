# CHANGELOG


## v3.1.2 (2025-02-12)

### Bug Fixes

- Correct pytest.ini syntax for GitHub Actions
  ([`a177482`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/a177482ecefb1a448805e12fbc894b1582be6dc1))

### Continuous Integration

- Enable GitHub Actions for all branch pushes
  ([`090a52c`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/090a52c1de4b44c2977c5009c3f92855b81fb816))


## v3.1.1 (2025-02-12)

### Bug Fixes

- **repo**: Improve async type safety in user repository
  ([`52c1ea4`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/52c1ea4be4f4d36667b4ff13891aa361bfdee174))

- Add proper type hints for async results - Handle both SQLAlchemy and mocked async behavior -
  Remove redundant imports - Improve test compatibility with async mocks - Maintain 100% test
  coverage for repository layer

### Chores

- **docker**: Update test environment configuration
  ([`2d235bf`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/2d235bfef43e67e0465586be025cabf188213563))

- Update test database configuration - Improve test isolation - Configure test resource limits - Add
  test-specific environment variables

- **test**: Add coverage reports and analysis
  ([`7bb0caa`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/7bb0caaed1547ca95744909970db96eedc334f12))

- Add HTML coverage reports - Add XML coverage reports - Document current coverage status - Track
  coverage metrics for CI/CD

### Continuous Integration

- Add GitHub Actions workflow for tests
  ([`da27e4c`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/da27e4c1433a214d93091bbfce11e1877811899d))

- Add pytest workflow - Configure test matrix - Set up coverage reporting - Add mypy type checking -
  Configure test dependencies

### Documentation

- Update documentation and project configuration
  ([`f23457a`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/f23457a4a9260ca05b780c4be634e6c30b262c14))

- Update README with test instructions - Add coverage report patterns to .gitignore - Add detailed
  documentation in DOCS.md - Update development commands and scripts

### Testing

- **auth**: Improve auth dependency tests
  ([`4568160`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/45681608b106ef1ea927f024942d113d26d10193))

- Add test cases for auth dependencies - Fix async behavior in auth tests - Improve test coverage
  for auth module - Add proper type hints for auth dependencies

- **repo**: Add comprehensive test suite for user repository
  ([`74866f4`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/74866f4e90d5a13c14e784634fb79b6a968be2d9))

- Add test cases for all repository methods - Implement proper async mock handling - Test both
  success and error scenarios - Ensure proper test isolation - Add test fixtures and helpers


## v3.1.0 (2025-02-12)

### Chores

- House cleaning
  ([`9c742e3`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/9c742e343b9ced2e831ee5582e08d75c5d74058a))

### Code Style

- **middleware**: Improve code formatting in security headers
  ([`0bbc969`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/0bbc9697d8d1b2fc3c26fe3a3b0f5b17dcabd185))

- Enhance readability of security headers dictionary in development mode - Apply consistent
  multi-line formatting for dictionary updates

This is a code style improvement that makes the security headers configuration more readable and
  maintainable, following project formatting standards.

### Documentation

- Enhance auth flow documentation with sequence diagrams
  ([`9a84019`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/9a840196a46b46ab5780f844d36e6281515c186a))

- Add sequence diagrams for login flow and JWT token generation - Add sequence diagrams for token
  verification process - Add sequence diagrams for protected endpoint access - Add sequence diagrams
  for security middleware flow - Add sequence diagrams for rate limiting - Add sequence diagrams for
  error handling - Integrate diagrams with existing documentation - Maintain security features
  implementation section

- **roadmap**: Update development roadmap status
  ([`d8565a6`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/d8565a669c2cca4223b14c3b6bcf269a99f63db6))

- Update Authentication Dependencies section to complete (✅) - Add comprehensive test coverage
  details - Document JWT token validation features - List type safety improvements

- Enhance Middleware section details - Add CSP configuration information - Document
  environment-aware CORS - Add rate limiting configuration details - Note code formatting
  improvements

### Features

- **auth**: Implement FastAPI authentication dependencies
  ([`9d4d25a`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/9d4d25a81cdbb8a8578e950f56ddb3117d859e93))

- Add get_current_user dependency for required authentication - Add get_current_user_optional for
  optional authentication - Implement JWT token validation and user retrieval - Add proper error
  handling for token validation

### Testing

- **auth**: Add comprehensive tests for auth dependencies
  ([`07c93ff`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/07c93ffe909c5b98e9e14424546317999c36d807))

- Add test cases for get_current_user dependency - Add test cases for get_current_user_optional
  dependency - Improve async mock setup for database operations - Add test coverage for all error
  scenarios

- **auth**: Add comprehensive tests for auth dependencies
  ([`2d51826`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/2d518260656e5b9688ab3b81013e5333b3d3f2a0))

- Add test cases for get_current_user dependency - Add test cases for get_current_user_optional
  dependency - Improve async mock setup for database operations - Add test coverage for all error
  scenarios


## v3.0.1 (2025-02-12)

### Bug Fixes

- **security**: Update CSP headers to support ReDoc functionality
  ([`60535d5`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/60535d5938358d1a32e84ded68938da11fda9ef5))

- Add worker-src and script-src directives for Web Workers - Allow necessary sources for ReDoc
  documentation - Consolidate security headers in FastAPI middleware - Improve development
  environment CSP configuration - Remove redundant security headers from Traefik configuration

### Documentation

- Enhance project documentation and roadmap
  ([`92b9d0c`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/92b9d0c4416ce01d1207802b534f61b6f93487bc))

- Add comprehensive service layer documentation with examples - Update project roadmap with
  documentation milestone - Improve testing documentation with detailed examples - Maintain Docker
  Compose configuration in roadmap - Reorganize development steps for better clarity

This commit improves the overall documentation quality and organization, making it easier for
  developers to understand the project structure, testing approach, and development workflow.


## v3.0.0 (2025-02-12)

### Chores

- Added bcrypt
  ([`4f20a0a`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/4f20a0a32dfd6c05d938698313b331e4abec2a84))

### Features

- **api**: Improve error handling and response codes
  ([`d1d63ad`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/d1d63ad0320c8e695b6467910501a00df2413d08))

BREAKING CHANGE: standardize error responses across all endpoints

- Add proper exception handling for auth endpoints - Implement consistent error responses for user
  operations - Update OpenAPI documentation with all possible response codes - Handle email
  conflicts with 409 status code - Improve error messages for better debugging - Add proper
  WWW-Authenticate headers for auth failures

This change requires clients to handle the new error response format and status codes appropriately.

- **infrastructure**: Implement automated database migrations
  ([`492ab55`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/492ab5555b4621f909736f2638380fedea92731f))

BREAKING CHANGE: add automatic database migration on container startup

- Add startup script for database readiness check and migration - Configure Alembic for async
  PostgreSQL migrations - Update Dockerfile with PostgreSQL client and startup script - Add health
  check to ensure database and migrations are ready - Implement proper container initialization
  sequence

This change requires running containers to be recreated to use the new startup sequence.

### Breaking Changes

- **api**: Standardize error responses across all endpoints


## v2.0.0 (2025-02-12)

### Features

- **security**: Implement JWT configuration and SQLAlchemy Base
  ([`be8c48c`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/be8c48c9012c8f6c00eed865937ff8837ab22598))

BREAKING CHANGE: add JWT algorithm configuration and SQLAlchemy Base class

- Add JWT_ALGORITHM setting with HS256 default in Settings class - Add proper type hints and
  documentation for JWT settings - Implement SQLAlchemy Base class for model inheritance - Follow
  security best practices for JWT configuration

This change requires updating environment variables with JWT_ALGORITHM if a different algorithm than
  HS256 is needed.

### Breaking Changes

- **security**: Add JWT algorithm configuration and SQLAlchemy Base class


## v1.2.0 (2025-02-10)

### Bug Fixes

- **docker**: Improve container networking and volume configuration
  ([`2267464`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/22674649c89e1fff4879ee2e27cfd38a8645e2c7))

- Remove conflicting network_mode directive - Configure proper volume mounts for coverage reports -
  Set up proper container dependencies and healthchecks

- **test**: Update e2e test configuration and improve test coverage
  ([`d6e323b`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/d6e323b27c509b2cd5e53a1f071e97eadb8c0ba0))

- Fix e2e test base URL configuration - Update test settings configuration - Add comprehensive
  configuration tests

### Chores

- Update project dependencies and configuration
  ([`8be50aa`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/8be50aae22304a91f7de5fccb49b397edc2bb900))

- Updated project structure and added "tree --gitignore" to docs
  ([`3a1a2fc`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/3a1a2fc563bc0da316ca08c18572a1db0086b59c))

- **config**: Update environment variable templates
  ([`f423648`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/f423648e6e4ac6f5efa1434b961a24f3c62f8c28))

- Add test-specific environment variables - Document configuration options - Update default values
  for development

- **deps**: Update project dependencies
  ([`b57fffe`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/b57fffe6c81fbed50906f4dd5a92d3a73bd1f2a2))

- Add Playwright and pytest-playwright for e2e testing - Update FastAPI and related dependencies -
  Add test-specific dependency groups

### Code Style

- Apply black formatting to codebase
  ([`b80a88c`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/b80a88c309b6b1567c35e47469300c2926cf83cd))

- Format Python files according to Black style - 18 files reformatted for consistent code style -
  Maintain 88 character line length

- **black**: Add black configuration
  ([`23f02b7`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/23f02b78ea6fbbdb2e3ea68b820c047fd3bb85e0))

- Add Black configuration to pyproject.toml - Set line length to 88 - Configure Python 3.12 as
  target version - Add docs directory to exclude patterns

### Documentation

- Update documentation with latest architecture changes
  ([`77085dc`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/77085dc1893ce93393ecc35d56f422f0e3b99ea7))

- **readme**: Update project progress and database testing infrastructure
  ([`f2df40d`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/f2df40d7b5bfbda09db44fc65623a94cd2707742))

- Add database testing infrastructure details - Update development roadmap progress - Add
  comprehensive testing documentation - Include quick start guide and database testing guide

- **scripts**: Add comprehensive commands reference
  ([`f1a292d`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/f1a292d97a9c594acf8afb29ff89bcfa95bc86b8))

- Add development setup commands - Add testing and database operations - Add code quality and
  dependency management commands - Add Docker operations and health checks - Add production
  deployment commands - Add Ansible variables example - Add common issues and solutions - Prepare
  for future automation with Ansible

### Features

- **api**: Update endpoints to use repository pattern
  ([`02375d5`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/02375d52e140f3ae8926cbbb33246073cdac9a53))

- **auth**: Add authentication service with JWT token support
  ([`65e6d4b`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/65e6d4bdba993e63e47e591c0e24d82adb726c14))

- **config**: Implement test database settings and validation
  ([`9e71844`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/9e71844c0d3ba9096cb193cb68b0ec5c206eb088))

- Add test database configuration settings - Implement database URI validation - Add rate limit
  validation - Add comprehensive configuration tests - Fix database path construction

- **health**: Add comprehensive health check system
  ([`fd032c4`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/fd032c478cc37fe86f39b251fcf3409321f1aa98))

- Add health check service layer - Implement health status schema - Add database health monitoring -
  Add end-to-end health check tests - Improve test coverage

- **infra**: Add playwright browser installation and test dependencies
  ([`6986153`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/6986153873dc81e4460230bafcb39d2b36741cfd))

- Add Playwright browser installation in Dockerfile - Configure proper permissions for test
  directories - Set up environment variables for testing

- **infra**: Add test database configuration and dependencies
  ([`0781403`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/0781403c97c3fbb5023f3faf2780ecd20a463b86))

- Add test database service in docker-compose.yml - Configure test database environment variables -
  Update poetry dependencies for testing - Configure pytest for parallel execution

- **schema**: Implement comprehensive user schemas with validation
  ([`f7e1ad7`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/f7e1ad73587f910cf5d989959c9d0db06bece4da))

- **security**: Implement password hashing and JWT token management
  ([`56530aa`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/56530aa52ca51b82130ab1b2548835269237e0c4))

- **test**: Add pytest configuration file
  ([`68ad0db`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/68ad0db2871601eb09b30c84025924c59fc06baa))

- Add test categories and markers - Configure coverage reporting - Set default test environment
  variables

- **test**: Enhance test infrastructure with fixtures
  ([`0e72521`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/0e725215807d2fdc176a74e5c10a924d6bdc0355))

- Add database test fixtures - Implement test database isolation - Add API test utilities -
  Configure end-to-end test environment - Add test cleanup procedures

### Refactoring

- **user**: Implement repository pattern for user management
  ([`b183e22`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/b183e22fc7200f40b19858962fa99e28703afff0))

### Testing

- Add comprehensive test suite for services and schemas
  ([`bbb7e69`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/bbb7e69ef399dd5898140eac8dbbe0ca74014701))


## v1.1.0 (2025-02-10)

### Chores

- **config**: Update environment configuration template
  ([`9b2bf21`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/9b2bf216b145cc584e9deaad6df69f8cd175ed12))

- Add comprehensive environment variable structure - Separate settings by category (App, DB,
  Security, etc.) - Add development-specific settings section - Update security and monitoring
  configurations

- **deps**: Add Node.js package configuration
  ([`0a3658e`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/0a3658e5df375b094b78b411a8eeb91023f2db85))

- Add cursor-tools dependencies - Configure development scripts - Set up Playwright for testing

- **git**: Update gitignore patterns
  ([`51eb9bf`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/51eb9bf5d6201c745964ccdb6c39072e83d45634))

- Add Node.js related ignores - Add cursor-tools environment file - Update environment file patterns
  - Organize ignore patterns by category

- **tools**: Add cursor-tools configuration
  ([`1287e6f`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/1287e6fbeec75a6b77a3d4a3da9650e2c3673386))

- Add initial cursor-tools setup - Configure AI assistance integration - Set up development tooling

### Documentation

- **readme**: Update implementation status indicators
  ([`8e65b78`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/8e65b78d3f664c163376fbd6acb284c984386d32))

- Add status indicators (✅ Complete, 🟡 Partial, 🔴 Not Started) - Mark components with basic file
  structure as partially complete - Add Services Layer section to roadmap - Update implementation
  details for completed components - Clarify partial implementation status for components with basic
  structure - Remove placeholder code snippets for unimplemented features

Components marked as partial: - Database setup (session.py pending) - User model & schemas
  (structure only) - Auth dependencies & security utils - API endpoints structure - Logging
  configuration - Testing infrastructure

- **rules**: Enhance FastAPI core configuration rules
  ([`c88ba12`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/c88ba120dcf1656eb73eb5f0c6e9031ac37a8da1))

- Add async configuration guidelines - Update middleware configuration rules - Add type safety
  requirements - Update configuration management section

- **rules**: Enhance middleware implementation rules
  ([`b180b89`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/b180b89e31d882178b89b314bfff3797d7ea035d))

- Add strict middleware execution order - Update type hints requirements - Add performance
  monitoring guidelines - Add environment-aware behavior rules

- **rules**: Update environment variables guidelines
  ([`b93b40b`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/b93b40bbc15133ccec45e2badc002bd814d981d6))

- Add validation hints in examples - Add proper error messages for validation - Update configuration
  management guidelines - Add SecretStr and type validation rules

- **rules**: Update infrastructure deployment rules
  ([`7346259`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/7346259e7bd27935d1ae0b54d2e24e1283fb4981))

- Add Traefik configuration guidelines - Update Docker deployment standards - Add SSL/TLS
  configuration rules - Add proper network segmentation rules

- **rules**: Update security implementation rules
  ([`f1ee607`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/f1ee6077a66d906a6aaf6e6584456b4a5b389dd3))

- Add HTTPS and SSL configuration rules - Update CORS security guidelines - Add proper scheme
  handling rules - Enhance security headers configuration

### Features

- **api**: Enhance health check endpoint
  ([`bdd92f2`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/bdd92f2f10684c7233c74fded11aa768637d8cfe))

- Add request context to health check endpoint - Improve function documentation - Add request
  parameter for better debugging capabilities

- **ci**: Add deployment script
  ([`59b1fdc`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/59b1fdc606836752b4e22bf9e8a214fc2ec37f6b))

- Add production deployment automation - Configure environment setup - Add deployment safety checks
  - Include rollback capabilities

- **core**: Enhance FastAPI application configuration
  ([`757aa0a`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/757aa0acca202c247f9340b4edad89ec0e7c4494))

- Add HTTPS scheme handling middleware - Configure Swagger UI with improved parameters - Set up
  HTTPS-first server configuration - Add comprehensive API documentation settings

- **deploy**: Update development Docker configuration
  ([`89fed0c`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/89fed0cb6c9f3ab2085cf961f3c45f05c406155f))

- Add Traefik reverse proxy setup - Configure SSL termination - Set up CORS and security headers -
  Add development-specific settings - Configure proper container dependencies

- **deploy**: Update production Docker configuration
  ([`b1629c4`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/b1629c408521e3bcf8d7f184104c0614819ef4a5))

- Add resource limits and reservations - Configure Traefik integration with SSL - Set up proper
  container networking - Add health checks for database - Configure production-grade security
  settings

- **infra**: Implement Traefik configuration
  ([`22e0f8f`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/22e0f8f7c11ed72df8e643f2dcdf819ad5555c57))

- Add separate dev/prod Traefik configurations - Set up authentication for Traefik dashboard -
  Configure SSL/TLS with Let's Encrypt - Add security headers and CORS middleware

- **security**: Implement comprehensive middleware stack
  ([`6372989`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/63729898b9231722bcd22f63a55b75ff6e15feb3))

- Add RateLimitMiddleware with token bucket algorithm - Implement HTTPSRedirectMiddleware for secure
  connections - Add RequestID and Timing middleware for request tracking - Add
  SecurityHeadersMiddleware with CSP and HSTS - Configure environment-aware CORS settings

### Refactoring

- **infra**: Reorganize Traefik configuration
  ([`1f4aeb1`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/1f4aeb1a459f42804687a47653995bfd2a1672f6))

- Remove deprecated Traefik configuration - Move security headers to middleware stack - Consolidate
  configuration into dev/prod files

### Testing

- **e2e**: Update base URL configuration
  ([`f00b314`](https://github.com/gsinghjay/hccc-fastapi-sso/commit/f00b314bd87a99dfcd2c19ff519f87be7c6eb112))

- Remove port from base URL - Update test configuration for Traefik setup - Align with new
  infrastructure configuration


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

### Breaking Changes

- **config**: Removed ENVIRONMENT setting. Use DEBUG=True for development when needed.
