import os


class Iris2PrologConverter(object):
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
        self._rules = []
        self._p0 = 'sepalLength'
        self._p1 = 'sepalWidth'
        self._p2 = 'petalLength'
        self._p3 = 'petalWidth'
        self._p_setosa = 'irisSetosa'
        self._p_versicolour = 'irisVersicolour'
        self._p_virginica = 'irisVirginica'
        self._c_cntr = 1

        self._pid2p = {
            'Iris-setosa': self._p_setosa,
            'Iris-versicolor': self._p_versicolour,
            'Iris-virginica': self._p_virginica
        }

    def _get_next_c(self):
        c = 'c%03i' % self._c_cntr
        self._c_cntr += 1
        return c

    def convert(self, input_file_path, output_file_path):
        with open(input_file_path) as f:
            for line in f:
                parts = line.strip().split(',')

                if len(parts) == 1:
                    continue

                c = self._get_next_c()

                # 0. sepal length in cm
                self._rules.append('%s(%s, %s).' % (self._p0, c, parts[0]))

                # 1. sepal width in cm
                self._rules.append('%s(%s, %s).' % (self._p1, c, parts[1]))

                # 2. petal length in cm
                self._rules.append('%s(%s, %s).' % (self._p2, c, parts[2]))

                # 3. petal width in cm
                self._rules.append('%s(%s, %s).' % (self._p3, c, parts[3]))

                # 4. class
                self._rules.append('%s(%s).' % (self._pid2p[parts[4]], c))

        with open(output_file_path, 'w') as o:
            for rule in self._rules:
                o.write(rule)
                o.write(os.linesep)
