import os

from rdflib import BNode
from rdflib import Graph
from rdflib import Literal
from rdflib import OWL
from rdflib import RDF
from rdflib import RDFS
from rdflib import URIRef
from rdflib import XSD

from prolog.parser import GolemPrologParser, Fact
from utils import write_graph

a = RDF.type


class AlzheimerAmineUptake2RDFConverter(object):
    # <------------------------- converter functions ------------------------->
    # Idea: Converter function creates a bunch of triples and adds them to
    # self._g. Additionally it will return some kind of result resource that
    # can be passed up to a converter function of a predicate that got the
    # considered predicate as argument.
    # The converter functions here are mainly constructed based on the paper
    # 'Drug Design Using Inductive Logic Programming' (King, Srinivasan,
    # Muggleton, Feng, Lewis. Steinberg), Prolog mode declarations and some
    # basic biological understanding

    def _polar(self, component_indiv, polarity_term):
        """Hints:
        !- mode(polar(+,-)).

        % the formula N(CH3)2 can be represented as a list
        % polar([n,group(ch3,2)],polar1).
        % or as any other 2-arity function
        """
        if not isinstance(component_indiv, URIRef):
            component_indiv = self._indiv(component_indiv)
            self._g.add((component_indiv, a, OWL.Individual))
            self._g.add((component_indiv, a, self._cls_chem_component))

        polarity_indiv = self._indiv(polarity_term)

        self._g.add((component_indiv, self._prop_has_polarity, polarity_indiv))

        return polarity_indiv

    def _bond(self, first_component, second_component):
        """Hints:

        % the formula N(CH3)2 can be represented as a list
        % polar([n,group(ch3,2)],polar1).
        % or as any other 2-arity function
        polar(bond(n,group(ch3,2)),polar1).

        Represents a binding, e.g. N(CH3)2, as described above
        """
        if not isinstance(first_component, URIRef):
            first_component = self._indiv(first_component)
            self._g.add((first_component, a, OWL.Individual))
            self._g.add((first_component, a, self._cls_chem_component))

        if not isinstance(second_component, URIRef):
            second_component = self._indiv(second_component)
            self._g.add((second_component, a, OWL.Individual))
            self._g.add((second_component, a, self._cls_chem_component))

        bond_indiv = self._next_uri('bond%05i')

        self._g.add((bond_indiv, a, OWL.Individual))
        self._g.add((bond_indiv, a, self._cls_bond))
        self._g.add((bond_indiv, self._prop_first_comp, first_component))
        self._g.add((bond_indiv, self._prop_second_comp, second_component))

        return bond_indiv

    def _group(self, component_indiv, num):
        """Hints:
        % the formula N(CH3)2 can be represented as a list
        % polar([n,group(ch3,2)],polar1).

        !- mode(group(+,-)).
        """
        if not isinstance(component_indiv, URIRef):
            component_indiv = self._indiv(component_indiv)
            self._g.add((component_indiv, a, OWL.Individual))
            self._g.add((component_indiv, a, self._cls_chem_component))

        num_lit = Literal(num, None, XSD.nonNegativeInteger)

        grp_indiv = self._next_uri('group_%05i')

        self._g.add((grp_indiv, a, OWL.Individual))
        self._g.add((grp_indiv, a, self._cls_group))
        self._g.add((grp_indiv, self._prop_has_group_component,
                     component_indiv))
        self._g.add((grp_indiv, self._prop_num_components, num_lit))

        return grp_indiv

    def _size(self, chem_component_id, size_term):
        """Hints:

        !- mode(size(+,-)).

        size(ch3,size1).
        great_size(size9,size1).
        """
        if not isinstance(chem_component_id, URIRef):
            chem_component_indiv = self._indiv(chem_component_id)
            self._g.add((chem_component_indiv, a, OWL.Individual))
            self._g.add((chem_component_indiv, a, self._cls_chem_component))
        else:
            chem_component_indiv = chem_component_id

        size_indiv = self._indiv(size_term)

        self._g.add((chem_component_indiv, self._prop_has_size, size_indiv))

        return

    def _flex(self, chem_component_id, flex_term):
        """Hints:

        !- mode(flex(+,-)).

        flex(ch3,flex0).
        great_flex(flex9,flex0).

        """
        if not isinstance(chem_component_id, URIRef):
            chem_component_indiv = self._indiv(chem_component_id)
            self._g.add((chem_component_indiv, a, OWL.Individual))
            self._g.add((chem_component_indiv, a, self._cls_chem_component))
        else:
            chem_component_indiv = chem_component_id

        flex_indiv = self._indiv(flex_term)

        self._g.add((chem_component_indiv, self._prop_has_flex, flex_indiv))

        return

    def _h_doner(self, chem_component_id, h_doner_term):
        """Hints:

        !- mode(h_doner(+,-)).

        h_doner(ch3,h_don0).
        great_h_don(h_don9,h_don0).
        """
        if not isinstance(chem_component_id, URIRef):
            chem_component_indiv = self._indiv(chem_component_id)
            self._g.add((chem_component_indiv, a, OWL.Individual))
            self._g.add((chem_component_indiv, a, self._cls_chem_component))
        else:
            chem_component_indiv = chem_component_id

        h_doner_indiv = self._indiv(h_doner_term)

        self._g.add((chem_component_indiv, self._prop_has_h_doner,
                     h_doner_indiv))

        return

    def _h_acceptor(self, chem_component_id, h_acceptor_term):
        """Hints:

        !- mode(h_acceptor(+,-)).

        h_acceptor(ch3,h_acc0).
        great_h_acc(h_acc9,h_acc0).
        """
        if not isinstance(chem_component_id, URIRef):
            chem_component_indiv = self._indiv(chem_component_id)
        else:
            chem_component_indiv = chem_component_id

        h_acceptor_indiv = self._indiv(h_acceptor_term)

        self._g.add((chem_component_indiv, self._prop_has_h_acceptor,
                     h_acceptor_indiv))

        return

    def _pi_doner(self, chem_component_id, pi_doner_term):
        """Hints:

        !- mode(pi_doner(+,-)).

        pi_doner(ch3,pi_don0).
        great_pi_don(pi_don9,pi_don0).
        :return:
        """
        if not isinstance(chem_component_id, URIRef):
            chem_component_indiv = self._indiv(chem_component_id)
            self._g.add((chem_component_indiv, a, OWL.Individual))
            self._g.add((chem_component_indiv, a, self._cls_chem_component))
        else:
            chem_component_indiv = chem_component_id

        pi_doner_indiv = self._indiv(pi_doner_term)

        self._g.add((chem_component_indiv, self._prop_has_pi_doner,
                     pi_doner_indiv))

        return

    def _pi_acceptor(self, chem_component_id, pi_acceptor_term):
        """Hints:

        !- mode(pi_acceptor(+,-)).

        pi_acceptor(ch3,pi_acc0).
        great_pi_acc(pi_acc9,pi_acc0).
        """
        if not isinstance(chem_component_id, URIRef):
            chem_component_indiv = self._indiv(chem_component_id)
            self._g.add((chem_component_indiv, a, OWL.Individual))
            self._g.add((chem_component_indiv, a, self._cls_chem_component))
        else:
            chem_component_indiv = chem_component_id

        pi_acceptor_indiv = self._indiv(pi_acceptor_term)

        self._g.add((chem_component_indiv, self._prop_has_pi_acceptor,
                     pi_acceptor_indiv))

        return

    def _polarisable(self, component_id, polarisable_term):
        """Hints:

        !- mode(polarisable(+,-)).

        polarisable(ch3,polari1).
        great_polari(polari9,polari1).
        """
        if not isinstance(component_id, URIRef):
            component_indiv = self._indiv(component_id)
            self._g.add((component_indiv, a, OWL.Individual))
            self._g.add((component_indiv, a, self._cls_chem_component))
        else:
            component_indiv = component_id

        polarisable_indiv = self._indiv(polarisable_term)

        self._g.add((component_indiv, self._prop_has_polarisable,
                     polarisable_indiv))

        return

    def _sigma(self, chem_component_id, sigma_term):
        """Hints:

        !- mode(sigma(+,-)).

        sigma(ch3,sigma0).
        great_sigma(sigma9,sigma0).
        """
        if not isinstance(chem_component_id, URIRef):
            chem_component_indiv = self._indiv(chem_component_id)
            self._g.add((chem_component_indiv, a, OWL.Individual))
            self._g.add((chem_component_indiv, a, self._cls_chem_component))
        else:
            chem_component_indiv = chem_component_id

        sigma_indiv = self._indiv(sigma_term)

        self._g.add((chem_component_indiv, self._prop_has_sigma, sigma_indiv))

        return

    def _dummy(self, *args):
        """Just ignore the input"""
        return

    def _great_polar(self, polar_term1, polar_term2):
        """Hint:

        great_polar(polar1,polar0).
        great_polar(polar2,polar0).
        """
        polarity_indiv1 = self._indiv(polar_term1)
        self._g.add((polarity_indiv1, a, OWL.Individual))
        self._g.add((polarity_indiv1, a, self._cls_polarity))

        polarity_indiv2 = self._indiv(polar_term2)

        self._g.add((polarity_indiv1, self._prop_polar_greater_than,
                     polarity_indiv2))

        return

    def _great_size(self, size_term1, size_term2):
        """Hint:

        great_size(size1,size0).
        great_size(size2,size0).
        """
        size_indiv1 = self._indiv(size_term1)
        self._g.add((size_indiv1, a, OWL.Individual))
        self._g.add((size_indiv1, a, self._cls_size))

        size_indiv2 = self._indiv(size_term2)

        self._g.add((size_indiv1, self._prop_size_greater_than, size_indiv2))

        return

    def _great_flex(self, flex_term1, flex_term2):
        """Hint:

        great_flex(flex1,flex0).
        great_flex(flex2,flex0).
        """
        flex_indiv1 = self._indiv(flex_term1)
        self._g.add((flex_indiv1, a, OWL.Individual))
        self._g.add((flex_indiv1, a, self._cls_flex))

        flex_indiv2 = self._indiv(flex_term2)

        self._g.add((flex_indiv1, self._prop_flex_greater_than, flex_indiv2))

        return

    def _great_h_don(self, h_doner_term1, h_doner_term2):
        """Hints:

        great_h_don(h_don1,h_don0).
        great_h_don(h_don2,h_don0).
        """
        h_doner_indiv1 = self._indiv(h_doner_term1)
        self._g.add((h_doner_indiv1, a, OWL.Individual))
        self._g.add((h_doner_indiv1, a, self._cls_h_doner))

        h_doner_indiv2 = self._indiv(h_doner_term2)

        self._g.add((h_doner_indiv1, self._prop_h_doner_greater_than,
                     h_doner_indiv2))

        return

    def _great_h_acc(self, h_acceptor_term1, h_acceptor_term2):
        """Hints:

        great_h_acc(h_acc1,h_acc0).
        great_h_acc(h_acc2,h_acc0).
        great_h_acc(h_acc3,h_acc0).
        """
        h_acceptor_indiv1 = self._indiv(h_acceptor_term1)
        self._g.add((h_acceptor_indiv1, a, OWL.Individual))
        self._g.add((h_acceptor_indiv1, a, self._cls_h_acceptor))

        h_acceptor_indiv2 = self._indiv(h_acceptor_term2)

        self._g.add((h_acceptor_indiv1, self._prop_h_doner_greater_than,
                     h_acceptor_indiv2))

        return

    def _great_pi_don(self, pi_donator_term1, pi_donator_term2):
        """Hints:

        great_pi_don(pi_don1,pi_don0).
        great_pi_don(pi_don2,pi_don0).
        great_pi_don(pi_don3,pi_don0).
        """
        pi_donator_indiv1 = self._indiv(pi_donator_term1)
        self._g.add((pi_donator_indiv1, a, OWL.Individual))
        self._g.add((pi_donator_indiv1, a, self._cls_pi_doner))

        pi_donator_indiv2 = self._indiv(pi_donator_term2)

        self._g.add((pi_donator_indiv1, self._prop_pi_donator_greater_than,
                     pi_donator_indiv2))

        return

    def _great_pi_acc(self, pi_acceptor_term1, pi_acceptor_term2):
        """Hints:

        great_pi_acc(pi_acc1,pi_acc0).
        great_pi_acc(pi_acc2,pi_acc0).
        great_pi_acc(pi_acc3,pi_acc0).
        """
        pi_acceptor_indiv1 = self._indiv(pi_acceptor_term1)
        self._g.add((pi_acceptor_indiv1, a, OWL.Individual))
        self._g.add((pi_acceptor_indiv1, a, self._cls_pi_acceptor))

        pi_acceptor_indiv2 = self._indiv(pi_acceptor_term2)

        self._g.add((pi_acceptor_indiv1, self._prop_pi_acceptor_greater_than,
                     pi_acceptor_indiv2))

        return

    def _great_polari(self, polarisable_term1, polarisable_term2):
        """Hints:

        great_polari(polari1,polari0).
        great_polari(polari2,polari0).
        great_polari(polari3,polari0).
        """
        polarisable_indiv1 = self._indiv(polarisable_term1)
        self._g.add((polarisable_indiv1, a, OWL.Individual))
        self._g.add((polarisable_indiv1, a, self._cls_polarisable))

        polarisable_indiv2 = self._indiv(polarisable_term2)

        self._g.add((polarisable_indiv1, self._prop_polarisable_greater_than,
                     polarisable_indiv2))

        return

    def _great_sigma(self, sigma_term1, sigma_term2):
        """Hints:
        great_sigma(sigma1,sigma0).
        great_sigma(sigma2,sigma0).
        great_sigma(sigma3,sigma0).
        """
        sigma_indiv1 = self._indiv(sigma_term1)
        sigma_indiv2 = self._indiv(sigma_term2)

        self._g.add((sigma_indiv1, a, OWL.Individual))
        self._g.add((sigma_indiv1, a, self._cls_sigma))
        self._g.add((sigma_indiv1, self._prop_sigma_greater_than,
                     sigma_indiv2))

        return

    def _x_subst(self, drug_analogue_id, position, substituent_id):
        """Hints:

        !- mode(x_subst(+,-,-)).

        % substitution X at positions 6 or 7

        x_subst(b1,7,cl).
        x_subst(c1,6,cl).
        x_subst(d1,6,och3).
        x_subst(e1,6,cf3).
        x_subst(f1,6,f).
        x_subst(hh1,6,cl).
        x_subst(ii1,6,cl).
        x_subst(jj1,6,f).
        x_subst(kk1,6,f).
        x_subst(ll1,6,cf3).
        """
        if not isinstance(drug_analogue_id, URIRef):
            drug_analogue_indiv = self._indiv(drug_analogue_id)
        else:
            drug_analogue_indiv = drug_analogue_id

        substitution_indiv = self._next_uri('x_substitution_%05i')
        self._g.add((substitution_indiv, a, OWL.Individual))
        self._g.add((substitution_indiv, a, self._cls_x_substitution))

        position_literal = Literal(position, None, XSD.nonNegativeInteger)
        substituent_indiv = self._indiv(substituent_id)

        self._g.add((drug_analogue_indiv, self._prop_has_x_subst,
                     substitution_indiv))

        self._g.add((substitution_indiv, self._prop_subst_pos,
                     position_literal))
        self._g.add((substitution_indiv, self._prop_has_substituent,
                     substituent_indiv))

        return

    def _alk_groups(self, drug_analogue_id, num_alkyl_groups):
        """Hints:

        !- mode(alk_groups(+,-)).

        % number of alkyl substitutions

        alk_groups(a1,0).
        alk_groups(b1,0).
        alk_groups(h1,1).
        alk_groups(i1,3).

        alk_groups(n1, 4). --> drug n1 has 4 alkyl groups
        """
        drug_analogue_indiv = self._indiv(drug_analogue_id)
        num_alkyl_grps_literal = Literal(num_alkyl_groups, None,
                                         XSD.nonNegativeInteger)

        # class assignment is done here because all substitutions appear in
        # alk_groups, but not all in r_subst1/2/3 or x_subst
        self._g.add((drug_analogue_indiv, a, OWL.Individual))
        self._g.add((drug_analogue_indiv, a, self._cls_drug_analogue))
        self._g.add((drug_analogue_indiv, self._prop_num_alkyl_groups,
                     num_alkyl_grps_literal))

        return

    def _r_subst_pos(self, drug_analogue_id, pos, r_substituent_id):
        """Hints:

        !- mode(r_subst_1(+,-)).
        !- mode(r_subst_2(+,-)).
        !- mode(r_subst_3(+,-)).

        % substitution R in middle ring

        r_subst_1(a1,h).
        r_subst_1(b1,h).
        r_subst_1(c1,h).
        r_subst_1(d1,h).
        r_subst_1(e1,h).
        r_subst_1(h1,single_alk(1)).
        r_subst_1(i1,single_alk(3)).
        r_subst_1(j1,single_alk(2)).

        r_subst_1(i1,single_alk(3)). --> r_substitution group in drug i1 starts
        with 3 alkyl groups

        r_subst_2(l1,o).
        r_subst_2(m1,double_alk(1)).
        r_subst_2(n1,double_alk(1)).
        r_subst_2(o1,double_alk(1)).
        r_subst_2(p1,aro(1)).
        r_subst_2(q1,aro(1)).

        r_subst_2(n1,double_alk(1)). --> the final alkyl group in drug n1 has
        2 substitutions

        r_subst_3(l1,aro(1)).
        r_subst_3(m1,aro(2)).
        r_subst_3(n1,aro(2)).
        r_subst_3(o1,aro(2)).
        """
        if isinstance(r_substituent_id, URIRef):
            r_substituent_indiv = r_substituent_id
        else:
            r_substituent_indiv = self._indiv(r_substituent_id)
            self._g.add((r_substituent_indiv, a, OWL.Individual))
            self._g.add((r_substituent_indiv, a,
                         self._cls_middle_ring_substitution))

        drug_analogue_indiv = self._indiv(drug_analogue_id)
        substitution_indiv = self._next_uri('middle_ring_substitution_%05i')
        pos_lit = Literal(pos, None, XSD.nonNegativeInteger)

        self._g.add((substitution_indiv, a, OWL.Individual))
        self._g.add((substitution_indiv, a,
                     self._cls_middle_ring_substitution))
        self._g.add((substitution_indiv, self._prop_has_substituent,
                     r_substituent_indiv))
        self._g.add((substitution_indiv, self._prop_subst_pos, pos_lit))

        self._g.add((drug_analogue_indiv, self._prop_has_r_subst,
                     substitution_indiv))

        return

    def _r_subst_1(self, drug_analogue_id, r_substituent_id):
        """Hints:
        !- mode(r_subst_2(+,-)).

        !- mode(r_subst_1(+,-)).

        % substitution R in middle ring

        r_subst_1(a1,h).
        r_subst_1(b1,h).
        r_subst_1(c1,h).
        r_subst_1(d1,h).
        r_subst_1(e1,h).
        r_subst_1(h1,single_alk(1)).
        r_subst_1(i1,single_alk(3)).
        r_subst_1(j1,single_alk(2)).

        r_subst_1(i1,single_alk(3)). --> r_substitution group in drug i1 starts
        with 3 alkyl groups


        r_subst_2(l1,o).
        r_subst_2(m1,double_alk(1)).
        r_subst_2(n1,double_alk(1)).
        r_subst_2(o1,double_alk(1)).
        r_subst_2(p1,aro(1)).
        r_subst_2(q1,aro(1)).

        r_subst_2(n1,double_alk(1)). --> the final alkyl group in drug n1 has
        2 substitutions
        """
        return self._r_subst_pos(drug_analogue_id, 1, r_substituent_id)

    def _r_subst_2(self, drug_analogue_id, r_substituent_id):
        """Hints:

        !- mode(r_subst_2(+,-)).

        r_subst_2(l1,o).
        r_subst_2(m1,double_alk(1)).
        r_subst_2(n1,double_alk(1)).
        r_subst_2(o1,double_alk(1)).
        r_subst_2(p1,aro(1)).
        r_subst_2(q1,aro(1)).

        r_subst_2(n1,double_alk(1)). --> the final alkyl group in drug n1 has
        2 substitutions
        """
        return self._r_subst_pos(drug_analogue_id, 2, r_substituent_id)

    def _r_subst_3(self, drug_analogue_id, r_substituent_id):
        """Hints:

        !- mode(r_subst_3(+,-)).

        r_subst_3(l1,aro(1)).
        r_subst_3(m1,aro(2)).
        r_subst_3(n1,aro(2)).
        r_subst_3(o1,aro(2)).
        """
        return self._r_subst_pos(drug_analogue_id, 3, r_substituent_id)

    def _n_val(self, drug_analogue_id, val):
        """Hints:

        !- mode(n_val(+,-)).

        alk_groups(g1,0).
        r_subst_1(g1,h).
        n_val(g1,1).

        Only used this one time!
        """
        if not isinstance(drug_analogue_id, URIRef):
            drug_analogue_indiv = self._indiv(drug_analogue_id)
        else:
            drug_analogue_indiv = drug_analogue_id

        val_lit = Literal(val, None, XSD.integer)

        self._g.add((drug_analogue_indiv, self._prop_n_val, val_lit))

        return

    def _single_alk(self, num):
        """Hints:

        r_subst_1(f1,h).
        r_subst_1(g1,h).

        r_subst_1(h1,single_alk(1)).
        r_subst_1(i1,single_alk(3)).
        r_subst_1(j1,single_alk(2)).

        r_subst_1(i1,single_alk(3)). --> r_substitution group in drug i1 starts
        with 3 alkyl groups
        """
        r_subst_group_indiv = self._next_uri('r_subst_group_%05i')
        num_single_alk_groups_lit = Literal(num, None, XSD.nonNegativeInteger)

        self._g.add((r_subst_group_indiv, a, OWL.Individual))
        self._g.add((r_subst_group_indiv, a, self._cls_single_alkyl))
        self._g.add((r_subst_group_indiv, self._prop_num_single_alk_groups,
                     num_single_alk_groups_lit))

        return r_subst_group_indiv

    def _double_alk(self, num):
        """Hints:

        r_subst_2(m1,double_alk(1)). --> The final alkyl group in drug m1 has 2
        substitutions
        """
        r_subst_group_indiv = self._next_uri('r_subst_group_%05i')
        num_double_alk_groups_lit = Literal(num, None, XSD.nonNegativeInteger)

        self._g.add((r_subst_group_indiv, a, OWL.Individual))
        self._g.add((r_subst_group_indiv, a, self._cls_double_alkyl))
        self._g.add((r_subst_group_indiv, self._prop_num_double_alk_groups,
                     num_double_alk_groups_lit))

        return r_subst_group_indiv

    def _aro(self, num):
        """Hints:

        r_subst_3(m1,aro(2)). --> drug m1 has two aromatic rings
        """
        r_subst_group_indiv = self._next_uri('r_subst_group_%05i')
        num_aro_rings_lit = Literal(num, None, XSD.nonNegativeInteger)

        self._g.add((r_subst_group_indiv, a, OWL.Individual))
        self._g.add((r_subst_group_indiv, a, self._cls_aromatic_ring))
        self._g.add((r_subst_group_indiv, self._prop_num_arom_rings,
                     num_aro_rings_lit))

        return r_subst_group_indiv

    def _ring_substitutions(self, drug_analogue_id, num):
        """Hints:

        % number of substituents in ring
        % 0 == normal benzene ring

        ring_substitutions(k1,0).
        ring_substitutions(l1,0).
        ring_substitutions(m1,0).
        ring_substitutions(n1,1).
        ring_substitutions(o1,1).
        ring_substitutions(p1,0).
        ring_substitutions(q1,1).

        ring_substitutions(n1,1). --> the aromatic rings of drug n1 have 1
        substitution
        """
        drug_analogue_indiv = self._indiv(drug_analogue_id)
        num_lit = Literal(num, None, XSD.nonNegativeInteger)

        self._g.add((drug_analogue_indiv, self._prop_num_ring_substs, num_lit))

        return

    def _ring_subst_pos(self, drug_analogue_id, pos, substituent_id):
        """Hints:

        !- mode(ring_subst_1(+,-)).

        % substitents in ring
        % ring_subs_Pos(Drug,Substituent)

        ring_subst_4(n1,f).
        ring_subst_3(o1,f).
        ring_subst_2(q1,cl).
        ring_subst_3(r1,cl).
        ring_subst_4(s1,cl).

        ring_subst_4(n1,f). --> the aromatic rings have substitutions at
        position 4
        """
        drug_analogue_indiv = self._indiv(drug_analogue_id)
        ring_subst_indiv = self._next_uri('ring_substitution_%05i')
        pos_lit = Literal(pos, None, XSD.nonNegativeInteger)

        if isinstance(substituent_id, URIRef):
            substituent_indiv = substituent_id
        else:
            substituent_indiv = self._indiv(substituent_id)
            self._g.add((substituent_indiv, a, OWL.Individual))
            self._g.add((substituent_indiv, a, self._cls_chem_component))

        self._g.add((ring_subst_indiv, a, OWL.Individual))
        self._g.add((ring_subst_indiv, a, self._cls_ring_substitution))
        self._g.add((ring_subst_indiv, self._prop_subst_pos, pos_lit))
        self._g.add((ring_subst_indiv, self._prop_has_substituent,
                     substituent_indiv))

        self._g.add((drug_analogue_indiv, self._prop_has_ring_substitution,
                     ring_subst_indiv))

        return

    def _ring_subst_1(self, drug_analogue_id, substituent_id):
        return self._ring_subst_pos(drug_analogue_id, 1, substituent_id)

    def _ring_subst_2(self, drug_analogue_id, substituent_id):
        return self._ring_subst_pos(drug_analogue_id, 2, substituent_id)

    def _ring_subst_3(self, drug_analogue_id, substituent_id):
        return self._ring_subst_pos(drug_analogue_id, 3, substituent_id)

    def _ring_subst_4(self, drug_analogue_id, substituent_id):
        return self._ring_subst_pos(drug_analogue_id, 4, substituent_id)

    def _ring_subst_5(self, drug_analogue_id, substituent_id):
        return self._ring_subst_pos(drug_analogue_id, 5, substituent_id)

    def _ring_subst_6(self, drug_analogue_id, substituent_id):
        return self._ring_subst_pos(drug_analogue_id, 6, substituent_id)

    def _great_ne(self, greater_drug_analogue_id, lesser_drug_analogue_id):
        """Hints:

        great_ne(b1,a1).
        great_ne(b1,c1).
        great_ne(b1,h1).
        great_ne(b1,i1).
        great_ne(b1,ff1).
        great_ne(f1,a1).
        great_ne(f1,c1).
        great_ne(f1,h1).
        """
        greater_drug_analogue_indiv = self._indiv(greater_drug_analogue_id)
        lesser_drug_analogue_indiv = self._indiv(lesser_drug_analogue_id)

        comp_indiv = self._next_uri('comparison%05i')
        self._g.add((comp_indiv, a, OWL.Individual))
        if self._which_kind_of_examples == 'pos':
            self._g.add((comp_indiv, a, self._cls_pos_example))
        else:
            self._g.add((comp_indiv, a, self._cls_neg_example))

        self._g.add((comp_indiv, self._prop_comp_greater,
                     greater_drug_analogue_indiv))
        self._g.add((comp_indiv, self._prop_comp_lesser,
                     lesser_drug_analogue_indiv))

    # </------------------------ converter functions ------------------------->

    _predicate_converters = {
        'alk_groups': _alk_groups,
        'single_alk': _single_alk,
        'double_alk': _double_alk,
        'aro': _aro,
        'r_subst_1': _r_subst_1,
        'r_subst_2': _r_subst_2,
        'r_subst_3': _r_subst_3,
        'ring_substitutions': _ring_substitutions,
        'ring_subst_1': _ring_subst_1,
        'ring_subst_2': _ring_subst_2,
        'ring_subst_3': _ring_subst_3,
        'ring_subst_4': _ring_subst_4,
        'ring_subst_5': _ring_subst_5,
        'ring_subst_6': _ring_subst_6,
        'great_sigma': _great_sigma,
        'sigma': _sigma,
        'bond': _bond,
        'group': _group,
        'polarisable': _polarisable,
        'great_polari': _great_polari,
        'polar': _polar,
        'great_polar': _great_polar,
        'size': _size,
        'great_size': _great_size,
        'flex': _flex,
        'great_flex': _great_flex,
        'h_doner': _h_doner,
        'great_h_don': _great_h_don,
        'pi_acceptor': _pi_acceptor,
        'great_pi_acc': _great_pi_acc,
        'pi_doner': _pi_doner,
        'great_pi_don': _great_pi_don,
        'h_acceptor': _h_acceptor,
        'great_h_acc': _great_h_acc,
        'gt': _dummy,
        'x_subst': _x_subst,
        'n_val': _n_val,
        'great_ne': _great_ne,
    }

    def __init__(self):
        self._determinate_kb_file_name = 'd_alz.b'
        self._pos_file_name = 'amine.f'
        self._neg_file_name = 'amine.n'
        # will be switched to 'neg' when positive examples are done
        self._which_kind_of_examples = 'pos'

        # self._n_determinate_kb_file_name = 'd_alz.b'
        self._g = Graph()
        self._prefix = 'http://dl-learner.org/benchmark/alzheimer/'
        self._ont_prefix = self._prefix + 'ont/'
        self._uri_cntrs = {}
        self._cls_cache = {}
        self._prop_cache = {}
        # classes
        self._cls_drug_analogue = self._cls('DrugAnalogue')
        self._cls_r_subst_grp = self._cls('R-SubstitutionGroup')
        self._cls_single_alkyl = self._cls('SingleAlkylGroup')
        self._cls_double_alkyl = self._cls('DoubleAlkylGroup')
        self._cls_aromatic_ring = self._cls('AromaticRingGroup')
        self._cls_chem_component = self._cls('ChemicalComponent')
        self._cls_substitution = self._cls('Substitution')
        self._cls_substituent = self._cls('Substituent')
        self._cls_ring_substitution = self._cls('RingSubstitution')
        self._cls_middle_ring_substitution = \
            self._cls('MiddleRingSubstitution')
        self._cls_x_substitution = self._cls('XSubstitution')
        self._cls_sigma = self._cls('Sigma')
        self._cls_polarity = self._cls('Polarity')
        self._cls_bond = self._cls('Bond')
        self._cls_group = self._cls('Group')
        self._cls_size = self._cls('Size')
        self._cls_flex = self._cls('Flex')
        self._cls_h_doner = self._cls('H-Doner')
        self._cls_h_acceptor = self._cls('H-Acceptor')
        self._cls_pi_doner = self._cls('Pi-Doner')
        self._cls_pi_acceptor = self._cls('Pi-Acceptor')
        self._cls_polarisable = self._cls('Polarisable')
        self._cls_drug_activity_comparison = \
            self._cls('DrugActivityComparison')
        self._cls_pos_example = self._cls('PositiveExample')
        self._cls_neg_example = self._cls('NegativeExample')

        # properties
        self._prop_num_r_subst_groups = \
            self._p('number_of_r-substitution_groups')
        self._prop_num_alkyl_groups = self._p('number_of_alkyl_groups')
        self._prop_num_single_alk_groups = \
            self._p('number_of_single_alkyl_groups')
        self._prop_num_double_alk_groups = \
            self._p('number_of_double_alkyl_groups')
        self._prop_num_arom_rings = self._p('number_of_aromatic_rings')
        self._prop_has_substitution = self._p('has_substitution')
        self._prop_has_r_subst = self._p('has_middle_ring_substitution')
        self._prop_num_ring_substs = self._p('number_of_ring_substitutions')
        self._prop_subst_pos = self._p('substitution_position')
        self._prop_has_substituent = self._p('has_substituent')
        self._prop_has_ring_substitution = self._p('has_ring_substitution')
        self._prop_sigma_greater_than = self._p('sigma_greater_than')
        self._prop_has_binding_component = self._p('has_binding_component')
        self._prop_first_comp = self._p('first_component')
        self._prop_second_comp = self._p('second_component')
        self._prop_polarisable_greater_than = \
            self._p('polarisable_greater_than')
        self._prop_has_polarity = self._p('has_polarity')
        self._prop_has_group_component = self._p('has_group_component')
        self._prop_has_size = self._p('has_size')
        self._prop_polar_greater_than = self._p('polar_greater_than')
        self._prop_num_components = self._p('number_of_components')
        self._prop_has_flex = self._p('has_flex')
        self._prop_has_h_doner = self._p('has_h-doner')
        self._prop_has_h_acceptor = self._p('has_h-acceptor')
        self._prop_has_pi_doner = self._p('has_pi-doner')
        self._prop_has_pi_acceptor = self._p('has_pi-acceptor')
        self._prop_has_sigma = self._p('has_sigma')
        self._prop_has_polarisable = self._p('has_polarisable')
        self._prop_size_greater_than = self._p('size_greater_than')
        self._prop_flex_greater_than = self._p('flex_greater_than')
        self._prop_h_doner_greater_than = self._p('h-doner_greater_than')
        self._prop_h_acceptor_greater_than = self._p('h-acceptor_greater_than')
        self._prop_pi_donator_greater_than = self._p('pi-donator_greater_than')
        self._prop_pi_acceptor_greater_than = \
            self._p('pi-acceptor_greater_than')
        self._prop_has_x_subst = self._p('has_x_substitution')
        self._prop_n_val = self._p('n_val')
        self._prop_comp_greater = self._p('greater')
        self._prop_comp_lesser = self._p('lesser')

    def _indiv(self, local_part):
        if isinstance(local_part, URIRef):
            return local_part
        else:
            return URIRef(self._prefix + local_part)

    def _p(self, prop):
        p_uri = self._prop_cache.get(prop)

        if p_uri is None:
            p_uri = URIRef(self._ont_prefix + prop)
            self._cls_cache[prop] = p_uri
        return p_uri

    def _next_uri(self, local_part_pattern):
        if self._uri_cntrs.get(local_part_pattern) is None:
            self._uri_cntrs[local_part_pattern] = 0

        cntr = self._uri_cntrs[local_part_pattern] + 1
        self._uri_cntrs[local_part_pattern] = cntr

        return URIRef(self._prefix + local_part_pattern % cntr)

    def _cls(self, cls):
        cls_uri = self._cls_cache.get(cls)

        if cls_uri is None:
            cls_uri = URIRef(self._ont_prefix + cls)
            self._cls_cache[cls] = cls_uri
        return cls_uri

    @staticmethod
    def _path(alz_dir, dataset):
        return os.path.join(alz_dir, dataset)

    @staticmethod
    def _obj_prop(prop, dom, rnge):
        tmp = Graph()

        tmp.add((prop, a, OWL.ObjectProperty))
        tmp.add((prop, RDFS.domain, dom))
        tmp.add((prop, RDFS.range, rnge))

        return tmp

    @staticmethod
    def _dt_prop(prop, dom, rnge):
        tmp = Graph()

        tmp.add((prop, a, OWL.DatatypeProperty))
        tmp.add((prop, RDFS.domain, dom))
        tmp.add((prop, RDFS.range, rnge))

        return tmp

    @staticmethod
    def _subclassof_has_some(subcls, prop, cls2):
        tmp = Graph()
        restr_cls = BNode()

        tmp.add((subcls, RDFS.subClassOf, restr_cls))
        tmp.add((restr_cls, a, OWL.Class))
        tmp.add((restr_cls, a, OWL.Restriction))
        tmp.add((restr_cls, OWL.onProperty, prop))
        tmp.add((restr_cls, OWL.someValuesFrom, cls2))

        return tmp

    def _add_axioms(self):
        g = self._g
        # ------------ classes ------------
        # DrugAnalogue
        g.add((self._cls_drug_analogue, a, OWL.Class))
        # ChemicalComponent
        g.add((self._cls_chem_component, a, OWL.Class))
        # R-SubstitutionGroup
        g.add((self._cls_r_subst_grp, a, OWL.Class))
        g.add((self._cls_r_subst_grp, RDFS.subClassOf,
               self._cls_chem_component))
        # SingleAlkylGroup
        g.add((self._cls_single_alkyl, a, OWL.Class))
        g.add((self._cls_single_alkyl, RDFS.subClassOf, self._cls_r_subst_grp))
        # DoubleAlkylGroup
        g.add((self._cls_double_alkyl, a, OWL.Class))
        g.add((self._cls_double_alkyl, RDFS.subClassOf, self._cls_r_subst_grp))
        # AromaticRing
        g.add((self._cls_aromatic_ring, a, OWL.Class))
        g.add((self._cls_aromatic_ring, RDFS.subClassOf, self._cls_r_subst_grp))
        # Substituent
        g.add((self._cls_substituent, a, OWL.Class))
        g.add((self._cls_substituent, RDFS.subClassOf,
               self._cls_chem_component))
        # Substitution
        g.add((self._cls_substitution, a, OWL.Class))
        # ...substitution_position some xsd:nonNegativeInteger and
        #    position has_substituent some Substituent
        g += self._subclassof_has_some(self._cls_substitution,
                                       self._prop_subst_pos,
                                       XSD.nonNegativeInteger)
        g += self._subclassof_has_some(self._cls_substitution,
                                       self._prop_has_substituent,
                                       self._cls_substituent)
        # RingSubstitution
        g.add((self._cls_ring_substitution, a, OWL.Class))
        g.add((self._cls_ring_substitution, RDFS.subClassOf,
               self._cls_substitution))
        # MiddleRingSubstitution
        g.add((self._cls_middle_ring_substitution, a, OWL.Class))
        g.add((self._cls_middle_ring_substitution, RDFS.subClassOf,
               self._cls_substitution))
        # Sigma
        g.add((self._cls_sigma, a, OWL.Class))
        # Polarity
        g.add((self._cls_polarity, a, OWL.Class))
        # Bond
        g.add((self._cls_bond, a, OWL.Class))
        g.add((self._cls_bond, RDFS.subClassOf, self._cls_chem_component))
        # Group
        g.add((self._cls_group, a, OWL.Class))
        g += self._subclassof_has_some(self._cls_group,
                                       self._prop_has_group_component,
                                       self._cls_chem_component)
        g += self._subclassof_has_some(self._cls_group,
                                       self._prop_num_components,
                                       XSD.nonNegativeInteger)
        g.add((self._cls_group, RDFS.subClassOf, self._cls_chem_component))
        # Size
        g.add((self._cls_size, a, OWL.Class))
        # Flex
        g.add((self._cls_flex, a, OWL.Class))
        # H-Doner
        g.add((self._cls_h_doner, a, OWL.Class))
        # H-Acceptor
        g.add((self._cls_h_acceptor, a, OWL.Class))
        # Pi-Doner
        g.add((self._cls_pi_doner, a, OWL.Class))
        # Pi-Acceptor
        g.add((self._cls_pi_acceptor, a, OWL.Class))
        # Polarisable
        g.add((self._cls_polarisable, a, OWL.Class))
        # XSubstitution
        g.add((self._cls_x_substitution, a, OWL.Class))
        g.add((self._cls_x_substitution, RDFS.subClassOf,
               self._cls_substitution))
        # DrugActivityComparison
        g.add((self._cls_drug_activity_comparison, a, OWL.Class))
        g += self._subclassof_has_some(self._cls_drug_activity_comparison,
                                       self._prop_comp_lesser,
                                       self._cls_drug_analogue)
        g += self._subclassof_has_some(self._cls_drug_activity_comparison,
                                       self._prop_comp_greater,
                                       self._cls_drug_analogue)
        # PositiveExample
        g.add((self._cls_pos_example, a, OWL.Class))
        # NegativeExample
        g.add((self._cls_neg_example, a, OWL.Class))

        # ------------ properties ------------
        # number_of_f-substitution_groups
        g += self._dt_prop(self._prop_num_r_subst_groups,
                           self._cls_r_subst_grp, XSD.nonNegativeInteger)
        # number_of_alkyl_groups
        g += self._dt_prop(self._prop_num_alkyl_groups,
                           self._cls_drug_analogue, XSD.nonNegativeInteger)
        # number_of_single_alkyl_groups
        g.add((self._prop_num_single_alk_groups, RDFS.subPropertyOf,
               self._prop_num_r_subst_groups))
        g += self._dt_prop(self._prop_num_single_alk_groups,
                           self._cls_single_alkyl, XSD.nonNegativeInteger)
        # number_of_double_alkyl_groups
        g.add((self._prop_num_double_alk_groups, RDFS.subPropertyOf,
               self._prop_num_r_subst_groups))
        g += self._dt_prop(self._prop_num_double_alk_groups,
                           self._cls_double_alkyl, XSD.nonNegativeInteger)
        # number_of_aromatic_rings
        g += self._dt_prop(self._prop_num_arom_rings, self._cls_aromatic_ring,
                           XSD.nonNegativeInteger)
        g.add((self._prop_num_arom_rings, RDFS.subPropertyOf,
               self._prop_num_r_subst_groups))
        # has_substitution
        g += self._obj_prop(self._prop_has_substitution,
                            self._cls_drug_analogue, self._cls_substitution)
        # has_middle_ring_substitution
        g += self._obj_prop(self._prop_has_r_subst, self._cls_drug_analogue,
                            self._cls_middle_ring_substitution)
        g.add((self._prop_has_r_subst, RDFS.subPropertyOf,
               self._prop_has_substitution))
        # number_of_ring_substitutions
        g += self._dt_prop(self._prop_num_ring_substs, self._cls_drug_analogue,
                           XSD.nonNegativeInteger)
        # substitution_position
        g += self._dt_prop(self._prop_subst_pos, self._cls_substitution,
                           XSD.nonNegativeInteger)
        # has_substituent
        g += self._obj_prop(self._prop_has_substituent,
                            self._cls_substitution, self._cls_substituent)
        # has_ring_substitution
        g += self._obj_prop(self._prop_has_ring_substitution,
                            self._cls_drug_analogue,
                            self._cls_ring_substitution)
        g.add((self._prop_has_ring_substitution, RDFS.subPropertyOf,
               self._prop_has_substitution))
        # sigma_greater_than
        g += self._obj_prop(self._prop_sigma_greater_than, self._cls_sigma,
                            self._cls_sigma)
        g.add((self._prop_sigma_greater_than, a, OWL.TransitiveProperty))
        # has_binding_component
        g += self._obj_prop(self._prop_has_binding_component, self._cls_bond,
                            self._cls_chem_component)
        # first_component
        g.add((self._prop_first_comp, RDFS.subPropertyOf,
               self._prop_has_binding_component))
        # second_component
        g.add((self._prop_second_comp, RDFS.subPropertyOf,
               self._prop_has_binding_component))
        # has_polarity
        g += self._obj_prop(self._prop_has_polarity, self._cls_chem_component,
                            self._cls_polarity)
        # has_group_component
        g += self._obj_prop(self._prop_has_group_component, self._cls_group,
                            self._cls_chem_component)
        # number_of_components
        g += self._dt_prop(self._prop_num_components, self._cls_group,
                           XSD.nonNegativeInteger)
        # has_size
        g += self._obj_prop(self._prop_has_size, self._cls_chem_component,
                            self._cls_size)
        # polar_greater_than
        g += self._obj_prop(self._prop_polar_greater_than, self._cls_polarity,
                            self._cls_polarity)
        g.add((self._prop_polar_greater_than, a, OWL.TransitiveProperty))
        # has_polarisable
        g += self._obj_prop(self._prop_has_polarisable,
                            self._cls_chem_component, self._cls_polarisable)
        # has_flex
        g += self._obj_prop(self._prop_has_flex, self._cls_chem_component,
                            self._cls_flex)
        # has_h-doner
        g += self._obj_prop(self._prop_has_h_doner, self._cls_chem_component,
                            self._cls_h_doner)
        # has_h-acceptor
        g += self._obj_prop(self._prop_has_h_acceptor,
                            self._cls_chem_component, self._cls_h_acceptor)
        # has_pi-doner
        g += self._obj_prop(self._prop_has_pi_doner, self._cls_chem_component,
                            self._cls_pi_doner)
        # has_pi-acceptor
        g += self._obj_prop(self._prop_has_pi_acceptor,
                            self._cls_chem_component, self._cls_pi_acceptor)
        # has_sigma
        g += self._obj_prop(self._prop_has_sigma, self._cls_chem_component,
                            self._cls_sigma)
        # size_greater_than
        g += self._obj_prop(self._prop_size_greater_than, self._cls_size,
                            self._cls_size)
        g.add((self._prop_size_greater_than, a, OWL.TransitiveProperty))
        # flex_greater_than
        g += self._obj_prop(self._prop_flex_greater_than, self._cls_flex,
                            self._cls_flex)
        g.add((self._prop_flex_greater_than, a, OWL.TransitiveProperty))
        # h-doner_greater_than
        g += self._obj_prop(self._prop_h_doner_greater_than, self._cls_h_doner,
                            self._cls_h_doner)
        g.add((self._prop_h_doner_greater_than, a, OWL.TransitiveProperty))
        # h-acceptor_greater_than
        g += self._obj_prop(self._prop_h_acceptor_greater_than,
                            self._cls_h_acceptor, self._cls_h_acceptor)
        g.add((self._prop_h_acceptor_greater_than, a, OWL.TransitiveProperty))
        # pi-donator_greater_than
        g += self._obj_prop(self._prop_pi_donator_greater_than,
                            self._cls_pi_doner, self._cls_pi_doner)
        g.add((self._prop_pi_donator_greater_than, a, OWL.TransitiveProperty))
        # pi-acceptor_greater_than
        g += self._obj_prop(self._prop_pi_acceptor_greater_than,
                            self._cls_pi_acceptor, self._cls_pi_acceptor)
        g.add((self._prop_pi_acceptor_greater_than, a, OWL.TransitiveProperty))
        # polarisable_greater_than
        g += self._obj_prop(self._prop_polarisable_greater_than,
                            self._cls_polarisable, self._cls_polarisable)
        g.add((self._prop_polarisable_greater_than, a, OWL.TransitiveProperty))
        # n_val
        g += self._dt_prop(self._prop_n_val, self._cls_drug_analogue,
                           XSD.integer)
        # has_x_substitution
        g += self._obj_prop(self._prop_has_x_subst, self._cls_drug_analogue,
                            self._cls_x_substitution)
        g.add((self._prop_has_x_subst, RDFS.subPropertyOf,
               self._prop_has_substitution))
        # greater
        g += self._obj_prop(self._prop_comp_greater,
                            self._cls_drug_activity_comparison,
                            self._cls_drug_analogue)
        # lesser
        g += self._obj_prop(self._prop_comp_lesser,
                            self._cls_drug_activity_comparison,
                            self._cls_drug_analogue)

    def _convert(self, parsed):
        if isinstance(parsed, Fact):
            new_args = []
            for arg in parsed.arguments:
                new_args.append(self._convert(arg))

            conv_fn = self._predicate_converters[parsed.predicate]

            return conv_fn(self, *new_args)
        else:
            return parsed

    def convert(self, alz_dir, output_file_path):
        parser = GolemPrologParser()
        facts = parser.parse_facts(
            self._path(alz_dir, self._determinate_kb_file_name))

        for fact in facts:
            self._convert(fact)

        self._add_axioms()

        pos_facts = parser.parse_facts(
            self._path(alz_dir, self._pos_file_name))

        for pos_fact in pos_facts:
            self._convert(pos_fact)

        self._which_kind_of_examples = 'neg'
        neg_facts = parser.parse_facts(
            self._path(alz_dir, self._neg_file_name))

        for neg_fact in neg_facts:
            self._convert(neg_fact)

        write_graph(self._g, output_file_path)
