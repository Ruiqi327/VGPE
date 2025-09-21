import networkx as nx
import random
from string import ascii_uppercase

def node_qa(G):
    letters = list(ascii_uppercase)  # ['A', 'B', ..., 'Z']
    index=random.choice(letters)
    answer=["Yes"] if G.has_node(index) else ["No"]
    return [["Please answer the following question only with Yes or No, do not add any other words. Does Node " + str(index) + " exist in this graph?"], answer]

def direct_qa(G,graph_type):
    answer = ["No"] if graph_type == "undirected_unweighted" or graph_type=="undirected_weighted" else ["Yes"]
    return [["Please answer the following question only with Yes or No, do not add any other words. Is this graph directed?"], answer]

def weight_qa(G, graph_type):
    answer=["No"] if graph_type=="undirected_unweighted" or graph_type=="directed_unweighted" else ["Yes"]
    return [["Please answer the following question only with Yes or No, do not add any other words. Is this graph weighted?"],answer]

def edge_qa(G):
    nodes=list(G.nodes())
    edges = list(G.edges())  # 获取所有边
    has_edges = len(edges) > 0
    if has_edges and random.random() < 0.5:
        index1, index2 = random.choice(edges)
    else:
        index1, index2 = random.sample(nodes, 2)

    has_edge = G.has_edge(index1, index2) or G.has_edge(index2, index1)
    answer = ["Yes"] if has_edge else ["No"]
    question = ["Please answer the following question only with Yes or No, do not add any other words. Without distinguishing the direction of edges, is there an edge between Node " +
        str(index1) + " and Node " + str(index2) + "?"]
    return [question, answer]


def degree_qa(G):
    count = G.number_of_nodes()
    nodes=list(G.nodes())
    index = random.choice(nodes)
    answer = str(G.degree(index))
    return [["Please answer the following question with only one number, do not add any other words. Without distinguishing the direction of edges, how many edges are associated with Node " + str(index) + "?"], [answer]]

def point_qa(G):
    edges = list(G.edges())
    original_u, original_v = random.choice(edges)
    if random.choice([True, False]):
        index1, index2 = original_v, original_u
    else:
        index1, index2 = original_u, original_v
    answer = ["Yes"] if G.has_edge(index1, index2) else ["No"]
    return [["Regardless of direction, please check if there is any edge between Node "+str(index1)+" and Node "+str(index2)+", if you don't see any edge between them, please only answer 0. If there is an edge, then answer Yes if Node "+str(index1)+" points to Node "+str(index2)+", otherwise answer No. Do not add any other words"],answer]

def query_weight_qa(G):
    edges = list(G.edges())
    index1,index2 = random.choice(edges)
    edge_data = G.get_edge_data(index1, index2)
    if edge_data is not None:
        answer = str(edge_data['weight'])
    else:
        answer = str(0)
    return [["Please answer the following question with only one number, do not add any other words. Without distinguishing the direction of edges, what is the weight of the edge connecting Node "+str(index1)+" with Node "+str(index2)+"? If you don't see any edge between them, please only answer 0."],[answer]]

def generate_qa(graph_type,G):
    if graph_type == "undirected_unweighted":
        return [node_qa(G),
                direct_qa(G,graph_type),
                weight_qa(G,graph_type),
                degree_qa(G),
                degree_qa(G),
                edge_qa(G),
                edge_qa(G),
                node_qa(G),
                edge_qa(G),
                node_qa(G)]

    elif graph_type == "undirected_weighted":
        return [node_qa(G),
                direct_qa(G,graph_type),
                weight_qa(G,graph_type),
                degree_qa(G),
                degree_qa(G),
                query_weight_qa(G),
                query_weight_qa(G),
                edge_qa(G),
                edge_qa(G),
                node_qa(G),
                edge_qa(G),
                node_qa(G),
                query_weight_qa(G)]


    elif graph_type == "directed_unweighted":
        return [node_qa(G),
                direct_qa(G,graph_type),
                weight_qa(G,graph_type),
                degree_qa(G),
                degree_qa(G),
                point_qa(G),
                point_qa(G),
                edge_qa(G),
                edge_qa(G),
                node_qa(G),
                edge_qa(G),
                node_qa(G),
                point_qa(G)]
    else:
        return [node_qa(G),
                direct_qa(G,graph_type),
                weight_qa(G,graph_type),
                degree_qa(G),
                degree_qa(G),
                query_weight_qa(G),
                query_weight_qa(G),
                point_qa(G),
                point_qa(G),
                edge_qa(G),
                edge_qa(G),
                node_qa(G),
                edge_qa(G),
                node_qa(G),
                point_qa(G),
                query_weight_qa(G)]