NAME="edrf"

up:
	docker-compose up -d
down:
	docker-compose down -v
restart:
	docker restart ${NAME}
logs:
	docker logs -f ${NAME}
exec:
	docker exec -it ${NAME} sh
build:
	docker build -t edrf:1.0.0 .
