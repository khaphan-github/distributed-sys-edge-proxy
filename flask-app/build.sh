docker build -f docker/Dockerfile -t livescores .
docker run --rm -p 5200:5200 livescores