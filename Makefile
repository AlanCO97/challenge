.PHONY: start-container requirements start-reservation start-passenger alembic-upgrade-pasajeros alembic-upgrade-reservas migrate

RESERVAS_DIR = reservas
PASAJEROS_DIR = pasajeros
ALEMBIC = alembic

start-container:
	docker-compose up -d

requirements:
	pip install -r requirements.txt

# Target to upgrade the database in reservas to the latest version
alembic-upgrade-reservas:
	@echo "Migrando reservas"
	@cd $(RESERVAS_DIR) && $(ALEMBIC) upgrade head

# Target to upgrade the database in pasajeros to the latest version
alembic-upgrade-pasajeros:
	@echo "Migrando pasajeros"
	@cd $(PASAJEROS_DIR) && $(ALEMBIC) upgrade head

migrate: alembic-upgrade-reservas alembic-upgrade-pasajeros

start-reservation:
	fastapi dev reservas/main.py

start-passenger:
	python pasajeros/main.py