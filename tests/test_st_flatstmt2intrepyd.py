"""
Copyright (C) 2018 Roberto Bruttomesso <roberto.bruttomesso@gmail.com>

This file is distributed under the terms of the 3-clause BSD License.
A copy of the license can be found in the root directory or at
https://opensource.org/licenses/BSD-3-Clause.

Author: Roberto Bruttomesso <roberto.bruttomesso@gmail.com>
  Date: 30/12/2018
"""

import unittest
from intrepyd.iec611312py.plcopen import parsePlcOpenFile
from intrepyd.iec611312py.parsest import parseST
from intrepyd.iec611312py.variable import Variable
from intrepyd.iec611312py.flatstmt2intrepyd import FlatStmt2Intrepyd
from intrepyd.iec611312py.flattener import flattenStmtBlock
from intrepyd.iec611312py.expression import VariableOcc, Ite
from intrepyd.iec611312py.statement import Assignment
from intrepyd.iec611312py.datatype import Primitive, Struct

boolType = Primitive('BOOL')
intType = Primitive('INT')
FALSE = 'ctx.mk_false()'
TRUE = 'ctx.mk_true()'

class TestSTFlatStmt2Intrepyd(unittest.TestCase):
    def normalize_string(self, string):
        string = string.replace(' ', '')
        string = string.replace('\n', '')
        return string

    def _run_tests(self, program, name2var, var2latch, expected):
        statements = parseST(program, name2var)
        flattened_statements = flattenStmtBlock(statements)
        flatstmt2intrepyd = FlatStmt2Intrepyd(4, 'ctx', var2latch)
        flatstmt2intrepyd.processStatements(flattened_statements)
        self.assertEquals(self.normalize_string(expected),
                          self.normalize_string(flatstmt2intrepyd.result))

    def test_assignment_1(self):
        name2var = {
            'In1' : Variable('In1', boolType, Variable.INPUT),
            'In2' : Variable('In2', boolType, Variable.INPUT),
            'Out1' : Variable('Out1', boolType, Variable.OUTPUT)
        }
        program = 'Out1 := In1 AND In2;'
        expected = \
            """
            __tmp_1 = ctx.mk_and(In1, In2)
            Out1 = __tmp_1
            """
        self._run_tests(program, name2var, {}, expected)

    def test_assignment_2(self):
        name2var = {
            'a' : Variable('a', boolType, Variable.INPUT),
            'b' : Variable('b', boolType, Variable.INPUT),
            'c' : Variable('c', boolType, Variable.LOCAL),
        }
        program = 'c := a AND b;'
        expected = \
            """
            __tmp_1 = ctx.mk_and(a, b)
            ctx.set_latch_init_next(latch, ctx.mk_false(), __tmp_1)
            """
        self._run_tests(program, name2var, {'c': ('latch', FALSE)}, expected)

    def test_if_1(self):
        name2var = {
            'a' : Variable('a', boolType, Variable.LOCAL),
            'b' : Variable('b', boolType, Variable.LOCAL),
            'c' : Variable('c', boolType, Variable.LOCAL),
        }
        program = \
            """
            IF a THEN
                b := c;
            END_IF;
            """
        expected = \
            """
            __tmp_1 = ctx.mk_ite(a,c,b)
            b = __tmp_1
            """
        self._run_tests(program, name2var, {}, expected)

    def test_case_1(self):
        name2var = {
            'a' : Variable('a', intType, Variable.LOCAL),
            'b' : Variable('b', boolType, Variable.LOCAL),
            'c' : Variable('c', boolType, Variable.LOCAL),
            'd' : Variable('d', boolType, Variable.LOCAL),
        }
        program = \
            """
            CASE a OF
            0:
                b := c;
            END_CASE;
            """
        expected = \
            """
            __tmp_1 = ctx.mk_eq(a, 0)
            __tmp_2 = ctx.mk_ite(__tmp_1,c,b)
            b = __tmp_2
            """
        self._run_tests(program, name2var, {}, expected)
