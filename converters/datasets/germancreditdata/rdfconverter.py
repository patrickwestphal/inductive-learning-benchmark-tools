from pprint import pprint as pp
from rdflib import BNode
from rdflib import Graph
from rdflib import Literal
from rdflib import RDF
from rdflib import RDFS
from rdflib import OWL
from rdflib import URIRef
from rdflib import XSD

from utils import write_graph

a = RDF.type
xsd_nn_int = XSD.term('nonNegativeInteger')
xsd_bool = XSD.term('boolean')


class GermanCreditData2RDFConverter(object):
    """
    [http://archive.ics.uci.edu/ml/datasets/Statlog+%28German+Credit+Data%29]
    """

    def __init__(self):
        self._g = Graph()
        self._cust_cntr = 1
        self._cust_pattern = 'http://dl-learner/german-credit/customer%03i'
        self._res_prefix = 'http://dl-learner/german-credit/res/'
        self._ont_prefix = 'http://dl-learner/german-credit/ont/'
        self._cust_cls = URIRef(self._ont_prefix + 'Customer')
        self._categories = {}

        # attr classes
        self._attrs = {
            # Attribute 0: (qualitative)
            # Status of existing checking account
            # A11 : ... < 0 DM
            # A12 : 0 <= ... < 200 DM
            # A13 : ... >= 200 DM / salary assignments for at least 1 year
            # A14 : no checking account
            0: {
                'base_cls': URIRef(self._ont_prefix + 'CheckingAccountStatus'),
                'classes': [
                    URIRef(self._ont_prefix + 'CheckingAccountStatus1'),
                    URIRef(self._ont_prefix + 'CheckingAccountStatus2'),
                    URIRef(self._ont_prefix + 'CheckingAccountStatus3'),
                    URIRef(self._ont_prefix + 'NoCheckingAccount')
                ],
                'cls_labels': [
                    Literal('less than 0 DM per salary assignments for at '
                            'least 1 year'),
                    Literal('between 0 (incl.) and 200 (excl.) DM per salary '
                            'assignments for at least 1 year'),
                    Literal('more than or equal to 200 DM per salary '
                            'assignments for at least 1 year'),
                    Literal('no checking account')
                ],
                'property': URIRef(self._ont_prefix +
                                   'hasCheckingAccountStatus')
            },
            # Attribute 1: (numerical)
            # Duration in month
            1: {
                'property': URIRef(self._ont_prefix + 'durationInMonths')
            },
            # Attribute 2: (qualitative)
            # Credit history
            # A30 : no credits taken/ all credits paid back duly
            # A31 : all credits at this bank paid back duly
            # A32 : existing credits paid back duly till now
            # A33 : delay in paying off in the past
            # A34 : critical account/ other credits existing (not at this bank)
            2: {
                'base_cls': URIRef(self._ont_prefix + 'CreditHistory'),
                'classes': [
                    URIRef(self._ont_prefix + 'CreditHistoryType1'),
                    URIRef(self._ont_prefix + 'CreditHistoryType2'),
                    URIRef(self._ont_prefix + 'CreditHistoryType3'),
                    URIRef(self._ont_prefix + 'CreditHistoryType4'),
                    URIRef(self._ont_prefix + 'CreditHistoryType5')
                ],
                'cls_labels': [
                    Literal('no credits taken/ all credits paid back duly'),
                    Literal('all credits at this bank paid back duly'),
                    Literal('existing credits paid back duly till now'),
                    Literal('delay in paying off in the past'),
                    Literal('critical account/ other credits existing (not at '
                            'this bank)')
                ],
                'property': URIRef(self._ont_prefix + 'hasCreditHistory')
            },
            # Attribute 3: (qualitative)
            # Purpose
            # A40 : car (new)
            # A41 : car (used)
            # A42 : furniture/equipment
            # A43 : radio/television
            # A44 : domestic appliances
            # A45 : repairs
            # A46 : education
            # A47 : (vacation - does not exist?)
            # A48 : retraining
            # A49 : business
            # A410 : others
            3: {
                'base_cls': URIRef(self._ont_prefix + 'CreditPurpose'),
                'classes': [
                    URIRef(self._ont_prefix + 'PurposeCarNew'),
                    URIRef(self._ont_prefix + 'PurposeCarUsed'),
                    URIRef(self._ont_prefix + 'PurposeFurnitureEquipment'),
                    URIRef(self._ont_prefix + 'PurposeRadioTelevision'),
                    URIRef(self._ont_prefix + 'PurposeDomesticAppliances'),
                    URIRef(self._ont_prefix + 'PurposeRepairs'),
                    URIRef(self._ont_prefix + 'PurposeEducation'),
                    URIRef(self._ont_prefix + 'PurposeVacation'),
                    URIRef(self._ont_prefix + 'PurposeRetraining'),
                    URIRef(self._ont_prefix + 'PurposeBusiness'),
                    URIRef(self._ont_prefix + 'PurposeOther')
                ],
                'cls_labels': [
                    Literal('car (new)'),
                    Literal('car (used)'),
                    Literal('furniture/equipment'),
                    Literal('radio/television'),
                    Literal('domestic appliances'),
                    Literal('repairs'),
                    Literal('education'),
                    Literal('vacation'),
                    Literal('retraining'),
                    Literal('business'),
                    Literal('others')
                ],
                'property': URIRef(self._ont_prefix + 'creditPurpose')
            },
            # Attribute 4: (numerical)
            # Credit amount
            4: {
                'property': URIRef(self._ont_prefix + 'creditAmount')
            },
            # Attibute 5: (qualitative)
            # Savings account/bonds
            # A61 : ... < 100 DM
            # A62 : 100 <= ... < 500 DM
            # A63 : 500 <= ... < 1000 DM
            # A64 : .. >= 1000 DM
            # A65 : unknown/ no savings account
            5: {
                'base_cls': URIRef(self._ont_prefix +
                                   'SavingsAccountCategory'),
                'classes': [
                    URIRef(self._ont_prefix + 'SavingsAccountCategory1'),
                    URIRef(self._ont_prefix + 'SavingsAccountCategory2'),
                    URIRef(self._ont_prefix + 'SavingsAccountCategory3'),
                    URIRef(self._ont_prefix + 'SavingsAccountCategory4'),
                    URIRef(self._ont_prefix + 'SavingsAccountCategory5'),
                ],
                'cls_labels': [
                    Literal('... < 100 DM'),
                    Literal('100 <= ... < 500 DM'),
                    Literal('500 <= ... < 1000 DM'),
                    Literal('.. >= 1000 DM'),
                    Literal('unknown/ no savings account')
                ],
                'property': URIRef(self._ont_prefix + 'savingsAccountCategory')
            },
            # Attribute 6: (qualitative)
            # Present employment since
            # A71 : unemployed
            # A72 : ... < 1 year
            # A73 : 1 <= ... < 4 years
            # A74 : 4 <= ... < 7 years
            # A75 : .. >= 7 years
            6: {
                'base_cls': URIRef(self._ont_prefix +
                                   'EmploymentDurationCategory'),
                'classes': [
                    URIRef(self._ont_prefix + 'EmploymentDurationCategory1'),
                    URIRef(self._ont_prefix + 'EmploymentDurationCategory2'),
                    URIRef(self._ont_prefix + 'EmploymentDurationCategory3'),
                    URIRef(self._ont_prefix + 'EmploymentDurationCategory4'),
                    URIRef(self._ont_prefix + 'EmploymentDurationCategory5')
                ],
                'cls_labels': [
                    Literal('unemployed'),
                    Literal('... < 1 year'),
                    Literal('1 <= ... < 4 years'),
                    Literal('4 <= ... < 7 years'),
                    Literal('.. >= 7 years')
                ],
                'property': URIRef(self._ont_prefix +
                                   'employmentDurationCategory')
            },
            # Attribute 7: (numerical)
            # Installment rate in percentage of disposable income
            7: {
                'property':
                    URIRef(self._ont_prefix +
                           'installmentRateInPercentageOfDisposableIncome')
            },
            # Attribute 8: (qualitative)
            # Personal status and sex
            # A91 : male : divorced/separated
            # A92 : female : divorced/separated/married
            # A93 : male : single
            # A94 : male : married/widowed
            # A95 : female : single
            8: {
                'base_cls': URIRef(self._ont_prefix +
                                   'PersonalStatusAndSexCategory'),
                'classes': [
                    URIRef(self._ont_prefix + 'SeparatedMale'),
                    URIRef(self._ont_prefix + 'MarriedOrSeparatedFemale'),
                    URIRef(self._ont_prefix + 'SingleMale'),
                    URIRef(self._ont_prefix + 'MarriedOrWidowedMale'),
                    URIRef(self._ont_prefix + 'SingeFemale')
                ],
                'cls_labels': [
                    Literal('male : divorced/separated'),
                    Literal('female : divorced/separated/married'),
                    Literal('male : single'),
                    Literal('male : married/widowed'),
                    Literal('female : single')
                ],
                'property': URIRef(self._ont_prefix +
                                   'hasPersonalStatusAndSex')
            },
            # Attribute 9: (qualitative)
            # Other debtors / guarantors
            # A101 : none
            # A102 : co-applicant
            # A103 : guarantor
            9: {
                'base_cls': URIRef(self._ont_prefix +
                                   'OtherDebtorsOrGuarantorsCategory'),
                'classes': [
                    URIRef(self._ont_prefix +
                           'NoOtherDebtorsOrGuarantors'),
                    URIRef(self._ont_prefix +
                           'CoApplicant'),
                    URIRef(self._ont_prefix +
                           'Guarantor')
                ],
                'cls_labels': [
                    Literal('none'),
                    Literal('co-applicant'),
                    Literal('guarantor')
                ],
                'property': URIRef(self._ont_prefix +
                                   'otherDebtorsGuarantorsCategory')
            },
            # Attribute 10: (numerical)
            # Present residence since
            10: {
                'property': URIRef(self._ont_prefix + 'presentResidenceSince')
            },
            # Attribute 11: (qualitative)
            # Property
            # A121 : real estate
            # A122 : if not A121 : building society savings agreement/ life
            #        insurance
            # A123 : if not A121/A122 : car or other, not in attribute 6
            # A124 : unknown / no property
            11: {
                'base_cls': URIRef(self._ont_prefix + 'Property'),
                'classes': [
                    URIRef(self._ont_prefix + 'RealEstate'),
                    URIRef(self._ont_prefix + 'BuildingSocietySavingsAgreement'
                                              'OrLifeInsurance'),
                    URIRef(self._ont_prefix + 'CorOrOther'),
                    URIRef(self._ont_prefix + 'PropertyNotKnown')
                ],
                'cls_labels': [
                    Literal('real estate'),
                    Literal(
                        'building society savings agreement/ life insurance'),
                    Literal('car or other'),
                    Literal('unknown / no property')
                ],
                'property': URIRef(self._ont_prefix + 'hasProperty')
            },
            # Attribute 12: (numerical)
            # Age in years
            12: {
                'property': URIRef(self._ont_prefix + 'ageInYears')
            },
            # Attribute 13: (qualitative)
            # Other installment plans
            # A141 : bank
            # A142 : stores
            # A143 : none
            13: {
                'base_cls': URIRef(self._ont_prefix + 'InstallmentPlan'),
                'classes': [
                    URIRef(self._ont_prefix + 'Bank'),
                    URIRef(self._ont_prefix + 'Stores'),
                    URIRef(self._ont_prefix + 'NoInstallmentPlan')
                ],
                'cls_labels': [
                    Literal('bank'),
                    Literal('stores'),
                    Literal('none')
                ],
                'property': URIRef(self._ont_prefix + 'otherInstallmentPlans')
            },
            # Attribute 14: (qualitative)
            # Housing
            # A151 : rent
            # A152 : own
            # A153 : for free
            14: {
                'base_cls': URIRef(self._ont_prefix + 'Housing'),
                'classes': [
                    URIRef(self._ont_prefix + 'Rent'),
                    URIRef(self._ont_prefix + 'OwnHouse'),
                    URIRef(self._ont_prefix + 'FreeHousing')
                ],
                'cls_labels': [
                    Literal('rent'),
                    Literal('own'),
                    Literal('for free')
                ],
                'property': URIRef(self._ont_prefix + 'hasHousing')
            },
            # Attribute 15: (numerical)
            # Number of existing credits at this bank
            15: {
                'property': URIRef(self._ont_prefix +
                                   'nrOfExistingCreditsAtThisBank')
            },
            # Attribute 16: (qualitative)
            # Job
            # A171 : unemployed/ unskilled - non-resident
            # A172 : unskilled - resident
            # A173 : skilled employee / official
            # A174 : management/ self-employed/
            # highly qualified employee/ officer
            16: {
                'base_cls': URIRef(self._ont_prefix + 'JobCategory'),
                'classes': [
                    URIRef(self._ont_prefix + 'LowQualityJobNonResident'),
                    URIRef(self._ont_prefix + 'LowQualityJobResident'),
                    URIRef(self._ont_prefix + 'MediumQualityJob'),
                    URIRef(self._ont_prefix + 'HighQualityJob'),
                ],
                'cls_labels': [
                    Literal('unemployed/ unskilled - non-resident'),
                    Literal('unskilled - resident'),
                    Literal('skilled employee / official'),
                    Literal('management/ self-employed / highly qualified '
                            'employee/ officer')
                ],
                'property': URIRef(self._ont_prefix + 'hasJob')
            },
            # Attribute 17: (numerical)
            # Number of people being liable to provide maintenance for
            17: {
                'property': URIRef(self._ont_prefix +
                                   'numPeopleLiableToProvideMaintenanceFor')
            },
            # Attribute 18: (qualitative)
            # Telephone
            # A191 : none
            # A192 : yes, registered under the customers name
            18: {
                'base_cls': URIRef(self._ont_prefix +
                                   'TelephoneConnectionCategory'),
                'classes': [
                    URIRef(self._ont_prefix + 'NoTelephoneConnection'),
                    URIRef(self._ont_prefix +
                           'TelephoneRegisteredUnderCustomersName')
                ],
                'cls_labels': [
                    Literal('none'),
                    Literal('yes, registered under the customers name')
                ],
                'property': URIRef(self._ont_prefix +
                                   'hasTelephoneConnectionType')
            }
        }
        # Attribute 19: (qualitative)
        # foreign worker
        # A201 : yes
        # A202 : no
        # - cannot be handled in generic fashion -
        self._p19 = URIRef(self._ont_prefix + 'isForeignWorker')

        self._attr2uri = {
            'A11': self._attrs[0]['classes'][0],
            'A12': self._attrs[0]['classes'][1],
            'A13': self._attrs[0]['classes'][2],
            'A14': self._attrs[0]['classes'][3],
            'A30': self._attrs[2]['classes'][0],
            'A31': self._attrs[2]['classes'][1],
            'A32': self._attrs[2]['classes'][2],
            'A33': self._attrs[2]['classes'][3],
            'A34': self._attrs[2]['classes'][4],
            'A40': self._attrs[3]['classes'][0],
            'A41': self._attrs[3]['classes'][1],
            'A42': self._attrs[3]['classes'][2],
            'A43': self._attrs[3]['classes'][3],
            'A44': self._attrs[3]['classes'][4],
            'A45': self._attrs[3]['classes'][5],
            'A46': self._attrs[3]['classes'][6],
            'A47': self._attrs[3]['classes'][7],
            'A48': self._attrs[3]['classes'][8],
            'A49': self._attrs[3]['classes'][9],
            'A410': self._attrs[3]['classes'][10],
            'A61': self._attrs[5]['classes'][0],
            'A62': self._attrs[5]['classes'][1],
            'A63': self._attrs[5]['classes'][2],
            'A64': self._attrs[5]['classes'][3],
            'A65': self._attrs[5]['classes'][4],
            'A71': self._attrs[6]['classes'][0],
            'A72': self._attrs[6]['classes'][1],
            'A73': self._attrs[6]['classes'][2],
            'A74': self._attrs[6]['classes'][3],
            'A75': self._attrs[6]['classes'][4],
            'A91': self._attrs[8]['classes'][0],
            'A92': self._attrs[8]['classes'][1],
            'A93': self._attrs[8]['classes'][2],
            'A94': self._attrs[8]['classes'][3],
            'A95': self._attrs[8]['classes'][4],
            'A101': self._attrs[9]['classes'][0],
            'A102': self._attrs[9]['classes'][1],
            'A103': self._attrs[9]['classes'][2],
            'A121': self._attrs[11]['classes'][0],
            'A122': self._attrs[11]['classes'][1],
            'A123': self._attrs[11]['classes'][2],
            'A124': self._attrs[11]['classes'][3],
            'A141': self._attrs[13]['classes'][0],
            'A142': self._attrs[13]['classes'][1],
            'A143': self._attrs[13]['classes'][2],
            'A151': self._attrs[14]['classes'][0],
            'A152': self._attrs[14]['classes'][1],
            'A153': self._attrs[14]['classes'][2],
            'A171': self._attrs[16]['classes'][0],
            'A172': self._attrs[16]['classes'][1],
            'A173': self._attrs[16]['classes'][2],
            'A174': self._attrs[16]['classes'][3],
            'A191': self._attrs[18]['classes'][0],
            'A192': self._attrs[18]['classes'][1]
        }

    def _next_customer_res(self):
        iri_str = self._cust_pattern % self._cust_cntr
        self._cust_cntr += 1

        return URIRef(iri_str)

    def _add_ont_defs(self):
        self._g.add((self._cust_cls, a, OWL.Class))

        for attr_item in self._attrs.values():
            p = attr_item['property']

            if attr_item.get('base_cls') is not None:
                # categorical attributes
                base_cls = attr_item['base_cls']
                clss = attr_item['classes']
                lbls = attr_item['cls_labels']

                self._g.add((base_cls, a, OWL.Class))

                for i in range(len(clss)):
                    cls = clss[i]
                    lbl = lbls[i]

                    self._g.add((cls, a, OWL.Class))
                    self._g.add((cls, RDFS.subClassOf, base_cls))
                    self._g.add((cls, RDFS.label, lbl))

                self._g.add((p, a, OWL.ObjectProperty))
                self._g.add((p, RDFS.domain, self._cust_cls))
                self._g.add((p, RDFS.range, base_cls))

            else:
                # numeric attributes
                self._g.add((p, a, OWL.DatatypeProperty))
                self._g.add((p, RDFS.domain, self._cust_cls))
                self._g.add((p, RDFS.range, xsd_nn_int))

        # Attribute 20: (qualitative)
        # foreign worker
        # A201 : yes
        # A202 : no
        self._g.add((self._p19, a, OWL.DatatypeProperty))
        self._g.add((self._p19, a, OWL.FunctionalProperty))
        self._g.add((self._p19, RDFS.domain, self._cust_cls))
        self._g.add((self._p19, RDFS.range, xsd_bool))

    @staticmethod
    def _has_some(res, prop, cls):
        tmp_g = Graph()
        res_cls = BNode()

        tmp_g.add((res, a, res_cls))
        tmp_g.add((res_cls, a, OWL.Class))
        tmp_g.add((res_cls, a, OWL.Restriction))
        tmp_g.add((res_cls, OWL.onProperty, prop))
        tmp_g.add((res_cls, OWL.someValuesFrom, cls))

        return tmp_g

    def _add_example(self, uri, category):
        if self._categories.get(category) is None:
            self._categories[category] = []

        self._categories[category].append(str(uri))

    def convert(self, input_file_path, output_file_path):
        self._add_ont_defs()

        with open(input_file_path) as f:
            for line in f:
                parts = line.strip().split(' ')

                if len(parts) == 1:
                    continue

                customer = self._next_customer_res()
                self._g.add((customer, a, self._cust_cls))

                # Attribute 0: Status of existing checking account
                cls = self._attr2uri[parts[0]]
                has_some_status = self._has_some(
                    customer, self._attrs[0]['property'], cls)
                self._g += has_some_status

                # Attribute 1: Duration in month
                l1 = Literal(parts[1], None, xsd_nn_int)
                self._g.add((customer, self._attrs[1]['property'], l1))

                # Attribute 2: Credit history
                cls = self._attr2uri[parts[2]]
                has_some_history = self._has_some(
                    customer, self._attrs[2]['property'], cls)
                self._g += has_some_history

                # Attribute 3: Purpose
                cls = self._attr2uri[parts[3]]
                has_some_purpose = self._has_some(
                    customer, self._attrs[3]['property'], cls)
                self._g += has_some_purpose

                # Attribute 4: Credit amount
                l4 = Literal(parts[4], None, xsd_nn_int)
                self._g.add((customer, self._attrs[4]['property'], l4))

                # Attibute 5: Savings account/bonds
                cls = self._attr2uri[parts[5]]
                has_some_sa_category = self._has_some(
                    customer, self._attrs[5]['property'], cls)
                self._g += has_some_sa_category

                # Attribute 6: Present employment since
                cls = self._attr2uri[parts[6]]
                has_some_deployment_duration_category = self._has_some(
                    customer, self._attrs[6]['property'], cls)
                self._g += has_some_deployment_duration_category

                # Attribute 7: Installment rate in percentage of disposable
                # income
                l7 = Literal(parts[7], None, xsd_nn_int)
                self._g.add((customer, self._attrs[7]['property'], l7))

                # Attribute 8: Personal status and sex
                cls = self._attr2uri[parts[8]]
                has_some_pss_category = self._has_some(
                    customer, self._attrs[8]['property'], cls)
                self._g += has_some_pss_category

                # Attribute 9: Other debtors / guarantors
                cls = self._attr2uri[parts[9]]
                has_some_dg_category = self._has_some(
                    customer, self._attrs[9]['property'], cls)
                self._g += has_some_dg_category

                # Attribute 10: Present residence since
                l10 = Literal(parts[10], None, xsd_nn_int)
                self._g.add((customer, self._attrs[10]['property'], l10))

                # Attribute 11: Property
                cls = self._attr2uri[parts[11]]
                has_some_prop_category = self._has_some(
                    customer, self._attrs[11]['property'], cls)
                self._g += has_some_prop_category

                # Attribute 12: Age in years
                l12 = Literal(parts[12], None, xsd_nn_int)
                self._g.add((customer, self._attrs[12]['property'], l12))

                # Attribute 13: Other installment plans
                cls = self._attr2uri[parts[13]]
                has_some_inst_plan = self._has_some(
                    customer, self._attrs[13]['property'], cls)
                self._g += has_some_inst_plan

                # Attribute 14: Housing
                cls = self._attr2uri[parts[14]]
                has_some_housing = self._has_some(
                    customer, self._attrs[14]['property'], cls)
                self._g += has_some_housing

                # Attribute 15: Number of existing credits at this bank
                l15 = Literal(parts[15], None, xsd_nn_int)
                self._g.add((customer, self._attrs[15]['property'], l15))

                # Attribute 16: Job
                cls = self._attr2uri[parts[16]]
                has_some_job_category = self._has_some(
                    customer, self._attrs[16]['property'], cls)
                self._g += has_some_job_category

                # Attribute 17: Number of people being liable to provide
                # maintenance for
                l17 = Literal(parts[17], None, xsd_nn_int)
                self._g.add((customer, self._attrs[17]['property'], l17))

                # Attribute 18: Telephone
                cls = self._attr2uri[parts[18]]
                has_some_phone_conn_type = self._has_some(
                    customer, self._attrs[18]['property'], cls)
                self._g += has_some_phone_conn_type

                # Attribute 19: foreign worker
                v19 = parts[19]
                if v19 == 'A201':
                    v = 'true'
                else:
                    v = 'false'
                l19 = Literal(v, None, xsd_bool)
                self._g.add((customer, self._p19, l19))

                self._add_example(customer, parts[20])
        write_graph(self._g, output_file_path)

        pp(self._categories)
