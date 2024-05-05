all:
	python3 flu.py \
		--mindate "2021/01/01" \
		--maxdate "2021/01/14" \
		--plotfile "tree.pdf" \
		--treefile "tree.newick" \
		--email "wena@mailinator.com" \
		--query "Influenza+A+Virus[Organism]+H3N2[ALL]+HA[ALL]" \
		data/refs.txt

clean:
	rm -f tree.*
