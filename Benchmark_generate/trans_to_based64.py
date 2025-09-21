import networkx as nx
import io
import base64
from PIL import Image
from graphviz import Digraph, Graph
import subprocess  # 用于执行graphviz命令
import random


def generate_unique_colors(count):
    colors = set()
    while len(colors) < count:
        # 生成RGB各分量（0-255）
        r = random.randint(30, 150)
        g = random.randint(30, 150)
        b = random.randint(30, 150)
        # 转换为十六进制格式
        color = f"#{r:02x}{g:02x}{b:02x}"
        colors.add(color)
    return list(colors)
edge_colors = generate_unique_colors(60)


def graph_to_base64(G, node_number, graph_type):
    # 根据图类型选择有向图或无向图
    if graph_type.startswith("directed"):
        dot = Digraph()
    else:
        dot = Graph()

    # 设置图形属性
    dot.attr(overlap='false')

    # 设置节点样式
    dot.attr('node', shape='circle', style='filled', color='lightblue',
             fontsize='16', width='0.6', height='0.6', fixedsize='true',margin='0')

#default:    dot.attr('node', shape='circle', style='filled', color='lightblue',
#            fontsize='16', width='0.6', height='0.6')

# default:    for tiny, fontsize=12,width=0.15,height=0.15, for small, fontsize=14,width==0.3,height=0.3, for big, fontsize=18,width=0.9,height=0.9
#

    edge_size=1
    weight_size=14

#default edge_size=1,weight_size=14
#thick1: edge_size=0.5, weight_size=14
#thick2: edge_size=2, weight_size=15
#thick3: edge_size=3, weight_size=16


    # 添加节点
    for node in G.nodes():
        dot.node(str(node))

    # 添加边   red blue green mixed
    if graph_type.endswith("unweighted"):
        for u, v in G.edges():
            dot.edge(str(u), str(v),penwidth=str(edge_size),color=random.choice(edge_colors))
    else:
        edge_labels = nx.get_edge_attributes(G, 'weight')
        for (u, v), weight in edge_labels.items():
            dot.edge(str(u), str(v), label=str(weight), penwidth=str(edge_size), fontcolor='red', fontsize=str(weight_size),overlap='false',color=random.choice(edge_colors))
    dot.attr(size='10')
    dot.attr(dpi='200!')

    buffer = io.BytesIO()
    dot_source = dot.source.encode('utf-8')

    # default: dot
    # 1:neato  2: twopi  3: circo

    cmd = ['dot', '-Tpng']
    try:
        # 执行命令并将输出写入缓冲区
        result = subprocess.run(
            cmd,
            input=dot_source,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        # 将命令输出写入缓冲区
        buffer.write(result.stdout)
        buffer.seek(0)

        # 转换为base64
        img = Image.open(buffer)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='png')
        img_byte_arr = img_byte_arr.getvalue()
        base64_str = base64.b64encode(img_byte_arr).decode('utf-8')

        return f"data:image/png;base64,{base64_str}"

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Graphviz渲染失败: {e.stderr.decode('utf-8')}")
    finally:
        buffer.close()