import sys
import dendropy
from dendropy.calculate import treecompare

t1_filename = sys.argv[1]
t2_filename = sys.argv[2]

# Create taxon namespace
tns = dendropy.TaxonNamespace()

# Read in the trees
t1 = dendropy.Tree.get(path=t1_filename, schema="newick", taxon_namespace=tns)
t2 = dendropy.Tree.get(path=t2_filename, schema="newick", taxon_namespace=tns)

# Calculate rf distance
rf_dist = treecompare.robinson_foulds_distance(t1, t2)

# Calculate weighted rf distance
weighted_rf_dist = treecompare.weighted_robinson_foulds_distance(t1, t2)

print("Your rf dist: " + str(rf_dist) + ".")
print("Your weighted rf dist: " + str(weighted_rf_dist) + ".")
