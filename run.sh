docker run --rm -it \
-p 8080:8080 -p 8081:8081 -p 8082:8082 \
-v $(pwd)/model-store:/home/model-server/model-store torchserve_custom:latest \
torchserve --start --model-store model-store --ts-config model-store/config.properties
