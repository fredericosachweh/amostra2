# -*- encoding: utf-8 -*-
import decimal
from decimal import Decimal as D


from django.test import TestCase
from django.core.management import call_command, CommandError

from exercises import models


class CategoriesTestCase(TestCase):
    """
    Data autogeneration test.
    """
    fixtures = [
        'exercises_categories.json',
    ]

    def setUp(self):
        pass

    def compare(self, exercise, group, match, joiner='', tabindex=None):
        """
        Given an exercise group or questions or answers, turn it into a string
        and compares with the match string.
        """
        values = exercise.questions.get(group, exercise.answers.get(group, []))
        concat = joiner.join([unicode(x.value) for x in values])
        self.assertEqual(concat, match)

        if tabindex:
            indexes = [x.tabindex for x in values]
            self.assertEqual(tabindex, indexes)
        return values

    def compare_tags(self, exercise, *tags):
        exercise_tags = sorted(exercise.tags.split(','))
        self.assertEqual(exercise_tags, sorted(tags))

    def convert_operation(self, command, operation, **kwargs):
        models.Exercise.objects.all().delete()  # clear any previously created
        call_command(command, operation=operation, **kwargs)
        exercises = list(models.Exercise.objects.all())
        if len(exercises) == 1:
            return exercises[0]
        else:
            return exercises

    def test_addition(self):
        e = self.convert_operation('createaddition', '936+487')
        self.assertEqual(e.filter1, 936)
        self.assertEqual(e.filter2, 487)
        self.compare(e, 'support', '11')   #    11
        self.compare(e, 'line1', '936')    #    936
        self.compare(e, 'line2', '487')    # +  487
        self.compare(e, 'result', '1423')  # = 1423

        e = self.convert_operation('createaddition', '93+486')
        self.assertEqual(e.filter1, 93)
        self.assertEqual(e.filter2, 486)
        self.compare(e, 'support', '10')  #   10
        self.compare(e, 'line1', '93')    #    93
        self.compare(e, 'line2', '486')   # + 487
        self.compare(e, 'result', '579')  # = 580

        e = self.convert_operation('createaddition', '215+24')
        self.assertEqual(e.filter1, 215)
        self.assertEqual(e.filter2, 24)
        self.compare(e, 'support', '00')  #   00
        self.compare(e, 'line1', '215')   #   215
        self.compare(e, 'line2', '24')    # +  24
        self.compare(e, 'result', '239')  # = 239

    def test_additionthreeaddends(self):
        e = self.convert_operation('createadditionthreeaddends', '4+3+9')
        self.assertEqual(e.filter1, 3)
        self.assertEqual(e.filter2, 9)
        self.compare(e, 'line1', '4')                      #    4
        self.compare(e, 'line2', '3')                      # +  3
        self.compare(e, 'line3', '9')                      # +  9
        self.compare(e, 'result', '16', tabindex=[2, 1])   # = 16

        e = self.convert_operation('createadditionthreeaddends', '69+55+57')
        self.assertEqual(e.filter1, 55)
        self.assertEqual(e.filter2, 69)
        self.compare(e, 'support', '2', tabindex=[2])          #     2
        self.compare(e, 'line1', '69')                         #    69
        self.compare(e, 'line2', '55')                         # +  55
        self.compare(e, 'line3', '57')                         # +  57
        self.compare(e, 'result', '181', tabindex=[4, 3, 1])   # = 181

        e = self.convert_operation('createadditionthreeaddends', '789+295+690')
        self.assertEqual(e.filter1, 295)
        self.assertEqual(e.filter2, 789)
        self.compare(e, 'support', '21', tabindex=[4, 2])          #    21
        self.compare(e, 'line1', '789')                            #    789
        self.compare(e, 'line2', '295')                            # +  295
        self.compare(e, 'line3', '690')                            # +  690
        self.compare(e, 'result', '1774', tabindex=[6, 5, 3, 1])   # = 1774

        e = self.convert_operation('createadditionthreeaddends', '78+5+344')
        self.assertEqual(e.filter1, 5)
        self.assertEqual(e.filter2, 344)
        self.compare(e, 'support', '11', tabindex=[4, 2])       #   11
        self.compare(e, 'line1', '78')                          #    78
        self.compare(e, 'line2', '5')                           # +   5
        self.compare(e, 'line3', '344')                         # + 344
        self.compare(e, 'result', '427', tabindex=[5, 3, 1])    # = 427

        e = self.convert_operation('createadditionthreeaddends', '72+2+342')
        self.assertEqual(e.filter1, 2)
        self.assertEqual(e.filter2, 342)
        support = self.compare(e, 'support', '10', tabindex=[4, 2])  #   10
        self.compare(e, 'line1', '72')                               #    72
        self.compare(e, 'line2', '2')                                # +   2
        self.compare(e, 'line3', '342')                              # + 342
        self.compare(e, 'result', '416', tabindex=[5, 3, 1])         # = 416

        # asserts that when the support answer isn't needed (zero), his type is
        # digit_or_blank to accept an empty string
        self.assertEqual(support[1].type, 'digit_or_blank')

    def test_additionexpressions(self):
        e = self.convert_operation('createadditionexpressions', '12+3-2', terms=3)
        self.assertEqual(e.filter1, 2)   # min value
        self.assertEqual(e.filter2, 12)  # max value
        self.compare(e, 'exp', ',12,+,3,-,2', joiner=',')  # blank space at first instead of a plus sign
        self.compare(e, 'result', '15,13', joiner=',')
        self.compare_tags(e, 'inicio-posit', 'result-posit')

        e = self.convert_operation('createadditionexpressions', '-3+5-9+4', terms=4)
        self.assertEqual(e.filter1, 3)  # min value
        self.assertEqual(e.filter2, 9)  # max value
        self.compare(e, 'exp', '-,3,+,5,-,9,+,4', joiner=',')
        self.compare(e, 'result', '2,-7,-3', joiner=',')
        self.compare_tags(e, 'inicio-negat', 'result-negat')

    def test_additionexpressionspotentiation(self):
        e = self.convert_operation('createadditionexpressionspotentiation', '4^2+4-2^3-10', terms=4)
        self.assertEqual(e.filter1, 2)   # min value
        self.assertEqual(e.filter2, 10)  # max value
        self.compare(e, 'exp', '+,4,^,2,+,4,-,2,^,3,-,10', joiner=',')  # blank space at first instead of a plus sign
        self.compare(e, 'result', '16,8,20,12,2', joiner=',', tabindex=[1, 2, 3, 4, 5])
        self.compare_tags(e, 'inicio-posit', 'result-posit')

        e = self.convert_operation('createadditionexpressionspotentiation', '-3^2+5+9^3+4', terms=4)
        self.assertEqual(e.filter1, 2)  # min value
        self.assertEqual(e.filter2, 9)  # max value
        self.compare(e, 'exp', '-,3,^,2,+,5,+,9,^,3,+,4', joiner=',')
        self.compare(e, 'result', '9,729,14,743,747', joiner=',', tabindex=[1, 2, 3, 4, 5])
        self.compare_tags(e, 'inicio-negat', 'result-posit')

        e = self.convert_operation('createadditionexpressionspotentiation', '100r2+4-125r3-10', terms=4)
        self.assertEqual(e.filter1, 2)   # min value
        self.assertEqual(e.filter2, 125)  # max value
        self.compare(e, 'exp', '+,100,r,2,+,4,-,125,r,3,-,10', joiner=',')  # blank space at first instead of a plus sign
        self.compare(e, 'result', '10,5,14,9,-1', joiner=',', tabindex=[1, 2, 3, 4, 5])
        self.compare_tags(e, 'inicio-posit', 'result-negat')

    def test_multiplicationexpressionspotentiation(self):
        e = self.convert_operation('createmultiplicationexpressionspotentiation', '4^2*4-4^3/8', terms=4)
        self.assertEqual(e.filter1, 2)   # min value
        self.assertEqual(e.filter2, 8)  # max value
        self.compare(e, 'exp', '+,4,^,2,*,4,-,4,^,3,/,8', joiner=',')  # blank space at first instead of a plus sign
        self.compare(e, 'result', '16,64,64,8,56', joiner=',', tabindex=[1, 2, 3, 4, 5])
        self.compare_tags(e, 'inicio-posit', 'result-posit')

        e = self.convert_operation('createmultiplicationexpressionspotentiation', '-7^3*3+5^3/25', terms=4)
        self.assertEqual(e.filter1, 3)   # min value
        self.assertEqual(e.filter2, 25)  # max value
        self.compare(e, 'exp', '-,7,^,3,*,3,+,5,^,3,/,25', joiner=',')  # blank space at first instead of a plus sign
        self.compare(e, 'result', '-343,125,-1029,5,-1024', joiner=',', tabindex=[1, 2, 3, 4, 5])
        self.compare_tags(e, 'inicio-negat', 'result-negat')

        e = self.convert_operation('createmultiplicationexpressionspotentiation', '-7^2*3+5^3/25', terms=4)
        self.assertEqual(e.filter1, 2)   # min value
        self.assertEqual(e.filter2, 25)  # max value
        self.compare(e, 'exp', '-,7,^,2,*,3,+,5,^,3,/,25', joiner=',')  # blank space at first instead of a plus sign
        self.compare(e, 'result', '49,125,147,5,152', joiner=',', tabindex=[1, 2, 3, 4, 5])
        self.compare_tags(e, 'inicio-negat', 'result-posit')

        e = self.convert_operation('createmultiplicationexpressionspotentiation', '4r2*4-64r3/2', terms=4)
        self.assertEqual(e.filter1, 2)   # min value
        self.assertEqual(e.filter2, 64)  # max value
        self.compare(e, 'exp', '+,4,r,2,*,4,-,64,r,3,/,2', joiner=',')  # blank space at first instead of a plus sign
        self.compare(e, 'result', '2,4,8,2,6', joiner=',', tabindex=[1, 2, 3, 4, 5])
        self.compare_tags(e, 'inicio-posit', 'result-posit')

    def test_decimaladdition(self):
        e = self.convert_operation('createdecimaladdition', '9,36+4,87', decimal_places='2')
        self.assertEqual(e.filter1, D('9.36'))
        self.assertEqual(e.filter2, D('4.87'))
        self.compare(e, 'support', '11')   #    11
        self.compare(e, 'line1', '936')    #    936
        self.compare(e, 'comma1', ', ')    #     ,_
        self.compare(e, 'line2', '487')    # +  487
        self.compare(e, 'comma2', ', ')    #     ,_
        self.compare(e, 'result', '1423')  # = 1423
        self.compare(e, 'comma', '010')    # =  _,_

        e = self.convert_operation('createdecimaladdition', '9,30+4,86', decimal_places='2')
        self.assertEqual(e.filter1, D('9.3'))
        self.assertEqual(e.filter2, D('4.86'))
        self.compare(e, 'support', '10')   #    10
        self.compare(e, 'line1', '930')    #    930
        self.compare(e, 'comma1', ', ')    #     ,_
        self.compare(e, 'line2', '486')    # +  486
        self.compare(e, 'comma2', ', ')    #     ,_
        self.compare(e, 'result', '1416')  # = 1416
        self.compare(e, 'comma', '010')    # =  _,_

        e = self.convert_operation('createdecimaladdition', '21,5+2,4', decimal_places='1')
        self.assertEqual(e.filter1, D('21.5'))
        self.assertEqual(e.filter2, D('2.4'))
        self.compare(e, 'support', '00')  #   00
        self.compare(e, 'line1', '215')   #   215
        self.compare(e, 'comma1', ' ,')   #    _,
        self.compare(e, 'line2', '24')    # +  24
        self.compare(e, 'comma2', ',')    #     ,
        self.compare(e, 'result', '239')  # = 239
        self.compare(e, 'comma', '01')    # =  _,

    def test_decimaladditionthreeaddends(self):
        e = self.convert_operation('createdecimaladditionthreeaddends', '9,36+4,87+5,21', decimal_places='2')
        self.assertEqual(e.filter1, D('4.87'))
        self.assertEqual(e.filter2, D('9.36'))
        self.compare(e, 'support', '11')   #    11
        self.compare(e, 'line1', '936')    #    936
        self.compare(e, 'comma1', ', ')    #     ,_
        self.compare(e, 'line2', '487')    # +  487
        self.compare(e, 'comma2', ', ')    #     ,_
        self.compare(e, 'line3', '521')    # +  521
        self.compare(e, 'comma3', ', ')    #     ,_
        self.compare(e, 'result', '1944')  # = 1944
        self.compare(e, 'comma', '010')    # =  _,_

        e = self.convert_operation('createdecimaladditionthreeaddends', '21,5+2,4+4,1', decimal_places='1')
        self.assertEqual(e.filter1, D('2.4'))
        self.assertEqual(e.filter2, D('21.5'))
        self.compare(e, 'support', '01')  #   01
        self.compare(e, 'line1', '215')   #   215
        self.compare(e, 'comma1', ' ,')   #    _,
        self.compare(e, 'line2', '24')    # +  24
        self.compare(e, 'comma2', ' ,')   #    _,
        self.compare(e, 'line3', '41')    # +  41
        self.compare(e, 'comma3', ' ,')   #    _,
        self.compare(e, 'result', '280')  # = 280
        self.compare(e, 'comma', '01')    # =  _,

    def test_decimalmultiplication(self):
        e = self.convert_operation('createdecimalmultiplication', '2.5*3.6')
        self.assertEqual(e.filter1, D('2.5'))
        self.assertEqual(e.filter2, D('3.6'))
        self.compare(e, 'support2', '1', tabindex=[6])          #    1
        self.compare(e, 'support1', '3', tabindex=[2])          #    3
        self.compare(e, 'line1', '25')                          #    25
        self.compare(e, 'comma1', ',')                          #     ,
        self.compare(e, 'line2', '36')                          # *  36
        self.compare(e, 'comma2', ',')                          #     ,
        self.compare(e, 'partial1', '150', tabindex=[4, 3, 1])  # > 150
        self.compare(e, 'partial2', '75', tabindex=[7, 5])      # > 75+
        self.compare(e, 'result', '900', tabindex=[10, 9, 8])   # = 900
        self.compare(e, 'comma', '10')                          # =  ,_

        e = self.convert_operation('createdecimalmultiplication', '2.59*36.5')
        self.assertEqual(e.filter1, D('2.59'))
        self.assertEqual(e.filter2, D('36.5'))
        self.compare(e, 'support3', '12', tabindex=[16, 14])               #     12
        self.compare(e, 'support2', '35', tabindex=[10, 8])                #     35
        self.compare(e, 'support1', '24', tabindex=[4, 2])                 #     24
        self.compare(e, 'line1', '259')                                    #     259
        self.compare(e, 'comma1', ', ')                                    #      ,_
        self.compare(e, 'line2', '365')                                    # *   365
        self.compare(e, 'comma2', ' ,')                                    #      _,
        self.compare(e, 'partial1', '1295', tabindex=[6, 5, 3, 1])         # >  1295
        self.compare(e, 'partial2', '1554', tabindex=[12, 11, 9, 7])       # > 1554+
        self.compare(e, 'partial3', '777', tabindex=[17, 15, 13])          # > 777++
        self.compare(e, 'result', '94535', tabindex=[22, 21, 20, 19, 18])  # = 94535
        self.compare(e, 'comma', '0100')                                   # =  _,__

        e = self.convert_operation('createdecimalmultiplication', '27.1*2.2')
        self.assertEqual(e.filter1, D('27.1'))
        self.assertEqual(e.filter2, D('2.2'))
        spt1 = self.compare(e, 'support2', '10', tabindex=[9, 7])     #    10
        spt2 = self.compare(e, 'support1', '10', tabindex=[4, 2])     #    10
        self.compare(e, 'line1', '271')                               #    271
        self.compare(e, 'comma1', ' ,')                               #     _,
        self.compare(e, 'line2', '22')                                # *   22
        self.compare(e, 'comma2', ',')                                #      ,
        self.compare(e, 'partial1', '542', tabindex=[5, 3, 1])        # >  542
        self.compare(e, 'partial2', '542', tabindex=[10, 8, 6])       # > 542+
        self.compare(e, 'result', '5962', tabindex=[14, 13, 12, 11])  # = 5962
        self.compare(e, 'comma', '010')                               # =  _,_

        # asserts that when the support answer isn't needed (zero), his type is
        # digit_or_blank to accept an empty string
        self.assertTrue(spt1[1].type == spt2[1].type == 'digit_or_blank')

        # special case involving numbers lesser than 1
        e = self.convert_operation('createdecimalmultiplication', '0.02*65')
        self.assertEqual(e.filter1, D('0.02'))
        self.assertEqual(e.filter2, 65)
        self.compare(e, 'support2', '01')         #    01
        self.compare(e, 'support1', '01')         #    01
        self.compare(e, 'line1', '002')           #    002
        self.compare(e, 'comma1', ', ')           #     ,_
        self.compare(e, 'line2', '65')            # *   65
        self.compare(e, 'comma2', ' ')            #      _  (no comma at all!)
        self.compare(e, 'partial1', '010')        # >  010
        self.compare(e, 'partial2', '012')        # > 012+
        res = self.compare(e, 'result', '0130')   # = 0130
        self.compare(e, 'comma', '010')           # =  _,_

        # asserts that the first zero from 0130 is optional (can be an empty
        # string once his type is digit_or_blank) but the last one is required
        self.assertTrue(res[0].type == 'digit_or_blank')
        self.assertTrue(res[-1].type == 'digit')

    def test_decimalperintegermultiplication(self):
        e = self.convert_operation('createdecimalperintegermultiplication', '2.5*3')
        self.assertEqual(e.filter1, D('2.5'))
        self.assertEqual(e.filter2, D('3'))
        self.compare(e, 'support1', '1', tabindex=[2])   #    1
        self.compare(e, 'line1', '25')                   #    25
        self.compare(e, 'comma1', ',')                   #     ,
        self.compare(e, 'line2', '3')                    # *   3
        self.compare(e, 'partial1', '75', tabindex=[3,1])  # =  75
        self.compare(e, 'result', '')  # the result was ignored if only one partial
        self.compare(e, 'comma', '1')                    # =   ,

        e = self.convert_operation('createdecimalperintegermultiplication', '0.02*65')
        self.assertEqual(e.filter1, D('0.02'))
        self.assertEqual(e.filter2, 65)
        self.compare(e, 'support2', '01')         #    01
        self.compare(e, 'support1', '01')         #    01
        self.compare(e, 'line1', '002')           #    002
        self.compare(e, 'comma1', ', ')           #     ,_
        self.compare(e, 'line2', '65')            # *   65
        self.compare(e, 'comma2', ' ')            #      _  (no comma at all!)
        self.compare(e, 'partial1', '010')        # >  010
        self.compare(e, 'partial2', '012')        # > 012+
        res = self.compare(e, 'result', '0130')   # = 0130
        self.compare(e, 'comma', '010')           # =  _,_

        # asserts that the first zero from 0130 is optional (can be an empty
        # string once his type is digit_or_blank) but the last one is required
        self.assertTrue(res[0].type == 'digit_or_blank')
        self.assertTrue(res[-1].type == 'digit')

    def test_decimalmultiplicationperdozen(self):
        e = self.convert_operation('createdecimalmultiplicationperdozen', '2.55*10')
        self.assertEqual(e.filter1, D('2.55'))
        self.assertEqual(e.filter2, D('10'))
        self.compare(e, 'term1', '2,55')
        self.compare(e, 'term2', '10')
        self.compare(e, 'result', '255', tabindex=[1, 2, 3])  # 255
        self.compare(e, 'comma', '01')                        # _,

        e = self.convert_operation('createdecimalmultiplicationperdozen', '2.214*100')
        self.assertEqual(e.filter1, D('2.214'))
        self.assertEqual(e.filter2, D('100'))
        self.compare(e, 'term1', '2,214')
        self.compare(e, 'term2', '100')
        self.compare(e, 'result', '2214', tabindex=[1, 2, 3, 4])  # 2214
        self.compare(e, 'comma', '001')                           # __,

        e = self.convert_operation('createdecimalmultiplicationperdozen', '2.215*1000')
        self.assertEqual(e.filter1, D('2.215'))
        self.assertEqual(e.filter2, D('1000'))
        self.compare(e, 'term1', '2,215')
        self.compare(e, 'term2', '1000')
        self.compare(e, 'result', '2215', tabindex=[1, 2, 3, 4])  # 2215
        self.compare(e, 'comma', '000')                           # ___

        e = self.convert_operation('createdecimalmultiplicationperdozen', '22.15*1000')
        self.assertEqual(e.filter1, D('22.15'))
        self.assertEqual(e.filter2, D('1000'))
        self.compare(e, 'term1', '22,15')
        self.compare(e, 'term2', '1000')
        self.compare(e, 'result', '22150', tabindex=[1, 2, 3, 4, 5])  # 22150
        self.compare(e, 'comma', '0000')                              # ____

    def test_decimalsubtraction(self):
        e = self.convert_operation('createdecimalsubtraction', '2.23-1.40', decimal_places='2')
        self.assertEqual(e.filter1, D('2.23'))
        self.assertEqual(e.filter2, D('1.4'))
        self.compare(e, 'support', '10')   #   10
        self.compare(e, 'line1', '223')    #   223
        self.compare(e, 'comma1', ', ')    #    ,_
        self.compare(e, 'line2', '140')    # - 140
        self.compare(e, 'comma2', ', ')    #    ,_
        self.compare(e, 'result', '083')   # = 083
        self.compare(e, 'comma', '10')     # =  ,_

        e = self.convert_operation('createdecimalsubtraction', '100.1-9.9', decimal_places='1')
        self.assertEqual(e.filter1, D('100.1'))
        self.assertEqual(e.filter2, D('9.9'))
        self.compare(e, 'support', '099')  #   099
        self.compare(e, 'line1', '1001')   #   1000
        self.compare(e, 'comma1', '  ,')   #    __,
        self.compare(e, 'line2', '99')     # -   99
        self.compare(e, 'comma2', ',')     #      ,
        self.compare(e, 'result', '0902')  # = 0902
        self.compare(e, 'comma', '001')     #     _,

    def test_decimaldivisionperdozen(self):
        e = self.convert_operation('createdecimaldivisionperdozen', '2.23/10')
        self.assertEqual(e.filter1, D('2.23'))
        self.assertEqual(e.filter2, 10)
        self.compare(e, 'term1', '2,23')
        self.compare(e, 'term2', '10')
        self.compare(e, 'result', '0223', tabindex=[1, 2, 3, 4])  # 0223
        self.compare(e, 'comma', '100')                           # ,__

        e = self.convert_operation('createdecimaldivisionperdozen', '350.21/10')
        self.assertEqual(e.filter1, D('350.21'))
        self.assertEqual(e.filter2, 10)
        self.compare(e, 'term1', '350,21')
        self.compare(e, 'term2', '10')
        self.compare(e, 'result', '35021', tabindex=[1, 2, 3, 4, 5])  # 35021
        self.compare(e, 'comma', '0100')                              # _,__

        e = self.convert_operation('createdecimaldivisionperdozen', '4.123/1000')
        self.assertEqual(e.filter1, D('4.123'))
        self.assertEqual(e.filter2, 1000)
        self.compare(e, 'term1', '4,123')
        self.compare(e, 'term2', '1000')
        self.compare(e, 'result', '0004123', tabindex=[1, 2, 3, 4, 5, 6, 7])  # 0004123
        self.compare(e, 'comma', '100000')                                    # ,_____

    def test_division(self):
        e = self.convert_operation('createdivision', '307/125')
        self.assertEqual(e.filter1, 307)
        self.assertEqual(e.filter2, 125)
        self.compare(e, 'divided', '307')
        self.compare(e, 'divisor', '125')
        self.compare(e, 'quotient', '2', joiner=',', tabindex=[1])
        self.compare(e, 'product0', '0,5,2', joiner=',', tabindex=[4, 3, 2])
        self.compare(e, 'rest0', '7,5,0', joiner=',', tabindex=[5, 6, 7])
        self.compare_tags(e, 'com-resto')

        e = self.convert_operation('createdivision', '77/4')
        self.assertEqual(e.filter1, 77)
        self.assertEqual(e.filter2, 4)
        self.compare(e, 'divided', '77')
        self.compare(e, 'divisor', '4')
        self.compare(e, 'quotient', '1,9', joiner=',', tabindex=[1, 5])
        self.compare(e, 'product0', '4', tabindex=[2])
        self.compare(e, 'rest0', '3', tabindex=[3])
        self.compare(e, 'down0', '7', tabindex=[4])
        self.compare(e, 'product1', '6,3', joiner=',', tabindex=[7, 6])
        self.compare(e, 'rest1', '1,0', joiner=',', tabindex=[8, 9])
        self.compare_tags(e, 'com-resto')

        e = self.convert_operation('createdivision', '248/6')
        self.assertEqual(e.filter1, 248)
        self.assertEqual(e.filter2, 6)
        self.compare(e, 'divided', '248')
        self.compare(e, 'divisor', '6')
        self.compare(e, 'quotient', '4,1', joiner=',', tabindex=[1, 7])
        self.compare(e, 'product0', '4,2', joiner=',', tabindex=[3, 2])
        self.compare(e, 'rest0', '0,0', joiner=',', tabindex=[4, 5])
        self.compare(e, 'down0', '8', tabindex=[6])
        self.compare(e, 'product1', '6', joiner=',', tabindex=[8])
        self.compare(e, 'rest1', '2', joiner=',', tabindex=[9])
        self.compare_tags(e, 'com-resto')

        e = self.convert_operation('createdivision', '3000/3')
        self.assertEqual(e.filter1, 3000)
        self.assertEqual(e.filter2, 3)
        self.compare(e, 'divided', '3000')
        self.compare(e, 'divisor', '3')
        self.compare(e, 'quotient', '1,0,0,0', joiner=',', tabindex=[1, 5, 7, 9])
        self.compare(e, 'product0', '3', joiner=',', tabindex=[2])
        self.compare(e, 'rest0', '0', joiner=',', tabindex=[3])
        self.compare(e, 'down0', '0,0,0', joiner=',', tabindex=[8, 6, 4])
        self.compare_tags(e, 'sem-resto')

        e = self.convert_operation('createdivision', '30060/30')
        self.assertEqual(e.filter1, 30060)
        self.assertEqual(e.filter2, 30)
        self.compare(e, 'divided', '30060')
        self.compare(e, 'divisor', '30')
        self.compare(e, 'quotient', '1,0,0,2', joiner=',', tabindex=[1, 7, 9, 11])
        self.compare(e, 'product0', '0,3', joiner=',', tabindex=[3, 2])
        self.compare(e, 'rest0', '0,0', joiner=',', tabindex=[4, 5])
        self.compare(e, 'down0', '0,6,0', joiner=',', tabindex=[10, 8, 6])
        self.compare(e, 'product3', '0,6', joiner=',', tabindex=[13, 12])
        self.compare(e, 'rest3', '0,0', joiner=',', tabindex=[14, 15])
        self.compare_tags(e, 'sem-resto')

    def test_decimalresultdivision(self):
        e = self.convert_operation(
            'createdecimalresultdivision', '8/5', decimal_places=1)
        self.assertEqual(e.filter1, 8)
        self.assertEqual(e.filter2, 5)
        self.compare(e, 'divided', '8 ')
        self.compare(e, 'divisor', '5')
        self.compare(e, 'quotient', '1,6', joiner=',', tabindex=[1, 5])
        self.compare(e, 'product0', '5', joiner=',', tabindex=[2])
        self.compare(e, 'rest0', '3', joiner=',', tabindex=[3])
        self.compare(e, 'down0', '0', joiner=',', tabindex=[4])
        self.compare(e, 'product1', '0,3', joiner=',', tabindex=[7, 6])
        self.compare(e, 'rest1', '0,0', joiner=',', tabindex=[8, 9])
        self.compare(e, 'comma', '1')
        self.compare_tags(e, '1-casas')

        e = self.convert_operation(
            'createdecimalresultdivision', '15/4', decimal_places=2)
        self.assertEqual(e.filter1, 15)
        self.assertEqual(e.filter2, 4)
        self.compare(e, 'divided', '15  ')
        self.compare(e, 'divisor', '4')
        self.compare(e, 'quotient', '3,7,5', joiner=',', tabindex=[1, 7, 13])
        self.compare(e, 'product0', '2,1', joiner=',', tabindex=[3, 2])
        self.compare(e, 'rest0', '3,0', joiner=',', tabindex=[4, 5])
        self.compare(e, 'down0', '0', joiner=',', tabindex=[6])
        self.compare(e, 'product1', '8,2', joiner=',', tabindex=[9, 8])
        self.compare(e, 'rest1', '2,0', joiner=',', tabindex=[10, 11])
        self.compare(e, 'down1', '0', joiner=',', tabindex=[12])
        self.compare(e, 'product2', '0,2', joiner=',', tabindex=[15, 14])
        self.compare(e, 'rest2', '0,0', joiner=',', tabindex=[16, 17])
        self.compare(e, 'comma', '1,0', joiner=',')
        self.compare_tags(e, '2-casas')

    def test_decimaldivision(self):
        e = self.convert_operation(
            'createdecimaldivision', '1,8/1,2', decimal_places=1)
        self.assertEqual(e.filter1, D('1.8'))
        self.assertEqual(e.filter2, D('1.2'))
        self.compare(e, 'divided', '18 ')
        self.compare(e, 'comma_divided', ', ')
        self.compare(e, 'divisor', '12')
        self.compare(e, 'comma_divisor', ',')
        self.compare(e, 'quotient', '1,5', joiner=',', tabindex=[1, 7])
        self.compare(e, 'product0', '2,1', joiner=',', tabindex=[3, 2])
        self.compare(e, 'rest0', '6,0', joiner=',', tabindex=[4, 5])
        self.compare(e, 'down0', '0', joiner=',', tabindex=[6])
        self.compare(e, 'product1', '0,6', joiner=',', tabindex=[9, 8])
        self.compare(e, 'rest1', '0,0', joiner=',', tabindex=[10, 11])
        self.compare(e, 'comma', '1')
        self.compare_tags(e, '1-casas')

    def test_decimalperintegerdivision(self):
        e = self.convert_operation(
            'createdecimalperintegerdivision', '751.8/42', decimal_places=1)
        self.assertEqual(e.filter1, D('751.8'))
        self.assertEqual(e.filter2, 42)
        self.compare(e, 'quotient', '1,7,9', joiner=',', tabindex=[1, 7, 15])
        self.compare(e, 'product0', '2,4', joiner=',', tabindex=[3, 2])
        self.compare(e, 'rest0', '3,3', joiner=',', tabindex=[4, 5])
        self.compare(e, 'down0', '1', joiner=',', tabindex=[6])
        self.compare(e, 'product1', '4,9,2', joiner=',', tabindex=[10, 9, 8])
        self.compare(e, 'rest1', '7,3,0', joiner=',', tabindex=[11, 12, 13])
        self.compare(e, 'down1', '8', joiner=',', tabindex=[14])
        self.compare(e, 'product2', '8,7,3', joiner=',', tabindex=[18, 17, 16])
        self.compare(e, 'rest2', '0,0,0', joiner=',', tabindex=[19, 20, 21])
        self.compare(e, 'comma', '01')
        self.compare_tags(e, '1-casas')

    def test_equivalentfraction(self):
        """
        Tests the creation of equivalent fraction exercises.

        Ensure that there is only one missing field in the second column. The
        other missing must be unexistent.
        """
        e = self.convert_operation('createequivalentfraction', '1/2=2/4')
        self.assertEqual(e.filter1, 1)  # min value of terms
        self.assertEqual(e.filter2, 4)  # max value of terms
        self.compare(e, 'term1', '1')
        self.compare(e, 'term2', '2')
        self.compare(e, 'term3', '2')
        self.compare(e, 'term4', '')
        self.compare(e, 'missing3', '')
        self.compare(e, 'missing4', '4')

        e = self.convert_operation('createequivalentfraction', '3/5=9/15')
        self.assertEqual(e.filter1, 3)  # min value of terms
        self.assertEqual(e.filter2, 15)  # max value of terms
        self.compare(e, 'term1', '3')
        self.compare(e, 'term2', '5')
        self.compare(e, 'term3', '9')
        self.compare(e, 'term4', '')
        self.compare(e, 'missing3', '')
        self.compare(e, 'missing4', '15')

    def test_fractionmultiplicationbyinteger(self):
        """
        Test the creation of fraction multiplication by integer.
        """
        e = self.convert_operation('createfractionmultiplicationbyinteger', '3*3/5')
        self.assertEqual(e.filter1, 3)  # min value of terms
        self.assertEqual(e.filter2, 5)  # max value of terms
        self.compare(e, 'term1', '3')
        self.compare(e, 'term2', '3/5', joiner='/')
        self.compare(e, 'missing', '9/5', joiner='/', tabindex=[1,2])

        e = self.convert_operation('createfractionmultiplicationbyinteger', '4*1/6')
        self.assertEqual(e.filter1, 1)  # min value of terms
        self.assertEqual(e.filter2, 6)  # max value of terms
        self.compare(e, 'term1', '4')
        self.compare(e, 'term2', '1/6', joiner='/')

        # The result is not simplified!
        try:
            self.compare(e, 'missing', '2/3', joiner='/')
        except AssertionError:
            self.compare(e, 'missing', '4/6', joiner='/', tabindex=[1,2])

    def test_fractiondivisionbyinteger(self):
        """
        Test the creation of fraction divisible by integer.
        """
        e = self.convert_operation('createfractiondivisionbyinteger', '2/3 / 4')
        self.assertEqual(e.filter1, 2)
        self.assertEqual(e.filter2, 4)
        self.compare(e, 'term1', '2/3', joiner='/')
        self.compare(e, 'term2', '4')
        self.compare(e, 'partial1', '2/3', joiner='/', tabindex=[1, 2])
        self.compare(e, 'partial2', '1/4', joiner='/', tabindex=[3, 4])
        self.compare(e, 'result', '2/12', joiner='/', tabindex=[5, 6])

        e = self.convert_operation('createfractiondivisionbyinteger', '1/9 / 2')
        self.assertEqual(e.filter1, 1)
        self.assertEqual(e.filter2, 9)
        self.compare(e, 'term1', '1/9', joiner='/')
        self.compare(e, 'term2', '2')
        self.compare(e, 'partial1', '1/9', joiner='/', tabindex=[1, 2])
        self.compare(e, 'partial2', '1/2', joiner='/', tabindex=[3, 4])
        self.compare(e, 'result', '1/18', joiner='/', tabindex=[5, 6])

    def test_fractionmultiplication(self):
        """
        Test the creation of fractions multiplication.

        Note the multiplication result is not simplified.
        """
        e = self.convert_operation('createfractionmultiplication', '2/4*3/5')
        self.assertEqual(e.filter1, 2)  # min value of terms
        self.assertEqual(e.filter2, 5)  # max value of terms
        self.compare(e, 'term1', '2/4', joiner='/')
        self.compare(e, 'term2', '3/5', joiner='/')

        # The missing term is not simplified!
        try:
            self.compare(e, 'missing', '3/10', joiner='/')
        except AssertionError:
            self.compare(e, 'missing', '6/20', joiner='/', tabindex=[1,2])

        e = self.convert_operation('createfractionmultiplication', '1/4*1/3')
        self.assertEqual(e.filter1, 1)  # min value of terms
        self.assertEqual(e.filter2, 4)  # max value of terms
        self.compare(e, 'term1', '1/4', joiner='/')
        self.compare(e, 'term2', '1/3', joiner='/')
        self.compare(e, 'missing', '1/12', joiner='/', tabindex=[1,2])

    def test_fractiondivision(self):
        """
        Test the creation of fractions division.
        """
        e = self.convert_operation('createfractiondivision', '2/4 / 3/5')
        self.assertEqual(e.filter1, 2)
        self.assertEqual(e.filter2, 5)
        self.compare(e, 'term1', '2/4', joiner='/')
        self.compare(e, 'term2', '3/5', joiner='/')
        self.compare(e, 'partial1', '2/4', joiner='/', tabindex=[1, 2])
        self.compare(e, 'partial2', '5/3', joiner='/', tabindex=[3, 4])
        self.compare(e, 'result', '10/12', joiner='/', tabindex=[5, 6])

        e = self.convert_operation('createfractiondivision', '1/2 / 3/4')
        self.assertEqual(e.filter1, 1)
        self.assertEqual(e.filter2, 4)
        self.compare(e, 'term1', '1/2', joiner='/')
        self.compare(e, 'term2', '3/4', joiner='/')
        self.compare(e, 'partial1', '1/2', joiner='/', tabindex=[1, 2])
        self.compare(e, 'partial2', '4/3', joiner='/', tabindex=[3, 4])
        self.compare(e, 'result', '4/6', joiner='/', tabindex=[5, 6])

    def test_irreduciblefraction(self):
        """
        Tests the creation of irreducible fraction exercises.

        Ensure that there is only two values to fraction.
        """
        e = self.convert_operation('createirreduciblefraction', '4/16=1/4')
        self.assertEqual(e.filter1, 1)  # min value of terms
        self.assertEqual(e.filter2, 16)  # max value of terms
        self.compare(e, 'term', '4/16', joiner='/')
        self.compare(e, 'missing', '1/4', joiner='/', tabindex=[1, 2])

        # do not generate not equivalent exercises
        with self.assertRaises(ValueError):
            e = self.convert_operation('createirreduciblefraction', '1/2=1/3')

    def test_choiceirreduciblefraction(self):
        e = self.convert_operation('createchoiceirreduciblefraction', '4/16=1/4')
        self.assertEqual(e.filter1, 1)
        self.assertEqual(e.filter2, 16)
        self.compare(e, 'fraction', '4/16', joiner='/')

        answer = e.answer_set.get()  # only one answer
        self.assertEqual(answer.choice_set.count(), 20)
        correct = answer.choice_set.correct().get()  # only one correct
        self.assertEqual(correct.description, '1/4')

    def test_fractionadditiondifferentbase(self):
        """
        Tests the creation of fraction with different denominator

        Ensure that there is at least two different denominator.
        """
        e = self.convert_operation('createfractionadditiondifferentbase', '4/6+2/5')
        self.assertEqual(e.filter1, 2)  # min value of terms
        self.assertEqual(e.filter2, 6)  # max value of terms
        self.compare(e, 'term1', '4/6', joiner='/')
        self.compare(e, 'term2', '2/5', joiner='/')
        self.compare(e, 'missing1', '30')
        self.compare(e, 'missing2', '20')
        self.compare(e, 'missing3', '12')
        self.compare(e, 'missing4', '32')
        self.compare(e, 'missing5', '30')

    def test_fractionsubtractiondifferentbase(self):
        """
        Tests the creation of fraction with different denominator

        Ensure that there is at least two different denominator.
        """
        e = self.convert_operation('createfractionsubtractiondifferentbase', '4/6-2/5')
        self.assertEqual(e.filter1, 2)  # min value of terms
        self.assertEqual(e.filter2, 6)  # max value of terms
        self.compare(e, 'term1', '4/6', joiner='/')
        self.compare(e, 'term2', '2/5', joiner='/')
        self.compare(e, 'missing1', '30')
        self.compare(e, 'missing2', '20')
        self.compare(e, 'missing3', '12')
        self.compare(e, 'missing4', '8')
        self.compare(e, 'missing5', '30')

    def test_figuretofraction(self):
        e = self.convert_operation('createfiguretofraction', '3/9')
        self.assertEqual(e.filter1, 3)
        self.assertEqual(e.filter2, 9)
        self.compare(e, 'fraction', '3/9', joiner='/')

        # choices are 1/8 to 8/8, 1/9 to 9/9 and 1/10 to 10/10
        answer = e.answer_set.get()  # only one answer
        self.assertEqual(answer.choice_set.count(), 8 + 9 + 10)
        correct = answer.choice_set.correct().get()  # only one correct
        self.assertEqual(correct.description, '3/9')

        e = self.convert_operation('createfiguretofraction', '1/2')
        self.assertEqual(e.filter1, 1)
        self.assertEqual(e.filter2, 2)
        self.compare(e, 'fraction', '1/2', joiner='/')

        # choices are 1/2 to 2/2 and 1/3 to 3/3
        answer = e.answer_set.get()  # only one answer
        self.assertEqual(answer.choice_set.count(), 2 + 3)
        correct = answer.choice_set.correct().get()  # only one correct
        self.assertEqual(correct.description, '1/2')

    def test_figuretoimproperfraction(self):
        e = self.convert_operation('createfiguretoimproperfraction', '4/3')
        self.assertEqual(e.filter1, 4)
        self.assertEqual(e.filter2, 3)
        self.compare(e, 'fraction', '4/3', joiner='/')

        # choices are 3/2, 4/2, 4/3 to 6/3, 5/4 to 8/4
        answer = e.answer_set.get()  # only one answer
        self.assertEqual(answer.choice_set.count(), 2 + 3 + 4)
        correct = answer.choice_set.correct().get()  # only one correct
        self.assertEqual(correct.description, '4/3')

        e = self.convert_operation('createfiguretoimproperfraction', '10/6')
        self.assertEqual(e.filter1, 10)
        self.assertEqual(e.filter2, 6)
        self.compare(e, 'fraction', '10/6', joiner='/')

        # choices are 6/5 to 10/5, 7/6 to 12/6 and 8/7 to 14/7
        answer = e.answer_set.get()  # only one answer
        self.assertEqual(answer.choice_set.count(), 5 + 6 + 7)
        correct = answer.choice_set.correct().get()  # only one correct
        self.assertEqual(correct.description, '10/6')

    def test_fractionadditionsamebase(self):
        e = self.convert_operation('createfractionadditionsamebase', '2/5 + 1/5')
        self.assertEqual(e.filter1, 2)  # filter1 is the numerator
        self.assertEqual(e.filter2, 5)  # filter2 is the denominator
        self.compare(e, 'term1', '2/5', joiner='/')
        self.compare(e, 'term2', '1/5', joiner='/')
        self.compare(e, 'result', '3/5', joiner='/', tabindex=[1, 2])

        e = self.convert_operation('createfractionadditionsamebase', '9/19 + 12/19')
        self.assertEqual(e.filter1, 12)  # filter1 is the numerator
        self.assertEqual(e.filter2, 19)  # filter2 is the denominator
        self.compare(e, 'term1', '9/19', joiner='/')
        self.compare(e, 'term2', '12/19', joiner='/')
        self.compare(e, 'result', '21/19', joiner='/', tabindex=[1, 2])

    def test_threefractionsmultiplication(self):
        e = self.convert_operation('createthreefractionsmultiplication', '3/6 * 7/10 * 2/12')
        self.assertEqual(e.filter1, 12)   # term1 is the max question digit
        self.assertEqual(e.filter2, 720)  # term2 is the max answer digit
        self.compare(e, 'term1', '3/6', joiner='/')
        self.compare(e, 'term2', '7/10', joiner='/')
        self.compare(e, 'term3', '2/12', joiner='/')
        self.compare(e, 'result', '42/720', joiner='/', tabindex=[1, 2])

    def test_threefractionsadditionsamebase(self):
        """
        In addition of 3 fractions, all fractions can be positive.
        """
        e = self.convert_operation('createthreefractionsadditionsamebase', '2/5 + 1/5 + 3/5')
        self.assertEqual(e.filter1, 3)  # filter1 is the numerator
        self.assertEqual(e.filter2, 5)  # filter2 is the denominator
        self.compare(e, 'sign1', '+')
        self.compare(e, 'term1', '2/5', joiner='/')
        self.compare(e, 'sign2', '+')
        self.compare(e, 'term2', '1/5', joiner='/')
        self.compare(e, 'sign3', '+')
        self.compare(e, 'term3', '3/5', joiner='/')
        self.compare(e, 'result', '6/5', joiner='/', tabindex=[1, 2])

    def test_threefractionsadditionsamebase_with_subtractions(self):
        """
        In addition of 3 fractions, any fraction can be negative.
        """
        e = self.convert_operation('createthreefractionsadditionsamebase', '4/5 - 1/5 - 2/5')
        self.assertEqual(e.filter1, 4)  # filter1 is the numerator
        self.assertEqual(e.filter2, 5)  # filter2 is the denominator
        self.compare(e, 'sign1', '+')
        self.compare(e, 'term1', '4/5', joiner='/')
        self.compare(e, 'sign2', '-')
        self.compare(e, 'term2', '1/5', joiner='/')
        self.compare(e, 'sign3', '-')
        self.compare(e, 'term3', '2/5', joiner='/')
        self.compare(e, 'result', '1/5', joiner='/', tabindex=[1, 2])

        e = self.convert_operation('createthreefractionsadditionsamebase', '4/5 + 1/5 - 2/5')
        self.assertEqual(e.filter1, 4)  # filter1 is the numerator
        self.assertEqual(e.filter2, 5)  # filter2 is the denominator
        self.compare(e, 'sign1', '+')
        self.compare(e, 'term1', '4/5', joiner='/')
        self.compare(e, 'sign2', '+')
        self.compare(e, 'term2', '1/5', joiner='/')
        self.compare(e, 'sign3', '-')
        self.compare(e, 'term3', '2/5', joiner='/')
        self.compare(e, 'result', '3/5', joiner='/', tabindex=[1, 2])

    def test_threefractionsadditionsamebase_starts_with_subtraction(self):
        """
        In addition of 3 fractions, even the 1st term can be negative.

        In this case, the exercise is properly tagged.
        """
        e = self.convert_operation('createthreefractionsadditionsamebase', '-4/5 + 3/5 + 2/5')
        self.assertEqual(e.filter1, 4)  # filter1 is the numerator
        self.assertEqual(e.filter2, 5)  # filter2 is the denominator
        self.compare(e, 'sign1', '-')
        self.compare(e, 'term1', '4/5', joiner='/')
        self.compare(e, 'sign2', '+')
        self.compare(e, 'term2', '1/5', joiner='/')
        self.compare(e, 'sign3', '+')
        self.compare(e, 'term3', '2/5', joiner='/')
        self.compare(e, 'result', '1/5', joiner='/', tabindex=[1, 2])
        self.compare_tags(e, 'inicio-negat')

    def test_threefractionsadditionsamebase_starts_with_addition(self):
        """
        In addition of 3 fractions, if 1st term is posit., there is also a tag.
        """
        e = self.convert_operation('createthreefractionsadditionsamebase', '4/5 + 1/5 - 2/5')
        self.compare_tags(e, 'inicio-posit')

    def test_threefractionsadditionsamebase_cant_results_zero(self):
        try:
            self.convert_operation('createthreefractionsadditionsamebase', '-4/5 + 2/5 + 2/5')
            raise AssertionError('The result can\'t be zero!')
        except CommandError:
            pass

    def test_threefractionsadditionsamebase_cant_results_negative(self):
        try:
            self.convert_operation('createthreefractionsadditionsamebase', '-4/5 + 1/5 + 2/5')
            raise AssertionError('The result can\'t be negative!')
        except CommandError:
            pass

    def test_threefractionadditiondifferentbase(self):
        """
        Addition of 3 fractions with diff. bases can use positive fractions.

        Make note that the filter1 is the max question digit (numerator or
        denominator of any fraction) and the filter2 is the max answer digit.
        This way, it is possible to filter exercises to be mindly resolved.
        """
        e = self.convert_operation('createthreefractionadditiondifferentbase', '2/5+1/2+3/4')
        self.assertEqual(e.filter1, 5)   # filter1 is the max question digit
        self.assertEqual(e.filter2, 33)  # filter2 is the max answer digit
        self.compare(e, 'sign1', '+')
        self.compare(e, 'term1', '2/5', joiner='/')
        self.compare(e, 'sign2', '+')
        self.compare(e, 'term2', '1/2', joiner='/')
        self.compare(e, 'sign3', '+')
        self.compare(e, 'term3', '3/4', joiner='/')
        self.compare(e, 'multiplier', '20', tabindex=[1])
        self.compare(e, 'partial', '8,10,15', tabindex=[2, 3, 4])
        self.compare(e, 'result', '33/20', joiner='/', tabindex=[5, 6])

    def test_threefractionadditiondifferentbase_with_subtraction(self):
        """
        Addition of 3 fractions with diff. bases can use negative fractions.
        """
        e = self.convert_operation('createthreefractionadditiondifferentbase', '-1/5-1/6+1/2')
        self.assertEqual(e.filter1, 6)   # filter1 is the max question digit
        self.assertEqual(e.filter2, 30)  # filter2 is the max answer digit
        self.compare(e, 'sign1', '-')
        self.compare(e, 'term1', '1/5', joiner='/')
        self.compare(e, 'sign2', '-')
        self.compare(e, 'term2', '1/6', joiner='/')
        self.compare(e, 'sign3', '+')
        self.compare(e, 'term3', '1/2', joiner='/')
        self.compare(e, 'multiplier', '30', tabindex=[1])
        self.compare(e, 'partial', '6,5,15', tabindex=[2, 3, 4])
        self.compare(e, 'result', '4/30', joiner='/', tabindex=[5, 6])

    def test_threefractionadditiondifferentbase_tags(self):
        """
        Addition of 3 fractions with diff. bases has question dependant tags.

        There is a tag for negative starting exercises and for positive
        starting ones.
        """
        e = self.convert_operation('createthreefractionadditiondifferentbase', '-1/5-1/6+1/2')
        self.compare_tags(e, 'inicio-negat')

        e = self.convert_operation('createthreefractionadditiondifferentbase', '1/5-1/6+1/2')
        self.compare_tags(e, 'inicio-posit')

    def test_threefractionadditiondifferentbase_must_differ_base(self):
        try:
            self.convert_operation('createthreefractionadditiondifferentbase', '4/6-2/3-1/6')
            raise AssertionError('There should be at least 2 different basis')
        except CommandError:
            pass

    def test_threefractionadditiondifferentbase_cant_results_zero(self):
        try:
            self.convert_operation('createthreefractionadditiondifferentbase', '4/6-1/3-2/6')
            raise AssertionError('The result can\'t be zero!')
        except CommandError:
            pass

    def test_threefractionadditiondifferentbase_cant_results_negative(self):
        try:
            self.convert_operation('createthreefractionadditiondifferentbase', '4/6-1/3-3/6')
            raise AssertionError('The result can\'t be negative!')
        except CommandError:
            pass

    def test_fractioncomparison(self):
        e = self.convert_operation('createfractioncomparison', '2/5, 3/6, gt')
        self.assertEqual(e.filter1, 2)
        self.assertEqual(e.filter2, 6)
        self.compare(e, 'fraction1', '2/5', joiner='/')
        self.compare(e, 'fraction2', '3/6', joiner='/')
        self.compare(e, 'operator', 'maior')  # greater than, in pt_BR

        # choices tell if the greater is 2/5, 3/6 or both equal
        answer = e.answer_set.get()  # only one answer
        self.assertEqual(answer.choice_set.count(), 3)
        correct = answer.choice_set.correct().get()  # only one correct
        self.assertEqual(correct.description, '3/6')

        e = self.convert_operation('createfractioncomparison', '2/5, 3/6, lt')
        self.assertEqual(e.filter1, 2)
        self.assertEqual(e.filter2, 6)
        self.compare(e, 'fraction1', '2/5', joiner='/')
        self.compare(e, 'fraction2', '3/6', joiner='/')
        self.compare(e, 'operator', 'menor')  # lesser than, in pt_BR

        # choices tell if the lesser is 2/5, 3/6 or both equal
        answer = e.answer_set.get()  # only one answer
        self.assertEqual(answer.choice_set.count(), 3)
        correct = answer.choice_set.correct().get()  # only one correct
        self.assertEqual(correct.description, '2/5')

        e = self.convert_operation('createfractioncomparison', '1/2, 4/8, gt')
        self.assertEqual(e.filter1, 1)
        self.assertEqual(e.filter2, 8)
        self.compare(e, 'fraction1', '1/2', joiner='/')
        self.compare(e, 'fraction2', '4/8', joiner='/')
        self.compare(e, 'operator', 'maior')  # greater than, in pt_BR

        # choices tell if the lesser is 2/5, 3/6 or both equal
        answer = e.answer_set.get()  # only one answer
        self.assertEqual(answer.choice_set.count(), 3)
        correct = answer.choice_set.correct().get()  # only one correct
        self.assertNotEqual(correct.description, '1/2')
        self.assertNotEqual(correct.description, '4/8')

    def test_fractionsubtractionsamebase(self):
        e = self.convert_operation('createfractionsubtractionsamebase', '2/5 - 1/5')
        self.assertEqual(e.filter1, 2)  # filter1 is the numerator
        self.assertEqual(e.filter2, 5)  # filter2 is the denominator
        self.compare(e, 'term1', '2/5', joiner='/')
        self.compare(e, 'term2', '1/5', joiner='/')
        self.compare(e, 'result', '1/5', joiner='/', tabindex=[1, 2])

        e = self.convert_operation('createfractionsubtractionsamebase', '12/19 - 9/19')
        self.assertEqual(e.filter1, 12)  # filter1 is the numerator
        self.assertEqual(e.filter2, 19)  # filter2 is the denominator
        self.compare(e, 'term1', '12/19', joiner='/')
        self.compare(e, 'term2', '9/19', joiner='/')
        self.compare(e, 'result', '3/19', joiner='/', tabindex=[1, 2])

        # can't create negative result subtractions!
        try:
            e = self.convert_operation('createfractionadditionsamebase', '9/19 - 12/19')
        except ValueError:
            pass

    def test_fractiontofigure(self):
        e = self.convert_operation('createfractiontofigure', '2/5')
        self.assertEqual(e.filter1, 2)
        self.assertEqual(e.filter2, 5)
        self.compare(e, 'fraction', '2/5', joiner='/')

        # choices are 1/4 to 4/4, 1/5 to 5/5 and 1/6 to 6/6
        answer = e.answer_set.get()  # only one answer
        self.assertEqual(answer.choice_set.count(), 4 + 5 + 6)
        correct = answer.choice_set.correct().get()  # only one correct
        self.assertEqual(correct.description, '2/5')

        e = self.convert_operation('createfiguretofraction', '3/6')
        self.assertEqual(e.filter1, 3)
        self.assertEqual(e.filter2, 6)
        self.compare(e, 'fraction', '3/6', joiner='/')

        # choices are 1/5 to 5/5, 1/6 to 6/6 and 1/7 to 7/7
        answer = e.answer_set.get()  # only one answer
        self.assertEqual(answer.choice_set.count(), 5 + 6 + 7)
        correct = answer.choice_set.correct().get()  # only one correct
        self.assertEqual(correct.description, '3/6')

    def test_hourstominutes(self):
        (e, f) = self.convert_operation('createhourstominutes', '1')
        self.assertEqual(e.filter1, 1)  # always the hour part
        self.assertEqual(e.filter2, 60)  # always the minutes part
        self.compare(e, 'term1', '1')
        self.compare(e, 'term2', '60', tabindex=[1])

        self.assertEqual(f.filter1, 1)  # always the hour part
        self.assertEqual(f.filter2, 60)  # always the minutes part
        self.compare(f, 'term1', '60')
        self.compare(f, 'term2', '1', tabindex=[1])

    def test_minutestoseconds(self):
        (e, f) = self.convert_operation('createminutestoseconds', '1')
        self.assertEqual(e.filter1, 1)  # always the minutes part
        self.assertEqual(e.filter2, 60)  # always the seconds part
        self.compare(e, 'term1', '1')
        self.compare(e, 'term2', '60', tabindex=[1])

        self.assertEqual(f.filter1, 1)  # always the minutes part
        self.assertEqual(f.filter2, 60)  # always the seconds part
        self.compare(f, 'term1', '60')
        self.compare(f, 'term2', '1', tabindex=[1])

    def test_decompositionintoprimefactors(self):
        e = self.convert_operation('createdecompositionintoprimefactors', '12')
        self.assertEqual(e.filter1, 12)
        self.assertEqual(e.filter2, 12)
        self.compare(e, 'numbers', '12')
        self.compare(e, 'divisors', '2,2,3', joiner=',', tabindex=[1, 3, 5])
        self.compare(e, 'steps', '6,3,1', joiner=',', tabindex=[2, 4, 6])

        e = self.convert_operation('createdecompositionintoprimefactors', '14')
        self.assertEqual(e.filter1, 14)
        self.assertEqual(e.filter2, 14)
        self.compare(e, 'numbers', '14')
        self.compare(e, 'divisors', '2,7', joiner=',', tabindex=[1, 3])
        self.compare(e, 'steps', '7,1', joiner=',', tabindex=[2, 4])

    def test_lcm(self):
        e = self.convert_operation('createlcm', 'LCM(12, 18)', terms=2)
        self.compare(e, 'numbers', '12,18', joiner=',')
        self.compare(e, 'result', '36', tabindex=[13])
        self.compare(e, 'divisors', '2,2,3,3', joiner=',', tabindex=[1, 4, 7, 10])
        self.compare(e, 'steps', '6,9,3,9,1,3,1,1', joiner=',', tabindex=[2, 3, 5, 6, 8, 9, 11, 12])

        e = self.convert_operation('createlcm', 'LCM(50, 32)', terms=2)
        self.compare(e, 'numbers', '50,32', joiner=',')
        self.compare(e, 'result', '800', tabindex=[22])
        self.compare(e, 'divisors', '2,2,2,2,2,5,5', joiner=',',
                     tabindex=[1, 4, 7, 10, 13, 16, 19])
        self.compare(e, 'steps', '25,16,25,8,25,4,25,2,25,1,5,1,1,1', joiner=',',
                     tabindex=[2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 18, 20, 21])

        e = self.convert_operation('createlcm', 'LCM(9, 15, 12)', terms=3)
        self.compare(e, 'numbers', '9,15,12', joiner=',')
        self.compare(e, 'result', '180', tabindex=[21])
        self.compare(e, 'divisors', '2,2,3,3,5', joiner=',', tabindex=[1, 5, 9, 13, 17])
        self.compare(e, 'steps', '9,15,6,9,15,3,3,5,1,1,5,1,1,1,1', joiner=',',
                     tabindex=[2, 3, 4, 6, 7, 8, 10, 11, 12, 14, 15, 16, 18, 19, 20])

        e = self.convert_operation('createlcm', 'LCM(13, 19, 29)', terms=3)
        self.compare(e, 'numbers', '13,19,29', joiner=',')
        self.compare(e, 'result', '7163', tabindex=[13])
        self.compare(e, 'divisors', '13,19,29', joiner=',', tabindex=[1, 5, 9])
        self.compare(e, 'steps', '1,19,29,1,1,29,1,1,1', joiner=',',
                     tabindex=[2, 3, 4, 6, 7, 8, 10, 11, 12])

    def test_multiplication_one_partial(self):
        e = self.convert_operation('createmultiplication', '138*2')
        self.assertEqual(e.filter1, 138)
        self.assertEqual(e.filter2, 2)
        self.compare(e, 'support1', '01', tabindex=[4, 2])       #   01
        self.compare(e, 'line1', '138')                          #   138
        self.compare(e, 'line2', '2')                            # *   2
        self.compare(e, 'partial1', '276', tabindex=[5, 3, 1])   # = 276
        self.compare(e, 'result', '')  # the result was ignored if only one partial

        e = self.convert_operation('createmultiplication', '290*3')
        self.assertEqual(e.filter1, 290)
        self.assertEqual(e.filter2, 3)
        self.compare(e, 'support1', '20', tabindex=[4, 2])       #   20
        self.compare(e, 'line1', '290')                          #   290
        self.compare(e, 'line2', '3')                            # *   3
        self.compare(e, 'partial1', '870', tabindex=[5, 3, 1])   # = 870
        self.compare(e, 'result', '')  # the result was ignored if only one partial

        e = self.convert_operation('createdecimalmultiplication', '0.04*3')
        self.assertEqual(e.filter1, D('0.04'))
        self.assertEqual(e.filter2, D('3'))
        self.compare(e, 'support1', '01', tabindex=[4, 2])      #    10
        self.compare(e, 'line1', '004')                         #    004
        self.compare(e, 'comma1', ', ')                         #     ,_
        self.compare(e, 'line2', '3')                           # *    2
        self.compare(e, 'comma2', '')                           #
        self.compare(e, 'partial1', '012', tabindex=[5, 3, 1])  # =  012
        self.compare(e, 'comma', '10')                          # =   ,_
        self.compare(e, 'result', '')  # the result was ignored if only one partial

    def test_multiplication(self):
        e = self.convert_operation('createmultiplication', '25*36')
        self.assertEqual(e.filter1, 25)
        self.assertEqual(e.filter2, 36)
        self.compare(e, 'support2', '1', tabindex=[6])          #    1
        self.compare(e, 'support1', '3', tabindex=[2])          #    3
        self.compare(e, 'line1', '25')                          #    25
        self.compare(e, 'line2', '36')                          # *  36
        self.compare(e, 'partial1', '150', tabindex=[4, 3, 1])  # > 150
        self.compare(e, 'partial2', '75', tabindex=[7, 5])      # > 75+
        self.compare(e, 'result', '900', tabindex=[10, 9, 8])   # = 900

        e = self.convert_operation('createmultiplication', '259*365')
        self.assertEqual(e.filter1, 259)
        self.assertEqual(e.filter2, 365)
        self.compare(e, 'support3', '12', tabindex=[16, 14])               #     12
        self.compare(e, 'support2', '35', tabindex=[10, 8])                #     35
        self.compare(e, 'support1', '24', tabindex=[4, 2])                 #     24
        self.compare(e, 'line1', '259')                                    #     259
        self.compare(e, 'line2', '365')                                    # *   365
        self.compare(e, 'partial1', '1295', tabindex=[6, 5, 3, 1])         # >  1295
        self.compare(e, 'partial2', '1554', tabindex=[12, 11, 9, 7])       # > 1554+
        self.compare(e, 'partial3', '777', tabindex=[17, 15, 13])          # > 777++
        self.compare(e, 'result', '94535', tabindex=[22, 21, 20, 19, 18])  # = 94535

        e = self.convert_operation('createmultiplication', '271*22')
        self.assertEqual(e.filter1, 271)
        self.assertEqual(e.filter2, 22)
        spt1 = self.compare(e, 'support2', '10', tabindex=[9, 7])     #    10
        spt2 = self.compare(e, 'support1', '10', tabindex=[4, 2])     #    10
        self.compare(e, 'line1', '271')                               #    271
        self.compare(e, 'line2', '22')                                # *   22
        self.compare(e, 'partial1', '542', tabindex=[5, 3, 1])        # >  542
        self.compare(e, 'partial2', '542', tabindex=[10, 8, 6])       # > 542+
        self.compare(e, 'result', '5962', tabindex=[14, 13, 12, 11])  # = 5962

        # asserts that when the support answer isn't needed (zero), his type is
        # digit_or_blank to accept an empty string
        self.assertTrue(spt1[1].type == spt2[1].type == 'digit_or_blank')

    def test_multiplicationexpressions(self):
        """
        In multiplication expressions, first the student solves the
        multiplications or divisions and then the additions or subtractions.
        """
        e = self.convert_operation('createmultiplicationexpressions', '5*8+7')
        self.assertEqual(e.filter1, 5)
        self.assertEqual(e.filter2, 8)
        self.compare(e, 'product', '40', tabindex=[1])
        self.compare(e, 'addition', '47', tabindex=[2])
        self.compare_tags(e, 'sem-zero', 'inicio-posit', 'result-posit', 'sem-divisao')

        e = self.convert_operation('createmultiplicationexpressions', '5*8-7')
        self.assertEqual(e.filter1, 5)
        self.assertEqual(e.filter2, 8)
        self.compare(e, 'product', '40', tabindex=[1])
        self.compare(e, 'addition', '33', tabindex=[2])
        self.compare_tags(e, 'sem-zero', 'inicio-posit', 'result-posit', 'sem-divisao')

        e = self.convert_operation('createmultiplicationexpressions', '5*11-9*4')
        self.assertEqual(e.filter1, 4)
        self.assertEqual(e.filter2, 11)
        self.compare(e, 'product', '55,36', joiner=',', tabindex=[1, 2])
        self.compare(e, 'addition', '19', tabindex=[3])
        self.compare_tags(e, 'sem-zero', 'inicio-posit', 'result-posit', 'sem-divisao')

        e = self.convert_operation('createmultiplicationexpressions', '-3+18/3-2*2')
        self.assertEqual(e.filter1, 2)
        self.assertEqual(e.filter2, 18)
        self.compare(e, 'product', '6,4', joiner=',', tabindex=[1, 2])
        self.compare(e, 'addition', '3,-1', joiner=',', tabindex=[3, 4])
        self.compare_tags(e, 'sem-zero', 'inicio-negat', 'result-negat', 'com-divisao')

        e = self.convert_operation('createmultiplicationexpressions', '10-4*7')
        self.assertEqual(e.filter1, 4)
        self.assertEqual(e.filter2, 7)
        self.compare(e, 'product', '28', tabindex=[1])
        self.compare(e, 'addition', '-18', tabindex=[2])
        self.compare_tags(e, 'sem-zero', 'inicio-posit', 'result-negat', 'sem-divisao')

        e = self.convert_operation('createmultiplicationexpressions', '-10+4*7')
        self.assertEqual(e.filter1, 4)
        self.assertEqual(e.filter2, 7)
        self.compare(e, 'product', '28', tabindex=[1])
        self.compare(e, 'addition', '18', tabindex=[2])
        self.compare_tags(e, 'sem-zero', 'inicio-negat', 'result-posit', 'sem-divisao')

        e = self.convert_operation('createmultiplicationexpressions', '0*7+6/3')
        self.assertEqual(e.filter1, 0)
        self.assertEqual(e.filter2, 7)
        self.compare(e, 'product', '0,2', joiner=',', tabindex=[1, 2])
        self.compare(e, 'addition', '2', tabindex=[3])
        self.compare_tags(e, 'com-zero', 'inicio-posit', 'result-posit', 'com-divisao')

    def test_multiplicationtable(self):
        e = self.convert_operation('createmultiplicationtable', '2*2')
        self.assertEqual(e.filter1, 2)
        self.assertEqual(e.filter2, 2)
        self.compare(e, 'result', '4', tabindex=[1])

        e = self.convert_operation('createmultiplicationtable', '8*7')
        self.assertEqual(e.filter1, 8)
        self.assertEqual(e.filter2, 7)
        self.compare(e, 'result', '56', tabindex=[1])

        e = self.convert_operation('createmultiplicationtable', '10*10')
        self.assertEqual(e.filter1, 10)
        self.assertEqual(e.filter2, 10)
        self.compare(e, 'result', '100', tabindex=[1])

    def test_subtraction(self):
        e = self.convert_operation('createsubtraction', '123-24')
        self.assertEqual(e.filter1, 123)
        self.assertEqual(e.filter2, 24)
        self.compare(e, 'support', '01')   #   01
        self.compare(e, 'line1', '123')    #   123
        self.compare(e, 'line2', '24')     # -  24
        self.compare(e, 'result', '099')   # = 099

        e = self.convert_operation('createsubtraction', '1000-99')
        self.assertEqual(e.filter1, 1000)
        self.assertEqual(e.filter2, 99)
        self.compare(e, 'support', '099')  #   099
        self.compare(e, 'line1', '1000')   #   1000
        self.compare(e, 'line2', '99')     # -   99
        self.compare(e, 'result', '0901')  # = 0901

    def validate_polygons(self, operation):
        # Figures with more than 12 sides are difficult to interpret, avoid
        # generate it
        with self.assertRaises(ValueError):
            e = self.convert_operation('createregularpolygonstoname', '13')

        e = self.convert_operation('createregularpolygonstoname', '12')
        self.compare(e, 'term', '12')
        answer = e.answer_set.get()  # only one answer
        self.assertEqual(answer.choice_set.count(), 10)
        correct = answer.choice_set.correct().get()  # only one correct
        self.assertEqual(correct.description, '12')

        # Figures with less than 3 sides don't exists
        with self.assertRaises(ValueError):
            e = self.convert_operation('createregularpolygonstoname', '2')

        e = self.convert_operation('createregularpolygonstoname', '3')
        self.compare(e, 'term', '3')
        answer = e.answer_set.get()  # only one answer
        self.assertEqual(answer.choice_set.count(), 10)
        correct = answer.choice_set.correct().get()  # only one correct
        self.assertEqual(correct.description, '3')

    def test_regularpolygonstoname(self):
        self.validate_polygons('createregularpolygonstoname')

    def test_nametoregularpolygons(self):
        self.validate_polygons('createnametoregularpolygons')

    def test_solidtoname(self):
        e = self.convert_operation('createsolidtoname', 'cube')
        self.compare(e, 'term', 'cube')

        answer = e.answer_set.get()  # only one answer
        self.assertEqual(answer.choice_set.count(), 11)
        correct = answer.choice_set.correct().get()  # only one correct
        self.assertEqual(correct.description, 'cube')

    def test_nametosolid(self):
        e = self.convert_operation('createnametosolid', 'cube')
        self.compare(e, 'term', 'cube')

        answer = e.answer_set.get()  # only one answer
        self.assertEqual(answer.choice_set.count(), 11)
        correct = answer.choice_set.correct().get()  # only one correct
        self.assertEqual(correct.description, 'cube')

    def test_polyhedronfaces(self):
        e = self.convert_operation('createpolyhedronfaces', 'cube')
        self.compare(e, 'term', 'cube')
        self.compare(e, 'result', '6')

        # Only polyhedrons (sphere is not a polyhedron)
        with self.assertRaises(ValueError):
            e = self.convert_operation('createpolyhedronfaces', 'sphere')

    def test_polyhedronedges(self):
        e = self.convert_operation('createpolyhedronedges', 'cube')
        self.compare(e, 'term', 'cube')
        self.compare(e, 'result', '12')

        # Only polyhedrons (sphere is not a polyhedron)
        with self.assertRaises(ValueError):
            e = self.convert_operation('createpolyhedronfaces', 'sphere')

    def test_polyhedronvertices(self):
        e = self.convert_operation('createpolyhedronvertices', 'cube')
        self.compare(e, 'term', 'cube')
        self.compare(e, 'result', '8')

        # Only polyhedrons (cone is not a polyhedron)
        with self.assertRaises(ValueError):
            e = self.convert_operation('createpolyhedronfaces', 'cone')

    def test_polyhedronvolume(self):
        e = self.convert_operation('createpolyhedronvolume', '3,3,3')
        self.compare(e, 'type', 'cube')
        self.compare(e, 'term', '3,3,3', joiner=',')
        self.compare(e, 'result', '27')

        e = self.convert_operation('createpolyhedronvolume', '3,4,5')
        self.compare(e, 'type', 'rectangular_prism')
        self.compare(e, 'term', '3,4,5', joiner=',')
        self.compare(e, 'result', '60')

    def test_tilearea(self):
        e = self.convert_operation('createtilearea', '7:1')
        self.assertEqual(e.filter1, 7)
        self.assertEqual(e.filter2, 1)
        self.compare(e, 'result', '7')

        e = self.convert_operation('createtilearea', '5:1')
        self.assertEqual(e.filter1, 5)
        self.assertEqual(e.filter2, 1)
        self.compare(e, 'result', '5')

        e = self.convert_operation('createtilearea', '7:2')
        self.assertEqual(e.filter1, 14)
        self.assertEqual(e.filter2, 2)
        self.compare(e, 'result', '14')

    def test_tileperimeter(self):
        """
        Creates various tests to assert the tiles perimeter.

        The way the square blocks are arranged gives us a specific rule for
        calculate perimeter. They are distributed from left to right, from top
        to bottom in a area equal to the next perfect square available.
        """
        # 7 squares fits in 9 and the perimeter would be 12
        e = self.convert_operation('createtileperimeter', '7:1')
        self.assertEqual(e.filter1, 12)
        self.assertEqual(e.filter2, 1)
        self.compare(e, 'result', '12')

        # 10 squares fits in 16 and the perimeter would be 14
        e = self.convert_operation('createtileperimeter', '10:1')
        self.assertEqual(e.filter1, 14)
        self.assertEqual(e.filter2, 1)
        self.compare(e, 'result', '14')

        # 21 squares fits in 25 and the perimeter would be 20
        e = self.convert_operation('createtileperimeter', '21:1')
        self.assertEqual(e.filter1, 20)
        self.assertEqual(e.filter2, 1)
        self.compare(e, 'result', '20')

        # just one square fits inside itself and we count each side
        e = self.convert_operation('createtileperimeter', '1:1')
        self.assertEqual(e.filter1, 4)
        self.assertEqual(e.filter2, 1)
        self.compare(e, 'result', '4')

        # If the square side is doubled (or the area get 4 times bigger), the
        # perimeter gets doubled too
        e = self.convert_operation('createtileperimeter', '7:4')
        self.assertEqual(e.filter1, 24)
        self.assertEqual(e.filter2, 4)
        self.compare(e, 'result', '24')

        # Can't generate if the square side is not integer
        with self.assertRaises(ValueError):
            e = self.convert_operation('createtileperimeter', '7:2')

    def test_decimaltileperimeter(self):
        # 7 squares fits in 9 and the perimeter would be 18
        e = self.convert_operation('createdecimaltileperimeter', '7:1.5', decimal_places=1)
        self.assertEqual(e.filter1, 18)
        self.assertEqual(e.filter2, D(1.5))
        self.compare(e, 'result', '18')

        # 21 squares fits in 25 and the perimeter would be
        e = self.convert_operation('createdecimaltileperimeter', '21:3.5', decimal_places=1)
        self.assertEqual(e.filter1, 70)
        self.assertEqual(e.filter2, D(3.5))
        self.compare(e, 'result', '70')

        # 21 squares fits in 25 and the perimeter would be
        e = self.convert_operation('createdecimaltileperimeter', '8:3.4', decimal_places=1)
        self.assertEqual(e.filter1, D('40.8'))
        self.assertEqual(e.filter2, D('3.4'))
        self.compare(e, 'result', '40.8')

    def test_squareroot(self):
        e = self.convert_operation('createsquareroot', '4')
        self.assertEqual(e.filter1, 4)
        self.assertEqual(e.filter2, 4)
        self.compare(e, 'result', '2')

        e = self.convert_operation('createsquareroot', '9')
        self.assertEqual(e.filter1, 9)
        self.assertEqual(e.filter2, 9)
        self.compare(e, 'result', '3')

        e = self.convert_operation('createsquareroot', '16')
        self.assertEqual(e.filter1, 16)
        self.assertEqual(e.filter2, 16)
        self.compare(e, 'result', '4')

        e = self.convert_operation('createsquareroot', '121')
        self.assertEqual(e.filter1, 121)
        self.assertEqual(e.filter2, 121)
        self.compare(e, 'result', '11')

    def test_exponents(self):
        e = self.convert_operation('createexponents', '25^0')
        self.assertEqual(e.filter1, 25)
        self.assertEqual(e.filter2, 0)
        self.compare(e, 'partial', '')  # no partial!
        self.compare(e, 'result', '1', tabindex=[1])

        e = self.convert_operation('createexponents', '25^1')
        self.assertEqual(e.filter1, 25)
        self.assertEqual(e.filter2, 1)
        self.compare(e, 'partial', '')  # no partial!
        self.compare(e, 'result', '25', tabindex=[1])

        e = self.convert_operation('createexponents', '2^2')
        self.assertEqual(e.filter1, 2)
        self.assertEqual(e.filter2, 2)
        self.compare(e, 'partial', '2,2', joiner=',', tabindex=[1, 2])
        self.compare(e, 'result', '4', tabindex=[3])

        e = self.convert_operation('createexponents', '5^4')
        self.assertEqual(e.filter1, 5)
        self.assertEqual(e.filter2, 4)
        self.compare(e, 'partial', '5,5,5,5', joiner=',', tabindex=[1, 2, 3, 4])
        self.compare(e, 'result', '625', tabindex=[5])

        e = self.convert_operation('createexponents', '13^7')
        self.assertEqual(e.filter1, 13)
        self.assertEqual(e.filter2, 7)
        self.compare(e, 'partial', '13,13,13,13,13,13,13', joiner=',', tabindex=[1, 2, 3, 4, 5, 6, 7])
        self.compare(e, 'result', '62748517', tabindex=[8])

        # 14^7 will be greater than 99.999.999, our limit due models
        # configuration
        try:
            e = self.convert_operation('createexponents', '14^7')
        except decimal.InvalidOperation:
            pass

    def test_exponents_tags(self):
        """
        Exponents exercises may have 2 tags to tell if the number is a dozen.

        The tag "dezena", which means dozen, tells the number is divisible per
        10. The tag "unidade", which means unity, tells the number isn't
        divisible by 10.
        """
        e = self.convert_operation('createexponents', '20^3')
        self.compare_tags(e, 'dezena')

        e = self.convert_operation('createexponents', '21^3')
        self.compare_tags(e, 'unidade')

    def test_divisibilitycriteria(self):
        e = self.convert_operation('createdivisibilitycriteria', '3')
        self.assertEqual(e.filter1, 3)
        self.assertEqual(e.filter2, None)
        self.compare(e, 'number', '3')  # the question is embed in a phrase

        # There will be only one answer with one correct choices and all other
        # criterias as incorrect choices
        answer = e.answer_set.get()
        self.assertEqual(answer.choice_set.count(), 9)

        # Only one correct choice
        correct = answer.choice_set.correct().get()
        self.assertEqual(
            correct.description,
            u'Quando a soma dos valores absolutos dos seus algarismos é '
            u'divisível por 3.'
        )

        # All choices from 2 to 12 are incorrect, except inexistent 7 and the
        # too complex 11
        descriptions = [
            (2, u'Quando ele termina em um algarismo par, ou seja, quando '
                u'termina em 0, 2, 4, 6 ou 8.'),
            (4, u'Quando termina em 00 ou quando o número formado pelos dois '
                u'últimos algarismos da direita for divisível por 4.'),
            (5, u'Quando ele termina em 0 ou 5.'),
            (6, u'Quando é divisível por 2 e por 3.'),
            (8, u'Quando termina em 000, ou quando o número formado pelos '
                u'três últimos algarismos da direita for divisível por 8.'),
            (9, u'Quando a soma dos valores absolutos dos seus algarismos '
                u'for divisível por 9.'),
            (10, u'Quando ele termina em 0.'),
            (12, u'Quando é divisível por 3 e por 4.'),
        ]
        for choice, desc in zip(answer.choice_set.incorrect(), descriptions):
            self.assertEqual(choice.description, desc[1])

    def test_fractionalmetersproblems(self):
        (e, f) = self.convert_operation('createfractionalmetersproblems', '2.5,m')
        self.assertEqual(e.filter1, D('2.5'))
        self.assertEqual(e.filter2, D('25'))
        self.compare(e, 'question', '2,5')
        self.compare(e, 'question_type', u'metros')
        self.compare(e, 'result_type', u'decímetros')
        self.compare(e, 'result', '25', tabindex=[1])

        self.assertEqual(f.filter1, D('2.5'))
        self.assertEqual(f.filter2, D('250'))
        self.compare(f, 'question', '2,5')
        self.compare(f, 'question_type', u'metros')
        self.compare(f, 'result_type', u'centímetros')
        self.compare(f, 'result', '250', tabindex=[1])

        e = self.convert_operation('createfractionalmetersproblems', '2.5,cm')
        self.assertEqual(e.filter1, D('2.5'))
        self.assertEqual(e.filter2, D('25'))
        self.compare(e, 'question', '2,5')
        self.compare(e, 'question_type', u'centímetros')
        self.compare(e, 'result_type', u'milímetros')
        self.compare(e, 'result', '25', tabindex=[1])

        (e, f) = self.convert_operation('createfractionalmetersproblems', '2,km')
        self.assertEqual(e.filter1, D('2'))
        self.assertEqual(e.filter2, D('20'))
        self.compare(e, 'question', '2,0')
        self.compare(e, 'question_type', u'quilômetros')
        self.compare(e, 'result_type', u'hectômetros')
        self.compare(e, 'result', '20', tabindex=[1])

        self.assertEqual(f.filter1, D('2'))
        self.assertEqual(f.filter2, D('200'))
        self.compare(f, 'question', '2,0')
        self.compare(f, 'question_type', u'quilômetros')
        self.compare(f, 'result_type', u'decâmetros')
        self.compare(f, 'result', '200', tabindex=[1])

    def test_isoscelestrianglearea(self):
        e = self.convert_operation('createisoscelestrianglearea', '2,10')
        self.assertEqual(e.filter1, 2)   # base
        self.assertEqual(e.filter2, 10)  # height
        self.compare(e, 'base', '2')
        self.compare(e, 'height', '10')
        self.compare(e, 'result', '10', tabindex=[1])

        e = self.convert_operation('createisoscelestrianglearea', '13,8')
        self.assertEqual(e.filter1, 13)  # base
        self.assertEqual(e.filter2, 8)   # height
        self.compare(e, 'base', '13')
        self.compare(e, 'height', '8')
        self.compare(e, 'result', '52', tabindex=[1])

    def test_righttrianglearea(self):
        e = self.convert_operation('createrighttrianglearea', '3,12')
        self.assertEqual(e.filter1, 3)   # base
        self.assertEqual(e.filter2, 12)  # height
        self.compare(e, 'base', '3')
        self.compare(e, 'height', '12')
        self.compare(e, 'result', '18', tabindex=[1])

        e = self.convert_operation('createrighttrianglearea', '11,4')
        self.assertEqual(e.filter1, 11)  # base
        self.assertEqual(e.filter2, 4)   # height
        self.compare(e, 'base', '11')
        self.compare(e, 'height', '4')
        self.compare(e, 'result', '22', tabindex=[1])

    def test_isoscelestrianglearea_fails_for_decimal(self):
        """
        Decimal result isosceles triangle area won't be generated.
        """
        try:
            self.convert_operation('createisoscelestrianglearea', '13,7')
            raise AssertionError('A decimal result isosceles triangle area '
                                 'shouldn\'t be generated.')
        except CommandError:
            pass

    def test_straightlinecombination(self):
        """
        Tests straight line combinations based in a known image.

        As we know the image, the combinations are also known.
        """
        e = self.convert_operation('createstraightlinecombination', 'a,b')
        self.compare(e, 'term1', 'a')
        self.compare(e, 'term2', 'b')
        answer = e.answer_set.get()

        self.assertEqual(answer.choice_set.count(), 3)

        correct = answer.choice_set.correct().get()
        self.assertEqual(correct.description, u'Paralelas')

        incorrects = [u'Secantes/concorrentes e perpendiculares',
                      u'Secantes/concorrentes e não perpendiculares']
        for choice in answer.choice_set.incorrect():
            incorrects.remove(choice.description)
        self.assertEqual(incorrects, [])  # assert cleared the incorrects

        e = self.convert_operation('createstraightlinecombination', 'a,c')
        self.compare(e, 'term1', 'a')
        self.compare(e, 'term2', 'c')
        answer = e.answer_set.get()

        self.assertEqual(answer.choice_set.count(), 3)

        correct = answer.choice_set.correct().get()
        self.assertEqual(correct.description,
                         u'Secantes/concorrentes e não perpendiculares')

        incorrects = [u'Paralelas', u'Secantes/concorrentes e perpendiculares']
        for choice in answer.choice_set.incorrect():
            incorrects.remove(choice.description)
        self.assertEqual(incorrects, [])  # assert cleared the incorrects

    def test_findprimenumber(self):
        e = self.convert_operation('createfindprimenumber', '7')
        self.assertEqual(e.filter1, 7)
        answer = e.answer_set.get()  # only one answer
        self.assertEqual(answer.choice_set.count(), 30)
        correct = answer.choice_set.correct().get()  # only one correct
        self.assertEqual(correct.description, '7')

        e = self.convert_operation('createfindprimenumber', '11')
        self.assertEqual(e.filter1, 11)
        answer = e.answer_set.get()  # only one answer
        self.assertEqual(answer.choice_set.count(), 30)
        correct = answer.choice_set.correct().get()  # only one correct
        self.assertEqual(correct.description, '11')

    def test_identifypolygons(self):
        e = self.convert_operation('createidentifypolygons', 'losango')
        self.compare(e, 'term', 'rhombus')  # term is the image filename

        answer = e.answer_set.get()  # only one answer
        self.assertEqual(answer.choice_set.count(), 9)

        correct = answer.choice_set.correct().get()  # only one correct
        self.assertEqual(correct.description, 'losango')

        descriptions = [
            'quadrado',
            u'triângulo isósceles',
            u'trapézio',
            'paralelogramo',
            u'triângulo retângulo',
            u'triângulo equilátero',
            u'retângulo',
            u'triângulo escaleno',
        ]
        for choice in answer.choice_set.incorrect():
            descriptions.remove(choice.description)
        self.assertEqual(descriptions, [])

        e = self.convert_operation('createidentifypolygons', 'paralelogramo')
        self.compare(e, 'term', 'parallelogram')

        answer = e.answer_set.get()  # only one answer
        self.assertEqual(answer.choice_set.count(), 9)

        correct = answer.choice_set.correct().get()  # only one correct
        self.assertEqual(correct.description, 'paralelogramo')

        descriptions = [
            'quadrado',
            u'triângulo escaleno',
            u'triângulo isósceles',
            u'trapézio',
            u'triângulo retângulo',
            u'triângulo equilátero',
            u'retângulo',
            'losango',
        ]
        for choice in answer.choice_set.incorrect():
            descriptions.remove(choice.description)
        self.assertEqual(descriptions, [])

    def test_fractiontopercentage(self):
        e = self.convert_operation('createfractiontopercentage', '3/100')
        self.assertEqual(e.filter1, 3)
        self.assertEqual(e.filter2, None)
        self.compare(e, 'term1', '3')
        self.compare(e, 'term2', '100')
        self.compare(e, 'result', '3')

        e = self.convert_operation('createfractiontopercentage', '10/100')
        self.assertEqual(e.filter1, 10)
        self.assertEqual(e.filter2, None)
        self.compare(e, 'term1', '10')
        self.compare(e, 'term2', '100')
        self.compare(e, 'result', '10')

    def test_percentagetofraction(self):
        e = self.convert_operation('createpercentagetofraction', '3')
        self.assertEqual(e.filter1, 3)
        self.assertEqual(e.filter2, None)
        self.compare(e, 'question', '3')
        self.compare(e, 'result', '3/100', joiner='/', tabindex=[1, 2])

        e = self.convert_operation('createpercentagetofraction', '10')
        self.assertEqual(e.filter1, 10)
        self.assertEqual(e.filter2, None)
        self.compare(e, 'question', '10')
        self.compare(e, 'result', '10/100', joiner='/', tabindex=[1, 2])

    def test_fractiontodecimal(self):
        e = self.convert_operation('createfractiontodecimal', '15/100')
        self.assertEqual(e.filter1, 15)
        self.assertEqual(e.filter2, None)
        self.compare(e, 'term1', '15')
        self.compare(e, 'term2', '100')
        self.compare(e, 'result', '0.15', tabindex=[1])

        e = self.convert_operation('createfractiontodecimal', '333/100')
        self.assertEqual(e.filter1, 333)
        self.assertEqual(e.filter2, None)
        self.compare(e, 'term1', '333')
        self.compare(e, 'term2', '100')
        self.compare(e, 'result', '3.33', tabindex=[1])

    def test_decimaltofraction(self):
        e = self.convert_operation('createdecimaltofraction', '0.33')
        self.assertEqual(e.filter1, D('0.33'))
        self.assertEqual(e.filter2, None)
        self.compare(e, 'question', '0.33')
        self.compare(e, 'result', '33/100', joiner='/', tabindex=[1, 2])

        e = self.convert_operation('createdecimaltofraction', '0.53')
        self.assertEqual(e.filter1, D('0.53'))
        self.assertEqual(e.filter2, None)
        self.compare(e, 'question', '0.53')
        self.compare(e, 'result', '53/100', joiner='/', tabindex=[1, 2])

        e = self.convert_operation('createdecimaltofraction', '1.53')
        self.assertEqual(e.filter1, D('1.53'))
        self.assertEqual(e.filter2, None)
        self.compare(e, 'question', '1.53')
        self.compare(e, 'result', '153/100', joiner='/', tabindex=[1, 2])

    def test_rectanglearea(self):
        e = self.convert_operation('createrectanglearea', '7,3')
        self.assertEqual(e.filter1, 7)  # base
        self.assertEqual(e.filter2, 3)  # height
        self.compare(e, 'base', '7')
        self.compare(e, 'height', '3')
        self.compare(e, 'result', '21')

        e = self.convert_operation('createrectanglearea', '10,10')
        self.assertEqual(e.filter1, 10)  # base
        self.assertEqual(e.filter2, 10)  # height
        self.compare(e, 'base', '10')
        self.compare(e, 'height', '10')
        self.compare(e, 'result', '100')

    def test_parallelogramarea(self):
        e = self.convert_operation('createparallelogramarea', '10,53')
        self.assertEqual(e.filter1, 10)  # base
        self.assertEqual(e.filter2, 53)  # height
        self.compare(e, 'base', '10')
        self.compare(e, 'height', '53')
        self.compare(e, 'result', '530', tabindex=[1])

        e = self.convert_operation('createparallelogramarea', '12,16')
        self.assertEqual(e.filter1, 12)  # base
        self.assertEqual(e.filter2, 16)  # height
        self.compare(e, 'base', '12')
        self.compare(e, 'height', '16')
        self.compare(e, 'result', '192', tabindex=[1])

    def test_trapezoidarea(self):
        e = self.convert_operation('createtrapezoidarea', '16,14,80')
        self.assertEqual(e.filter1, 16)  # base
        self.assertEqual(e.filter2, 14)  # height
        self.compare(e, 'base1', '16')
        self.compare(e, 'base2', '13')
        self.compare(e, 'height', '14')
        self.compare(e, 'result', '203', tabindex=[1])

        e = self.convert_operation('createtrapezoidarea', '9,4,65')
        self.assertEqual(e.filter1, 9)  # base
        self.assertEqual(e.filter2, 4)  # height
        self.compare(e, 'base1', '9')
        self.compare(e, 'base2', '6')
        self.compare(e, 'height', '4')
        self.compare(e, 'result', '30', tabindex=[1])

    def test_measuresegment(self):
        e = self.convert_operation('createmeasuresegment', 'a,c,r')
        self.assertEqual(e.filter1, 0)  # value of first term ex: a
        self.assertEqual(e.filter2, 6)  # value of second term ex: c
        self.compare(e, 'points', 'ac')
        self.compare(e, 'straight', 'r')
        self.compare(e, 'segments', '0,4,6,9,10', joiner=',')
        self.compare(e, 'result', '6', tabindex=[1])

        e = self.convert_operation('createmeasuresegment', 'b,d,r')
        self.assertEqual(e.filter1, 4)   # value of first term ex: b
        self.assertEqual(e.filter2, 9)   # value of second term ex: d
        self.compare(e, 'points', 'bd')
        self.compare(e, 'straight', 'r')
        self.compare(e, 'segments', '0,4,6,9,10', joiner=',')
        self.compare(e, 'result', '5', tabindex=[1])

    def test_gcd(self):
        e = self.convert_operation('creategcd', 'MDC(12, 18)', terms=2)
        self.compare(e, 'numbers', '12,18', joiner=',')
        self.compare(e, 'result', '6', tabindex=[13])
        self.compare(e, 'divisors', '2,2,3,3', joiner=',', tabindex=[1, 4, 7, 10])
        self.compare(e, 'steps', '6,9,3,9,1,3,1,1', joiner=',', tabindex=[2, 3, 5, 6, 8, 9, 11, 12])

        e = self.convert_operation('creategcd', 'MDC(50, 32)', terms=2)
        self.compare(e, 'numbers', '50,32', joiner=',')
        self.compare(e, 'result', '2', tabindex=[22])
        self.compare(e, 'divisors', '2,2,2,2,2,5,5', joiner=',',
                     tabindex=[1, 4, 7, 10, 13, 16, 19])
        self.compare(e, 'steps', '25,16,25,8,25,4,25,2,25,1,5,1,1,1', joiner=',',
                     tabindex=[2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 18, 20, 21])
