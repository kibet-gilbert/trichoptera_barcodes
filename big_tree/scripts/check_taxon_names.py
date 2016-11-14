import sys

tree_taxa = open(sys.argv[1])
alignment_file = open(sys.argv[2])
alignment = alignment_file.read()

for i in tree_taxa.readlines():
    taxon_name = i.strip("\n")
    if taxon_name in alignment:
        print("In")
    else:
        print("Yikes, this taxon: " + str(taxon_name) + " is not in the alignment!")

tree_taxa.close()
alignment_file.close()
