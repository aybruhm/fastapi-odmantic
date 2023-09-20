build_dev:
	docker compose -f "docker-compose.dev.yml" build

up_dev:
	docker compose -f "docker-compose.dev.yml" up -d

run_dev:
	docker compose -f "docker-compose.dev.yml" up -d --build

run_prod:
	docker compose -f "docker-compose.prod.yml" up -d --build

down_dev:
	docker compose -f "docker-compose.dev.yml" down

freeze_deps:
	pipenv requirements > requirements.txt