.PHONY: help
.DEFAULT_GOAL := help

help:
	@echo "Availabale jobs:"
	@echo "  dev - run all necessary services in dev mode (hot-reload etc)"
	@echo "  rebuild - rebuld dev containers"
	@echo "  prod - build and run all necessary services in prod mode (in background)"
	@echo "  prod-recreate - same as prod, but forces to recreate containers"
	@echo "  new-migration - create new migration. Usage: \$ make new-migration MESSAGE=_your_message_ "

dev: stop-web-celery
	docker-compose up -d

test:
	MODE=TEST docker-compose up migrate

build: rebuild
rebuild:
	docker-compose build

prod:
	docker-compose -f docker-compose.prod.yml up  -d --build

prod-recreate:
	docker-compose --force-recreate -f docker-compose.prod.yml up  -d --build

new-migration:
	MODE=NEW_MIGRATION MIGRATION_MESSAGE="${MESSAGE}" docker-compose up migrate

migrate:
	docker-compose up migrate

downgrade-db:
	MODE=DOWNGRADE docker-compose up migrate

upgrade-db: migrate

sync-from-git:
	git pull

full-stop:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml down

stop-web-celery:
	docker-compose stop celery web

generate-translations:
	MODE=GENERATE_TRANSLATIONS docker-compose up migrate

compile-translations:
	MODE=COMPILE_TRANSLATIONS docker-compose up migrate
