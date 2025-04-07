install:
	pip install -r requirements.txt

dev:
	DEBUG=1 python app.py

start:
	ASSETS="PROD" ENV="PROD" gunicorn app:app

webpack:
	cd fin-track-ui && npm start