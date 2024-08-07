from gekko import GEKKO

#m = GEKKO(remote = False)

m = GEKKO(remote = False)

m.options.SOLVER = 1

m.solver_options = ['minlp_maximum_iterations 500', \
                    # minlp iterations with integer solution
                    'minlp_max_iter_with_int_sol 10', \
                    # treat minlp as nlp
                    'minlp_as_nlp 0', \
                    # nlp sub-problem max iterations
                    'nlp_maximum_iterations 50', \
                    # 1 = depth first, 2 = breadth first
                    'minlp_branch_method 1', \
                    # maximum deviation from whole number
                    'minlp_integer_tol 0.05', \
                    # covergence tolerance
                    'minlp_gap_tol 0.01']

# (+ 12157 35563)  47720

q0 = 3029
q1 = 7027
q2 = 3429
q3 = 9041
q4 = 3677
q5 = 2164
q6 = 3497
q7 = 4731
q8 = 4753
q9 = 6372

p0 = 98.2046
p1 = 100.1812
p2 = 99.6207
p3 = 100.1746
p4 = 98.9762
p5 = 98.0859
p6 = 100.5188
p7 = 100.0064
p8 = 100.5751
p9 = 98.2218

m0  = m.Var(value = 245  , lb=0, ub = 47720)
m1  = m.Var(value = 1367, lb=0, ub = 47720)
m2  = m.Var(value = 1324, lb=0, ub = 47720)
m3  = m.Var(value = 1367, lb=0, ub = 47720)
m4  = m.Var(value = 1266, lb=0, ub = 47720)
m5  = m.Var(value = 1207, lb=0, ub = 47720)
m6  = m.Var(value = 1393, lb=0, ub = 47720)
m7  = m.Var(value = 1356, lb=0, ub = 47720)
m8  = m.Var(value = 1397, lb=0, ub = 47720)
m9  = m.Var(value = 1236, lb=0, ub = 47720)

s0 =  m.Var(value = 2784 , lb = 0, ub = 47720)
s1 =  m.Var(value = 5660 , lb = 0, ub = 47720)
s2 =  m.Var(value = 2105 , lb = 0, ub = 47720)
s3 =  m.Var(value = 7674 , lb = 0, ub = 47720)
s4 =  m.Var(value = 2411 , lb = 0, ub = 47720)
s5 =  m.Var(value = 957   , lb = 0, ub = 47720)
s6 =  m.Var(value = 2104 , lb = 0, ub = 47720)
s7 =  m.Var(value = 3375 , lb = 0, ub = 47720)
s8 =  m.Var(value = 3356 , lb = 0, ub = 47720)
s9 =  m.Var(value = 5136 , lb = 0, ub = 47720)

m.Equation(s0 + s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8 + s9 == 35562)
m.Equation(m0 + m1 + m2 + m3 + m4 + m5 + m6 + m7 + m8 + m9 == 12158)

m.Equation( m0 + s0 == q0)
m.Equation( m1 + s1 == q1)
m.Equation( m2 + s2 == q2)
m.Equation( m3 + s3 == q3)
m.Equation( m4 + s4 == q4)
m.Equation( m5 + s5 == q5)
m.Equation( m6 + s6 == q6)
m.Equation( m7 + s7 == q7)
m.Equation( m8 + s8 == q8)
m.Equation( m9 + s9 == q9)

m.Obj( (s0 * p0 + s1 * p1 + s2 * p2 + s3 * p3 + s4 * p4 + s5 * p5 + s6 * p6 + s7 * p7 + s8 * p8 + s9 * p9) - (m0 * p0 + m1 * p1 + m2 * p2 + m3 * p3 + m4 * p4 + m5 * p5 + m6 * p6 + m7 * p7 + m8 * p8 + m9 * p9) )

m.solve(disp = True)
