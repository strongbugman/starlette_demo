all: test

prepare_test_env:
	docker run --name test_postgres --rm -d -p 5432:5432 -e POSTGRES_PASSWORD=letmein postgres
	docker run --name test_redis --rm -d -p 6379:6379 redis:4
	sleep 5
	docker exec -ti test_postgres su postgres -c "createdb {{cookiecutter.app_name}}_test"
	docker exec -ti test_postgres su postgres -c "createdb {{cookiecutter.app_name}}"
	pip install -U -r requirements.txt
	pip install -U -r test_requirements.txt

test:
	black . --check
	flake8 app tests
	mypy --ignore-missing-imports app
	pytest

destroy_test_env:
	docker stop test_postgres
	docker stop test_redis

