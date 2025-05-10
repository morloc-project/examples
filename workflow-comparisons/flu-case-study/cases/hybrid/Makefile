all: nexus
	snakemake -c1

nexus:
	morloc make main.loc

clean:
	rm -rf .snakemake
	rm -rf pool* nexus* *pdf *rda __pycache__ tree.json
	rm -rf 0*
