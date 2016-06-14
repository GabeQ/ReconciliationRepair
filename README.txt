# cheeta.py

# Created by Matt Dohlen, Chen Pekker, Gabriel Quiroz
# June 2016

# Requirements
biopython
enum
errno
ete3
networkx

# What is Cheeta

Cheeta is a program that takes as input a .nexus or .tree file containing a 
host tree, a parasite tree, and the tip mappings between the trees. It runs
the Dynamic Programing Method (Tarzan), a fixer algorithm (Cheeta) to ensure that
the reconciliation is temporally consistent, and a meta heuristic (Jane) in order
to try and determine whether Jane has produced an optimal reconciliation or whether
the user should try to run Jane with larger parameters in order to obtain better 
results.