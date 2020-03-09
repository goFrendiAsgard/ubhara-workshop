prepare:
	docker-compose run --rm server create_db
	docker-compose up
	#docker-compose up -d

start-with-crawler:
	docker start ubhara_redis_1 ubhara_server_1 ubhara_scheduled_worker_1 ubhara_scheduler_1 ubhara_adhoc_worker_1 ubhara_nginx_1 ubhara_postgres_1 ubhara_crawler_1

start:
	docker start ubhara_redis_1 ubhara_server_1 ubhara_scheduled_worker_1 ubhara_scheduler_1 ubhara_adhoc_worker_1 ubhara_nginx_1 ubhara_postgres_1

stop:
	docker stop ubhara_redis_1 ubhara_server_1 ubhara_scheduled_worker_1 ubhara_scheduler_1 ubhara_adhoc_worker_1 ubhara_nginx_1 ubhara_postgres_1 ubhara_crawler_1

tear-down:
	docker rm ubhara_redis_1 ubhara_server_1 ubhara_scheduled_worker_1 ubhara_scheduler_1 ubhara_adhoc_worker_1 ubhara_nginx_1 ubhara_postgres_1 ubhara_crawler_1
