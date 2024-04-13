# Compile
run:
	docker run -v .:/case -w /case flu-comp  

shell:
	docker run -v .:/case -w /case -it flu-comp /bin/bash 

# Build the required docker image
build:
	docker build -t flu-comp .
