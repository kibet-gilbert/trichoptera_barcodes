'''This script was written to change the constraint taxon names to match the
names in the collapsed haplotype FASTA file
'''

import sys

def create_process_id_key(process_id_filename):
    '''Creates a key with the process ids and the sample ids
    '''
    # Open file with process IDs and Sample IDs
    process_file = open(process_id_filename)
    process_id_key = {}
    # Loop through and assign each sample id a process id
    for line in process_file.readlines():
        line = line.strip("\n")
        this_line = line.split("\t")
        process_id_key[this_line[1]] = this_line[0]
    process_file.close()
    return process_id_key

def create_species_id_2_taxon_key(constraint_taxa_filename):
    '''Create a key of species id's and species
    '''
    # Open file with lines that contain species IDs and taxon names
    constraint_taxa_file = open(constraint_taxa_filename)
    constraint_taxa_key = {}
    for line in constraint_taxa_file.readlines():
        species_id = line.split(" ")[0]
        constraint_taxa_key[species_id] = line.strip("\n")
    constraint_taxa_file.close()
    return constraint_taxa_key

def create_process_id_tree(constraint_tree_filename, process_id_key,
 constraint_taxa_key):
    '''Replaces species IDs and taxon names with process IDs
    '''
    constraint_tree_file = open(constraint_tree_filename)
    constraint_tree = constraint_tree_file.readline().strip("\n")
    process_ids_of_constraints = []
    # print constraint_tree
    for record in constraint_taxa_key:
        constraint_tree = constraint_tree.replace(constraint_taxa_key[record],
         process_id_key[record])
        process_ids_of_constraints.append(process_id_key[record])
    return constraint_tree, process_ids_of_constraints

def create_collapsed_haplo_key(process_ids_of_constraints,
 process_2_haplotypes_filename):
    process_2_haplotypes_file = open(process_2_haplotypes_filename)
    process_2_haplotype_key = {}
    for count,line in enumerate(process_2_haplotypes_file.readlines()):
        if count == 0:
            pass
        else:
            split_line = line.split(",")
            process_id = split_line[0]
            taxon_name = split_line[1].strip("\n")
            if len(taxon_name) > 256:
                print "This taxon name is too long for RAxML! Fix it! Taxon: " + str(taxon_name)
            if process_id in process_ids_of_constraints:
                process_2_haplotype_key[process_id] = taxon_name
    process_2_haplotypes_file.close()
    return process_2_haplotype_key

def create_collapsed_haplo_tree(constraint_tree, process_2_haplotype_key):
    for i in process_2_haplotype_key:
        constraint_tree = constraint_tree.replace(i, process_2_haplotype_key[i])
    return constraint_tree

# def in_process_id_key(constraint_species_id_filename, process_id_key):
#     species_ids = open(constraint_species_id_filename)
#     for line in species_ids.readlines():
#         line = line.strip("\n")
#         if line not in process_id_key:
#             print line

# def create_seq_collection(fasta_file):
#     seq_collection = []
#     for seq in skbio.io.read(fasta_file, format='fasta'):
#         seq_collection.append(seq)
#     return seq_collection

# def collapse_haplotypes(seq_collection):
#     new_seq_collection = []
#     for count, seq in enumerate(seq_collection):
#         for item, seq2 in enumerate(seq_collection):
#             if count == item:
#                 pass
#             else:
#                 if seq.lowercase() == seq2.lowercase():
#                     pass




if __name__ == "__main__":
    # The original constraint tree exported from Mesquite
    constraint_tree_filename = sys.argv[1]
    # The file includes the process ids and the sample ids that they corrrespond
    # to
    process_id_filename = sys.argv[2]
    # This file contains the names of all of the constraint taxa
    constraint_taxa_filename = sys.argv[3]
    # This file contains the process ids and the taxon names for the collapsed
    # haplotypes
    process_2_haplotypes_filename = sys.argv[4]
    process_id_key = create_process_id_key(process_id_filename)
    # print process_id_key
    constraint_taxa_key = create_species_id_2_taxon_key\
    (constraint_taxa_filename)
    # print constraint_taxa_key
    process_id_tree, process_ids_of_constraints = create_process_id_tree\
    (constraint_tree_filename, process_id_key, constraint_taxa_key)
    process_2_haplotype_key = create_collapsed_haplo_key\
    (process_ids_of_constraints, process_2_haplotypes_filename)
    final_constraint_tree = create_collapsed_haplo_tree(process_id_tree, process_2_haplotype_key)
    final_tree = open("collapsed_haplo_tree", "w")
    final_tree.write(final_constraint_tree)
