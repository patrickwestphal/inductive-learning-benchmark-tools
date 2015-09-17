class SDFConverter(object):
    """Interface class

    There are 4 main parts to convert:
    - the counts line
    - the atom block (updated by optional properties block)
    - the bound block
    - SDF items
    """
    _atom_coords_x_str = 'atom_coordinates_x'
    _atom_coords_y_str = 'atom_coordinates_y'
    _atom_coords_z_str = 'atom_coordinates_z'
    _atom_symbol_str = 'atom_symbol'
    _mass_diff_str = 'mass_difference'
    _charge_str = 'charge'
    _atom_stereo_parity_str = 'atom_stereo_parity'
    _hydrogen_count_plus_1_str = 'hydrogen_count'
    _valence_str = 'valence'
    _h0_designator_str = 'h_atoms_allowed'
    _atom_atom_mapping_number_str = 'atom_atom_mapping_number'
    _exact_change_flag_str = 'exact_change'
    _is_doublet_radical_str = 'is_doublet_radical'

    def convert_counts_line(self, parsing_results):
        """Converts the counts line which looks sth like this:
        20 22  0  0  0  0  0  0  0  0  1 V2000

        :param parsing_results: the parsed counts line which looks sth like
            this:
            (Pdb) parse_results
            (['20', '22', '0', '0', '0', '0', '0', '0', '0', '0', '1', 'V2000'], {})
        :return: no return values expected
        """
        raise NotImplementedError()

    def read_atom_block(self, parsing_results):
        """Reads the atom block which is held (and not converted yet) until the
        self.finalize_atom_block_conversion(...) method is called. This is done
        since the actual values in the atom block can be overridden in a part
        that is read later (properties block)

        :param parsing_results: the parsed atom block which looks sth like this:
            (Pdb) parse_results
            (['5.3203', '-2.3043', '0.0000', 'C', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0', '0', '3.9874', '-2.3043', '0.0000', 'C',
            '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
            '3.3209', '-3.4565', '0.0000', 'C', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0', '0', '1.9880', '-3.4565', '0.0000', 'C',
            '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
            '1.3329', '-2.3043', '0.0000', 'C', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0', '0', '1.9880', '-1.1522', '0.0000', 'C',
            '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
            '3.3209', '-1.1522', '0.0000', 'C', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0', '0', '3.9874', '0.0000', '0.0000', 'O',
            '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
            '0.0000', '-2.3043', '0.0000', 'O', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0', '0', '3.9874', '-4.6086', '0.0000', 'O',
            '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
            '5.3203', '-4.6086', '0.0000', 'C', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0', '0', '5.9754', '-3.4565', '0.0000', 'C',
            '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
            '7.3083', '-3.4565', '0.0000', 'C', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0', '0', '7.9748', '-2.3043', '0.0000', 'C',
            '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
            '9.3077', '-2.3043', '0.0000', 'C', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0', '0', '9.9628', '-3.4565', '0.0000', 'C',
            '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
            '9.3077', '-4.6086', '0.0000', 'C', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0', '0', '7.9748', '-4.6086', '0.0000', 'C',
            '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
            '11.2957', '-3.4565', '0.0000', 'O', '0', '0', '0', '0', '0', '0',
            '0', '0', '0', '0', '0', '0', '5.9754', '-1.1522', '0.0000', 'O',
            '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], {})
        :return: no return value expected
        """
        raise NotImplementedError()

    def convert_bound_block(self, parsing_results):
        """Converts the bound block.

        :param parsing_results: the parsed bound block values; e.g.
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
        :return: no return value expected
        """
        raise NotImplementedError()

    def update_atom_block(self, parsing_results):
        """
        :param parsing_results: sth like this:
            (Pdb) parsing_results
            (['M  CHG', '6', '18', '-1', '27', '-1', '35', '-1', '36', '1',
              '37', '1', '38', '1'], {})
        :return: no return value expected
        """
        raise NotImplementedError()

    def finalize_atom_block_conversion(self):
        """This function is called when the end of the properties block was
        read. The actual implementation should then convert a locally held
        atom block data structure to the considered output format

        :return: no return value expected
        """
        raise NotImplementedError()

    def read_sdf_item(self, parsing_results):
        """
        :param parsing_results: sth like
            (Pdb) parsing_results
            (['DSSTox_RID', '22308'], {})
        :return: no return value expected
        """
        raise NotImplementedError()

    def finalize_sdf_items(self):
        """Will be called after all compound blocks were read. This is mainly
        to consistently set the datatypes of the SDF property item values

        :return: no return value expected
        """
        raise NotImplementedError()

    def write_results_to_file(self, out_file_path):
        """Should write the converted data to file.

        :param out_file_path: string containing the path to the output file
        :return: no return value expected
        """
        raise NotImplementedError()
