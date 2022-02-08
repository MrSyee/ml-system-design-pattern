format:
	black .
	isort .

run:
	sh run.sh

post:
	curl \
		-X POST \
		-H "Content-Type: application/json" \
		-d '{"data": [[1.0, 2.0, 3.0, 4.0]]}' \
		localhost:8000/predict