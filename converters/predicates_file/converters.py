class PredicateFileConverter(object):
    """Interface class"""

    def convert_predicate(self, predicate, arguments):
        raise NotImplementedError()

    def register_class_mapping(self, id2cls):
        raise NotImplementedError()

    def finalize(self):
        raise NotImplementedError()

    def write_results_to_file(self, out_file_path):
        raise NotImplementedError()