```bash
# Create a Docker network named 'dtawn'
docker network create dtawn

# Run the container for weather API
docker run -d --network dtawn -p 5555:5555 --rm --name api rudbeck/demo_weather_api

# Run the client for weather API
docker run --network dtawn --rm --env HOST=api -v ${PWD}/dtawout:/app/data dtawc
```