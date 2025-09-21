import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
from string import ascii_uppercase
import networkx as nx
import random

def generate_undirected_unweighted_graph(node_number, edge_probability):
    G = None
    # 循环生成直到图中至少有一条边
    while G is None or G.number_of_edges() == 0:
        G = nx.erdos_renyi_graph(
            n=node_number,
            p=edge_probability,
            directed=False,
            seed=None
        )

    letters = list(ascii_uppercase)  # ['A', 'B', ..., 'Z']
    random.shuffle(letters)
    selected_letters = letters[:node_number]  # 选取前N个字母
    node_list = list(G.nodes())
    name_mapping = {node: selected_letters[i] for i, node in enumerate(node_list)}
    G_renamed = nx.relabel_nodes(G, name_mapping, copy=True)
    return G_renamed


def generate_directed_unweighted_graph(node_number, edge_probability):
    G = None
    # 循环生成直到图中至少有一条边
    while G is None or G.number_of_edges() == 0:
        G = nx.DiGraph()
        G.add_nodes_from(range(node_number))
        for i in range(node_number):
            for j in range(i + 1, node_number):
                if random.random() < edge_probability:
                    if random.random() < 0.5:
                        G.add_edge(i, j)
                    else:
                        G.add_edge(j, i)
    letters = list(ascii_uppercase)  # ['A', 'B', ..., 'Z']
    random.shuffle(letters)
    selected_letters = letters[:node_number]  # 选取前N个字母
    node_list = list(G.nodes())
    name_mapping = {node: selected_letters[i] for i, node in enumerate(node_list)}
    G_renamed = nx.relabel_nodes(G, name_mapping, copy=True)
    return G_renamed


def generate_undirected_weighted_graph(node_number, edge_probability):
    G = None
    # 循环生成直到图中至少有一条边
    while G is None or G.number_of_edges() == 0:
        G = nx.erdos_renyi_graph(
            n=node_number,
            p=edge_probability,
            directed=False,
            seed=None
        )
        # 为边添加权重
        for u, v in G.edges():
            G.edges[u, v]['weight'] = random.randint(1, 5)

    letters = list(ascii_uppercase)  # ['A', 'B', ..., 'Z']
    random.shuffle(letters)
    selected_letters = letters[:node_number]  # 选取前N个字母
    node_list = list(G.nodes())
    name_mapping = {node: selected_letters[i] for i, node in enumerate(node_list)}
    G_renamed = nx.relabel_nodes(G, name_mapping, copy=True)
    return G_renamed


def generate_directed_weighted_graph(node_number, edge_probability):
    G = None
    # 循环生成直到图中至少有一条边
    while G is None or G.number_of_edges() == 0:
        G = nx.DiGraph()
        G.add_nodes_from(range(node_number))
        for i in range(node_number):
            for j in range(i + 1, node_number):
                if random.random() < edge_probability:
                    if random.random() < 0.5:
                        G.add_edge(i, j, weight=random.randint(1, 5))
                    else:
                        G.add_edge(j, i, weight=random.randint(1, 5))

    letters = list(ascii_uppercase)
    random.shuffle(letters)
    selected_letters = letters[:node_number]  # 选取前N个字母
    node_list = list(G.nodes())
    name_mapping = {node: selected_letters[i] for i, node in enumerate(node_list)}
    G_renamed = nx.relabel_nodes(G, name_mapping, copy=True)
    return G_renamed


def generate_graph(type,node_number,edge_probability=0.2):
    if type == 'undirected_unweighted':
        return generate_undirected_unweighted_graph(node_number, edge_probability)
    elif type == 'undirected_weighted':
        return generate_undirected_weighted_graph(node_number, edge_probability)
    elif type == 'directed_unweighted':
        return generate_directed_unweighted_graph(node_number, edge_probability)
    elif type == 'directed_weighted':
        return generate_directed_weighted_graph(node_number, edge_probability)
    else:
        return None

