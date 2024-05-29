.PHONY: start-container requirements start-reservation start-passenger


start-container:
	docker-compose up -d

requirements:
	pip install -r requirements.txt

start-reservation:
	fastapi dev reservas/main.py

start-passenger:
	python pasajeros/main.py