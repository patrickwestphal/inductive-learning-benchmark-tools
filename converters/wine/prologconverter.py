import os


class Wine2PrologConverter(object):
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
        self._rules = []
        self._const_cntr = 1
        self._const_pattern = 'c%03i'

        self._p1 = 'alcohol'
        self._p2 = 'malicAcid'
        self._p3 = 'ash'
        self._p4 = 'alcalinityOfAsh'
        self._p5 = 'magnesium'
        self._p6 = 'totalPhenols'
        self._p7 = 'flavanoids'
        self._p8 = 'nonflavanoidPhenols'
        self._p9 = 'proanthocyanins'
        self._p10 = 'colorIntensity'
        self._p11 = 'hue'
        self._p12 = 'od280_od315OfDilutedWines'
        self._p13 = 'proline'

        self._id2pred = {
            '1': 'wineType1',
            '2': 'wineType2',
            '3': 'wineType3'
        }

    def _next_c(self):
        const = self._const_pattern % self._const_cntr
        self._const_cntr += 1

        return const

    def convert(self, input_file_path, output_file_path):
        with open(input_file_path) as f:
            for line in f:
                const = self._next_c()
                parts = line.strip().split(',')

                if len(parts) == 1:
                    continue

                # 0) Type
                self._rules.append('%s(%s).' % (self._id2pred[parts[0]],
                                                const))

                # 1) Alcohol
                self._rules.append('%s(%s, %s).' % (self._p1, const, parts[1]))

                # 2) Malic acid
                self._rules.append('%s(%s, %s).' % (self._p2, const, parts[2]))

                # 3) Ash
                self._rules.append('%s(%s, %s).' % (self._p3, const, parts[3]))

                # 4) Alcalinity of ash
                self._rules.append('%s(%s, %s).' % (self._p4, const, parts[4]))

                # 5) Magnesium
                self._rules.append('%s(%s, %s).' % (self._p5, const, parts[5]))

                # 6) Total phenols
                self._rules.append('%s(%s, %s).' % (self._p6, const, parts[6]))

                # 7) Flavanoids
                self._rules.append('%s(%s, %s).' % (self._p7, const, parts[7]))

                # 8) Nonflavanoid phenols
                self._rules.append('%s(%s, %s).' % (self._p8, const, parts[8]))

                # 9) Proanthocyanins
                self._rules.append('%s(%s, %s).' % (self._p9, const, parts[9]))

                # 10)Color intensity
                self._rules.append('%s(%s, %s).' % (self._p10, const,
                                                    parts[10]))

                # 11)Hue
                self._rules.append('%s(%s, %s).' % (self._p11, const,
                                                    parts[11]))

                # 12)OD280/OD315 of diluted wines
                self._rules.append('%s(%s, %s).' % (self._p12, const,
                                                    parts[12]))

                # 13)Proline
                self._rules.append('%s(%s, %s).' % (self._p13, const,
                                                    parts[13]))

        with open(output_file_path, 'w') as o:
            for rule in self._rules:
                o.write(rule)
                o.write(os.linesep)
