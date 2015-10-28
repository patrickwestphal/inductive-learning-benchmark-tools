import os

from pyparsing import alphas
from pyparsing import alphanums
from pyparsing import Literal
from pyparsing import OneOrMore
from pyparsing import Word
from pyparsing import ZeroOrMore


class PredicatesFileParser(object):
    val = Word(alphanums + ':' + '_') + Literal(',').suppress()
    lastval = Word(alphanums + ':' + '_')
    predicate_name = Word(alphas)
    predicate = predicate_name + Literal('(').suppress() + ZeroOrMore(val) + \
        lastval + Literal(')').suppress()
    pred_file = OneOrMore(predicate)

    def __init__(self):
        self.predicate.addParseAction(self._predicate_hook)
        self._converters = []

    def _predicate_hook(self, parsing_results):
        pred = parsing_results[0]
        args = parsing_results[1:]
        for converter in self._converters:
            converter.convert_predicate(pred, args)

    def _parse_class_types(self, file_path):
        id2cls = {}
        with open(file_path) as f:
            for line in f.readlines():
                id, cls = line.strip().split()
                id2cls[id] = cls

        return id2cls

    def parse(self, dir_path):
        cls_types_file_path = os.path.join(dir_path, 'classtypes.txt')
        if os.path.isfile(cls_types_file_path):
            id2cls = self._parse_class_types(cls_types_file_path)

            for converter in self._converters:
                converter.register_class_mapping(id2cls)

        for file_name in os.listdir(dir_path):
            path = os.path.join(dir_path, file_name)
            if os.path.isfile(path):
                if path.endswith('.preds'):
                    self.pred_file.parseFile(path)

        for converter in self._converters:
            converter.finalize()

    def register_converter(self, converter):
        """
        :param converter: a subclass of PredicateFileConverter
        """
        self._converters.append(converter)
