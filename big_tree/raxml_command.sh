# RAxML command: this was run ten times (100 trees total) and the tree with the best maximum likelihood was chosen

raxmlHPC-PTHREADS-SSE3 -T 4 -s trich_collapsed.fas -g constraint_tree.tre -m GTRCAT -n barcodes_constraint_$1 -p $RANDOM -f a -N 10 -x $RANDOM