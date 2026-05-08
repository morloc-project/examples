all:
	morloc make main.loc 

clean:
	rm -rf nexus nexus.c pool.cpp *out */nexus */*out */pool.cpp revcom.fasta log

run:
	./nexus fastaRevcom '"revcom.fasta"' '"test.fasta"' && cat revcom.fasta
