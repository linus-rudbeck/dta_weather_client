```bash
# Create a Docker network named 'dtawn'
docker network create dtawn

# Build the Docker image for the weather API
docker run -d --network dtawn -p 5555:5555 --rm --name api rudbeck/demo_weather_api
```