## Big Tree Analysis

#### Steps:

##### 1. Download the data
Visit the [project page](http://dx.doi.org/dx.doi.org/10.5883/DS-TBOL) in BOLD. Download both the `.tsv` of the specimen data and the FASTA file (by clicking on the buttons on the upper right hand part of the webpage). The name of the FASTA file will be referred to as `<FASTA_filename>` for the rest of these steps.

##### 2. Prepare file with geographic information
From the `.tsv` file downloaded from BOLD, pull the columns for Process ID, Country, and Province/State and create a new tab-delimited file with those three columns in that order. Save this file (it will be referred to as `<geographic_information_filename>` for the rest of these steps).

##### 3. Filter for unique haplotypes, while retaining geographic information

Make sure that you have Python 2.7.x installed on your computer and that it is your default Python. Download `seqio.py` and `haplo_plus_geography.py` from the [scripts](scripts) directory and ensure that they are in your working directory along with the FASTA file that you downloaded from step 1. Run the following command to generate the `HaplotypeTable.html`, `outfile.fas` (your FASTA file with the haplotypes collapsed and new location labels), and `processids.csv`. FYI, `$` refers to a command prompt in a Linux terminal, do not copy this as part of your command.
```
$ python haplo_plus_geograph.py <FASTA_filename> <geographic_information_filename>
```

##### 4. Clean up `oufile.fas`

`oufile.fas` contains some characters, `[` and `]`, that are not allowed by RAxML. We will now clean them up with `sed`. Make a new copy of `outfile.fas` called `trich_collapsed.fas`.

```
$ cp outfile.fas trich_collapsed.fas
```

Now replace the brackets in `trich_collapsed.fas` with `sed`:

```
$ sed -i -e 's/\[/_/g' trich_collapsed.fas
```
```
$ sed -i -e 's/]/_/g' trich_collapsed.fas
```

`trich_collapsed.fas` is now ready to run in RAxML

##### 5. Run RAxML tree searches with the constraing tree

During this step we will be running 100 RAxML searches with a constraint tree defined via the `-g` option in RAxML. The RAxML command that we used is kept in `raxml_command.sh`. 

This portion required the `pthreads` version of RAxML v8.2. Instructions on how to build this program are given in the [RAxML GitHub repository](https://github.com/stamatak/standard-RAxML).

You will notice that the tree that we used for the constraint was `constraint_tree.tre`. This tree was created manually using "known relationships" from previous phylogenetic hypotheses on Trichoptera. The relationships that we were not confident in were kept as a polytomy, which is resolved by RAxML. We ran the command in `raxml_command.sh` 10 times in order to generate 100 different ML trees. If you download `raxml_command.sh` and have `raxmlHPC-PTHREADS-SSE3` in your path, you can run these with something like:

```
for i in {1..10}; do
sh raxml_commands.sh
done
```

Once this is finished, choose the tree with the best maximum likelihood for the final, maximum likelihood tree.