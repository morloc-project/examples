REPO=morloc-debug

# Build the required docker image
build:
	podman build --no-cache -t ${REPO} .

# Open a shell
shell:
	podman run -v ${PWD}:/workflow-comparisons -w /workflow-comparisons -it ${REPO} /bin/bash
