
import os
import networkx as nx
import matplotlib.pyplot as plt
from source import graph_utilities as utilities

def test_load_tikz():
    file_path = os.path.join(os.path.dirname(__file__), 'test_files', 'example.tikz')
    graph, layout = utilities.load_tikz(file_path)
    # nx.draw(graph, pos=layout, with_labels=True)
    # plt.show()
    print(graph)
    return

def test_graph6_file_iterator():
    file_path = os.path.join(os.path.dirname(__file__), 'test_files', 'ZimGraph.g6')
    graphs = [graph for graph in utilities.graph6_file_iterator(file_path)]
    for graph in graphs:
        # nx.draw_kamada_kawai(graph, with_labels=True)
        # plt.show()
        print(graph)
    return

def test_directory_g6_iterator():
    file_path = os.path.join(os.path.dirname(__file__), 'test_files')
    graphs = [graph for graph in utilities.directory_g6_iterator(file_path)]
    for graph in graphs:
        # nx.draw_kamada_kawai(graph, with_labels=True)
        # plt.show()
        print(graph)
    return

def test_subdivide_edge():
    graph_1 = nx.cycle_graph(4)
    graph_2 = nx.cycle_graph(6)
    graph_3 = utilities.subdivide_edge(graph_1, [edge for edge in graph_1.edges()][0], 2)
    print(nx.is_isomorphic(graph_2, graph_3))
    return

def main_test():
    print('Testing loading tikz. The output should be: Graph with 4 nodes and 2 edges.')
    test_load_tikz()
    print('Testing loading graph6 file. The output should be: Graph with 11 nodes and 15 edges.')
    test_graph6_file_iterator()
    print('Testing loading tikz. The output should be: Graph with 7 nodes and 7 edges and Graph with 11 nodes and 15 edges.')
    test_directory_g6_iterator()
    print('Testing loading tikz. The output should be: True.')
    test_subdivide_edge()
    pass

if __name__ == '__main__':
    main_test()