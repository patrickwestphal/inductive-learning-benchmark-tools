from rdflib import Graph
from rdflib import Literal
from rdflib import OWL
from rdflib import RDF
from rdflib import RDFS
from rdflib import URIRef
from rdflib import XSD

from utils import write_graph

a = RDF.term('type')
rdfs_subClassOf = RDFS.term('subClassOf')
rdfs_domain = RDFS.term('domain')
rdfs_range = RDFS.term('range')
xsd_double = XSD.term('double')
owl_Class = OWL.term('Class')
owl_DatatypeProperty = OWL.term('DatatypeProperty')
owl_FunctionalProperty = OWL.term('FunctionalProperty')


class GlassIdentification2RDFConverter(object):
    """
    1. Id number: 1 to 214
    2. RI: refractive index
    3. Na: Sodium (unit measurement: weight percent in corresponding oxide, as
       are attributes 4-10)
    4. Mg: Magnesium
    5. Al: Aluminum
    6. Si: Silicon
    7. K: Potassium
    8. Ca: Calcium
    9. Ba: Barium
    10. Fe: Iron
    11. Type of glass: (class attribute)
    -- 1 building_windows_float_processed
    -- 2 building_windows_non_float_processed
    -- 3 vehicle_windows_float_processed
    -- 4 vehicle_windows_non_float_processed (none in this database)
    -- 5 containers
    -- 6 tableware
    -- 7 headlamps

    [https://archive.ics.uci.edu/ml/datasets/Glass+Identification]
    """

    def __init__(self):
        self._g = Graph()
        self._res_pattern = 'http://dl-learner.org/glass/res%03i'
        self._ont_prefix = 'http://dl-learner.org/ont/'
        self._p1 = URIRef(self._ont_prefix + 'refractiveIndex')
        self._p2 = URIRef(self._ont_prefix + 'sodium')
        self._p3 = URIRef(self._ont_prefix + 'magnesium')
        self._p4 = URIRef(self._ont_prefix + 'alumium')
        self._p5 = URIRef(self._ont_prefix + 'silicon')
        self._p6 = URIRef(self._ont_prefix + 'potassium')
        self._p7 = URIRef(self._ont_prefix + 'calcium')
        self._p8 = URIRef(self._ont_prefix + 'barium')
        self._p9 = URIRef(self._ont_prefix + 'iron')

        self._cls_build_win_float_proc = \
            URIRef(self._ont_prefix + 'BuildingWindowFloatProcessed')
        self._cls_build_win_non_float_proc = \
            URIRef(self._ont_prefix + 'BuildingWindowNonFloat_processed')
        self._cls_vehcle_win_float_proc = \
            URIRef(self._ont_prefix + 'VehicleWindowFloatProcessed')
        self._cls_vehcle_win_non_float_proc = \
            URIRef(self._ont_prefix + 'VehicleWindosNonFloatProcessed')
        self._cls_containers = URIRef(self._ont_prefix + 'Container')
        self._cls_tableware = URIRef(self._ont_prefix + 'Tableware')
        self._cls_headlamp = URIRef(self._ont_prefix + 'Headlamp')

        self._type2_cls = {
            '1': self._cls_build_win_float_proc,
            '2': self._cls_build_win_non_float_proc,
            '3': self._cls_vehcle_win_float_proc,
            '4': self._cls_vehcle_win_non_float_proc,
            '5': self._cls_containers,
            '6': self._cls_tableware,
            '7': self._cls_headlamp
        }

    def _res(self, r_id):
        return URIRef(self._res_pattern % r_id)

    def add_ont_axioms(self):
        glss_cls = URIRef(self._ont_prefix + 'Glass')

        clss = [
            self._cls_build_win_float_proc, self._cls_build_win_non_float_proc,
            self._cls_vehcle_win_float_proc,
            self._cls_vehcle_win_non_float_proc, self._cls_containers,
            self._cls_tableware, self._cls_headlamp
        ]

        for cls in clss:
            self._g.add((cls, rdfs_subClassOf, glss_cls))

        props = [
            self._p1, self._p2, self._p3, self._p4, self._p5, self._p6,
            self._p7, self._p8, self._p9
        ]

        for p in props:
            self._g.add((p, a, owl_DatatypeProperty))
            self._g.add((p, rdfs_domain, glss_cls))
            self._g.add((p, rdfs_range, xsd_double))
            self._g.add((p, a, owl_FunctionalProperty))

    def convert(self, input_file_path, output_file_path):
        self.add_ont_axioms()

        with open(input_file_path) as f:
            for line in f:
                parts = line.strip().split(',')

                if len(parts) == 1:
                    continue

                # 1. Id number: 1 to 214
                r_id = int(parts[0])
                res = self._res(r_id)

                # 2. RI: refractive index
                l1 = Literal(parts[1], None, xsd_double)
                self._g.add((res, self._p1, l1))

                # 3. Na: Sodium (unit measurement: weight percent in
                # corresponding oxide, as are attributes 4-10)
                l2 = Literal(parts[2], None, xsd_double)
                self._g.add((res, self._p2, l2))

                # 4. Mg: Magnesium
                l3 = Literal(parts[3], None, xsd_double)
                self._g.add((res, self._p3, l3))

                # 5. Al: Aluminum
                l4 = Literal(parts[4], None, xsd_double)
                self._g.add((res, self._p4, l4))

                # 6. Si: Silicon
                l5 = Literal(parts[5], None, xsd_double)
                self._g.add((res, self._p5, l5))

                # 7. K: Potassium
                l6 = Literal(parts[6], None, xsd_double)
                self._g.add((res, self._p6, l6))

                # 8. Ca: Calcium
                l7 = Literal(parts[7], None, xsd_double)
                self._g.add((res, self._p7, l7))

                # 9. Ba: Barium
                l8 = Literal(parts[8], None, xsd_double)
                self._g.add((res, self._p8, l8))

                # 10. Fe: Iron
                l9 = Literal(parts[9], None, xsd_double)
                self._g.add((res, self._p9, l9))

                # 11. Type of glass
                cls = self._type2_cls[parts[10]]
                self._g.add((res, a, cls))

        write_graph(self._g, output_file_path)
