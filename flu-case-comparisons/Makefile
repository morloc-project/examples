REPO=arendsee/flucase-comparisons

# Build the required docker image
build:
	docker build -t ${REPO} .

# Open a shell
shell:
	docker run -v ${PWD}:/case -w /case -it ${REPO} /bin/bash
