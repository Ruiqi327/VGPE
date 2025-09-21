import networkx as nx

def generate_caption(G, graph_type):
    adj_matrix = nx.adjacency_matrix(G).todense()
    node_count = len(G.nodes)
    nodes=list(G.nodes())
    descriptions = ["We now describe a graph node by node. Each node's connections will be introduced independently, and there exists AT MOST one edge between any two nodes.\n"]

    if graph_type == "undirected_unweighted":
        for i in range(node_count):
            neighbors = []
            for j in range(node_count):
                if i != j and adj_matrix[i, j] != 0:  # 移除 i<j 条件
                    neighbors.append(f"Node {nodes[j]}")
            if not neighbors:
                desc = f"Node {nodes[i]} has no connections, without weights or directions.\n"
            elif len(neighbors) == 1:
                desc = f"Node {nodes[i]} is connected to {neighbors[0]}, without weights or directions.\n"
            elif len(neighbors) == 2:
                desc = f"Node {nodes[i]} is connected to {neighbors[0]} and {neighbors[1]}, without weights or directions.\n"
            else:
                last_neighbor = neighbors.pop()
                neighbors_str = ", ".join(neighbors)
                desc = f"Node {nodes[i]} is connected to {neighbors_str}, and {last_neighbor}, without weights or directions.\n"
            descriptions.append(desc)
        return descriptions

    elif graph_type == "undirected_weighted":
        for i in range(node_count):
            connections = []
            for j in range(node_count):
                if i != j and adj_matrix[i, j] != 0:  # 移除 i<j 条件
                    weight_val = adj_matrix[i, j]
                    connections.append(f"Node {nodes[j]} with the weight of {weight_val}")
            if not connections:
                desc = f"Node {nodes[i]} has no connections, without directions.\n"
            elif len(connections) == 1:
                desc = f"Node {nodes[i]} is connected to {connections[0]}, without directions.\n"
            elif len(connections) == 2:
                desc = f"Node {nodes[i]} is connected to {connections[0]} and {connections[1]}, without directions.\n"
            else:
                last_connection = connections.pop()
                connections_str = ", ".join(connections)
                desc = f"Node {nodes[i]} is connected to {connections_str}, and {last_connection}, without directions.\n"
            descriptions.append(desc)
        return descriptions


    elif graph_type == "directed_unweighted":
        for i in range(node_count):
            # 计算指向当前节点的节点（来源节点）
            sources = []
            for k in range(node_count):
                if k != i and adj_matrix[k, i] != 0:
                    sources.append(f"Node {nodes[k]}")
            # 生成来源节点的描述部分
            if not sources:
                source_part = f"Node {nodes[i]} is not pointed by any other nodes"
            elif len(sources) == 1:
                source_part = f"Node {nodes[i]} is pointed by {sources[0]}"
            elif len(sources) == 2:
                source_part = f"Node {nodes[i]} is pointed by {sources[0]} and {sources[1]}"
            else:
                last_source = sources.pop()
                sources_str = ", ".join(sources)
                source_part = f"Node {nodes[i]} is pointed by {sources_str}, and {last_source}"
            # 计算当前节点指向的节点（目标节点）
            targets = []
            for j in range(node_count):
                if i != j and adj_matrix[i, j] != 0:
                    targets.append(f"Node {nodes[j]}")
            # 生成目标节点的描述部分
            if not targets:
                target_part = f"points to no other nodes"
            elif len(targets) == 1:
                target_part = f"points to {targets[0]}"
            elif len(targets) == 2:
                target_part = f"points to {targets[0]} and {targets[1]}"
            else:
                last_target = targets.pop()
                targets_str = ", ".join(targets)
                target_part = f"points to {targets_str}, and {last_target}"
            desc = f"{source_part} without weights, {target_part} without weights.\n"
            descriptions.append(desc)
        return descriptions

    else:  # directed_weighted
        for i in range(node_count):
            # 计算指向当前节点的节点（来源节点）及权重
            sources = []
            for k in range(node_count):
                if k != i and adj_matrix[k, i] != 0:
                    weight_val = adj_matrix[k, i]
                    sources.append(f"Node {nodes[k]} with the weight of {weight_val}")

            # 生成来源节点的描述部分
            if not sources:
                source_part = f"Node {nodes[i]} is not pointed by any other nodes"
            elif len(sources) == 1:
                source_part = f"Node {nodes[i]} is pointed by {sources[0]}"
            elif len(sources) == 2:
                source_part = f"Node {nodes[i]} is pointed by {sources[0]} and {sources[1]}"
            else:
                last_source = sources.pop()
                sources_str = ", ".join(sources)
                source_part = f"Node {nodes[i]} is pointed by {sources_str}, and {last_source}"

            # 计算当前节点指向的节点（目标节点）及权重
            targets = []
            for j in range(node_count):
                if i != j and adj_matrix[i, j] != 0:
                    weight_val = adj_matrix[i, j]
                    targets.append(f"Node {nodes[j]} with the weight of {weight_val}")
            # 生成目标节点的描述部分
            if not targets:
                target_part = f"points to no other nodes"
            elif len(targets) == 1:
                target_part = f"points to {targets[0]}"
            elif len(targets) == 2:
                target_part = f"points to {targets[0]} and {targets[1]}"
            else:
                last_target = targets.pop()
                targets_str = ", ".join(targets)
                target_part = f"points to {targets_str}, and {last_target}"
            # 组合两部分描述
            desc = f"{source_part}, {target_part}.\n"
            descriptions.append(desc)
        return descriptions