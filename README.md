# Reconciliation-Repair

Use/run the files in the following order:  

1. Unzip real-100taxa.zip. This should result in a folder named real-100taxa in the root directory containing about 5000 .newick files.  
2. Run newickToTreeParser.py. This should convert all .newick files in folder real-100taxa into corresponding .tree files and store them in a newly created folder named treeFiles.  
3. Run fixer.py. This should run the TemporalConsistencyFixer algorithm on the first 100 .newick files in folder real-100taxa and write outputs into corresponding .txt files in a newly created folder named fixerOut.  
4. Run execJane.py. This should execute Jane on the first 100 .tree files in folder treeFiles and write outputs into corresponding .txt files in a newly created folder named janeOut.  
5. Run calcJaneCost.py. This should calculate the reconciliation costs for all files in folder janeOut and store them in corresponding .txt files in a newly created folder named janeCosts.  
6. Run makePlot.py. This should plot costs of temporally consistent reconciliations found by TemporalConsistencyFixer algorithm as well as those found by Jane against file indices based on files in folders fixOut and janeCosts.

A few notes:  
* The following external libraries are required to run the code: biopython, ete2, networkx, numpy, matplotlib.  
* There are already two generated plots in folder plots. Both plots compare reconciliation costs found by TemporalConsistencyFixer algorithm and Jane for the first 100 files in real-100taxa dataset. Both plots are generated using DTL values of 2, 3 and 1, respectively. The only difference between the two plots is that plot30\_30.png is generated using 30 generations and a population of size 30 for Jane while plot100\_100.png is generated using 100 generations and a population of size 100 for Jane.
