all: test

prepare_test_env:
	docker run --name test_postgres --rm -d -p 5432:5432 -e POSTGRES_PASSWORD=letmein postgres
	docker run --name test_redis --rm -d -p 6379:6379 redis:4
	docker run --name test_rabbitmq --rm -d -p 15672:15672 -p 5672:5672 -e RABBITMQ_DEFAULT_USER=rabbit -e RABBITMQ_DEFAULT_PASS=letmein rabbitmq:3-management
	sleep 5
	docker exec -ti test_postgres su postgres -c "createdb startlette_demo_test"
	docker exec -ti test_postgres su postgres -c "createdb startlette_demo"
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
	docker stop test_rabbitmq

