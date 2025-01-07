# PII Removal

docker build -t myapp:1.0 --build-arg NAME=myapp .
docker run -p 8080:8080 --name myrunningapp -e PORT=8080 myapp:1.0
curl -X POST http://localhost:8080/analyze -H "Content-Type: application/json" -d '{"text": "My name is Alex", "language": "en"}'

# Use a pre-build image
