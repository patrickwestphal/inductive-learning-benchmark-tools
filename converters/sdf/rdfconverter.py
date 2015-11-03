from rdflib import BNode
from rdflib import Graph
from rdflib import Literal
from rdflib import URIRef
from rdflib.namespace import XSD, RDF, RDFS, OWL

from .parser import charge_mapping, hydrogen_count_mapping, \
    atom_stereo_parity_mapping, bond_type_mapping, bond_stereo_mapping, \
    bond_topology_mapping, reacting_center_status_mapping

from sdf.converters import SDFConverter
from utils import write_graph


class SDF2RDFConverter(SDFConverter):
    _more_general_types = {
        XSD.term('string'): [],
        XSD.term('integer'): [XSD.term('double')],
        XSD.term('double'): [],
        XSD.term('nonNegativeInteger'): [XSD.term('integer'),
                                         XSD.term('double')]
    }

    def _get_cls_uri(self, type2local_part_dict, type_):
        local_part = type2local_part_dict[type_]
        return URIRef(self._ont_uri_prefix + local_part)

    _atom_stereo_parity_type_to_cls_local_part = {
        'not stereo': 'AtomParityNotStereo',
        'odd': 'AtomParityOdd',
        'even': 'AtomParityEven',
        'either or unmarked stereo center':
            'AtomParityEitherOrUnmarkedStereoCenter'
    }

    _bond_type_to_cls_local_part = {
        # SDF bond type
        #         (local part,   (super types, ...))
        'Single': ('SingleBond', ('Single or Double', 'Single or Aromatic',
                                  'Any')),
        'Double': ('DoubleBond', ('Single or Double', 'Double or Aromatic',
                                  'Any')),
        'Triple': ('TripleBond', ('Any',)),
        'Aromatic': ('AromaticBond', ('Single or Aromatic',
                                      'Double or Aromatic', 'Any')),
        'Single or Double': ('SingleOrDoubleBond', ('Any',)),
        'Single or Aromatic': ('SingleOrAromaticBond', ('Any',)),
        'Double or Aromatic': ('DoubleOrAromaticBond', ('Any',)),
        'Any': ('Bond', ())
    }

    def _get_bond_cls_uri(self, sdf_type):
        local_part = self._bond_type_to_cls_local_part[sdf_type][0]
        return URIRef(self._ont_uri_prefix + local_part)

    _bond_stereo_to_cls_local_part = {
        'Not stereo': 'NonStereoBond',
        'Up': 'SingleBondUpStereochemistry',
        'Either': 'SingleBondEitherUpOrDownStereochemistry',
        'Down': 'SingleBondDownStereochemistry',
        'Use x-, y-, z-coords from atom block to determine cis or trans':
            'DoubleBondDeriveCisOrTransIsomerismFromXYZCoords',
        'Either cis or trans double bond':
            'DoubleBondEitherCisOrTransIsomerism'
    }

    _bond_topology_to_cls_local_part = {
        'Either': 'EitherRingOrChainTopology',
        'Ring': 'RingTopology',
        'Chain': 'ChainTopology'
    }

    _reacting_center_status_to_cls_local_part = {
        'unmarked': 'Unmarked',
        'a center': 'ACenter',
        'not a center': 'NotACenter',
        'no change': 'NoChange',
        'bond made/broken': 'BondMadeOrBroken',
        'bond order changes': 'BondOrderChanges',
        'bond made/broken + bond order changes':
            'BondMadeOrBrokenAndBondOrderChanges',
        'bond made/broken + a center': 'BondMadeOrBrokenAndACenter',
        'bond made/broken + bond order changes + a center':
            'BondMadeOrBrokenAndBondOrderChangesAndACenter'
    }

    def __init__(self):
        self._resource_uri_prefix = 'http://dl-learner.org/nctrer/'
        self._ont_uri_prefix = 'http://dl-learner.org/ont/'
        self._g = Graph()
        self._curr_res = None
        self._res_cntr = 1
        self._bond_ctr = 1

        # will contain properties (URIRef) as keys and the most general
        # datatype as value
        self._props = {}
        # will contain properties (URIRef) as keys and a list of (sub, val)
        # pairs as value; needs to be done this way since the correct datatype
        # is only known after having seen all values of a property
        self._props_data = {}

        # atom block will be read but not converted directly since it needs to
        # be hold until the properties block is read which might update some
        # of the settings in the atom block
        self._curr_atm_blck = None
        self._init_ontology()

    def _init_ontology(self):
        # ---------------------- basic vocabulary elements --------------------
        self.xsd_nnint = XSD.term('nonNegativeInteger')
        self.xsd_int = XSD.term('integer')
        self.xsd_bool = XSD.term('boolean')
        self.xsd_double = XSD.term('double')

        a = RDF.term('type')

        rdfs_dom = RDFS.term('domain')
        rdfs_rnge = RDFS.term('range')
        rdfs_subcls_of = RDFS.term('subClassOf')

        owl_class = OWL.term('Class')
        owl_dtype_prop = OWL.term('DatatypeProperty')
        owl_obj_prop = OWL.term('ObjectProperty')

        # --------------------------- basic classes ---------------------------
        # dllont:Molecule
        self.cls_molecule = URIRef(self._ont_uri_prefix + 'Molecule')
        self._g.add((self.cls_molecule, a, owl_class))

        # dllont:Atom
        self.cls_atom = URIRef(self._ont_uri_prefix + 'Atom')
        self._g.add((self.cls_atom, a, owl_class))

        # dllont:AtomSymbol
        self.cls_atom_symbol = URIRef(self._ont_uri_prefix + 'AtomSymbol')
        self._g.add((self.cls_atom_symbol, a, owl_class))

        # ----------------- atom stereo parity class hierarchy ----------------
        # dllont:AtomParity
        cls_atom_parity = URIRef(self._ont_uri_prefix + 'AtomParity')
        self._g.add((cls_atom_parity, a, owl_class))

        # dllont:AtomParityNotStereo, dllont:AtomParityOdd,
        # dllont:AtomParityEven, dllont:AtomParityEitherOrUnmarkedStereoCenter
        for val in atom_stereo_parity_mapping.values():
            cls = self._get_cls_uri(
                self._atom_stereo_parity_type_to_cls_local_part, val)
            self._g.add((cls, a, owl_class))
            self._g.add((cls, rdfs_subcls_of, cls_atom_parity))

        # ----------------- hydrogen count resources and class ----------------
        # dllont:HydrogenCount
        self.cls_hydrogen_count = \
            URIRef(self._ont_uri_prefix + 'HydrogenCount')
        self._g.add((self.cls_hydrogen_count, a, owl_class))

        for val in hydrogen_count_mapping.values():
            if val is not None:
                hc_res = URIRef(self._resource_uri_prefix + val.lower())
                self._g.add((hc_res, a, self.cls_hydrogen_count))

        # ------------------------ bond class hierarchy -----------------------
        # dllont:Bond
        self.cls_bond = URIRef(self._ont_uri_prefix + 'Bond')
        self._g.add((self.cls_bond, a, owl_class))

        # dllont:SingleBond, dllont:DoubleBond, dllont:TripleBond,
        # dllont:AromaticBond, dllont:SingleOrDoubleBond,
        # dllont:SingleOrAromaticBond, dllont:DoubleOrAromaticBond
        for val in bond_type_mapping.values():
            bond_cls = self._get_bond_cls_uri(val)
            self._g.add((bond_cls, a, owl_class))

            for sdf_type in self._bond_type_to_cls_local_part[val][1]:
                super_cls = self._get_bond_cls_uri(sdf_type)

                self._g.add((bond_cls, rdfs_subcls_of, super_cls))

        # ------------------- bond isomerism class hierarchy ------------------
        # dllont:NonStereoBond
        non_st_bond_cls = self._get_cls_uri(
            self._bond_stereo_to_cls_local_part, 'Not stereo')
        self._g.add((non_st_bond_cls, a, owl_class))
        self._g.add((non_st_bond_cls, rdfs_subcls_of, self.cls_bond))

        # dllont:SingleBondEitherUpOrDownStereochemistry
        either_up_or_down_cls = self._get_cls_uri(
            self._bond_stereo_to_cls_local_part, 'Either')
        self._g.add((either_up_or_down_cls, a, owl_class))
        self._g.add((
            either_up_or_down_cls,
            rdfs_subcls_of,
            self._get_bond_cls_uri('Single')
        ))

        # dllont:SingleBondUpStereochemistry
        up_stereo_cls = self._get_cls_uri(
            self._bond_stereo_to_cls_local_part, 'Up')
        self._g.add((up_stereo_cls, a, owl_class))
        self._g.add((up_stereo_cls, rdfs_subcls_of, either_up_or_down_cls))

        # dllont:SingleBondDownStereochemistry
        down_stereo_cls = self._get_cls_uri(
            self._bond_stereo_to_cls_local_part, 'Down')
        self._g.add((down_stereo_cls, a, owl_class))
        self._g.add((down_stereo_cls, rdfs_subcls_of, either_up_or_down_cls))

        cls_double_bond = self._get_bond_cls_uri('Double')

        # dllont:DoubleBondDeriveCisOrTransIsomerismFromXYZCoords
        derive_iso_cls = self._get_cls_uri(
            self._bond_stereo_to_cls_local_part,
            'Use x-, y-, z-coords from atom block to determine cis or trans')
        self._g.add((derive_iso_cls, a, owl_class))
        self._g.add((derive_iso_cls, rdfs_subcls_of, cls_double_bond))

        # dllont:DoubleBondEitherCisOrTransIsomerism
        cis_or_trans_cls = self._get_cls_uri(
            self._bond_stereo_to_cls_local_part,
            'Either cis or trans double bond')
        self._g.add((cis_or_trans_cls, a, owl_class))
        self._g.add((cis_or_trans_cls, rdfs_subcls_of, cls_double_bond))

        # -------------------------- topology classes -------------------------
        # dllont:BondTopology
        topology_cls = URIRef(self._ont_uri_prefix + 'BondTopology')
        self._g.add((topology_cls, a, owl_class))

        # dllont:EitherRingOrChainTopology
        either_topo_cls = self._get_cls_uri(
            self._bond_topology_to_cls_local_part, 'Either')
        self._g.add((either_topo_cls, a, owl_class))
        self._g.add((either_topo_cls, rdfs_subcls_of, topology_cls))

        # dllont:RingTopology
        ring_topo_cls = self._get_cls_uri(
            self._bond_topology_to_cls_local_part, 'Ring')
        self._g.add((ring_topo_cls, a, owl_class))
        self._g.add((ring_topo_cls, rdfs_subcls_of, either_topo_cls))

        # dllont:ChainTopology
        chain_topo_cls = self._get_cls_uri(
            self._bond_topology_to_cls_local_part, 'Chain')
        self._g.add((chain_topo_cls, a, owl_class))
        self._g.add((chain_topo_cls, rdfs_subcls_of, either_topo_cls))

        # --------------- reacting center status class hierarchy --------------
        # dllont:ReactingCenterStatus
        react_center_status_cls = URIRef(
            self._ont_uri_prefix + 'ReactingCenterStatus')
        self._g.add((react_center_status_cls, a, owl_class))

        # dllont:Unmarked
        react_unmarked_cls = self._get_cls_uri(
            self._reacting_center_status_to_cls_local_part, 'unmarked')
        self._g.add((react_unmarked_cls, a, owl_class))
        self._g.add(
            (react_unmarked_cls, rdfs_subcls_of, react_center_status_cls))

        # dllont:ACenter
        react_a_center_cls = self._get_cls_uri(
            self._reacting_center_status_to_cls_local_part, 'a center')
        self._g.add((react_a_center_cls, a, owl_class))
        self._g.add(
            (react_a_center_cls, rdfs_subcls_of, react_center_status_cls))

        # dllont:NotACenter
        react_not_a_center_cls = self._get_cls_uri(
            self._reacting_center_status_to_cls_local_part, 'not a center')
        self._g.add((react_not_a_center_cls, a, owl_class))
        self._g.add(
            (react_not_a_center_cls, rdfs_subcls_of, react_center_status_cls))
        self._g.add((
            react_a_center_cls,
            OWL.term('disjointWith'),
            react_not_a_center_cls
        ))

        # dllont:NoChange
        react_no_change_cls = self._get_cls_uri(
            self._reacting_center_status_to_cls_local_part, 'no change')
        self._g.add((react_no_change_cls, a, owl_class))
        self._g.add(
            (react_no_change_cls, rdfs_subcls_of, react_center_status_cls))

        # FIXME: add class intersections
        # dllont:BondMadeOrBroken
        react_bond_made_or_broken_cls = self._get_cls_uri(
            self._reacting_center_status_to_cls_local_part, 'bond made/broken')
        self._g.add((react_bond_made_or_broken_cls, a, owl_class))
        self._g.add((
            react_bond_made_or_broken_cls,
            rdfs_subcls_of,
            react_center_status_cls
        ))

        # dllont:BondOrderChanges
        react_bond_order_change_cls = self._get_cls_uri(
            self._reacting_center_status_to_cls_local_part,
            'bond order changes')
        self._g.add((react_bond_order_change_cls, a, owl_class))
        self._g.add((
            react_bond_order_change_cls,
            rdfs_subcls_of,
            react_center_status_cls
        ))

        # dllont:BondMadeOrBrokenAndBondOrderChanges
        react_bmob_and_boc_cls = self._get_cls_uri(
            self._reacting_center_status_to_cls_local_part,
            'bond made/broken + bond order changes')
        self._g.add((react_bmob_and_boc_cls, a, owl_class))
        self._g.add((
            react_bmob_and_boc_cls,
            rdfs_subcls_of,
            react_bond_made_or_broken_cls
        ))
        self._g.add((
            react_bmob_and_boc_cls,
            rdfs_subcls_of,
            react_bond_order_change_cls
        ))

        # dllont:BondMadeOrBrokenAndACenter
        react_bmob_and_a_center_cls = self._get_cls_uri(
            self._reacting_center_status_to_cls_local_part,
            'bond made/broken + a center')
        self._g.add((react_bmob_and_a_center_cls, a, owl_class))
        self._g.add((
            react_bmob_and_a_center_cls,
            rdfs_subcls_of,
            react_bond_made_or_broken_cls
        ))
        self._g.add((
            react_bmob_and_a_center_cls,
            rdfs_subcls_of,
            react_a_center_cls
        ))

        # dllont:BondMadeOrBrokenAndBondOrderChangesAndACenter
        react_bmob_and_boc_and_a_center_cls = self._get_cls_uri(
            self._reacting_center_status_to_cls_local_part,
            'bond made/broken + bond order changes + a center')
        self._g.add((react_bmob_and_boc_and_a_center_cls, a, owl_class))
        self._g.add((
            react_bmob_and_boc_and_a_center_cls,
            rdfs_subcls_of,
            react_bmob_and_boc_cls
        ))
        self._g.add((
            react_bmob_and_boc_and_a_center_cls,
            rdfs_subcls_of,
            react_bmob_and_a_center_cls
        ))
        self._g.add((
            react_bmob_and_boc_and_a_center_cls,
            rdfs_subcls_of,
            react_a_center_cls
        ))

        # ------------------------ property definitions -----------------------
        # dllont:number_of_atoms
        self.prop_num_atoms = \
            URIRef(self._ont_uri_prefix + 'number_of_atoms')
        self._g.add((self.prop_num_atoms, a, owl_dtype_prop))
        self._g.add((self.prop_num_atoms, rdfs_dom, self.cls_molecule))
        self._g.add((self.prop_num_atoms, rdfs_rnge, self.xsd_nnint))

        # dllont:number_of_bounds
        self.prop_num_bounds = \
            URIRef(self._ont_uri_prefix + 'number_of_bounds')
        self._g.add((self.prop_num_bounds, a, owl_dtype_prop))
        self._g.add((self.prop_num_bounds, rdfs_dom, self.cls_molecule))
        self._g.add((self.prop_num_bounds, rdfs_rnge, self.xsd_nnint))

        # dllont:number_of_atom_lists
        self.prop_num_atom_lists = URIRef(
            self._ont_uri_prefix + 'number_of_atom_lists')
        self._g.add((self.prop_num_atom_lists, a, owl_dtype_prop))
        self._g.add((self.prop_num_atom_lists, rdfs_dom, self.cls_molecule))
        self._g.add((self.prop_num_atom_lists, rdfs_rnge, self.xsd_nnint))

        # dllont:molecule_is_chiral
        self.prop_molec_is_chiral = URIRef(
            self._ont_uri_prefix + 'molecule_is_chiral')
        self._g.add((self.prop_molec_is_chiral, a, owl_dtype_prop))
        self._g.add((self.prop_molec_is_chiral, rdfs_dom, self.cls_molecule))
        self._g.add((self.prop_molec_is_chiral, rdfs_rnge, self.xsd_bool))

        # dllont:atom
        self.prop_atom = URIRef(self._ont_uri_prefix + 'atom')
        self._g.add((self.prop_atom, a, owl_obj_prop))
        self._g.add((self.prop_atom, rdfs_dom, self.cls_molecule))
        self._g.add((self.prop_atom, rdfs_rnge, self.cls_atom))

        # dllont:atom_number
        self.prop_atom_number = URIRef(self._ont_uri_prefix + 'atom_number')
        self._g.add((self.prop_atom_number, a, owl_dtype_prop))
        self._g.add((self.prop_atom_number, rdfs_dom, self.cls_atom))
        self._g.add((self.prop_atom_number, rdfs_rnge, self.xsd_nnint))

        # dllont:atom_coordinate_x
        self.prop_coord_x = URIRef(self._ont_uri_prefix + 'atom_coordinate_x')
        self._g.add((self.prop_coord_x, a, owl_dtype_prop))
        self._g.add((self.prop_coord_x, rdfs_dom, self.cls_atom))
        self._g.add((self.prop_coord_x, rdfs_rnge, self.xsd_double))

        # dllont:atom_coordinate_y
        self.prop_coord_y = URIRef(self._ont_uri_prefix + 'atom_coordinate_y')
        self._g.add((self.prop_coord_y, a, owl_dtype_prop))
        self._g.add((self.prop_coord_y, rdfs_dom, self.cls_atom))
        self._g.add((self.prop_coord_y, rdfs_rnge, self.xsd_double))

        # dllont:atom_coordinate_z
        self.prop_coord_z = URIRef(self._ont_uri_prefix + 'atom_coordinate_z')
        self._g.add((self.prop_coord_z, a, owl_dtype_prop))
        self._g.add((self.prop_coord_z, rdfs_dom, self.cls_atom))
        self._g.add((self.prop_coord_z, rdfs_rnge, self.xsd_double))

        # dllont:atom_symbol
        self.prop_atom_symbol = URIRef(self._ont_uri_prefix + 'atom_symbol')
        self._g.add((self.prop_atom_symbol, a, owl_obj_prop))
        self._g.add((self.prop_atom_symbol, rdfs_dom, self.cls_atom))
        self._g.add((self.prop_atom_symbol, rdfs_rnge, self.cls_atom_symbol))

        # dllont:mass_difference
        self.prop_mass_difference = URIRef(
            self._ont_uri_prefix + 'mass_difference')
        self._g.add((self.prop_mass_difference, a, owl_dtype_prop))
        self._g.add((self.prop_mass_difference, rdfs_dom, self.cls_atom))
        self._g.add((self.prop_mass_difference, rdfs_rnge, self.xsd_double))

        # dllont:charge
        self.prop_charge = URIRef(self._ont_uri_prefix + 'charge')
        self._g.add((self.prop_charge, a, owl_dtype_prop))
        self._g.add((self.prop_charge, rdfs_dom, self.cls_atom))
        self._g.add((self.prop_charge, rdfs_rnge, self.xsd_int))

        # dllont:hydrogen_count
        self.prop_hydrogen_count = URIRef(
            self._ont_uri_prefix + 'hydrogen_count')
        self._g.add((self.prop_hydrogen_count, a, owl_obj_prop))
        self._g.add((self.prop_hydrogen_count, rdfs_dom, self.cls_atom))
        self._g.add(
            (self.prop_hydrogen_count, rdfs_rnge, self.cls_hydrogen_count))

        # dllont:valence
        self.prop_valence = URIRef(self._ont_uri_prefix + 'valence')
        self._g.add((self.prop_valence, a, owl_dtype_prop))
        self._g.add((self.prop_valence, rdfs_dom, self.cls_atom))
        self._g.add((self.prop_valence, rdfs_rnge, self.xsd_nnint))

        # dllont:h_atoms_allowed
        self.prop_h_atoms_allowed = URIRef(
            self._ont_uri_prefix + 'h_atoms_allowed')
        self._g.add((self.prop_h_atoms_allowed, a, owl_dtype_prop))
        self._g.add((self.prop_h_atoms_allowed, rdfs_dom, self.cls_atom))
        self._g.add((self.prop_h_atoms_allowed, rdfs_rnge, self.xsd_bool))

        # dllont:atom-atom_mapping_number
        self.prop_atom_atom_mapping_nr = URIRef(
            self._ont_uri_prefix + 'atom-atom_mapping_number')
        self._g.add((self.prop_atom_atom_mapping_nr, a, owl_dtype_prop))
        self._g.add((self.prop_atom_atom_mapping_nr, rdfs_dom, self.cls_atom))
        self._g.add(
            (self.prop_atom_atom_mapping_nr, rdfs_rnge, self.xsd_nnint))

        # dllont:has_binding_with
        self.prop_has_binding_with = URIRef(
            self._ont_uri_prefix + 'has_binding_with')
        self._g.add((
            self.prop_has_binding_with,
            a,
            URIRef(OWL.term('SymmetricProperty'))
        ))
        self._g.add((self.prop_has_binding_with, rdfs_dom, self.cls_atom))
        self._g.add((self.prop_has_binding_with, rdfs_rnge, self.cls_atom))

        # dllont:first_bound_atom
        self.prop_first_bound_atom = URIRef(
            self._ont_uri_prefix + 'first_bound_atom')
        self._g.add((self.prop_first_bound_atom, a, owl_obj_prop))
        self._g.add((self.prop_first_bound_atom, rdfs_dom, self.cls_bond))
        self._g.add((self.prop_first_bound_atom, rdfs_rnge, self.cls_atom))

        # dllont:second_bound_atom
        self.prop_second_bound_atom = URIRef(
            self._ont_uri_prefix + 'second_bound_atom')
        self._g.add((self.prop_second_bound_atom, a, owl_obj_prop))
        self._g.add((self.prop_second_bound_atom, rdfs_dom, self.cls_bond))
        self._g.add((self.prop_second_bound_atom, rdfs_rnge, self.cls_atom))

        # dllont:has_topology
        self.prop_has_topology = URIRef(self._ont_uri_prefix + 'has_topology')
        self._g.add((self.prop_has_topology, a, owl_obj_prop))
        self._g.add((self.prop_has_topology, rdfs_dom, self.cls_bond))
        self._g.add((self.prop_has_topology, rdfs_rnge, topology_cls))

        # dllont:has_reacting_center_status
        self.prop_has_rc_status = URIRef(
            self._ont_uri_prefix + 'has_reacting_center_status')
        self._g.add((self.prop_has_rc_status, a, owl_obj_prop))
        self._g.add((self.prop_has_rc_status, rdfs_dom, self.cls_bond))
        self._g.add(
            (self.prop_has_rc_status, rdfs_rnge, react_center_status_cls))

    def _build_has_some(self, resource, prop, cls):
        tmp_graph = Graph()
        restr_res = BNode()
        tmp_graph.add((resource, RDF.term('type'), restr_res))
        tmp_graph.add((restr_res, RDF.term('type'), OWL.term('Restriction')))
        tmp_graph.add((restr_res, OWL.term('onProperty'), prop))
        tmp_graph.add((restr_res, OWL.term('someValuesFrom'), cls))

        return tmp_graph

    def convert_counts_line(self, parsing_results):
        """
        (Pdb) parsing_results
        (['20', '22', '0', '0', '0', '0', '0', '0', '0', '0', '1', 'V2000'], {})
        """
        # since this is called firs, a new RDF resource is created which will
        # have all the information attached
        self._curr_res = URIRef(self._resource_uri_prefix +
                                str(self._res_cntr))
        self._res_cntr += 1

        self._g.add((self._curr_res, RDF.term('type'), self.cls_molecule))

        num_atoms = parsing_results[0]
        num_bonds = parsing_results[1]
        num_atom_lists = parsing_results[2]
        molecule_is_chiral = 'true' if parsing_results[4] == 1 else 'false'

        # number of atoms
        self._g.add((
            self._curr_res,
            self.prop_num_atoms,
            Literal(num_atoms, None, self.xsd_nnint)
        ))

        # number of bounds
        self._g.add((
            self._curr_res,
            self.prop_num_bounds,
            Literal(num_bonds, None, self.xsd_nnint)
        ))

        # number of atom lists
        self._g.add((
            self._curr_res,
            self.prop_num_atom_lists,
            Literal(num_atom_lists, None, self.xsd_nnint)
        ))

        # molecule is chiral
        self._g.add((
            self._curr_res,
            self.prop_molec_is_chiral,
            Literal(molecule_is_chiral, None, self.xsd_bool)
        ))

    def read_atom_block(self, parsing_results):
        self._curr_atm_blck = []
        curr_row = 0

        pr_copy = parsing_results[:]

        while len(pr_copy) > 0:
            self._curr_atm_blck.append({})

            # atom coordinate X
            self._curr_atm_blck[curr_row][self._atom_coords_x_str] = \
                pr_copy.pop(0)

            # atom coordinate Y
            self._curr_atm_blck[curr_row][self._atom_coords_y_str] = \
                pr_copy.pop(0)

            # atom coordinate Z
            self._curr_atm_blck[curr_row][self._atom_coords_z_str] = \
                pr_copy.pop(0)

            # atom symbol
            tmp = pr_copy.pop(0)
            if tmp == 'L':
                # FIXME
                raise NotImplementedError('atom symbol == L not implemented')
            elif tmp == 'A' or tmp == 'Q' or tmp == '*':
                # FIXME
                raise NotImplementedError(
                    'atom symbol is unspecified not implemented')
            elif tmp == 'LP':
                # FIXME
                raise NotImplementedError('atom symbol == LP not implemented')
            self._curr_atm_blck[curr_row][self._atom_symbol_str] = tmp

            # mass difference
            self._curr_atm_blck[curr_row][self._mass_diff_str] = pr_copy.pop(0)

            # charge
            tmp = pr_copy.pop(0)
            val = charge_mapping[tmp]

            if val is None:
                self._curr_atm_blck[curr_row][self._is_doublet_radical_str] = \
                    True
            else:
                self._curr_atm_blck[curr_row][self._charge_str] = val

            # atom stereo parity
            tmp = pr_copy.pop(0)
            atom_stereo_parity_val = atom_stereo_parity_mapping[tmp]
            # written to self._curr_atom_block under 'stereo care box'

            # hydrogen count + 1
            tmp = pr_copy.pop(0)
            val = hydrogen_count_mapping[tmp]
            if val is not None:
                self._curr_atm_blck[curr_row][self._hydrogen_count_plus_1_str]\
                    = val

            # stereo care box
            tmp = pr_copy.pop(0)
            if tmp == '1':
                self._curr_atm_blck[curr_row][self._atom_stereo_parity_str] = \
                    atom_stereo_parity_val

            # valence
            tmp = pr_copy.pop(0)
            if tmp != '0':
                val = int(tmp)
                if val == 15:
                    val = 0
                self._curr_atm_blck[curr_row][self._valence_str] = val

            # H0 designator
            tmp = pr_copy.pop(0)
            if tmp == 1:
                self._curr_atm_blck[curr_row][self._h0_designator_str] = \
                    'false'

            # not used (twice)
            pr_copy.pop(0)
            pr_copy.pop(0)

            # atom-atom mapping number
            self._curr_atm_blck[curr_row][self._atom_atom_mapping_number_str] \
                = int(pr_copy.pop(0))

            # inversion/retention flag
            tmp = pr_copy.pop(0)
            if tmp != '0':
                # FIXME
                raise NotImplementedError()

            # exact change flag
            tmp = pr_copy.pop(0)
            if tmp != '0':
                # FIXME
                raise NotImplementedError()

            curr_row += 1

    def convert_bound_block(self, parsing_results):
        pr_copy = parsing_results[:]
        while len(pr_copy) > 0:
            # bond resource
            bond_res = URIRef(self._resource_uri_prefix + 'bond' +
                              str(self._bond_ctr))
            self._bond_ctr += 1

            # first atom number
            first_atom_nr = pr_copy.pop(0)
            first_atom = URIRef(self._resource_uri_prefix +
                                str(self._res_cntr) + '/atom' + first_atom_nr)
            # second atom number
            second_atom_nr = pr_copy.pop(0)
            second_atom = URIRef(self._resource_uri_prefix +
                                 str(self._res_cntr) + '/atom' +
                                 second_atom_nr)

            self._g.add((first_atom, self.prop_has_binding_with, second_atom))
            self._g.add((bond_res, self.prop_first_bound_atom, first_atom))
            self._g.add((bond_res, self.prop_second_bound_atom, second_atom))

            # bond type
            bond_type = bond_type_mapping[pr_copy.pop(0)]
            bond_cls = self._get_bond_cls_uri(bond_type)
            self._g.add((bond_res, RDF.term('type'), bond_cls))

            # bond stereo
            if bond_type in bond_stereo_mapping:
                bond_isomerism = bond_stereo_mapping[bond_type][pr_copy.pop(0)]

                bond_isomerism_cls = self._get_cls_uri(
                    self._bond_stereo_to_cls_local_part, bond_isomerism)
                self._g.add((bond_res, RDF.term('type'), bond_isomerism_cls))
            else:
                # skip (values are all 0 in NCTRER dataset)
                pr_copy.pop(0)

            # not used
            pr_copy.pop(0)

            # bond topology
            bond_topology = bond_topology_mapping[pr_copy.pop(0)]
            bond_topology_cls = self._get_cls_uri(
                self._bond_topology_to_cls_local_part, bond_topology)
            for trpl in self._build_has_some(
                    bond_res, self.prop_has_topology, bond_topology_cls):
                self._g.add(trpl)

            # reacting center status
            rc_status = reacting_center_status_mapping[pr_copy.pop(0)]
            rc_status_cls = self._get_cls_uri(
                self._reacting_center_status_to_cls_local_part, rc_status)

            for trpl in self._build_has_some(
                    bond_res, self.prop_has_rc_status, rc_status_cls):
                self._g.add(trpl)

    def update_atom_block(self, parsing_results):
        """
        :param parsing_results: sth like this:
            (Pdb) parsing_results
            (['M  CHG', '6', '18', '-1', '27', '-1', '35', '-1', '36', '1',
              '37', '1', '38', '1'], {})
        """
        pr_copy = parsing_results[:]

        while len(pr_copy) > 0:
            prop_type = pr_copy.pop(0)
            num_entries = int(pr_copy.pop(0))

            # TODO: add further property types
            # (the SDF file I wanted to convert only contained the CHG
            # property)
            if prop_type == 'M  CHG':
                for i in range(num_entries):
                    atom_nr = int(pr_copy.pop(0)) - 1
                    charge = int(pr_copy.pop(0))
                    self._curr_atm_blck[atom_nr][self._charge_str] = charge

    def finalize_atom_block_conversion(self):
        atom_cntr = 1

        for entry in self._curr_atm_blck:
            atom_res = URIRef('%s/atom%i' % (str(self._curr_res), atom_cntr))
            self._g.add((atom_res, RDF.term('type'), self.cls_atom))

            # atom
            self._g.add((
                self._curr_res,
                URIRef(self._ont_uri_prefix + 'atom'),
                atom_res
            ))

            # atom number
            self._g.add((
                atom_res,
                self.prop_atom_number,
                Literal(atom_cntr, None, self.xsd_nnint)
            ))

            # atom coords X
            self._g.add((
                atom_res,
                self.prop_coord_x,
                Literal(entry[self._atom_coords_x_str], None, self.xsd_double)
            ))

            # atom coords Y
            self._g.add((
                atom_res,
                self.prop_coord_y,
                Literal(entry[self._atom_coords_y_str], None, self.xsd_double)
            ))

            # atom coords Z
            self._g.add((
                atom_res,
                self.prop_coord_z,
                Literal(entry[self._atom_coords_z_str], None, self.xsd_double)
            ))

            # atom symbol
            res_atom_symbol = URIRef(
                self._resource_uri_prefix + 'atom/' +
                entry[self._atom_symbol_str])

            self._g.add(
                (res_atom_symbol, RDF.term('type'), self.cls_atom_symbol))
            self._g.add((
                atom_res,
                self.prop_atom_symbol,
                res_atom_symbol
            ))

            # mass difference
            self._g.add((
                atom_res,
                self.prop_mass_difference,
                Literal(entry[self._mass_diff_str], None, self.xsd_double)
            ))

            # charge
            self._g.add((
                atom_res,
                self.prop_charge,
                Literal(entry[self._charge_str], None, self.xsd_int)
            ))

            # atom stereo parity
            if entry.get(self._atom_stereo_parity_str) is not None:
                self._g.add((
                    atom_res,
                    RDF.term('type'),
                    URIRef(self._ont_uri_prefix +
                           entry[self._atom_stereo_parity_str])
                ))

            # hydrogen count
            if entry.get(self._hydrogen_count_plus_1_str) is not None:
                self._g.add((
                    atom_res,
                    self.prop_hydrogen_count,
                    URIRef(self._resource_uri_prefix +
                           entry[self._hydrogen_count_plus_1_str].lower())
                ))

            # valence
            if entry.get(self._valence_str) is not None:
                self._g.add((
                    atom_res,
                    self.prop_valence,
                    Literal(entry[self._valence_str], None, self.xsd_nnint)
                ))

            # H0 designator
            if entry.get(self._h0_designator_str) is not None:
                self._g.add((
                    atom_res,
                    self.prop_h_atoms_allowed,
                    Literal(entry[self._h0_designator_str], None,
                            self.xsd_bool)
                ))

            # atom-atom mapping number
            self._g.add((
                atom_res,
                self.prop_atom_atom_mapping_nr,
                Literal(entry[self._atom_atom_mapping_number_str], None,
                        self.xsd_nnint)
            ))

            atom_cntr += 1

    def _register_and_build_property(self, header, rnge):
        prop = URIRef(self._ont_uri_prefix + header)

        if self._props.get(prop) is None:
            self._props[prop] = rnge

        else:
            if rnge in self._more_general_types[self._props[prop]]:
                self._props[prop] = rnge

        return prop

    def read_sdf_item(self, parsing_results):
        """
        :param parsing_results: sth like
            (Pdb) parsing_results
            (['DSSTox_RID', '22308'], {})
        """
        # for now just assuming the data header (e.g. DSSTox_RID) is URI-safe
        header = parsing_results[0]
        value = ' '.join(parsing_results[1:])

        # if header == 'ActivityOutcome_NCTRER':
        #     print('%s\t%s' % (value, str(self._curr_res)))

        # if header.startswith('Activity'):
        #     return

        contains_dot = '.' in value
        is_negative = value.strip().startswith('-')

        if is_negative:
            tmp = value.strip()[1:]
        else:
            tmp = value.strip()
        is_num = tmp.replace('.', '').isnumeric()

        if is_num and contains_dot:
            dtype = self.xsd_double
        elif is_num and not is_negative:
            dtype = self.xsd_nnint
        elif is_num and is_negative:
            dtype = self.xsd_int
        else:
            dtype = XSD.term('string')

        prop = self._register_and_build_property(header, dtype)

        if self._props_data.get(prop) is None:
            self._props_data[prop] = []
        self._props_data[prop].append((self._curr_res, value))

    def finalize_sdf_items(self):
        # ontological axioms
        for prop, dtype in self._props.items():
            self._g.add((prop, RDF.term('type'), OWL.term('DatatypeProperty')))
            self._g.add((prop, RDFS.term('domain'), self.cls_molecule))
            self._g.add((prop, RDFS.term('range'), dtype))

        # the actual data
        for prop, data in self._props_data.items():
            dtype = self._props[prop]
            for subj, val in data:
                self._g.add((subj, prop, Literal(val, None, dtype)))

    def write_results_to_file(self, out_file_path):
        write_graph(self._g, out_file_path)
