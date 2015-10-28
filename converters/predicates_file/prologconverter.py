from predicates_file.converters import PredicateFileConverter


class PredicatesFile2PrologConverter(PredicateFileConverter):
    def __init__(self):
        self.facts = []
        self._id2cls = {}
        self._type_defs = {}  # instance --> classes (set)

    def _add_type_def(self, inst, cls_id):
        cls = self._id2cls[cls_id]

        if self._type_defs.get(inst) is None:
            self._type_defs[inst] = set()

        self._type_defs[inst].add(cls)

    def _build_fact(self, predicate, arguments):
        args = []

        for arg in arguments:
            tmp = arg.split(':')
            a = tmp[0]
            args.append(a)

            if len(tmp) > 1:
                self._add_type_def(a, tmp[1])

        fact = predicate + '('
        fact += ','.join(args)
        fact += ').'

        return fact

    def convert_predicate(self, predicate, arguments):
        self.facts.append(self._build_fact(predicate, arguments))

    def register_class_mapping(self, id2cls):
        self._id2cls = id2cls

    def finalize(self):
        for inst, clss in self._type_defs.items():
            for cls in clss:
                self.facts.append(self._build_fact(cls, inst))

    def write_results_to_file(self, out_file_path):
        with open(out_file_path, 'w') as f:
            for rule in self.facts:
                f.write(str(rule))
                f.write('\n')