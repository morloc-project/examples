REPO=ghcr.io/morloc-project/morloc/flu-case:0.51.0

# Build the required docker image
build:
	podman build --no-cache --force-rm -t ${REPO} .

# Open a shell
shell:
	podman run -v ${PWD}:/workflow-comparisons -w /workflow-comparisons -it ${REPO} /bin/bash

clean:
	for f in cases/*; do $(MAKE) -C $$f  clean; done
