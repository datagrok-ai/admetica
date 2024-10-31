#!/bin/bash
set -e

IMAGE_NAME="admetica"
CONTAINER_NAME="admetica_container"

echo "Building Docker image: $IMAGE_NAME"
docker build -t $IMAGE_NAME .

if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping and removing existing container: $CONTAINER_NAME"
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

echo "Running Docker container: $CONTAINER_NAME"
docker run -d \
    --name $CONTAINER_NAME \
    -p 1112:1112 \
    $IMAGE_NAME

# Wait for the service to start
while ! curl -s http://localhost:1112/apidocs > /dev/null; do
    echo "Waiting for the server to start..."
    sleep 2
done

URL="http://localhost:1112/apidocs"
echo "Opening API documentation in the browser..."

case "$(uname)" in
    Linux*)
        xdg-open "$URL"
        ;;
    Darwin*)
        open "$URL"
        ;;
    CYGWIN*|MINGW32*|MSYS*)
        start "$URL"
        ;;
    *)
        echo "Unsupported OS. Please open the URL manually: $URL"
        ;;
esac

echo "Admetica is running at $URL"