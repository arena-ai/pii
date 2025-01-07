#!/bin/bash

# This is a read-only-from-registry token, create your own
TOKEN=xxx

# Check if the first argument is provided
if [ -z "$1" ]; then
  echo "No argument supplied. Please provide 'presidio' or 'sarus' as the first argument."
  exit 1
fi

# Test feature based on the argument
if [ "$1" == "presidio" ]; then
    echo "Testing Presidio"
    # Pull the latest image of presidio analyzer
    docker pull mcr.microsoft.com/presidio-analyzer
    # Run containers with default ports
    container_id=$(docker run -d -p 5002:3000 mcr.microsoft.com/presidio-analyzer:latest)
elif [ "$1" == "sarus" ]; then
    echo "Testing Sarus"
    # Pull the latest image of arena analyzer
    echo "$TOKEN" | docker login registry.gitlab.com -u piir --password-stdin
    docker pull registry.gitlab.com/sarus-tech/lab/pii-removal/presidio-analyzer:latest
    # Run containers with default ports
    container_id=$(docker run -d -p 5002:3000 registry.gitlab.com/sarus-tech/lab/pii-removal/presidio-analyzer:latest)
else
    echo "Invalid argument. Please provide 'presidio' or 'sarus' as the first argument."
    exit 1
fi

# Give the service a few seconds to start
sleep 40

# Run a simple test
curl -X POST http://localhost:5002/analyze -H "Content-type: application/json" --data "{ \"text\": \"John Smith drivers license is AC432223\", \"language\" : \"en\"}"

# Stop and remove the container
docker stop $container_id
docker rm $container_id
echo "Service stopped and cleaned up."