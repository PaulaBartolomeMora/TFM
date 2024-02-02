#!/usr/bin/python3

import networkx as nx
import matplotlib.pyplot as plt


G = nx.barabasi_albert_graph(20, 5)
pos = nx.kamada_kawai_layout(G)
d = dict(G.degree)
nx.draw(G, pos=pos, node_color='#93edc0', with_labels=True, alpha=0.9,
        nodelist=d, node_size=[d[k]*300 for k in d])
plt.show()
