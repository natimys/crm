.PHONY: start migrate build

up:
	docker compose up -d
	docker compose logs -f

down:
	docker compose down

build:
	./build.sh
	$(MAKE) start

migrate:
	$(MAKE) start
	docker compose exec backend alembic upgrade head

create-migration:
	@if [ -z "$(desc)" ]; then echo "Error: desc is required"; exit 1; fi
	docker compose run --rm $(BACKEND_SVC) alembic revision --autogenerate -m "$(desc)"

logs:
	docker compose logs -f