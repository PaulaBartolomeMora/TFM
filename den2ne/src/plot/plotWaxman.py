#!/usr/bin/python3

import networkx as nx
import matplotlib.pyplot as plt


G = nx.waxman_graph(20, beta=0.8, alpha=0.6, L=None,
                    domain=(0, 0, 1, 1), metric=None, seed=None)
pos = nx.kamada_kawai_layout(G)
d = dict(G.degree)
nx.draw(G, pos=pos, node_color='#93edc0', with_labels=True,
        nodelist=d, node_size=[d[k]*300 for k in d])
plt.show()
