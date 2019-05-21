import csv
from neatGPLS import ensure_dir
from heapq import nsmallest
from my_operators import safe_div, mylog, mypower2, mypower3, mysqrt, myexp, negative, absolute, negexp
import random, operator
import numpy as np
from deap import gp
from numpy import median

pset = gp.PrimitiveSet("MAIN", 25)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(safe_div, 2)
pset.addPrimitive(np.cos, 1)
pset.addPrimitive(np.sin, 1)
pset.addPrimitive(myexp, 1)
pset.addPrimitive(mylog, 1)
pset.addPrimitive(mypower2, 1)
pset.addPrimitive(mypower3, 1)
pset.addPrimitive(mysqrt, 1)
pset.addPrimitive(np.tan, 1)
pset.addPrimitive(np.tanh, 1)
pset.addPrimitive(negative, 1)
pset.addPrimitive(negexp, 1)
pset.addPrimitive(absolute, 1)
pset.addEphemeralConstant("rand101", lambda: random.uniform(-1, 1))
pset.renameArguments(ARG0='x0', ARG1='x1', ARG2='x2', ARG3='x3', ARG4='x4', ARG5='x5', ARG6='x6', ARG7='x7',  ARG8='x8',
                     ARG9='x9',  ARG10='x10',  ARG11='x11',  ARG12='x12', ARG13='x13',
                     ARG14='x14', ARG15='x15', ARG16='x16', ARG17='x17', ARG18='x18', ARG19='x19', ARG20='x20',
                     ARG21='x21', ARG22='x22',
                     ARG23='x23', ARG24='x24')

def identity(x):
    return x

def len_ind(x):
    return x[1]

def fitness(x):
    return x[1]

def my_min(sequence, key_func=None, num_ =3):
    """
    Return the minimum element of a sequence.
    key_func is an optional one-argument ordering function.
    """
    if not sequence:
        raise ValueError('empty sequence')

    if not key_func:
        key_func = identity

    minimum = sequence[0]

    for item in sequence:
        # Ask the key func which property to compare
        if key_func(item) < key_func(minimum):
            minimum = item

    return minimum

def my_max(sequence, key_func=None):
    """
    Return the maximum element of a sequence.
    key_func is an optional one-argument ordering function.
    """
    if not sequence:
        raise ValueError('empty sequence')

    if not key_func:
        key_func = identity

    maximum = sequence[0]

    for item in sequence:
        # Ask the key func which property to compare
        if key_func(item) > key_func(maximum):
            maximum = item

    return maximum
#  c2=my_min(data, key_func=fitness)

def convrt(strg):
    strg = strg.replace(" ", "")
    str2 = strg.replace('(', ',')
    str2 = str2.replace(')', ',')
    text = str2.split(',')
    str_list = filter(None, text)
    return str_list



def get_args(strg, args):
    args_ = list()
    st = strg
    lin_tree=convrt(st)
    if len(args) >= 1:
        for id in args:
            if id in lin_tree:
                args_.append(id)
    return args_


def convrt_token(strg):
        strg = strg.replace(" ", "")
        str2 = strg.replace('(', ',')
        str2 = str2.replace(')', ',')
        text = str2.split(',')
        str_list = filter(None, text)
        return str_list


def add_subt(strg, params_):
    params = params_
    st = strg
    str2add = convrt_token(st)
    str_linear = ['add', str(params[0]), 'mul', str(params[1])]
    lin_tree = []
    for n in range(2, len(str2add)+2):
        cad = 'mul(%s)' % params[n]
        cad = convrt_token(cad)
        cad.append(str2add[n-2])
        lin_tree = lin_tree + cad
    lin_tree = str_linear + lin_tree
    return lin_tree


def get_data2(index_, out, out1):
    data = list()
    data3 = list()
    individuals = list()
    args= list()
    if len(pset.arguments) >= 1:
        for arg in pset.arguments:
            args.append(arg)

    for i in range(0, 10):
        cont = 0
        #direccion = "/media/treelab/84DF-9E7F/archivos_graficas/GraficasConvergenciaNGPLS_1/datosgraficas_Oct/Results/%s/bestind_LStr_%d_%d.txt"% (index_, i)
        #direccion = "./Results/%s/bestind_LStr_%d_%d.txt" % (directory, index_, i)
        direccion = "/home/treelab/Documents/Resultos/bestind_LStr_%d_0%d.txt" % (index_, i)
        with open(direccion) as spambase:
            spamReader = csv.reader(spambase,  delimiter=';', skipinitialspace=False)
            for row in spamReader:
                if row != []:
                    cont = cont + 1

        with open(direccion) as spambase:
            spamReader = csv.reader(spambase, delimiter=';', skipinitialspace=False)
            for row in spamReader:
                if row != [] and row[0] == str(cont-1):
                    data.append([i, float(row[1]), cont, row[3]])

    b = nsmallest(3, data, key=fitness)
    import operator
    a=list()
    for i in b:
        direccion2 = "/home/treelab/Documents/Resultos/pop_file_%d_0%d.txt" % (index_, i[0])
        # direccion2 = "./Results/%s/pop_file_%d_%d.txt" % (directory, index_, i[0])
        data2 = list()
        with open(direccion2) as spambase:
            spamReader = csv.reader(spambase, delimiter=';', skipinitialspace=False)
            for row in spamReader:
                if row != []:
                    if '-------------------------------------' not in row[0]:
                        if len(row)>2:
                            try:
                                a_test=float(row[4])
                            except:
                                print 'FALSE'
                            if row[1]!='None':
                                if float(row[1]) == i[1]:
                                    if len(row) == 4:
                                        ind1 = gp.PrimitiveTree.from_string(row[2], pset)
                                        ind_args = get_args(ind1.__str__(), args)
                                        data2.append([float(row[1]), len(ind1), i[0], ind_args, row[2]])

                            elif float(row[4]) == i[1]:
                                if len(row) > 5:
                                    ind1 = gp.PrimitiveTree.from_string(row[5], pset)
                                    ind_args = get_args(ind1.__str__(), args)
                                    data2.append([float(row[4]), len(ind1), i[0], ind_args, row[5]])
                                else:
                                    ind1 = gp.PrimitiveTree.from_string(row[2], pset)
                                    ind_args = get_args(ind1.__str__(), args)
                                    data2.append([float(row[1]), len(ind1), row[2], i[0], ind_args, row[3], i[3]])
        # c3 = my_min(data2)
        a.append(data2[-1])
    for item in a:
        out.write("%s\n\n" % (item[2]))
        out1.write("%f;%i;%s;%s;%s;%s;%s\n" % (item[0], item[1],item[2], item[3],[x for x in item[4]], item[5], item[6]))
    #     abc = sorted(data2, key=operator.itemgetter(1, 0))
    #     # aqui obtengo los primeros mejores 10 en cuanto a tamano y fitness
    #     best_b = nsmallest(10, abc, key=len_ind)
    #     # c2 = my_min(data2, key_func=len_ind)
    #     data3.extend(best_b)
    # abc1 = sorted(data3, key=operator.itemgetter(0, 1))
    # abc2 = abc1[50:150]
    # c3 = nsmallest(3, abc2)
    #
    # from tree2func import tree2f
    #
    # strg = c3[0][2]
    # a = c3[0][5].split(',')
    # l_strg = add_subt(strg, a)
    # c = tree2f()
    # cd = c.convert(l_strg)
    # # new_invalid_ind.append(cd)
    #
    # # c3 = my_min(abc2, key_func=fitness)
    # individuals = sorted(c3, key=operator.itemgetter(1, 0))
    # for item in individuals:
    #     out.write("%s\n" % item)
    #     out1.write("%s;%s\n" % (item[2], item[3]))



def get_data(directory, index_, out, out1):
    data = list()
    data3 = list()
    individuals = list()
    args= list()
    if len(pset.arguments) >= 1:
        for arg in pset.arguments:
            args.append(arg)

    for i in range(2, 31):
        cont = 0
        direccion = "/media/treelab/84DF-9E7F/archivos_graficas/GraficasConvergenciaNGPLS_1/datosgraficas_Oct/Results/%s/bestind_LStr_%d_%d.txt"% (directory, index_, i)
        #direccion = "./Results/%s/bestind_LStr_%d_%d.txt" % (directory, index_, i)
        with open(direccion) as spambase:
            spamReader = csv.reader(spambase,  delimiter=';', skipinitialspace=False)
            for row in spamReader:
                if row != []:
                    cont = cont + 1

        with open(direccion) as spambase:
            spamReader = csv.reader(spambase, delimiter=';', skipinitialspace=False)
            for row in spamReader:
                if row != [] and row[0] == str(cont-1):
                    data.append([i, float(row[1]), cont, row[2]])

    b = nsmallest(50, data, key=fitness)
    import operator

    for i in b:
        direccion2 = "/media/treelab/84DF-9E7F/archivos_graficas/GraficasConvergenciaNGPLS_1/datosgraficas_Oct/Results/%s/pop_file_%d_%d.txt"% (directory, index_, i[0])
        #direccion2 = "./Results/%s/pop_file_%d_%d.txt" % (directory, index_, i[0])
        data2 = list()
        with open(direccion2) as spambase:
            spamReader = csv.reader(spambase,  delimiter=';', skipinitialspace=False)
            for row in spamReader:
                if row != []:
                    if int(row[0])==i[2]:
                        if len(row)>5:
                            ind1 = gp.PrimitiveTree.from_string(row[6], pset)
                            ind_args = get_args(ind1.__str__(), args)
                            data2.append([float(row[1]), len(ind1),row[4], i[0],ind_args, row[6]])
                        else:
                            ind1 = gp.PrimitiveTree.from_string(row[3], pset)
                            ind_args = get_args(ind1.__str__(), args)
                            data2.append([float(row[1]),  len(ind1), row[3], i[0], ind_args,row[4]])
       # c3 = my_min(data2)
        abc = sorted(data2, key=operator.itemgetter(1, 0))
        # aqui obtengo los primeros mejores 10 en cuanto a tamano y fitness
        best_b = nsmallest(10, abc, key=len_ind)
        #c2 = my_min(data2, key_func=len_ind)
        data3.extend(best_b)
    abc1 = sorted(data3, key=operator.itemgetter(0, 1))
    abc2=abc1[50:150]
    c3 = nsmallest(3, abc2)

    from tree2func import tree2f

    strg = c3[0][2]
    a=c3[0][5].split(',')
    l_strg = add_subt(strg, a)
    c = tree2f()
    cd = c.convert(l_strg)
    #new_invalid_ind.append(cd)

    #c3 = my_min(abc2, key_func=fitness)
    individuals = sorted(c3, key=operator.itemgetter(1, 0))
    for item in individuals:
        out.write("%s\n" % item)
        out1.write("%s;%s\n" % (item[2], item[3]))



problem = 10130
d = '/home/treelab/Documents/Resultos/Graphs/short_data_%d.txt' % (problem)
ensure_dir(d)
out = open(d, 'a')
d1 = '/home/treelab/Documents/Resultos/Graphs/datashort_%d.txt' % (problem)
ensure_dir(d1)
out1 = open(d1, 'a')
get_data2(problem, out, out1)

# for nombre in ("Concrete", "Housing"):  # ,"EHeating", "ECooling", "Tower", "Yacht"
#     directory = nombre
#     # for i in (10107,10117):
#     problem = 10117  # i
#     d = './Graphs/short_data_%s_%d.txt' % (directory, problem)
#     ensure_dir(d)
#     out = open(d, 'a')
#     d1 = './Graphs/datashort_%s_%d.txt' % (directory, problem)
#     ensure_dir(d)
#     out1 = open(d1, 'a')
#     get_data(directory, problem, out, out1)

# c=data2[1]
# c1=min(data2)


# print min(data)

# num=data.index(min(data))+1
# print a[0]

# direccion2="./Results/%s/bestind_LStr_%d_%d.txt"%(directory,index_,num)
# with open(direccion2) as spambase:
#     spamReader = csv.reader(spambase,  delimiter=';', skipinitialspace=False)
#     for row in spamReader:
#         if row != [] and row[0]==str(cont):
#             #data2.append([num, row[2]])
#             print row[2]
#             out.write('\n%d;%s;%s;%s' % (index_, num, min(data), row[2]))


# print data2
