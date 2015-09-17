from pyparsing import alphas
from pyparsing import alphanums
from pyparsing import LineStart
from pyparsing import LineEnd
from pyparsing import Literal
from pyparsing import nums
from pyparsing import OneOrMore
from pyparsing import Optional
from pyparsing import SkipTo
from pyparsing import StringEnd
from pyparsing import Word
from pyparsing import ZeroOrMore


charge_mapping = {
    '0': 0,
    '1': 3,
    '2': 2,
    '3': 1,
    '4': None,
    '5': -1,
    '6': -2,
    '7': -3
}


atom_stereo_parity_mapping = {
    '0': 'not stereo',
    '1': 'odd',
    '2': 'even',
    '3': 'either or unmarked stereo center'
}


hydrogen_count_mapping = {
    '0': None,
    '1': 'H0',
    '2': 'H1',
    '3': 'H2',
    '4': 'H3',
    '5': 'H5'
}


bond_type_mapping = {
    '1': 'Single',
    '2': 'Double',
    '3': 'Triple',
    '4': 'Aromatic',
    '5': 'Single or Double',
    '6': 'Single or Aromatic',
    '7': 'Double or Aromatic',
    '8': 'Any'
}

bond_stereo_mapping = {
    'Single': {
        '0': 'Not stereo',
        '1': 'Up',
        '4': 'Either',
        '6': 'Down'
    },
    'Double': {
        '0': 'Use x-, y-, z-coords from atom block to determine cis or trans',
        '3': 'Either cis or trans double bond'
    }
}


bond_topology_mapping = {
    '0': 'Either',
    '1': 'Ring',
    '2': 'Chain'
}


reacting_center_status_mapping = {
    '0': 'unmarked',
    '1': 'a center',
    '-1': 'not a center',
    '2': 'no change',
    '4': 'bond made/broken',
    '8': 'bond order changes',
    '12': 'bond made/broken + bond order changes',
    '5': 'bond made/broken + a center',
    '13': 'bond made/broken + bond order changes + a center'
}


class SDFParser(object):

    some_line = LineStart() + SkipTo(LineEnd()).suppress()
    empty_line = LineStart() + LineEnd()

    num_atoms = Word(nums)
    num_bonds = Word(nums)
    num_atom_lists = Word(nums)
    obsolete1 = Word(nums)
    molecule_is_chiral = Word(nums)
    num_stext_entries = Word(nums)
    obsolete2 = Word(nums)
    obsolete3 = Word(nums)
    obsolete4 = Word(nums)
    obsolete5 = Word(nums)
    num_lines_with_add_properties = Word(nums)
    version = Word(alphanums)

    counts_line = num_atoms + num_bonds + num_atom_lists + \
        obsolete1 + molecule_is_chiral + num_stext_entries + obsolete2 + \
        obsolete3 + obsolete4 + obsolete5 + num_lines_with_add_properties + \
        version + LineEnd().suppress()

    atom_x_coordinate = Word(nums + '-.')
    atom_y_coordinate = Word(nums + '-.')
    atom_z_coordinate = Word(nums + '-.')
    # entry in periodic table or L for atom list, A, Q, * for unspecified atom,
    # and LP for lone pair, or R# for Rgroup label
    atom_symbol = Word(alphas)
    # -3, -2, -1, 0, 1, 2, 3, 4 (0 if value beyond these limits)
    atom_mass_difference = Word(nums + '-')
    # 0, 1, 2, 3, 4, 5, 6, 7 (0 if uncharged; 1, 2, 3 if positive charges where
    # 1 = +3, 2 = +2, 3 = +1; 4 if doublet radical; 5, 6, 7 if negative charges
    # where 5 = -1, 6 = -2, 7 = -3)
    # Wider range of values in M CHG and M RAD lines below. Retained for
    # compatibility with older Ctabs, M CHG and M RAD lines take precedence.
    atom_charge = Word(nums + '-')
    # 0 = not stereo, 1 = odd, 2 = even, 3 = either or unmarked stereo center
    atom_stereo_parity = Word(nums)
    # 1 = H0, 2 = H1, 3 = H2, 4 = H3, 5 = H4
    # H0 means no H atoms allowed unless explicitly drawn. Hn means atom must
    # have n or more H’s in excess of explicit H’s.
    hydrogen_count_plus_1 = Word(nums)
    # 0 = ignore stereo configuration of this double bond atom, 1 = stereo
    # configuration of double bond atom must match
    # Double bond stereochemistry is considered during atom_stereo_parity only
    # if both ends of the bond are marked with stereo care boxes.
    stereo_care_box = Word(nums)
    # 0 = no marking (default) (1 to 14) = (1 to 14) 15 = zero valence
    # Shows number of bonds to this atom, including bonds to implied H’s.
    valence = Word(nums)
    # 0 = not specified, 1 = no H atoms allowed
    # Redundant with hydrogen count information. Might be unsupported in future
    # releases of Symyx software.
    h0_designator = Word(nums)
    not_used1 = Word(nums)
    not_used2 = Word(nums)
    # 1 - number of atoms
    atom_atom_mapping_number = Word(nums)
    # 0 = property not applied, 1 = configuration is inverted,
    # 2 = configuration is retained
    inversion_retention_flag = Word(nums)
    # 0 = property not applied, 1 = change on atom must be exactly as shown
    exact_change_flag = Word(nums)

    atom_block_row = atom_x_coordinate + atom_y_coordinate + \
        atom_z_coordinate + atom_symbol + atom_mass_difference + \
        atom_charge + atom_stereo_parity + hydrogen_count_plus_1 + \
        stereo_care_box + valence + h0_designator + not_used1 + not_used2 + \
        atom_atom_mapping_number + inversion_retention_flag + \
        exact_change_flag + LineEnd().suppress()

    atom_block = OneOrMore(atom_block_row)

    # 1 - number of atoms
    first_atom_number = Word(nums)
    # 1 - number of atoms
    second_atom_number = Word(nums)
    # 1 = Single, 2 = Double, 3 = Triple, 4 = Aromatic, 5 = Single or Double,
    # 6 = Single or Aromatic, 7 = Double or Aromatic, 8 = Any
    bond_type = Word(nums)
    # Single bonds: 0 = not stereo, 1 = Up, 4 = Either, 6 = Down, Double bonds:
    # 0 = Use x-, y-, z-coords from atom block to determine cis or trans,
    # 3 = Cis or trans (either) double bond
    # The wedge (pointed) end of the stereo bond is at the first atom (Field
    # first_atom_number above)
    bond_stereo = Word(nums)
    not_used3 = Word(nums)
    # 0 = Either, 1 = Ring, 2 = Chain
    bond_topology = Word(nums)
    # 0 = unmarked, 1 = a center, -1 = not a center, Additional: 2 = no change,
    # 4 = bond made/broken, 8 = bond order changes 12 = 4+8 (both made/broken
    # and changes); 5 = (4 + 1), 9 = (8 + 1), and 13 = (12 + 1) are also
    # possible
    reacting_center_status = Word(nums)
    bound_block_row = first_atom_number + second_atom_number + bond_type + \
        bond_stereo + not_used3 + bond_topology + reacting_center_status + \
        LineEnd().suppress()

    bound_block = ZeroOrMore(bound_block_row)

    # M  CHG  6  18  -1  27  -1  35  -1  36   1  37   1  38   1
    #         ^  `--v--´ `--v--´
    #         |  entry 1 entry 2 ...
    #         6 entries following
    # entry 1: atom number 18 has charge -1
    # entry 2: atom number 27 has charge -1
    # ...
    num_charge_entries = Word(nums)
    charge_atom_number = Word(nums)
    charge_atom_charge = Word(nums + '-')
    charge_props_line = Literal('M  CHG') + num_charge_entries + \
        OneOrMore(charge_atom_number + charge_atom_charge) + \
        LineEnd().suppress()
    properties_block = ZeroOrMore(charge_props_line)
    blocks_end_marker = 'M  END' + LineEnd()

    key = Word(alphanums + '_')
    val = OneOrMore(Word(alphanums + '?&.,:;_=/\\\'-+*#@()[]{}'))
    sdf_item = Literal('>  <').suppress() + key + Literal('>').suppress() + \
        LineEnd().suppress() + val + LineEnd().suppress() + \
        empty_line.suppress()

    compound = counts_line + atom_block + bound_block + \
        Optional(properties_block) + blocks_end_marker.suppress() + \
        OneOrMore(sdf_item)

    compound_delimiter = Literal('$$$$')
    sdf = OneOrMore(compound + compound_delimiter.suppress()) + \
        StringEnd().suppress()

    def __init__(self):
        self.counts_line.addParseAction(self._counts_line_hook)
        self.atom_block.addParseAction(self._atom_block_hook)
        self.bound_block.addParseAction(self._bound_block_hook)
        self.properties_block.addParseAction(self._properties_block_hook)
        self.blocks_end_marker.addParseAction(self._blocks_end_hook)
        self.sdf_item.addParseAction(self._sdf_item_hook)
        self.sdf.addParseAction(self._finalize_sdf_items_hook)
        self._converters = []

    def _counts_line_hook(self, parsing_results):
        for converter in self._converters:
            converter.convert_counts_line(parsing_results)

    def _atom_block_hook(self, parsing_results):
        for converter in self._converters:
            converter.read_atom_block(parsing_results)

    def _bound_block_hook(self, parsing_results):
        for converter in self._converters:
            converter.convert_bound_block(parsing_results)

    def _properties_block_hook(self, parsing_results):
        for converter in self._converters:
            converter.update_atom_block(parsing_results)

    def _blocks_end_hook(self):
        for converter in self._converters:
            converter.finalize_atom_block_conversion()

    def _sdf_item_hook(self, parsing_results):
        for converter in self._converters:
            converter.read_sdf_item(parsing_results)

    def _finalize_sdf_items_hook(self, parsing_results):
        for converter in self._converters:
            converter.finalize_sdf_items()

    def parse(self, file_path):
        self.sdf.parseFile(file_path)

    def register_converter(self, converter):
        """
        :param converter: a subclass of SDFConverter
        """
        self._converters.append(converter)
