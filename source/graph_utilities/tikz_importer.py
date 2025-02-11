import re
import os

import networkx as nx

def load_tikz(Input_path:str) -> tuple[nx.Graph, dict]:
    '''
    This function generates a networkx graph from the provided input path.

    Args:
        Input_path (str): The path to the input .tikz file containing the graph description.

    Returns:
        (nx.Graph, dict): the networkx graph created from the input along with a dictionary with the node positions used in plotting the graph

    Raises:
        FileNotFoundError: If the provided input path does not exist.
        ValueError: If the provided file is not a .tikz file or if labeled vertices are not uniquely named.

    Example:
        graph, layout = load_graph('path_to_file.tikz')
    '''
    if not os.path.exists(Input_path):
        raise FileNotFoundError('Provided input path does not exist')
    if not Input_path.endswith('.tikz'):
        raise ValueError('Provided file must be a .tikz file')

    with open(Input_path, 'r') as in_file:
        file_content = in_file.read()

    # Regular expression patterns
    #     \node [style=#1] (#2) at (#3,#4) {#5};
    vertex_pattern = r'\\node\s+\[style=([^\]]+)\]\s+\(([\d]+)\)\s+at\s+\(([-\d.]+),\s+([-\d.]+)\)\s+\{(\w*)\};'
    #     \draw [style=#1] (#2) to (#3);
    styled_edge_pattern = r'\\draw\s+\[style=([^\]]+)\]\s+\((\w+)\)\s+to\s+\((\w+)\);'
    #     \draw (#1.center) to (#2.center);
    empty_edge_pattern = r'\\draw\s+\((\d+)\.center\)\s+to\s+\((\d+)\.center\);'

    # Extract node information
    vertices = re.findall(vertex_pattern, file_content)
    styled_edges = re.findall(styled_edge_pattern, file_content)
    empty_edges = re.findall(empty_edge_pattern, file_content)

    # Ensure unique node labels
    if len([vertex[4] for vertex in vertices if vertex[4] != '']) != len(set([vertex[4] for vertex in vertices if vertex[4] != ''])):
        raise ValueError('All labeled vertices must be uniquely named')

    # Make the nodes in the graph
    graph = nx.Graph()
    for node_style, node_id, x_coordinate, y_coordinate, node_label in vertices:
        node_attributes = {"node_style": node_style, "x_coordinate":float(x_coordinate), "y_coordinate":float(y_coordinate), "node_label":node_label}
        graph.add_node(node_id, **node_attributes)
    
    # Populate the edges in the graph
    for edge_style, source_id, target_id in styled_edges:
        edge_attributes = {"edge_style":edge_style}
        graph.add_edge(source_id, target_id, **edge_attributes)
    for source_id, target_id in empty_edges:
        graph.add_edge(source_id, target_id)

    # Use the provided labels where possible for the graph
    relabel_dictionary = {node:label for node,label in graph.nodes.data('node_label') if label}
    desired_node_labels = set(relabel_dictionary.values())
    numeric_node_labels = set()
    for label in desired_node_labels:
        try:
            numeric_node_labels.add(int(label))
        except ValueError:
            pass
    next_node_label = 1
    for node in graph:
        if node in relabel_dictionary:
            continue
        else:
            while next_node_label in numeric_node_labels:
                next_node_label += 1
            numeric_node_labels.add(next_node_label)
            relabel_dictionary[node] = str(next_node_label)
    graph = nx.relabel_nodes(graph, relabel_dictionary, copy=True)

    # extract out the x and y coordinates to generate the layout
    layout = {node:(data['x_coordinate'],data['y_coordinate']) for node, data in graph.nodes.data()}

    return graph, layout