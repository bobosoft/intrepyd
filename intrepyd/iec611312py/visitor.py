"""
Copyright (C) 2018 Roberto Bruttomesso <roberto.bruttomesso@gmail.com>

This file is distributed under the terms of the 3-clause BSD License.
A copy of the license can be found in the root directory or at
https://opensource.org/licenses/BSD-3-Clause.

Author: Roberto Bruttomesso <roberto.bruttomesso@gmail.com>
  Date: 02/11/2018

This module implements a generic vistor infrastructure
"""

from intrepyd.iec611312py.statement import Assignment
from intrepyd.iec611312py.expression import VariableOcc, Expression

class Visitor(object):
    """
    Abstract visitor class
    """
    def visit(self, obj):
        """
        Dispatches visit to a proper method
        """
        if isinstance(obj, Assignment):
            return self._visit_assignment(obj)
        elif isinstance(obj, Expression):
            return self._visit_expression(obj)
        elif isinstance(obj, VariableOcc):
            return self._visit_variable_occ(obj)
        raise TypeError('Type not found')

    def _visit_assignment(self, obj):
        """
        Visits Assignment
        """
        raise NotImplementedError

    def _visit_expression(self, obj):
        """
        Visits Expression
        """
        raise NotImplementedError

    def _visit_variable_occ(self, obj):
        """
        Visits Variable occurrence
        """
        raise NotImplementedError
