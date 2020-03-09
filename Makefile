prepare:
	docker-compose run --rm server create_db
	docker-compose up -d

stop:
	docker stop ubhara_redis_1 ubhara_server_1 ubhara_scheduled_worker_1 ubhara_scheduler_1 ubhara_adhoc_worker_1 ubhara_nginx_1 ubhara_postgres_1 ubhara_crawler_1
clear:
	docker rm ubhara_redis_1 ubhara_server_1 ubhara_scheduled_worker_1 ubhara_scheduler_1 ubhara_adhoc_worker_1 ubhara_nginx_1 ubhara_postgres_1 ubhawra_crawler_1
