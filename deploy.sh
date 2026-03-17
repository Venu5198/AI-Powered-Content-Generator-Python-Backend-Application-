#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Starting deployment of AI Content Generator..."

# 1. Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found. Please create one based on the README instructions."
    exit 1
fi

# 2. Stop and remove existing container if it's running
echo "🛑 Stopping existing containers on port 5000..."
# Find container ID using port 5000 and stop it
EXISTING_CONTAINER=$(docker ps -q --filter "ancestor=ai-content-generator")
if [ ! -z "$EXISTING_CONTAINER" ]; then
    docker rm -f $EXISTING_CONTAINER
    echo "✅ Removed old container."
fi

# 3. Build the Docker image
echo "🔨 Building the optimized Docker image..."
docker build -t ai-content-generator .

# 4. Run the new container
echo "🏃‍♂️ Starting the new container in the background..."
docker run -d -p 5000:5000 --env-file .env ai-content-generator

echo "🎉 Deployment successful! The application is running at http://localhost:5000"
