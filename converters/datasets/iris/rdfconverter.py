from rdflib import Graph
from rdflib import Literal
from rdflib import OWL
from rdflib import RDF
from rdflib import RDFS
from rdflib import URIRef
from rdflib import XSD

from utils import write_graph

a = RDF.term('type')
rdfs_domain = RDFS.term('domain')
rdfs_range = RDFS.term('range')
rdfs_subClassOf = RDFS.term('subClassOf')
xsd_double = XSD.term('double')
owl_Class = OWL.term('Class')
owl_DatatypeProperty = OWL.term('DatatypeProperty')
owl_FunctionalProperty = OWL.term('FunctionalProperty')


class Iris2RDFConverter(object):
    """
    Attribute Information:

    1. sepal length in cm
    2. sepal width in cm
    3. petal length in cm
    4. petal width in cm
    5. class:
    -- Iris Setosa
    -- Iris Versicolour
    -- Iris Virginica

    [https://archive.ics.uci.edu/ml/datasets/Iris]
    """

    def __init__(self):
        self._g = Graph()
        self._res_cntr = 1
        self._res_pattern = 'res%03i'
        self._res_prefix = 'http://dl-learner.org/iris/'
        self._ont_prefix = 'http://dl-learner.org/iris/ont/'
        self._p0 = URIRef(self._ont_prefix + 'sepalLength')
        self._p1 = URIRef(self._ont_prefix + 'sepalWidth')
        self._p2 = URIRef(self._ont_prefix + 'petalLength')
        self._p3 = URIRef(self._ont_prefix + 'petalWidth')
        self._cls_setosa = URIRef(self._ont_prefix + 'IrisSetosa')
        self._cls_versicolor = URIRef(self._ont_prefix + 'IrisVersicolor')
        self._cls_virginica = URIRef(self._ont_prefix + 'IrisVirginica')

        self._clsid2cls = {
            'Iris-setosa': self._cls_setosa,
            'Iris-versicolor': self._cls_versicolor,
            'Iris-virginica': self._cls_virginica
        }

    def _get_next_res(self):
        iri_str = self._res_prefix + self._res_pattern % self._res_cntr
        self._res_cntr += 1
        return URIRef(iri_str)

    def add_ont_defs(self):
        sup_cls = URIRef(self._ont_prefix + 'Iris')

        for c in [self._cls_setosa, self._cls_versicolor, self._cls_virginica]:
            self._g.add((c, a, owl_Class))
            self._g.add((c, rdfs_subClassOf, sup_cls))

        for p in [self._p0, self._p1, self._p2, self._p3]:
            self._g.add((p, a, owl_DatatypeProperty))
            self._g.add((p, a, owl_FunctionalProperty))
            self._g.add((p, rdfs_domain, sup_cls))
            self._g.add((p, rdfs_range, xsd_double))

    def convert(self, input_file_path, output_file_path):
        self.add_ont_defs()

        with open(input_file_path) as f:
            for line in f:
                res = self._get_next_res()
                parts = line.strip().split(',')

                if len(parts) == 1:
                    continue

                # 1. sepal length in cm
                l0 = Literal(parts[0], None, xsd_double)
                self._g.add((res, self._p0, l0))

                # 2. sepal width in cm
                l1 = Literal(parts[1], None, xsd_double)
                self._g.add((res, self._p1, l1))

                # 3. petal length in cm
                l2 = Literal(parts[2], None, xsd_double)
                self._g.add((res, self._p2, l2))

                # 4. petal width in cm
                l3 = Literal(parts[3], None, xsd_double)
                self._g.add((res, self._p3, l3))

                # 5. class
                self._g.add((res, a, self._clsid2cls[parts[4]]))

        write_graph(self._g, output_file_path)
