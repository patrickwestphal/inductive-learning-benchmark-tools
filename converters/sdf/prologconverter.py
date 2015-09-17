import hashlib

from sdf.converters import SDFConverter
from sdf.parser import charge_mapping, atom_stereo_parity_mapping, \
    hydrogen_count_mapping, bond_type_mapping, bond_stereo_mapping, \
    bond_topology_mapping, reacting_center_status_mapping


class Predicate(object):
    def __init__(self, name, values):
        self.name = name
        self.values = values

    def __str__(self):
        return '%s(%s)' % (self.name, ','.join(self.values))


class Fact(object):
    def __init__(self, predicates):
        self.predicates = predicates

    def __str__(self):
        return ', '.join([str(p) for p in self.predicates]) + '.'


class Body(object):
    def __init__(self, predicates):
        self.predicates = predicates

    def __str__(self):
        return ', '.join([str(p) for p in self.predicates])


class Head(object):
    def __init__(self, predicate):
        self.predicate = predicate

    def __str__(self):
        return str(self.predicate)


class Rule(object):
    def __init__(self, head, body):
        self.head = head
        self.body = body

    def __str__(self):
        return '%s :- %s.' % (str(self.head), str(self.body))


class Comment(object):
    def __init__(self, comment):
        self.comment = comment

    def __str__(self):
        return '%% %s' % self.comment


class SDF2PrologConverter(SDFConverter):
    _bond_type_to_pred = {
        'Single': 'single_bond',
        'Double': 'double_bond',
        'Triple': 'triple_bond',
        'Aromatic': 'aromatic_bond',
        'Single or Double': 'single_or_double_bond',
        'Single or Aromatic': 'single_or_aromatic_bond',
        'Any': 'bond'
    }

    _bond_isomerism_to_pred = {
        'Not stereo': 'non_stereo_bond',
        'Up': 'single_bond_up_stereochemistry',
        'Either': 'single_bond_either_up_or_down_stereochemistry',
        'Down': 'single_bond_down_stereochemistry',
        'Use x-, y-, z-coords from atom block to determine cis or trans':
            'double_bond_derive_cis_or_trans_isomerism_from_xyz_coords',
        'Either cis or trans double bond':
            'double_bond_either_cis_or_trans_isomerism'
    }

    _bond_topology_to_pred = {
        'Either': 'either_ring_or_chain_topology',
        'Ring': 'ring_topology',
        'Chain': 'chain_topology'
    }

    _reacting_center_status_to_pred = {
        'unmarked': 'unmarked',
        'a center': 'a_center',
        'not a center': 'not_a_Center',
        'no change': 'no_change',
        'bond made/broken': 'bond_made_or_broken',
        'bond order changes': 'bond_order_changes',
        'bond made/broken + bond order changes':
            'bond_made_or_broken_and_bond_order_changes',
        'bond made/broken + a center': 'bond_made_or_broken_and_a_center',
        'bond made/broken + bond order changes + a center':
            'bond_made_or_broken_and_bond_order_changes_and_a_Center'
    }

    def __init__(self):
        self._molec_const_cntr = 0
        self._molec_const_prefix = 'molecule'
        self._bond_const_cntr = 0
        self._bond_const_prefix = 'bond'
        self._curr_molec_const = None
        self._curr_atm_blck = None
        self._const_prefix = 'const'
        self.rules = []

        self._init_rules()

    def _init_rules(self):
        self._add_r('bond', 'X', ':-', 'single_or_double_bond', 'X')
        self._add_r('bond', 'X', ':-', 'single_or_aromatic_bond', 'X')
        self._add_r('bond', 'X', ':-', 'double_or_aromatic_bond', 'X')
        self._add_r('bond', 'X', ':-', 'triple_bond', 'X')

        self._add_r('single_or_double_bond', 'X', ':-', 'single_bond', 'X')
        self._add_r('single_or_double_bond', 'X', ':-', 'double_bond', 'X')

        self._add_r('single_or_aromatic_bond', 'X', ':-', 'single_bond', 'X')
        self._add_r('single_or_aromatic_bond', 'X', ':-', 'aromatic_bond', 'X')

        self._add_r('double_or_aromatic_bond', 'X', ':-', 'double_bond', 'X')
        self._add_r('double_or_aromatic_bond', 'X', ':-', 'aromatic_bond', 'X')

        self._add_r('single_bond_either_up_or_down_stereochemistry', 'X',
                    ':-', 'single_bond_up_stereochemistry', 'X')
        self._add_r('single_bond_either_up_or_down_stereochemistry', 'X',
                    ':-', 'single_bond_down_stereochemistry', 'X')

        self._add_r('either_ring_or_chain_topology', 'X', ':-',
                    'ring_topology', 'X')
        self._add_r('either_ring_or_chain_topology', 'X', ':-',
                    'chain_topology', 'X')

        self._add_r('bond_made_or_broken_and_bond_order_changes', 'X', ':-',
                    'bond_made_or_broken', 'X', ',', 'bond_order_changes', 'X')
        self._add_r('bond_made_or_broken_and_a_center', 'X', ':-',
                    'bond_made_or_broken', 'X', ',', 'a_center', 'X')
        self._add_r('bond_made_or_broken_and_bond_order_changes_and_a_Center',
                    'X', ':-', 'bond_made_or_broken', 'X', ',',
                    'bond_order_changes', 'X', ',', 'a_center', 'X')

        self._add_r('has_binding_with', 'X', 'Y', ':-', 'has_binding', 'Y', 'X')

    def _get_next_molecule_constant(self):
        self._molec_const_cntr += 1
        const = self._molec_const_prefix + str(self._molec_const_cntr)
        return const

    def _get_next_bond_constant(self):
        self._bond_const_cntr += 1
        const = self._bond_const_prefix + str(self._bond_const_cntr)
        return const

    def _f(self, *args):
        """Generates simple fact"""
        pred_name = args[0]
        vals = args[1:]
        return Fact((Predicate(pred_name, vals), ))

    def _add_f(self, *args):
        """Generates and adds simple fact"""
        pred_name = args[0]
        vals = args[1:]
        self.rules.append(Fact((Predicate(pred_name, vals), )))

    def _add_r(self, *args):
        """Generates and adds simple rule"""
        head_pred_name = args[0]
        head_pred_vals = []

        pos = 1

        for v in args[1:]:
            pos += 1
            if v == ':-':
                break
            else:
                head_pred_vals.append(v)

        body_preds = []
        body_pred_name_next = True
        tmp_body_pred_name = None
        tmp_body_pred_vals = []

        for v in args[pos:]:
            if v == ',':
                body_preds.append((tmp_body_pred_name, tmp_body_pred_vals))
                tmp_body_pred_name = None
                tmp_body_pred_vals = []
                body_pred_name_next = True
                continue

            if body_pred_name_next:
                body_pred_name_next = False
                tmp_body_pred_name = v
            else:
                tmp_body_pred_vals.append(v)

        body_preds.append((tmp_body_pred_name, tmp_body_pred_vals))

        head = Head(Predicate(head_pred_name, head_pred_vals))
        body = Body([Predicate(p[0], p[1]) for p in body_preds])

        self.rules.append(Rule(head, body))

    def _p(self):
        print('\n'.join([str(f) for f in self.rules]))

    def convert_counts_line(self, parsing_results):
        """
        :param parsing_results: sth like
        (Pdb) parsing_results
        (['20', '22', '0', '0', '0', '0', '0', '0', '0', '0', '1', 'V2000'], {})
        """
        self._curr_molec_const = self._get_next_molecule_constant()
        self._add_f('molecule', self._curr_molec_const)

        num_atoms = parsing_results[0]
        self._add_f('number_of_atoms', self._curr_molec_const, num_atoms)

        num_bonds = parsing_results[1]
        self._add_f('number_of_bonds', self._curr_molec_const, num_bonds)

        num_atom_lists = parsing_results[2]
        self._add_f(
            'number_of_atom_lists', self._curr_molec_const, num_atom_lists)

        molecule_is_chiral = 'true' if parsing_results[4] == 1 else 'false'
        self._add_f(
            'molecule_is_chiral', self._curr_molec_const, molecule_is_chiral)

    def read_atom_block(self, parsing_results):
        """
        :param parsing_results: sth like this:
        (Pdb) parsing_results
        (['5.3203', '-2.3043', '0.0000', 'C', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0',
          '3.9874', '-2.3043', '0.0000', 'C', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0',
          '3.3209', '-3.4565', '0.0000', 'C', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0',
          '1.9880', '-3.4565', '0.0000', 'C', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0',
          '1.3329', '-2.3043', '0.0000', 'C', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0',
          '1.9880', '-1.1522', '0.0000', 'C', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0',
          '3.3209', '-1.1522', '0.0000', 'C', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0',
          '3.9874', '0.0000', '0.0000', 'O', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0',
          '0.0000', '-2.3043', '0.0000', 'O', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0',
          '3.9874', '-4.6086', '0.0000', 'O', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0',
          '5.3203', '-4.6086', '0.0000', 'C', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0',
          '5.9754', '-3.4565', '0.0000', 'C', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0',
          '7.3083', '-3.4565', '0.0000', 'C', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0',
          '7.9748', '-2.3043', '0.0000', 'C', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0',
          '9.3077', '-2.3043', '0.0000', 'C', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0',
          '9.9628', '-3.4565', '0.0000', 'C', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0',
          '9.3077', '-4.6086', '0.0000', 'C', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0',
          '7.9748', '-4.6086', '0.0000', 'C', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0',
          '11.2957', '-3.4565', '0.0000', 'O', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0', '0',
          '5.9754', '-1.1522', '0.0000', 'O', '0', '0', '0', '0', '0', '0', '0',
          '0', '0', '0', '0', '0'], {})
        """
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
            self._curr_atm_blck[curr_row][self._atom_symbol_str] = tmp.lower()

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
                self._curr_atm_blck[curr_row][self._hydrogen_count_plus_1_str] \
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
                self._curr_atm_blck[curr_row][self._h0_designator_str] = 'false'

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
        """
        :param parsing_results: sth like this:
        (Pdb) parsing_results
        ([ '1',  '2', '1', '0', '0', '0', '0',
           '1', '12', '1', '0', '0', '0', '0',
           '1', '20', '2', '0', '0', '0', '0',
           '2',  '3', '2', '0', '0', '0', '0',
           '2',  '7', '1', '0', '0', '0', '0',
           '3',  '4', '1', '0', '0', '0', '0',
           '3', '10', '1', '0', '0', '0', '0',
           '4',  '5', '2', '0', '0', '0', '0',
           '5',  '6', '1', '0', '0', '0', '0',
           '5',  '9', '1', '0', '0', '0', '0',
           '6',  '7', '2', '0', '0', '0', '0',
           '7',  '8', '1', '0', '0', '0', '0',
          '10', '11', '1', '0', '0', '0', '0',
          '11', '12', '2', '0', '0', '0', '0',
          '12', '13', '1', '0', '0', '0', '0',
          '13', '14', '1', '0', '0', '0', '0',
          '13', '18', '2', '0', '0', '0', '0',
          '14', '15', '2', '0', '0', '0', '0',
          '15', '16', '1', '0', '0', '0', '0',
          '16', '17', '2', '0', '0', '0', '0',
          '16', '19', '1', '0', '0', '0', '0',
          '17', '18', '1', '0', '0', '0', '0'], {})
        """
        pr_copy = parsing_results[:]

        while len(pr_copy) > 0:
            bond_const = self._get_next_bond_constant()

            # first atom number
            first_atom_nr = pr_copy.pop(0)
            first_atom = 'atom_%i_%s' % (self._molec_const_cntr, first_atom_nr)

            # second atom number
            secnd_atom_nr = pr_copy.pop(0)
            secnd_atom = 'atom_%i_%s' % (self._molec_const_cntr, secnd_atom_nr)

            self._add_f('has_binding_with', first_atom, secnd_atom)

            self._add_f('first_bound_atom', bond_const, first_atom)
            self._add_f('second_bound_atom', bond_const, secnd_atom)

            # bond type
            bond_type = bond_type_mapping[pr_copy.pop(0)]
            bond_pred = self._bond_type_to_pred[bond_type]
            self._add_f(bond_pred, bond_const)

            # bond stereo
            # the bond isomerism types are ordered by bond type, i.e. single
            # bond, double bond, ...
            if bond_type in bond_stereo_mapping:
                bond_isomerism = bond_stereo_mapping[bond_type][pr_copy.pop(0)]

                bond_isomerism_pred = \
                    self._bond_isomerism_to_pred[bond_isomerism]
                self._add_f(bond_isomerism_pred, bond_const)

            else:
                # skip (values are all 0 in NCTRER dataset)
                pr_copy.pop(0)

            # not used
            pr_copy.pop(0)

            # bond topology
            bond_topology = bond_topology_mapping[pr_copy.pop(0)]

            bond_topology_pred = self._bond_topology_to_pred[bond_topology]
            self._add_f(bond_topology_pred, bond_const)

            # reacting center status
            rc_status = reacting_center_status_mapping[pr_copy.pop(0)]
            rc_pred = self._reacting_center_status_to_pred[rc_status]
            self._add_f(rc_pred, bond_const)

    def update_atom_block(self, parsing_results):
        pr_copy = parsing_results[:]

        while len(pr_copy) > 0:
            prop_type = pr_copy.pop(0)
            num_entries = int(pr_copy.pop(0))

            # TODO: add further property types
            # (the SDF file I wanted to convert only contained the CHG property)
            if prop_type == 'M  CHG':
                for i in range(num_entries):
                    atom_nr = int(pr_copy.pop(0)) - 1
                    charge = int(pr_copy.pop(0))
                    self._curr_atm_blck[atom_nr][self._charge_str] = charge

    def finalize_atom_block_conversion(self):
        atom_cntr = 1

        for entry in self._curr_atm_blck:
            atom_const = 'atom_%i_%s' % (self._molec_const_cntr, atom_cntr)

            self._add_f('is_atom', atom_const)

            # atom number
            self._add_f('atom_number', self._curr_molec_const, atom_const,
                        str(atom_cntr))

            # atom coords X
            self._add_f(
                'atom_coordinate_x', atom_const, entry[self._atom_coords_x_str])

            # atom coords Y
            self._add_f(
                'atom_coordinate_y', atom_const, entry[self._atom_coords_y_str])

            # atom coords Z
            self._add_f(
                'atom_coordinate_z', atom_const, entry[self._atom_coords_z_str])

            # atom symbol
            self._add_f('atom_symbol', atom_const, entry[self._atom_symbol_str])

            # mass difference
            self._add_f('mass_difference', atom_const,
                        entry[self._mass_diff_str])

            # charge
            self._add_f('charge', atom_const, str(entry[self._charge_str]))

            # atom stereo parity
            if entry.get(self._atom_stereo_parity_str) is not None:
                self._add_f('atom_stereo_parity', atom_const,
                            entry[self._atom_stereo_parity_str])

            # hydrogen count
            if entry.get(self._hydrogen_count_plus_1_str) is not None:
                self._add_f('hydrogen_count', atom_const,
                            entry[self._hydrogen_count_plus_1_str].lower())

            # valence
            if entry.get(self._valence_str) is not None:
                self._add_f('valence', atom_const, entry[self._valence_str])

            # H0 designator
            if entry.get(self._h0_designator_str) is not None:
                self._add_f('h_atoms_allowed', atom_const,
                            entry[self._h0_designator_str])

            # atom-atom mapping number
            self._add_f('atom_atom_mapping_number', atom_const,
                        str(entry[self._atom_atom_mapping_number_str]))

            atom_cntr += 1

    def _is_safe(self, value):
        """
        :param value: a string
        :return: True if the string can be used as Prolog constant and False
            otherwise
        """
        is_negative = value.strip().startswith('-')

        if is_negative:
            tmp = value.strip()[1:]
        else:
            tmp = value.strip()
        is_num = tmp.replace('.', '').isnumeric()

        if is_num:
            return True

        elif value[0].isnumeric():
            # value starts with number but some alphas follow
            return False

        elif '\'' in value or ' ' in value or '-' in value or ',' in value or \
                '(' in value or ')' in value or '=' in value or \
                '@' in value or '[' in value or ']' in value:
            return False

        else:
            return True

    def read_sdf_item(self, parsing_results):
        """
        :param parsing_results: sth like this:
        (['DSSTox_RID', '22308'], {})
        """
        if parsing_results[0] == 'ActivityOutcome_NCTRER':
            out = 'molecule(%s) %% ' % str(self._curr_molec_const)
            value = parsing_results[1]
            if value == 'active':
                out += 'pos'
                print(out)
            elif value == 'inactive':
                out += 'neg'
                print(out)

        if parsing_results[0].startswith('Activity'):
            return

        pred = parsing_results[0].lower()
        val = ' '.join(parsing_results[1:])

        if self._is_safe(val):
            self._add_f(pred, self._curr_molec_const, val.lower())
        else:
            const = self._const_prefix + \
                hashlib.sha224(val.encode('utf8')).hexdigest()
            self.rules.append(Comment('%s --> %s' % (const, val)))
            self._add_f(pred, self._curr_molec_const, const)

    def finalize_sdf_items(self):
        """Nothing to do here"""
        pass

    def write_results_to_file(self, out_file_path):
        with open(out_file_path, 'w') as f:
            for rule in self.rules:
                f.write(str(rule))
                f.write('\n')
