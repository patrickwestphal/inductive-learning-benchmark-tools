import os


class GermanCreditData2PrologConverter(object):
    def __init__(self):
        self._rules = []
        self._const_cntr = 1
        self._const_pattern = 'const%03i'

        self._attr_comments = {
            'checkingAccountStatus1':
                'less than 0 DM per salary assignments for at least 1 year',
            'CheckingAccountStatus2':
                'between 0 (incl.) and 200 (excl.) DM per salary assignments '
                'for at least 1 year',
            'CheckingAccountStatus3':
                'more than or equal to 200 DM per salary assignments for at '
                'least 1 year',
            'NoCheckingAccount':
                'no checking account',
            'creditHistoryType1':
                'no credits taken/ all credits paid back duly',
            'creditHistoryType2':
                'all credits at this bank paid back duly',
            'creditHistoryType3':
                'existing credits paid back duly till now',
            'creditHistoryType4':
                'delay in paying off in the past',
            'creditHistoryType5':
                'critical account/ other credits existing (not at this bank)',
            'purposeCarNew': 'car (new)',
            'purposeCarUsed': 'car (used)',
            'purposeFurnitureEquipment': 'furniture/equipment',
            'purposeRadioTelevision': 'radio/television',
            'purposeDomesticAppliances': 'domestic appliances',
            'purposeRepairs': 'repairs',
            'purposeEducation': 'education',
            'purposeVacation': 'vacation',
            'purposeRetraining': 'retraining',
            'purposeBusiness': 'business',
            'purposeOther': 'others',
            'savingsAccountCategory1': '... < 100 DM',
            'savingsAccountCategory2': '100 <= ... < 500 DM',
            'savingsAccountCategory3': '500 <= ... < 1000 DM',
            'savingsAccountCategory4': '.. >= 1000 DM',
            'savingsAccountCategory5': 'unknown/ no savings account',
            'employmentDurationCategory1': 'unemployed',
            'employmentDurationCategory2': '... < 1 year',
            'employmentDurationCategory3': '1 <= ... < 4 years',
            'employmentDurationCategory4': '4 <= ... < 7 years',
            'employmentDurationCategory5': '.. >= 7 years',
            'separatedMale': 'male : divorced/separated',
            'marriedOrSeparatedFemale': 'female : divorced/separated/married',
            'singleMale': 'male : single',
            'marriedOrWidowedMale': 'male : married/widowed',
            'singeFemale': 'female : single',
            'noOtherDebtorsOrGuarantors': 'none',
            'coApplicant': 'co-applicant',
            'guarantor': 'guarantor',
        }

        self._attr_data = {
            # Attribute 0: (qualitative)
            # Status of existing checking account
            # A11 : ... < 0 DM
            # A12 : 0 <= ... < 200 DM
            # A13 : ... >= 200 DM / salary assignments for at least 1 year
            # A14 : no checking account
            'A11': 'checkingAccountStatus1',
            'A12': 'checkingAccountStatus2',
            'A13': 'checkingAccountStatus3',
            'A14': 'noCheckingAccount',

            # Attribute 1: (numerical)
            # Duration in month
            # -- actual value used --

            # Attribute 2: (qualitative)
            # Credit history
            # A30 : no credits taken/ all credits paid back duly
            # A31 : all credits at this bank paid back duly
            # A32 : existing credits paid back duly till now
            # A33 : delay in paying off in the past
            # A34 : critical account/ other credits existing (not at this bank)
            'A30': 'creditHistoryType1',
            'A31': 'creditHistoryType2',
            'A32': 'creditHistoryType3',
            'A33': 'creditHistoryType4',
            'A34': 'creditHistoryType5',

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
            'A40': 'purposeCarNew',
            'A41': 'purposeCarUsed',
            'A42': 'purposeFurnitureEquipment',
            'A43': 'purposeRadioTelevision',
            'A44': 'purposeDomesticAppliances',
            'A45': 'purposeRepairs',
            'A46': 'purposeEducation',
            'A47': 'purposeVacation',
            'A48': 'purposeRetraining',
            'A49': 'purposeBusiness',
            'A410': 'purposeOther',

            # Attribute 4: (numerical)
            # Credit amount
            # -- actual value used --

            # Attibute 5: (qualitative)
            # Savings account/bonds
            # A61 : ... < 100 DM
            # A62 : 100 <= ... < 500 DM
            # A63 : 500 <= ... < 1000 DM
            # A64 : .. >= 1000 DM
            # A65 : unknown/ no savings account
            'A61': 'savingsAccountCategory1',
            'A62': 'savingsAccountCategory2',
            'A63': 'savingsAccountCategory3',
            'A64': 'savingsAccountCategory4',
            'A65': 'savingsAccountCategory5',

            # Attribute 6: (qualitative)
            # Present employment since
            # A71 : unemployed
            # A72 : ... < 1 year
            # A73 : 1 <= ... < 4 years
            # A74 : 4 <= ... < 7 years
            # A75 : .. >= 7 years
            'A71': 'employmentDurationCategory1',
            'A72': 'employmentDurationCategory2',
            'A73': 'employmentDurationCategory3',
            'A74': 'employmentDurationCategory4',
            'A75': 'employmentDurationCategory5',

            # Attribute 7: (numerical)
            # Installment rate in percentage of disposable income
            # -- actual value used --

            # Attribute 8: (qualitative)
            # Personal status and sex
            # A91 : male : divorced/separated
            # A92 : female : divorced/separated/married
            # A93 : male : single
            # A94 : male : married/widowed
            # A95 : female : single
            'A91': 'separatedMale',
            'A92': 'marriedOrSeparatedFemale',
            'A93': 'singleMale',
            'A94': 'marriedOrWidowedMale',
            'A95': 'singeFemale',

            # Attribute 9: (qualitative)
            # Other debtors / guarantors
            # A101 : none
            # A102 : co-applicant
            # A103 : guarantor
            'A101': 'noOtherDebtorsOrGuarantors',
            'A102': 'coApplicant',
            'A103': 'guarantor',

            # Attribute 10: (numerical)
            # Present residence since

            # Attribute 11: (qualitative)
            # Property
            # A121 : real estate
            # A122 : if not A121 : building society savings agreement/ life
            #        insurance
            # A123 : if not A121/A122 : car or other, not in attribute 6
            # A124 : unknown / no property

            # Attribute 12: (numerical)
            # Age in years

            # Attribute 13: (qualitative)
            # Other installment plans
            # A141 : bank
            # A142 : stores
            # A143 : none

            # Attribute 14: (qualitative)
            # Housing
            # A151 : rent
            # A152 : own
            # A153 : for free

            # Attribute 15: (numerical)
            # Number of existing credits at this bank

            # Attribute 16: (qualitative)
            # Job
            # A171 : unemployed/ unskilled - non-resident
            # A172 : unskilled - resident
            # A173 : skilled employee / official
            # A174 : management/ self-employed/
            # highly qualified employee/ officer

            # Attribute 17: (numerical)
            # Number of people being liable to provide maintenance for

            # Attribute 18: (qualitative)
            # Telephone
            # A191 : none
            # A192 : yes, registered under the customers name

            # Attribute 19: (qualitative)
            # foreign worker
            # A201 : yes
            # A202 : no
        }

        self._predicates = [
            'hasCheckingAccountStatus',
            'durationInMonths',
            'hasCreditHistory',
            'creditPurpose',
            'creditAmount',
            'savingsAccountCategory',
            'employmentDurationCategory',
            'installmentRateInPercentageOfDisposableIncome',
            'hasPersonalStatusAndSex',
            'otherDebtorsGuarantorsCategory',
            'presentResidenceSince'
        ]

    def _next_const(self):
        const = self._const_pattern % self._const_cntr
        self._const_cntr += 1
        return const

    def _add_comments(self):
        for val, comment in self._attr_comments.items():
            self._rules.append('%% %s: %s' % (val, comment))

    def convert(self, input_file_path, output_file_path):
        with open(input_file_path) as f:
            for line in f:
                parts = line.strip().split(' ')

                if len(parts) == 1:
                    continue

                const = self._next_const()

                for i in range(len(parts)):
                    if i > 10:
                        break
                    p = self._predicates[i]
                    val = self._attr_data.get(parts[i], parts[i])
                    self._rules.append('%s(%s, %s).' % (p, const, val))

        self._add_comments()

        with open(output_file_path, 'w') as o:
            for rule in self._rules:
                o.write(rule)
                o.write(os.linesep)