all: nexus.py
	snakemake -c1

nexus.py:
	morloc make main.loc

clean:
	rm -rf .snakemake
	rm -rf pool* nexus* *pdf *rda __pycache__ tree.json
	rm -rf 0*
