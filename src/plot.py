import networkx as nx
from map import get_edges_nodes


def plot_graph(G, labels):
    """
    Plot a graph
    :param G:
    :param labels:
    :return:
    """
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(150,150))
    fig.set_dpi=300
    pos = nx.spring_layout(G, k=1/5, iterations=100)
    nx.draw_networkx_nodes(G, pos=pos, ax=ax, alpha=0.5)
    nx.draw_networkx_edges(G, pos=pos, ax=ax, width=0.5, alpha=0.3)
    nx.draw_networkx_labels(G, pos=pos, labels=labels, font_size=6)
    plt.savefig("lanaja_map.png")


if __name__ == "__main__":
    nodes, edges = get_edges_nodes()

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)