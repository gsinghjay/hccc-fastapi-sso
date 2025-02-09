#!/bin/bash

# Start the FastAPI server in the background using FastAPI CLI
echo "Starting FastAPI server..."
poetry run fastapi dev app/main.py --port 8000 &
SERVER_PID=$!

# Wait for the server to start
echo "Waiting for server to start..."
sleep 3

# Run the e2e tests
echo "Running e2e tests..."
poetry run pytest tests/e2e/ -v -m e2e

# Cleanup: Kill the server
echo "Cleaning up..."
kill $SERVER_PID

echo "Done!" 