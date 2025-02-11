import os
import networkx as nx
from collections.abc import Iterator

def graph6_file_iterator(Input_file_path:str) -> Iterator[nx.Graph]:
    '''
        This function yields, one by one, the graphs in the provided file without generating the entire list in memory
    '''

    with open(Input_file_path, 'rb') as in_file:
        for line in in_file:
            yield nx.from_graph6_bytes(line.strip())

def directory_g6_iterator(Input_directory:str) -> Iterator[nx.Graph]:
    '''
        This function yields, one by one, the graphs in each of the files in the provided directory without generating the entire list of graphs in memory
    '''

    for dir_entry in (dir_entry for dir_entry in os.scandir(Input_directory) if dir_entry.is_file and dir_entry.name.endswith('.g6')):
        yield from graph6_file_iterator(dir_entry.path)