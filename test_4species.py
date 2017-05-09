import csv
import numpy as np
import random, operator
from my_operators import safe_div, mylog, mypower2, mypower3, mysqrt, myexp
from deap import gp

for i in range(1,2):
    problem='Tower2'
    p=1801
    n_corr=i
    n_archivo='./Results/%s/pop_file_%d_%d.txt'%(problem,p,n_corr)
    Matrix = np.empty((10000, 5,))
    
    cont=0
    gen=0

    pset = gp.PrimitiveSet("MAIN", 25)
    pset.addPrimitive(operator.add, 2)
    pset.addPrimitive(operator.sub, 2)
    pset.addPrimitive(operator.mul, 2)
    pset.addPrimitive(safe_div, 2)
    pset.addPrimitive(np.cos, 1)
    pset.addPrimitive(np.sin, 1)
    #pset.addPrimitive(myexp, 1)
    pset.addPrimitive(mylog, 1)
    pset.addPrimitive(mypower2, 1)
    pset.addPrimitive(mypower3, 1)
    pset.addPrimitive(mysqrt, 1)
    pset.addPrimitive(np.tan, 1)
    pset.addPrimitive(np.tanh, 1)
    pset.addEphemeralConstant("rand101", lambda: random.uniform(-1, 1))
	#pset.renameArguments(ARG0='x0',ARG1='x1', ARG2='x2', ARG3='x3', ARG4='x4', ARG5='x5', ARG6='x6', ARG7='x7',  ARG8='x8', ARG9='x9',  ARG10='x10',  ARG11='x11',  ARG12='x12')
    pset.renameArguments(ARG0='x0',ARG1='x1', ARG2='x2', ARG3='x3', ARG4='x4', ARG5='x5', ARG6='x6', ARG7='x7',
                     ARG8='x8', ARG9='x9', ARG10='x10', ARG11='x11', ARG12='x12', ARG13='x13', ARG14='x14', ARG15='x15',
                     ARG16='x16', ARG17='x17', ARG18='x18', ARG19='x19', ARG20='x20', ARG21='x21', ARG22='x22', ARG23='x23', ARG24='x24')
	
	# pset = gp.PrimitiveSet("MAIN", 13)
	# pset.addPrimitive(operator.add, 2)
	# pset.addPrimitive(operator.sub, 2)
	# pset.addPrimitive(operator.mul, 2)
	# pset.addPrimitive(safe_div, 2)
	# pset.addPrimitive(np.cos, 1)
	# pset.addPrimitive(np.sin, 1)
	# #pset.addPrimitive(myexp, 1)
	# pset.addPrimitive(mylog, 1)
	# pset.addPrimitive(mypower2, 1)
	# pset.addPrimitive(mypower3, 1)
	# pset.addPrimitive(mysqrt, 1)
	# pset.addPrimitive(np.tan, 1)
	# pset.addPrimitive(np.tanh, 1)
	# pset.addEphemeralConstant("rand101", lambda: random.uniform(-1, 1))
	

    with open(n_archivo) as spambase:
        spamReader = csv.reader(spambase, delimiter=';', skipinitialspace=True)
        for row in spamReader:
            if (row!=[]):
                try:
                    if cont<100:
                        print ''
                        #Matrix[cont, 0] = int(0)
                        #Matrix[cont,1]=row[0]
                        #ind1 = gp.PrimitiveTree.from_string(row[1], pset)
                        #Matrix[cont, 2]=len(ind1)
                        #Matrix[cont, 3] = ind1.height+1
                        #print row[0], row[1]
                    elif '-------------' in row[0]:
                        cont-=1
                        gen+=1
                    elif len(row)>2:
                        c2=cont-100
                        Matrix[c2, 0] = int(gen)
                        Matrix[c2, 1] = row[1]
                        ind1=gp.PrimitiveTree.from_string(row[2], pset)
                        Matrix[c2, 2] = len(ind1)
                        Matrix[c2, 3] = ind1.height+1
                    cont += 1
                except ValueError:
                    print ''

    cont=0
    n_archivot='./Specie/%s/specieind_%d_%d.txt'%(problem,p,n_corr)
    with open(n_archivot) as spambase:
        spamReader = csv.reader(spambase, delimiter=';', skipinitialspace=True)
        for row in spamReader:
            if (row!=[]):
                try:
                    if '--' not in row[0]:
                        if cont>=100:
                            c2=cont-100
                            Matrix[c2, 4] = row[0]
                        cont += 1
                except ValueError:
                    print ''

    Matrix.view('i8,f8,i8,i8,i8').sort(order=['f0','f4'], axis=0)


    np.savetxt('./M_Specie/%s_%d_%d.txt' % (problem,p, n_corr), Matrix, delimiter=",", fmt="%s")