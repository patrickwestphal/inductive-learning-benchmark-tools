from rdflib import Graph
from rdflib import Literal
from rdflib import OWL
from rdflib import URIRef
from rdflib import RDF
from rdflib import RDFS
from rdflib import XSD

from utils import write_graph

a = RDF.type
xsd_double = XSD.term('double')
xsd_int = XSD.term('integer')


class Wine2RDFConverter(object):
    """
    The attributes are (dontated by Riccardo Leardi, riclea '@' anchem.unige.it)
    1) Alcohol
    2) Malic acid
    3) Ash
    4) Alcalinity of ash
    5) Magnesium
    6) Total phenols
    7) Flavanoids
    8) Nonflavanoid phenols
    9) Proanthocyanins
    10)Color intensity
    11)Hue
    12)OD280/OD315 of diluted wines
    13)Proline

    [https://archive.ics.uci.edu/ml/datasets/Wine]
    """

    def __init__(self):
        self._g = Graph()
        self._res_cntr = 1
        self._res_pattern = 'resource%03i'
        self._res_prefix = 'http://dl-learner.org/wine/'
        self._ont_prefix = 'http://dl-learner.org/wine/ont/'

        # classes
        self._cls1 = URIRef(self._ont_prefix + 'WineType1')
        self._cls2 = URIRef(self._ont_prefix + 'WineType2')
        self._cls3 = URIRef(self._ont_prefix + 'WineType3')

        self._id2cls = {
            '1': self._cls1,
            '2': self._cls2,
            '3': self._cls3
        }

        # properties
        self._p1 = URIRef(self._ont_prefix + 'alcohol')
        self._p2 = URIRef(self._ont_prefix + 'malicAcid')
        self._p3 = URIRef(self._ont_prefix + 'ash')
        self._p4 = URIRef(self._ont_prefix + 'alcalinityOfAsh')
        self._p5 = URIRef(self._ont_prefix + 'magnesium')
        self._p6 = URIRef(self._ont_prefix + 'totalPhenols')
        self._p7 = URIRef(self._ont_prefix + 'flavanoids')
        self._p8 = URIRef(self._ont_prefix + 'nonflavanoidPhenols')
        self._p9 = URIRef(self._ont_prefix + 'proanthocyanins')
        self._p10 = URIRef(self._ont_prefix + 'colorIntensity')
        self._p11 = URIRef(self._ont_prefix + 'hue')
        self._p12 = URIRef(self._ont_prefix + 'od280_od315OfDilutedWines')
        self._p13 = URIRef(self._ont_prefix + 'proline')

    def _next_resource(self):
        iri_str = self._res_prefix + self._res_pattern % self._res_cntr
        self._res_cntr += 1

        return URIRef(iri_str)

    def _add_ont_defs(self):
        super_cls = URIRef(self._ont_prefix + 'Wine')

        for wine_cls in [self._cls1, self._cls2, self._cls3]:
            self._g.add((wine_cls, a, OWL.Class))
            self._g.add((wine_cls, RDFS.subClassOf, super_cls))

        xsd_double_props = [
            self._p1, self._p2, self._p3, self._p4, self._p6, self._p7,
            self._p8, self._p9, self._p10, self._p11, self._p12
        ]
        for p in xsd_double_props:
            self._g.add((p, a, OWL.DatatypeProperty))
            self._g.add((p, RDFS.domain, super_cls))
            self._g.add((p, RDFS.range, xsd_double))

        xsd_int_props = [self._p5, self._p13]
        for p in xsd_int_props:
            self._g.add((p, a, OWL.DatatypeProperty))
            self._g.add((p, RDFS.domain, super_cls))
            self._g.add((p, RDFS.range, xsd_int))

    def convert(self, input_file_path, output_file_path):
        self._add_ont_defs()

        with open(input_file_path) as f:
            for line in f:
                res = self._next_resource()
                parts = line.strip().split(',')

                if len(parts) == 1:
                    continue

                # 0) Type
                self._g.add((res, a, self._id2cls[parts[0]]))

                # 1) Alcohol
                l1 = Literal(parts[1], None, xsd_double)
                self._g.add((res, self._p1, l1))

                # 2) Malic acid
                l2 = Literal(parts[2], None, xsd_double)
                self._g.add((res, self._p2, l2))

                # 3) Ash
                l3 = Literal(parts[3], None, xsd_double)
                self._g.add((res, self._p3, l3))

                # 4) Alcalinity of ash
                l4 = Literal(parts[4], None, xsd_double)
                self._g.add((res, self._p4, l4))

                # 5) Magnesium
                l5 = Literal(parts[5], None, xsd_int)
                self._g.add((res, self._p5, l5))

                # 6) Total phenols
                l6 = Literal(parts[6], None, xsd_double)
                self._g.add((res, self._p6, l6))

                # 7) Flavanoids
                l7 = Literal(parts[7], None, xsd_double)
                self._g.add((res, self._p7, l7))

                # 8) Nonflavanoid phenols
                l8 = Literal(parts[8], None, xsd_double)
                self._g.add((res, self._p8, l8))

                # 9) Proanthocyanins
                l9 = Literal(parts[9], None, xsd_double)
                self._g.add((res, self._p9, l9))

                # 10)Color intensity
                l10 = Literal(parts[10], None, xsd_double)
                self._g.add((res, self._p10, l10))

                # 11)Hue
                l11 = Literal(parts[11], None, xsd_double)
                self._g.add((res, self._p11, l11))

                # 12)OD280/OD315 of diluted wines
                l12 = Literal(parts[12], None, xsd_double)
                self._g.add((res, self._p12, l12))

                # 13)Proline
                l13 = Literal(parts[13], None, xsd_int)
                self._g.add((res, self._p13, l13))

        write_graph(self._g, output_file_path)
