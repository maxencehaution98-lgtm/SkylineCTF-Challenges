#!/bin/bash

# Build the wizard image if it doesn't exist (or force update with --build)
if [[ "$(docker images -q skyline-wizard 2> /dev/null)" == "" ]] || [[ "$1" == "--build" ]]; then
    echo "🏗️  Construction de l'image Docker du wizard..."
    docker build -t skyline-wizard -f Dockerfile.wizard .
fi

echo "🧙‍♂️  Lancement du Wizard..."

# Run the container
# -v $(pwd):/app : Mount current directory to /app
# -it : Interactive mode
# --rm : Remove container after exit
# Ensure gh config dir exists (for auth persistence)
mkdir -p "${HOME}/.config/gh"

docker run -it --rm \
    -e PYTHONDONTWRITEBYTECODE=1 \
    -v "$(pwd):/app" \
    -v "${HOME}/.config/gh:/root/.config/gh" \
    skyline-wizard
