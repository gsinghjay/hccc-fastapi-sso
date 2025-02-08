#!/bin/bash

# Create main project directories
mkdir -p app/{api/v1,core,db,models,schemas,services,dependencies}
mkdir -p tests/{api,services}
mkdir -p alembic

# Create __init__.py files
touch app/__init__.py
touch app/api/__init__.py
touch app/api/v1/__init__.py
touch app/core/__init__.py
touch app/db/__init__.py
touch app/models/__init__.py
touch app/schemas/__init__.py
touch app/services/__init__.py
touch app/dependencies/__init__.py

# Create core files
touch app/main.py
touch app/core/{config,security,logging}.py

# Create API files
touch app/api/v1/{auth,users}.py

# Create database files
touch app/db/{base,session}.py

# Create model files
touch app/models/{base,user}.py

# Create schema files
touch app/schemas/{base,user}.py

# Create service files
touch app/services/user.py

# Create dependency files
touch app/dependencies/auth.py

# Create test files
touch tests/conftest.py
touch tests/api/__init__.py
touch tests/services/__init__.py

# Set permissions
chmod +x ./create_project.sh

echo "FastAPI project structure created successfully!"