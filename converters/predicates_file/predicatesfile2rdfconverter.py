from rdflib import BNode
from rdflib import Graph
from rdflib import OWL
from rdflib import RDF
a = RDF.term('type')
from rdflib import RDFS
from rdflib import URIRef

from predicates_file.converters import PredicateFileConverter
from predicates_file import ProgrammingError


class PredicatesFile2RDFConverter(PredicateFileConverter):
    _pred_uri_prefix = 'http://dl-learner.org/ont/p/'
    _cls_uri_prefix = 'http://dl-learner.org/ont/c/'
    _res_uri_prefix = 'http://dl-learner.org/res/'

    _file_suffix_to_serialization = {
        'ttl': 'turtle',
        'xml': 'xml',
        'rdf': 'xml',
        'n3': 'n3',
        'nt': 'nt'
    }

    def __init__(self):
        self._id2cls = {}
        self._type_defs = {}  # instance --> classes (set)
        self._predicates = set()
        self._classes = set()
        self._cls_hierarchy = {}  # cls --> subclasses (set)
        self._domains = {}  # predicate --> classes (set)
        self._ranges = {}  # predicate --> classes (set)
        self._nary_property_preds = {}  # prop --> n actual predicates (list)
        self._pred_counter = 1
        self._g = Graph()

    def _add_domain(self, predicate, cls_id):
        cls = self._id2cls[cls_id]

        if self._domains.get(predicate) is None:
            self._domains[predicate] = set()

        self._domains[predicate].add(cls)

    def _add_range(self, predicate, cls_id):
        cls = self._id2cls[cls_id]

        if self._ranges.get(predicate) is None:
            self._ranges[predicate] = set()

        self._ranges[predicate].add(cls)

    def _add_type_def(self, inst, cls_id):
        cls = self._id2cls[cls_id]

        if self._type_defs.get(inst) is None:
            self._type_defs[inst] = set()

        self._type_defs[inst].add(cls)

    def _add_sub_cls_axiom(self, sub_cls, super_cls):
        if self._cls_hierarchy.get(super_cls) is None:
            self._cls_hierarchy[super_cls] = set()

        self._cls_hierarchy[super_cls].add(sub_cls)

    def _new_p(self):
        pred = 'pred' + str(self._pred_counter)
        self._pred_counter += 1

        return pred

    def _get_predicate(self, prop, pos):
        if self._nary_property_preds.get(prop) is None:
            assert pos == 0
            self._nary_property_preds[prop] = []

        preds = self._nary_property_preds[prop]
        if len(preds) > pos:
            return preds[pos]

        elif len(preds) == pos:
            p = self._new_p()
            preds.append(p)
            return p

        else:
            raise ProgrammingError()

    def _pred_uri(self, pred):
        pred = pred[0].lower() + pred[1:]
        return URIRef(self._pred_uri_prefix + pred)

    def _cls_uri(self, cls):
        cls = cls[0].upper() + cls[1:]
        return URIRef(self._cls_uri_prefix + cls)

    def _res_uri(self, res):
        return URIRef(self._res_uri_prefix + res)

    def convert_predicate(self, predicate, arguments):
        """
        :param predicate: the predicate name
        :param arguments: a list containing the predicate arguments
        """
        if len(arguments) == 1:
            # In this case the whole predicate assignment is considered as class
            # assignment, i.e. the predicate is the class and the argument the
            # instance
            sub_cls = predicate
            self._classes.add(sub_cls)

            parts = arguments[0].split(':')
            argument = parts[0]

            if len(parts) > 1:
                cls_id = parts[1]
                self._add_type_def(argument, cls_id)
                super_cls = self._id2cls[cls_id]

                self._classes.add(super_cls)
                self._add_sub_cls_axiom(sub_cls, super_cls)

            self._g.add((self._res_uri(argument), a, self._cls_uri(sub_cls)))

        else:  # > 1
            self._predicates.add(predicate)

            if len(arguments) > 2:
                # In the case of more than 2 arguments
                # - the first argument (arg0) is considered as subject,
                # - the predicate is considered as predicate
                # - a blank node is introduced as object
                # - arg1 - argn are attached to the introduced blank node with
                #   a newly introduced predicate derived from the argument
                #   name
                parts0 = arguments[0].split(':')
                arg0 = parts0[0]
                subj = self._res_uri(arg0)

                if len(parts0) > 1:
                    self._add_type_def(arg0, parts0[1])
                    self._add_domain(predicate, parts0[1])

                args = arguments[1:]
                bnode = BNode()

                self._g.add((subj, self._pred_uri(predicate), bnode))

                for i in range(len(args)):
                    arg = args[i]
                    parts = arg.split(':')
                    argument = parts[0]

                    pred = self._get_predicate(predicate, i)
                    self._predicates.add(pred)

                    if len(parts) > 1:
                        self._add_type_def(argument, parts[1])
                        self._add_range(pred, parts[1])

                    self._g.add(
                        (bnode, self._pred_uri(pred), self._res_uri(argument)))

            else:  # exactly two arguments --> arg0 predicate arg1 .
                parts0 = arguments[0].split(':')
                arg0 = parts0[0]

                if len(parts0) > 1:
                    self._add_type_def(arg0, parts0[1])
                    self._add_domain(predicate, parts0[1])

                parts1 = arguments[1].split(':')
                arg1 = parts1[0]

                if len(parts1) > 1:
                    self._add_type_def(arg1, parts1[1])
                    self._add_range(predicate, parts1[1])

                self._predicates.add(predicate)

                self._g.add((
                    self._res_uri(arg0),
                    self._pred_uri(predicate),
                    self._res_uri(arg1)))

    def register_class_mapping(self, id2cls):
        self._id2cls = id2cls

    def finalize(self):
        """Write add type information
        pred in self._predicates --> pred a owl:ObjectProperty .
        cls in self._classes --> cls a owl:Class .
        sup, sub in self._cls_hierarchy --> sub rdfs:subClassOf sup .
        i, cls in self._type_defs --> i a cls .
        p, cls in self._domains --> p rdfs:domain cls .
        p, cls in self._ranges --> p rdfs:range cls .
        """
        owl_ObjectProperty = OWL.term('ObjectProperty')
        owl_Class = OWL.term('Class')
        owl_FunctionalProperty = OWL.term('FunctionalProperty')
        rdfs_subClassOf = RDFS.term('subClassOf')
        rdfs_domain = RDFS.term('domain')
        rdfs_range = RDFS.term('range')

        for pred in self._predicates:
            self._g.add((self._pred_uri(pred), a, owl_ObjectProperty))

        for cls in self._classes:
            self._g.add((self._cls_uri(cls), a, owl_Class))

        for super_cls, sub_clss in self._cls_hierarchy.items():
            for sub_cls in sub_clss:
                self._g.add((
                    self._cls_uri(sub_cls),
                    rdfs_subClassOf,
                    self._cls_uri(super_cls)))

        for inst, classes in self._type_defs.items():
            for cls in classes:
                self._g.add((self._res_uri(inst), a, self._cls_uri(cls)))

        for pred, clss in self._domains.items():
            for cls in clss:
                self._g.add(
                    (self._pred_uri(pred), rdfs_domain, self._cls_uri(cls)))

        for pred, clss in self._ranges.items():
            for cls in clss:
                self._g.add(
                    (self._pred_uri(pred), rdfs_range, self._cls_uri(cls)))

        for preds in self._nary_property_preds.values():
            for pred in preds:
                self._g.add((self._pred_uri(pred), a, owl_FunctionalProperty))

    def write_results_to_file(self, out_file_path):
        file_suffix = out_file_path.rsplit('.', 1)[-1]

        serialization = self._file_suffix_to_serialization.get(file_suffix)

        if serialization is None:
            self._g.serialize(out_file_path)
        else:
            self._g.serialize(out_file_path, serialization)