import networkx as nx

def subdivide_edge(Input_graph:nx.Graph, Input_edge:tuple, Input_number_of_nodes_to_add:int) -> nx.Graph:
    '''
        this function returns a new graph with the indicated edge subdivided the indicated number of times
    '''
    if Input_number_of_nodes_to_add <= 0:
        return Input_graph.copy()
    if Input_edge not in Input_graph.edges:
        assert LookupError('The provided edge does not exist in the provided graph')
    output_graph = Input_graph.copy()
    
    # remove the input edge
    output_graph.remove_edge(*Input_edge)
    
    # determine node labels that can be used for the new nodes
    integer_node_labels = set()
    next_node_label = 1
    for node in output_graph.nodes:
        try:
            integer_node_labels.add(int(node))
        except:
            pass
    added_nodes = list()
    for _ in range(Input_number_of_nodes_to_add):
        while next_node_label in integer_node_labels:
            next_node_label += 1
        integer_node_labels.add(next_node_label)
        added_nodes.append(next_node_label)
        
    # add the node labels as a path
    output_graph.add_edges_from(nx.path_graph(added_nodes).edges)
    
    # connect the ends of the added path to the endpoints of the input edge
    output_graph.add_edge(added_nodes[0], Input_edge[0])
    output_graph.add_edge(added_nodes[-1], Input_edge[-1])
    
    return output_graph