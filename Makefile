runserver:
	poetry run komtek/manage.py runserver 7005

makemigrations:
	poetry run komtek/manage.py makemigrations

migrate:
	poetry run komtek/manage.py migrate

superuser:
	poetry run komtek/manage.py createsuperuser

shell:
	poetry run komtek/manage.py shell