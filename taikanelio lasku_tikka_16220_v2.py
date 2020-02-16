# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 15:32:29 2020

@author: pauli
"""

#%% To solve macig cube(5X5) with MILP in PYTHON, Tikka 16.2.2020
#Compare to solving example of the system of equations 3 * x0 + x1 = 9 and x0 + 2 * x1 = 8:
#%https://developers.google.com/optimization/mip/mip_var_array
import numpy as np 
a1=65-(12+20+24)
a2=65-(14+21+17)
a3=65-(16+13+23)
a4=65-(22+15+18)
a5=65-(25+19)
a6=65-(12+14+25)
a7=65-(20+21+16)
a8=65-(17+13+22)
a9=65-(23+15+19)
a10=65-(24+18)
a11=65-(25+13+24)
a12=65-(12+21+13+15)
#%%
a = [   [1,1,0,0,0,0,0,0,0,0,0],
        [0,0,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,0,0,0],
        [0,0,0,0,0,0,1,1,0,0,0],
        [0,0,0,0,0,0,0,0,1,1,1],    
        [0,0,0,0,1,0,1,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,0,0],
        [1,0,0,0,0,0,0,0,0,1,0],    
        [0,1,1,0,0,0,0,0,0,0,0],        
        [0,0,0,1,0,1,0,0,0,0,1],    
        [0,0,1,0,0,0,0,1,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,1]  ]
b = [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12]

#https://scriptverse.academy/tutorials/python-solve-linear-equations.html

#%% MILP to the rescue!! (install first MS visual basic latest and then ortools with anaconda)
from __future__ import print_function
from ortools.linear_solver import pywraplp
#%
def create_data_model():
  """Stores the data for the problem."""
  data = {}
  data['constraint_coeffs'] =a 
  data['bounds'] = b
  data['obj_coeffs'] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
  data['num_vars'] = 11
  data['num_constraints'] = 12
  return data


def main():
  data = create_data_model()
  # Create the mip solver with the CBC backend.
  solver = pywraplp.Solver('simple_mip_program',
                           pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
#  solver.Add(data <= 3.5)
  infinity = solver.infinity()
#  model.Add(x != y)
  x = {}
  for j in range(data['num_vars']):
    x[j] = solver.IntVar(1, 11, 'x[%i]' % j)
  print('Number of variables =', solver.NumVariables())

  for i in range(data['num_constraints']):
    constraint = solver.RowConstraint(0, data['bounds'][i], '')
    for j in range(data['num_vars']):
      constraint.SetCoefficient(x[j], data['constraint_coeffs'][i][j])
  print('Number of constraints =', solver.NumConstraints())
  # In Python, you can also set the constraints as follows.
  # for i in range(data['num_constraints']):
  #  constraint_expr = \
  # [data['constraint_coeffs'][i][j] * x[j] for j in range(data['num_vars'])]
  #  solver.Add(sum(constraint_expr) <= data['bounds'][i])

  objective = solver.Objective()
  for j in range(data['num_vars']):
    objective.SetCoefficient(x[j], data['obj_coeffs'][j])
  objective.SetMaximization()
  # In Python, you can also set the objective as follows.
  # obj_expr = [data['obj_coeffs'][j] * x[j] for j in range(data['num_vars'])]
  # solver.Maximize(solver.Sum(obj_expr))

  status = solver.Solve()

  if status == pywraplp.Solver.OPTIMAL:
    print('Objective value =', solver.Objective().Value())
    for j in range(data['num_vars']):
      print(x[j].name(), ' = ', x[j].solution_value())
    print()
    print('Problem solved in %f milliseconds' % solver.wall_time())
    print('Problem solved in %d iterations' % solver.iterations())
    print('Problem solved in %d branch-and-bound nodes' % solver.nodes())
  else:
    print('The problem does not have an optimal solution.')


if __name__ == '__main__':
  main()
  
#%% Press enter above, and see what happens! :)