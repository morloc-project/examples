REPO=ghcr.io/morloc-project/morloc/flu-case:0.52.1

# Build the required docker image
build:
	podman build --no-cache --force-rm -t ${REPO} .

# Open a shell
shell:
	podman run -v ${PWD}:/workflow-comparisons -w /workflow-comparisons -it ${REPO} /bin/bash

clean:
	for f in cases/*; do $(MAKE) -C $$f  clean; done

push:
	podman push ${REPO}

# retrieve the latest morloc builds from the github registry
pull:
	podman pull ${REPO}
