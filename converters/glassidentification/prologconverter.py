import os


class GlassIdentification2PrologConverter(object):
    """
    1. Id number: 1 to 214
    2. RI: refractive index
    3. Na: Sodium (unit measurement: weight percent in corresponding oxide, as are attributes 4-10)
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
        self._rules = []
        self._p1 = 'refractiveIndex'
        self._p2 = 'sodium'
        self._p3 = 'magnesium'
        self._p4 = 'alumium'
        self._p5 = 'silicon'
        self._p6 = 'potassium'
        self._p7 = 'calcium'
        self._p8 = 'barium'
        self._p9 = 'iron'

        self._type_build_win_float_proc = 'buildingWindowFloatProcessed'
        self._type_build_win_non_float_proc = \
            'buildingWindowNonFloat_processed'
        self._type_vehcle_win_float_proc = 'vehicleWindowFloatProcessed'
        self._type_vehcle_win_non_float_proc = 'vehicleWindowNonFloatProcessed'
        self._type_containers = 'container'
        self._type_tableware = 'tableware'
        self._type_headlamps = 'headlamp'

        self._type2type_str = {
            '1': self._type_build_win_float_proc,
            '2': self._type_build_win_non_float_proc,
            '3': self._type_vehcle_win_float_proc,
            '4': self._type_vehcle_win_non_float_proc,
            '5': self._type_containers,
            '6': self._type_tableware,
            '7': self._type_headlamps
        }

    def convert(self, input_file_path, output_file_path):
        with open(input_file_path) as f:
            for line in f:
                parts = line.strip().split(',')

                if len(parts) == 1:
                    continue

                # 0. Id number: 1 to 214
                const = 'c%03i' % int(parts[0])

                # 1. RI: refractive index
                self._rules.append('%s(%s, %s).' % (self._p1, const, parts[1]))

                # 2. Na: Sodium
                self._rules.append('%s(%s, %s).' % (self._p2, const, parts[2]))

                # 3. Mg: Magnesium
                self._rules.append('%s(%s, %s).' % (self._p3, const, parts[3]))

                # 4. Al: Aluminum
                self._rules.append('%s(%s, %s).' % (self._p4, const, parts[4]))

                # 5. Si: Silicon
                self._rules.append('%s(%s, %s).' % (self._p5, const, parts[5]))

                # 6. K: Potassium
                self._rules.append('%s(%s, %s).' % (self._p6, const, parts[6]))

                # 7. Ca: Calcium
                self._rules.append('%s(%s, %s).' % (self._p7, const, parts[7]))

                # 8. Ba: Barium
                self._rules.append('%s(%s, %s).' % (self._p8, const, parts[8]))

                # 9. Fe: Iron
                self._rules.append('%s(%s, %s).' % (self._p9, const, parts[9]))

                # 10. Type of glass
                self._rules.append('%s(%s).' % (self._type2type_str[parts[10]],
                                               const))

        with open(output_file_path, 'w') as o:
            for rule in self._rules:
                o.write(rule)
                o.write(os.linesep)
