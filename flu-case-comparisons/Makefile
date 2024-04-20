# Build the required docker image
build:
	docker build -t flu-comp .

# Open a shell
shell:
	docker run -v .:/case -w /case -it flu-comp /bin/bash 
