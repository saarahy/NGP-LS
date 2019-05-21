from __future__ import division
from deap import base, creator, gp, tools
import numpy as np

#def distance(Ti, Tj):
    # b=0.5
    # Nij=len(ind1)+len(ind2) #34
    # Dij=(ind1.height+1)+(ind2.height+1) #6
    # common_tree=compare_tree(ind1,ind2) #3,2
    # nsij=common_tree[0] #3
    # dsij=common_tree[1] #2
    # d1=b*((Nij-(2*nsij))/(Nij-2))
    # d2=(1-b)*((Dij-(2*dsij))/(Dij-2))
    # d=d1+d2
    # return d


def bin_c(n1, n2):   # XNOR operator
    return (n1 and n2) or (not n1 and not n2)


def bin_and(n1, n2):
    return n1 and n2


def bin_contradiction(n1, n2):
    return n1&(not n1)


def split_list(alist, wanted_parts):
    length = len(alist)
    wanted_parts=int(wanted_parts)
    l1=[alist[i*length // wanted_parts: (i+1)*length // wanted_parts] for i in range(wanted_parts)]
    return l1


def test(li1, li2):
    if all(map(bin_c, li1, li2)):
        return map(bin_and, li1, li2)
    else:
        return map(bin_contradiction, li1, li2)

def recorrido(ind1, ind2):
    cromx = split_list(ind1[1:], wanted_parts=(len(ind1)-1)/2)
    cromy = split_list(ind2[1:], wanted_parts=(len(ind2)-1)/2)
    list1=[ind1[0]]

    for x, y in zip(cromx, cromy):
        list1.extend(test(x, y))
    return list1


def distance(ind1, ind2, version, beta):
    """
    This method determine the distance between two individuals
    Equation (2) of Leonardo Trujillo et al. neat Genetic Programming. Inf. Sci. 333, C (March 2016), 21-43.

    :param ind1: First Individual
    :param ind2: Second Individual
    :param version: This indicate the form of comparision between two individuals.
    :return: A number indicating the distance
    """

    b = beta
    Nij = len(ind1)+len(ind2)
    Dij = (ind1.height+1)+(ind2.height+1)

    if version == 1:
        ind1_b = ind1.binary_rep_get()#ind1.p_bin
        ind2_b = ind2.binary_rep_get()
        r = len(min(ind1_b, ind2_b))
        nivel = (np.log(r + 1.)) / (np.log(2.))
        nsij = sum(recorrido(ind1_b,ind2_b))
        dsij = nivel

    else: # if version is not binary comparision
        common_tree = compare_tree(ind1, ind2, version)
        nsij = common_tree[0]
        dsij = common_tree[1]

    d1 = b*((Nij-(2*nsij))/(Nij-2))
    d2 = (1-b)*((Dij-(2*dsij))/(Dij-2))

    d = d1+d2
    return d


def compare_tree(tree1, tree2, version):
    """
    This method compare the number of nodes and the depth between two
    individuals.
    Binary version does not enter here

    :param tree1: First Individual
    :param tree2: Second Individual
    :param version: Original version or modify version.
    :return: a tuple with the number of nodes and the common depth
    """
    nodo = 0
    lista_nivel = list()
    list_tree1 = list()
    list_tree2 = list()
    list_parent_t1 = list()
    list_parent_t2 = list()
    first_node = False
    lista_aristas = list()

    if version == 2:
        expr1 = tree1.nodefeat_get()
        expr2 = tree2.nodefeat_get()
    elif version == 3:
        expr1 = level_node(tree1)
        expr2 = level_node(tree2)

    for index in range(0, min(len(expr1), len(expr2))):
        if expr1[index][1] not in lista_nivel:
            if expr1[index][1] - 1 in lista_nivel:
                nivel_ant = expr1[index][1]-1
                list_tree1 = []
                list_tree2 = []
                [list_tree2.append(x) for x in expr2 if (x[1] == nivel_ant + 1)]
                [list_tree1.append(x) for x in expr1 if (x[1] == nivel_ant + 1)]
                x3 = []
                if list_tree1 != [] and list_tree2 != []:
                    x1 = list(zip(*list_tree1)[2])
                    x2 = list(zip(*list_tree2)[2])
                    n_ = min(len(x1),len(x2))
                    for i in range(n_):
                        for ix in range(expr1.index(list_tree1[i])-1, -1, -1):
                                if expr1[ix][1] == list_tree1[i][1]-1:
                                    padre1 = expr1[ix][0]
                                    break
                        for ix in range(expr2.index(list_tree2[i])-1, -1, -1):
                                if expr2[ix][1] == list_tree2[i][1]-1:
                                    padre2 = expr2[ix][0]
                                    break
                        if x1[i] == x2[i] and padre1 in list_parent_t1 and padre2 in list_parent_t2:
                            x3.append(x1[i])
                            lista_aristas.append(list_tree1[i][2])
                            lista_nivel.append(list_tree1[i][1])
                            list_parent_t1.append(list_tree1[i][0])
                            list_parent_t2.append(list_tree2[i][0])
                        elif padre1 in list_parent_t1 or padre2 in list_parent_t2:
                            lista_nivel.append(list_tree1[i][1])
            elif expr1[0] == expr2[0] and expr1[0][0] == 0 and not first_node:
                nodo += 1
                lista_aristas.append(expr1[0][2])
                first_node = True
                lista_nivel.append(expr1[0][1])
                list_parent_t1.append(expr1[0][0])
                list_parent_t2.append(expr1[0][0])
                list_tree1.append(expr1[0])
                list_tree2.append(expr1[0])
        if not first_node:
            return 1, 1
    nodo += sum(lista_aristas)
    return nodo, max(lista_nivel)


def level_node(expr):
    """
    This method review each node in the individual
    and it indicate the level, arity and number of node.
    :param expr: Individual to take the information
    :return: a list [node_num, level, arity]
    """
    nodes, edges, labels = gp.graph(expr)
    edge = sorted(edges)
    contador = 1
    nod = 0
    level=list()

    if len(expr) < 2:
        level.append([0, contador, 0])
    else:
        level.append([edge[0][0], contador, expr[0].arity])  # This is for the root.
        for i in range(max(nodes)):
            restart = True
            contador = 1
            nod = i+1
            while restart:
                restart=False
                for j in range(max(nodes)):
                    if edge[j][1]==nod:
                        contador += 1
                        nod = edge[j][0]
                    if(nod > 0) and (contador > 1):
                        restart = True
            level.append([i+1, contador, expr[i+1].arity])
    return level


def level_data(expr):
    """
        This method review each node in the individual
        and it indicate the level, arity, the number of node
        and the number of node of the father

        :param expr: Individual to take the information
        :return: a list [node_num, level, arity, father]
        """
    nodes, edges, labels = gp.graph(expr)
    edge = sorted(edges)
    contador = 1
    nod = 0
    level=list()
    if len(expr)<2:
        level.append([0, contador, 0, None])
    else:
        level.append([edge[0][0], contador, expr[0].arity, None])  # This is for the root.
        for i in range(max(nodes)):
            restart=True
            contador=1
            nod=i+1
            while restart:
                restart=False
                for j in range(max(nodes)):
                    if edge[j][1]==nod:
                        contador+=1
                        nod=edge[j][0]
                    if(nod>0 and contador>1):
                        restart=True
            for elem in edge:
                if elem[1]==(i+1):
                    nod_p=elem[0]
            level.append([i+1, contador, expr[i+1].arity, nod_p])
    return level


def tot_grpo(exp, nivel):
    total = 0
    for i in exp:
        if i[1] == nivel:
            total += 1
    return total

def tot_grpo_exp(exp, nivel,list_t):
    for i in exp:
        if i[1] == nivel:
            list_t.append(i)
    return list_t

def p_bin(ind1):
    size = (np.power(2, ind1.height + 1) - 1)
    if len(ind1) == size:
        bin = np.ones(size, int)
        bin = bin.tolist()
        return bin
    else:
        rep = []
        lista_pre = level_data(ind1)
        lista_pre.sort(key=lambda x: x[1])
        order = 2
        rep.append(1)
        num = len(ind1) - 1
        for i in range(1, ind1.height + 1):
            total = 0
            num_nodos = np.power(2, i - 1)
            for k in lista_pre:
                cont = 0
                if k[1] == i:
                    total += 1
                    num_nodo = k[0]
                    for j in lista_pre:
                        if j[3] == num_nodo:
                            cont += 1
                    dif = order - cont
                    for j in range(cont):
                        rep.append(1)
                    if dif > 0:
                        for k in range(dif):
                            num += 1
                            rep.append(0)
                            lista_pre.append([num, i + 1, None, num_nodo])
            if total < num_nodos:
                dif = num_nodos - total
                for j in range(dif):
                    rep.append(0)
                    rep.append(0)
    return rep


# def p_bin(self):
#     size=(np.power(2,self.height+1)-1)
#     if len(self) == size:
#         bin = np.ones(size, int)
#         bin = bin.tolist()
#         return bin
#     else:
#         rep = []
#         lista_pre = level_data(self)
#         lista_pre.sort(key=lambda x: x[1])
#         order = 2
#         rep.append(1)
#         num = len(self) - 1
#         for i in range(1, self.height + 1):
#             total = 0
#             num_nodos = np.power(2, i - 1)
#             for k in lista_pre:
#                 cont = 0
#                 if k[1] == i:
#                     total += 1
#                     num_nodo = k[0]
#                     for j in lista_pre:
#                         if j[3] == num_nodo:
#                             cont += 1
#                     dif = order - cont
#                     for j in range(cont):
#                         rep.append(1)
#                     if dif > 0:
#                         for k in range(dif):
#                             num += 1
#                             rep.append(0)
#                             lista_pre.append([num, i + 1, None, num_nodo])
#             if total < num_nodos:
#                 dif = num_nodos - total
#                 for j in range(dif):
#                     rep.append(0)
#                     rep.append(0)
#     return rep