from pyparsing import alphanums
from pyparsing import Empty
from pyparsing import Forward
from pyparsing import LineEnd
from pyparsing import Literal
from pyparsing import nums
from pyparsing import OneOrMore
from pyparsing import SkipTo
from pyparsing import Word
from pyparsing import ZeroOrMore
from string import ascii_lowercase


class Statement(object):
    pass


class Fact(Statement):
    def __init__(self, pred, *args):
        self.predicate = pred
        self.arguments = args

    def __repr__(self):
        return '%s(%s)' % (self.predicate,
                           ','.join([str(a) for a in self.arguments]))

    @property
    def predicate_arity(self):
        return len(self.arguments)


class GolemPrologParser():
    # predicate facts
    const = Word(initChars=ascii_lowercase, bodyChars=(alphanums + '_'))
    number = Word(nums)
    predicate = Forward()
    arg = (predicate ^ const ^ number) + Literal(',').suppress()
    last_arg = predicate ^ const ^ number
    args = ZeroOrMore(arg) + last_arg
    predicate_name = Word(initChars=ascii_lowercase, bodyChars=(alphanums + '_'))
    predicate << predicate_name + Literal('(').suppress() + args + \
        Literal(')').suppress()
    predicate_fact = predicate + Literal('.').suppress()

    # comments (ignored)
    comment = Literal('%') + SkipTo(LineEnd())
    # mode declarations (ignored)
    mode_decl = Literal('!-') + SkipTo(LineEnd())

    line = (predicate_fact | comment.suppress() | mode_decl.suppress() |
            Empty().suppress()) + LineEnd().suppress()
    pl = OneOrMore(line)

    dbg = predicate_name + Literal('(').suppress() + predicate + \
        Literal(',').suppress() + const + Literal(')').suppress()

    def __init__(self):
        self.predicate.addParseAction(self._process_predicate)
        self.comment.addParseAction(self._process_predicate)
        self.mode_decl.addParseAction(self._process_predicate)

    def parse_facts(self, file_path):
        facts = self.pl.parseFile(file_path)
        return facts[:]

    def _process_predicate(self, parsing_results):
        return Fact(*parsing_results)

    def _parse_number(self, parsing_results):
        return int(parsing_results)
