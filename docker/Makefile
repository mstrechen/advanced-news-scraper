.PHONY: help
.DEFAULT_GOAL := help

help:
	@echo "Availabale jobs:"
	@echo "  dev - run all necessary services in dev mode (hot-reload etc)"
	@echo "  prod - build and run all necessary services in prod mode (in background)"

dev:
	docker-compose up

rebuild:
	docker-compose build

prod:
	docker-compose -f docker-compose.prod.yml up  -d --build

prod-recreate:
	docker-compose --force-recreate -f docker-compose.prod.yml up  -d --build

sync-from-git:
	git pull