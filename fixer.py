# fixer.py
#
# Weiyun Ma, Dima Smirnov
# May 2016
#
# This file runs the TemporalConsistencyFixer algorithm on the 
# first 100 .newick files in the real-100taxa folder and writes
# outputs into corresponding .txt files in the fixerOut folder.
#
# Run with
#   python fixer.py


# python libraries
from cStringIO import StringIO

# BioPython libraries
from Bio import Phylo

import DP
import pickle
import networkx as nx
from ete2 import Tree
import newickFormatReader
from ReconciliationGraph import buildReconciliation
import MasterReconciliation
import os.path
import os


# Global variables (can be customized in the future)
dVal = 2
tVal = 3
lVal = 1
fileNum = 100

def recon_tree_to_dtl(T):
    sigma, delta, theta, xi = [], [], [], []
    M, L, tau = {}, {}, {}

    for mapping_node in T.keys():
        g, s = mapping_node

        event, _, _ = T[mapping_node]
        if event != 'L':
            M[g] = s
            if event == 'S':
                sigma.append(g)
            elif event == 'D':
                delta.append(g)
            elif event == 'C':
                L[g] = s
            elif event == 'T':
                theta.append(g)


    for g in theta:
        _, child_1, child_2 = T[(g, M[g])]
        g1, s1 = child_1
        g2, s2 = child_2
        if M[g] == s1:
            xi.append((g, g2))
            tau[g] = s2
        else:
            tau[g] = s1

    return (L, M, sigma, delta, theta, xi, tau)


def dtl_to_recon_tree(S, G, alpha):
    L, M, sigma, delta, theta, xi, tau = alpha
    T = {}
    for g in [node.name for node in G.traverse("preorder")]:
        if g in sigma:
            g_value = ['S']
        elif g in theta:
            g_value = ['T']
        elif g in delta:
            g_value = ['D']
        else:
            g_value = ['C']

        for g_child in [node.name for node in G.search_nodes(name=g)[0].children]:
            if g in sigma:
                dist = 0 if M[g] == M[g_child] else int(S.get_distance(M[g], M[g_child]))
                pa = M[g]
            elif g in theta and (g, g_child) in xi:
                dist = 1 if tau[g] == M[g_child] else int(S.get_distance(tau[g], M[g_child])) + 1
                pa = tau[g]
            else:
                dist = 1 if M[g] == M[g_child] else int(S.get_distance(M[g], M[g_child])) + 1
                pa = M[g]

            x = M[g_child]
            if x == pa or S.search_nodes(name=x)[0] in S.search_nodes(name=pa)[0].get_descendants():
                for _ in range(dist - 1):
                    T[(g_child, S.search_nodes(name=x)[0].up.name)] = ['L', (g_child, x), (None, None)]
                    x = S.search_nodes(name=x)[0].up.name
                g_value.append((g_child, x))
            else:
                for _ in range(dist - 1):
                    next_node = [node.name for node in S.search_nodes(name=x)[0].children
                                 if S.search_nodes(name=pa)[0] in S.search_nodes(name=node.name)[0].get_descendants()
                                 or pa == node.name]
                    T[(g_child, next_node[0])] = ['L', (g_child, x), (None, None)]
                    x = next_node[0]
                g_value.append((g_child, x))

        if len(g_value) == 1:
            g_value += [(None, None), (None, None)]
        T[(g, M[g])] = g_value

    return T


def pull_up_gene_node(G, S, alpha, g):
    L, M, sigma, delta, theta, xi, tau = alpha

    if g in sigma:
        sigma.remove(g)
        delta.append(g)
    elif g in delta:
        M[g] = S.search_nodes(name=M[g])[0].up.name
    elif g in theta:
        M[g] = S.search_nodes(name=M[g])[0].up.name
        if S.get_common_ancestor(M[g], tau[g]).name == M[g] and M[g] != tau[g]:
            theta.remove(g)
            delta.append(g)
            g1, g2 = G.search_nodes(name=g)[0].children
            if (g, g1.name) in xi:
                xi.remove((g, g1.name))
            else:
                xi.remove((g, g2.name))
            del tau[g]

    return alpha


def explore(F, visited, g, source):
    visited[g] = True
    for node in F[g]:
        if node is not None:  # note that a leaf in F has children list [None], not []
            if node == source:
                return True
            if node not in visited:
                if explore(F, visited, node, source):
                    return True
    return False


def is_cycle(F, g):
    return explore(F, {}, g, g)


def find_first_cycle(G, G_dict, S, S_dict, alpha):
    L, M, sigma, delta, theta, xi, tau = alpha
    T = dtl_to_recon_tree(S, G, alpha)
    F = buildReconciliation(S_dict, G_dict, T)

    post_order_S = [node.name for node in S.traverse("postorder")]
    nodes = sorted([node.name for node in G.search_nodes() if node not in G.search_nodes(children=[])],
                   key=lambda g: post_order_S.index(M[g]))

    for g in nodes:
        if is_cycle(F, g):
            return g

    return None


def temporal_consistency_fixer(G, G_dict, S, S_dict, alpha):
    g = find_first_cycle(G, G_dict, S, S_dict, alpha)
    i = 0
    while g is not None:
        i += 1
        alpha = pull_up_gene_node(G, S, alpha, g)
        g = find_first_cycle(G, G_dict, S, S_dict, alpha)
    return alpha, i


def out(S, G, alpha, outFile):
    T = dtl_to_recon_tree(S, G, alpha)
    d, s, t, l = 0, 0, 0, 0
    for key in T.keys():
        if T[key][0] == 'D':
            d += 1
        elif T[key][0] == 'S':
            s += 1
        elif T[key][0] == 'T':
            t += 1
        elif T[key][0] == 'L':
            l += 1

    print "D:", d, "S:", s, "T:", t, "L:", l, "total:", d * dVal + t * tVal + l * lVal
    outFile.write("D: {0} S: {1} T: {2} L: {3} total: {4}\n".format(str(d),
                                                                    str(s),
                                                                    str(t),
                                                                    str(l),
                                                                    str(d * dVal + t * tVal + l * lVal)))

    return d * dVal + t * tVal + l * lVal


def preprocess(st):
    while st.find(":") != -1:
        i = st.find(":")
        j = i + 1
        while st[j] not in [";", ",", ")"] :
            j += 1
        st = st[:i] + st[j:]
    return st


def eteTreeReader(fileName):
    """Takes a fileName as input and returns the hostTree and parasiteTree in ETE Tree format.
    """
    fileHandle = open(fileName, 'r')
    contents = fileHandle.read()
    fileHandle.close()

    hostString, parasiteString, phiString = contents.split(";")
    hostString = hostString.strip()
    parasiteString = parasiteString.strip()
    hostString += ";"
    parasiteString += ";"

    hostString = preprocess(hostString)
    parasiteString = preprocess(parasiteString)

    hostTree = Tree(hostString, format=8)
    parasiteTree = Tree(parasiteString, format=8)

    return hostTree, parasiteTree


def main():

    if not os.path.exists("fixerOut"):
        os.mkdir("fixerOut")

    for i in xrange(fileNum):

        index = str(i + 1)
        for j in xrange(4 - len(str(i + 1))):
            index = "0" + index

        fileName = "real-100taxa/COG" + index + ".newick"
        if not os.path.isfile(fileName):
            continue

        outFile = open("fixerOut/COG" + index + ".txt", 'w')

        print fileName[13:]
        outFile.write(fileName[13:] + "\n")

        S_dict, G_dict, _ = newickFormatReader.getInput(fileName)
        S, G = eteTreeReader(fileName)
        recs, allRecs = MasterReconciliation.Reconcile(["", fileName, str(dVal), str(tVal), str(lVal), "unit", "0", "1", "0", "1"])

        totRecs = len(allRecs)

        print "# of Infeasible Reconciliations: {0}".format(len(recs))
        outFile.write("# of Reconciliations: {0}\n".format(totRecs))
        outFile.write("# of Infeasible Reconciliations: {0}\n".format(len(recs)))

        min_cost = None

        for T in recs:
            alpha = recon_tree_to_dtl(T)
            out(S, G, alpha, outFile)
            alpha, pull_up = temporal_consistency_fixer(G, G_dict, S, S_dict, alpha)
            cost = out(S, G, alpha, outFile)
            if min_cost is None or cost < min_cost:
                min_cost = cost
            print "number of operations: {0}".format(pull_up)
            outFile.write("number of operations: {0}\n".format(pull_up))

        print "min total:", min_cost
        outFile.write("min total: " + str(min_cost) + "\n")

        outFile.close()


if __name__ == "__main__" :
   main()
