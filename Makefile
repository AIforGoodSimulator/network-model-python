launch-docker:
	docker build . -t network-model:1.0
	docker rm -f network-model || true
	docker run --cpus 4 --cpu-shares 1024 --name network-model -p 6969:6969 -d -v $(PWD):/app:rw network-model:1.0
	docker exec -it network-model bash
