_file_suffix_to_serialization = {
    'ttl': 'turtle',
    'xml': 'xml',
    'rdf': 'xml',
    'n3': 'n3',
    'nt': 'nt'
}


def write_graph(graph, output_file_path):
    """
    :param graph: an rdflib.Graph object
    :param output_file_path: a string representing the output file path
    """
    file_suffix = output_file_path.rsplit('.', 1)[-1]

    serialization = _file_suffix_to_serialization.get(file_suffix)

    if serialization is None:
        graph.serialize(output_file_path)
    else:
        graph.serialize(output_file_path, serialization)
