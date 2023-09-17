build_dev:
	docker compose -f "docker-compose.dev.yml" build

up_dev:
	docker compose -f "docker-compose.dev.yml" up -d

run_dev:
	docker compose -f "docker-compose.dev.yml" up --build

run_prod:
	docker compose -f "docker-compose.prod.yml" up --build

down_dev:
	docker compose -f "docker-compose.dev.yml" dow

freeze_deps:
	pipenv requirements > requirements.txt