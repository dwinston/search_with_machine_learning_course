dev:
	docker compose -f docker/docker-compose.yml up -d

gui:
	FLASK_ENV=development FLASK_APP=week1 flask run --port 3000