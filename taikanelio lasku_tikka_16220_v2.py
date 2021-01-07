# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 15:53:13 2020

@author: pauli
#Update, note, use linear program instead of mixed one
"""

#%%
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 15:32:29 2020
@author: pauli
"""

#%% To solve macig cube(5X5) with MILP in PYTHON, Tikka 16.2.2020
#Compare to solving example of the system of equations 3 * x0 + x1 = 9 and x0 + 2 * x1 = 8:
#%https://developers.google.com/optimization/mip/mip_var_array
import numpy as np 
a1=65-(21+20+18) #check..
a2=65-(16+23)
a3=65-(12+22+15)
a4=65-(13+14+24)
a5=65-(19+25+17)
a6=65-(21+12+19)
a7=65-(18+22+13)
a8=65-(16+14+25)
a9=65-(15+24+17)
a10=65-(20+23)
a11=65-(20+13+19)
a12=65-(21+24)
#a13=1+2+3+4+5+6+7+8+9+10+11
#%% [a,b,c,d,e,f,g,h,i,j,k] (the blanks that need to be solved with either 0/1 for every aux variable a(i))
#[1,2,3,4,5,6,7,8,9,10,11]
a = [   [1,1,0,0,0,0,0,0,0,0,0],
        [0,0,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,0,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,0,0],
        [0,0,0,0,0,0,0,0,0,1,1],       
        [0,0,1,0,0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0,0,0,1,0],
        [1,0,0,0,0,1,0,0,0,0,0],    
        [0,1,0,0,1,0,0,0,0,0,0],        
        [0,0,0,0,0,0,1,0,1,0,1],    
        [0,0,0,0,1,1,0,0,0,0,0],
        [0,0,0,1,0,1,0,0,0,0,1]]
#        [1,1,1,1,1,1,1,1,1,1,1]]
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
  data['num_constraints'] =12
  return data

#check also
#https://stackoverflow.com/questions/56042803/constrained-optimization-in-python-where-one-variable-depends-on-another-variabl
def main():
  data = create_data_model()
  # Create the mip solver with the CBC backend.
  solver = pywraplp.Solver('SolveSimpleSystem',
                           pywraplp.Solver.BOP_INTEGER_PROGRAMMING)
#  https://stackoverflow.com/questions/59116520/linear-programming-google-ortools-incorrect-decision-variable-final-values
#Note, this is integer problem, eventhough there are constraints
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

#Of course you can use matrix algebra (with python or Matlab), or, :)

#Pauli, 23717. Solving 5x5 magic qube spots, a+20+16+b+21=65 etc.:

#At matlab:
>>Ax=zeros(12,11) 		#11 variables, 12 equations, then fill a, bs, etc.s with 1:
>>Ax=[1	1	0	0	0	0	0	0	0	0	0
0	0	1	0	0	0	0	0	0	0	0
0	0	0	1	1	1	0	0	0	0	0
0	0	0	0	0	0	1	1	0	0	0
0	0	0	0	0	0	0	0	1	1	1
1	0	0	0	0	0	0	0	1	0	0
0	0	0	0	0	0	1	0	0	1	0
0	0	0	1	0	0	0	0	0	0	1
0	1	0	0	1	0	0	1	0	0	0
0	0	1	0	0	1	0	0	0	0	0
0	0	0	1	0	0	1	0	1	0	0
1	0	0	1	0	0	0	1	0	0	0];

>>Bx=[8                                  # 65-the rest makes a vector
1
25
16
16
14
12
13
22
5
25
25];

>> X=linsolve(Ax,Bx);        # the spots, Xs
>> X
X =
    6.0000
    2.0000
    1.0000
   10.0000
   11.0000
    4.0000
    7.0000
    9.0000
    8.0000
    5.0000
3.0000

#Refill the original magic cube with the missing above number (a=6, b=2 etc.). Solved.

