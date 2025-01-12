REPO=ghcr.io/morloc-project/morloc/flu-case:0.51.1

shell:
	# This command requires building the Dockerfile from flu-case-study
	podman run -v ${PWD}:/workflow-comparisons -w /workflow-comparisons -v /dev/shm:/dev/shm -it ${REPO} /bin/bash	

clean:
	rm -f test-data-*
