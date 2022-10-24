runserver:
	poetry run komtek/manage.py runserver 7000

makemigrations:
	poetry run komtek/manage.py makemigrations

migrate:
	poetry run komtek/manage.py migrate

superuser:
	poetry run komtek/manage.py createsuperuser

shell:
	poetry run komtek/manage.py shell

install:
	poetry run install

docker_up:
	docker compose up -d --build
