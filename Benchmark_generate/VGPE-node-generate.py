import networkx as nx
import matplotlib.pyplot as plt
import random
import os
import shutil
import io
import base64
import json
from PIL import Image
from question_answer_pair import generate_qa

from GraphEngine import generate_graph
from trans_to_based64 import graph_to_base64
#def    graph_to_base64(G,algorithm,node_number)->return base64_str
from caption import generate_caption
#def    generate_caption(G, direct, weight)->return descriptions


root_dir = " "
graph_parent = " "
subfolders = ["Graph_level1", "Graph_level2", "Graph_level3"]

#各种图的总数
atom_number=30
layout_number=1
type_number=4
level_number=3

#分配字典
level_node=[14,14,14]
level_edge=[0.25,0.25,0.25]
type_dic=["undirected_unweighted","undirected_weighted","directed_unweighted","directed_weighted"]

# 生成随机图并保存为JSON
for level in range(2,3):
    count_graph = 0
    for graph_type in range(type_number):
        for layout in range(layout_number):
            for atom in range(atom_number):
                count_graph += 1
                graph_node_number=level_node[level]+random.randint(-3,3)
                G = generate_graph(type_dic[graph_type], graph_node_number, level_edge[level])
                graph_base64_code = graph_to_base64(G, graph_node_number,type_dic[graph_type])
                graph_desc = generate_caption(G, type_dic[graph_type])
                graph_qa= generate_qa(type_dic[graph_type], G)
                if type_dic[graph_type]=="undirected_unweighted":
                    json_data = {
                        "pic_base64": graph_base64_code,
                        "pic_desc": ' '.join(graph_desc),
                        "node_question1": graph_qa[0][0][0],
                        "node_answer1": graph_qa[0][1][0],
                        "direct_question": graph_qa[1][0][0],
                        "direct_answer": graph_qa[1][1][0],
                        "weight_question": graph_qa[2][0][0],
                        "weight_answer": graph_qa[2][1][0],
                        "edge_question1": graph_qa[5][0][0],
                        "edge_answer1": graph_qa[5][1][0],
                        "edge_question2": graph_qa[6][0][0],
                        "edge_answer2": graph_qa[6][1][0],
                        "node_question2": graph_qa[7][0][0],
                        "node_answer2": graph_qa[7][1][0],
                        "edge_question3": graph_qa[8][0][0],
                        "edge_answer3": graph_qa[8][1][0],
                        "node_question3": graph_qa[9][0][0],
                        "node_answer3": graph_qa[9][1][0],
                    }
                elif type_dic[graph_type]=="undirected_weighted":
                    json_data = {
                        "pic_base64": graph_base64_code,
                        "pic_desc": ' '.join(graph_desc),
                        "node_question1": graph_qa[0][0][0],
                        "node_answer1": graph_qa[0][1][0],
                        "direct_question": graph_qa[1][0][0],
                        "direct_answer": graph_qa[1][1][0],
                        "weight_question": graph_qa[2][0][0],
                        "weight_answer": graph_qa[2][1][0],
                        "query_weight1": graph_qa[5][0][0],
                        "answer_weight1": graph_qa[5][1][0],
                        "query_weight2": graph_qa[6][0][0],
                        "answer_weight2": graph_qa[6][1][0],
                        "edge_question1": graph_qa[7][0][0],
                        "edge_answer1": graph_qa[7][1][0],
                        "edge_question2": graph_qa[8][0][0],
                        "edge_answer2": graph_qa[8][1][0],
                        "node_question2": graph_qa[9][0][0],
                        "node_answer2": graph_qa[9][1][0],
                        "edge_question3": graph_qa[10][0][0],
                        "edge_answer3": graph_qa[10][1][0],
                        "node_question3": graph_qa[11][0][0],
                        "node_answer3": graph_qa[11][1][0],
                        "query_weight3": graph_qa[12][0][0],
                        "answer_weight3": graph_qa[12][1][0],
                    }

                elif type_dic[graph_type] == "directed_unweighted":
                    json_data = {
                        "pic_base64": graph_base64_code,
                        "pic_desc": ' '.join(graph_desc),
                        "node_question1": graph_qa[0][0][0],
                        "node_answer1": graph_qa[0][1][0],
                        "direct_question": graph_qa[1][0][0],
                        "direct_answer": graph_qa[1][1][0],
                        "weight_question": graph_qa[2][0][0],
                        "weight_answer": graph_qa[2][1][0],
                        "query_point1": graph_qa[5][0][0],
                        "answer_point1": graph_qa[5][1][0],
                        "query_point2": graph_qa[6][0][0],
                        "answer_point2": graph_qa[6][1][0],
                        "edge_question1": graph_qa[7][0][0],
                        "edge_answer1": graph_qa[7][1][0],
                        "edge_question2": graph_qa[8][0][0],
                        "edge_answer2": graph_qa[8][1][0],
                        "node_question2": graph_qa[9][0][0],
                        "node_answer2": graph_qa[9][1][0],
                        "edge_question3": graph_qa[10][0][0],
                        "edge_answer3": graph_qa[10][1][0],
                        "node_question3": graph_qa[11][0][0],
                        "node_answer3": graph_qa[11][1][0],
                        "query_point3": graph_qa[12][0][0],
                        "answer_point3": graph_qa[12][1][0],
                    }
                else:
                    json_data = {
                        "pic_base64": graph_base64_code,
                        "pic_desc": ' '.join(graph_desc),
                        "node_question1": graph_qa[0][0][0],
                        "node_answer1": graph_qa[0][1][0],
                        "direct_question": graph_qa[1][0][0],
                        "direct_answer": graph_qa[1][1][0],
                        "weight_question": graph_qa[2][0][0],
                        "weight_answer": graph_qa[2][1][0],
                        "query_weight1": graph_qa[5][0][0],
                        "answer_weight1": graph_qa[5][1][0],
                        "query_weight2": graph_qa[6][0][0],
                        "answer_weight2": graph_qa[6][1][0],
                        "query_point1": graph_qa[7][0][0],
                        "answer_point1": graph_qa[7][1][0],
                        "query_point2": graph_qa[8][0][0],
                        "answer_point2": graph_qa[8][1][0],
                        "edge_question1": graph_qa[9][0][0],
                        "edge_answer1": graph_qa[9][1][0],
                        "edge_question2": graph_qa[10][0][0],
                        "edge_answer2": graph_qa[10][1][0],
                        "node_question2": graph_qa[11][0][0],
                        "node_answer2": graph_qa[11][1][0],
                        "edge_question3": graph_qa[12][0][0],
                        "edge_answer3": graph_qa[12][1][0],
                        "node_question3": graph_qa[13][0][0],
                        "node_answer3": graph_qa[13][1][0],
                        "query_point3": graph_qa[14][0][0],
                        "answer_point3": graph_qa[14][1][0],
                        "query_weight3": graph_qa[15][0][0],
                        "answer_weight3": graph_qa[15][1][0],
                    }

                    # 生成文件名（四位序号，如Graph001.json）
                file_name = f"Graph{count_graph:04d}.json"
                file_path = os.path.join(graph_parent,subfolders[level], file_name)  # 完整路径

                # 保存为JSON文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=2)  # indent=2让JSON更易读

                print(f"已生成：{file_path}")
