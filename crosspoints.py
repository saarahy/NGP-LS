import random
import copy
import funcEval
import numpy as np
from measure_tree import *


def neatcx(ind1, ind2, toolbox):
    hijo = copy.deepcopy(ind1)
    flag = 0
    n=0
    while n<10:
        e1,e2=ext_node(hijo,ind2)
        l1,l2=int_node(hijo,ind2)
        for i in range(len(l1)): #cambio de nodo interno
            if random.random()<0.5:
                if funcEval.LS_flag:
                    params_2=ind2.get_params()
                    params_1=hijo.get_params()
                    params_1[i]=params_2[i]
                    hijo.params_set(params_1)
                hijo[l1[i][0]]=l2[i][1]
                flag=1
        for i in e1: #camio de nodos externos
            if random.random()<0.5 or flag==0:
                e=random.choice(e2)
                if len(ind1)==1:
                    slice1=hijo.searchSubtree(0)
                else:
                    slice1=hijo.searchSubtree(i)
                if len(ind2)==1:
                    slice2=ind2.searchSubtree(0)
                else:
                    slice2=ind2.searchSubtree(e)
                if funcEval.LS_flag:
                    a=slice1.start
                    b=slice1.stop
                    c=slice2.start
                    d=slice2.stop
                    params1=hijo.get_params()
                    params2=ind2.get_params()
                    params1=params1.tolist()
                    params2=params2.tolist()
                    temp_p=params1[a+2:b+2]
                    params1[a+2:b+2]=params2[c+2:d+2]
                    params2[c+2:d+2]=temp_p
                    params1=np.asarray(params1)
                    params2=np.asarray(params2)
                    hijo.params_set(params1)
                    ind2.params_set(params2)
                hijo[slice1], ind2[slice2]=ind2[slice2], hijo[slice1]
                break
        if hijo==ind1 or hijo==ind2:
            n+=1
        else:
            break
    if hijo==ind1 or hijo==ind2:
        n=0
        while n<10:
            off=toolbox.mutate(hijo)
            if hijo==ind1 or hijo==ind2:
                n+=1
            else:
                break
    return hijo

def int_node(ind1, ind2):
    cont1=0
    cont2=0
    label1=list()
    label2=list()
    maxim=max(len(ind1), len(ind2))
    maxim=maxim-1
    while (cont1<maxim) and (cont2<maxim):
        if ind1[cont1].arity==ind2[cont2].arity and ind1[cont1].arity>0:
            if cont1==0:
                label1.append([cont1,ind1[cont1]])
                label2.append([cont2,ind2[cont2]])
            else:
                label1.append([cont1,ind1[cont1]])
                label2.append([cont2,ind2[cont2]])
            cont1+=1
            cont2+=1
        elif ind1[cont1].arity==ind2[cont2].arity and ind1[cont1].arity==0:
            cont1 += 1
            cont2 += 1
        else:
            if (ind1[cont1].arity > 0) and (ind2[cont2].arity > 0):
                copia1=copy.deepcopy(ind1)
                slice1=copia1.searchSubtree(cont1)
                copia1[1:]=copia1[slice1]
                long1=len(copia1)-1
                copia2=copy.deepcopy(ind2)
                slice2=copia2.searchSubtree(cont2)
                copia2[1:]=copia2[slice2]
                long2=len(copia2)-1
                cont1+=long1
                cont2+=long2
            else:
                if ind1[cont1].arity > 0:
                    copia = copy.deepcopy(ind1)
                    slice1 = copia.searchSubtree(cont1)
                    copia[1:] = copia[slice1]
                    long = len(copia)-1
                    cont1 += long
                    cont2 += 1
                elif ind2[cont2].arity > 0:
                    copia = copy.deepcopy(ind2)
                    slice1 = copia.searchSubtree(cont2)
                    copia[1:] = copia[slice1]
                    long = len(copia)-1
                    cont2 += long
                    cont1 += 1
    return label1,label2


def ext_node(ind1, ind2):
    cont1=0
    cont2=0
    edg1=list()
    edg2=list()
    maxim=max(len(ind1), len(ind2))
    while (cont1<maxim) and (cont2<maxim):
        if ind1[cont1].arity==ind2[cont2].arity and ind1[cont1].arity>0:
            cont1+=1
            cont2+=1
        elif ind1[cont1].arity==ind2[cont2].arity and ind1[cont1].arity==0:
            edg1.append(cont1)
            edg2.append(cont2)
            cont1+=1
            cont2+=1
        else:
            if cont1==0:
                edg1.append(cont1+1)
                edg2.append(cont2+1)
                cont1+=max(len(ind1), len(ind2))
            else:
                if ind1[cont1].arity>0 and ind2[cont2].arity>0:
                    edg1.append(cont1)
                    edg2.append(cont2)
                    copia1=copy.deepcopy(ind1)
                    slice1=copia1.searchSubtree(cont1)
                    copia1[1:]=copia1[slice1]
                    long1=len(copia1)-1
                    copia2=copy.deepcopy(ind2)
                    slice2=copia2.searchSubtree(cont2)
                    copia2[1:]=copia2[slice2]
                    long2=len(copia2)-1
                    cont1+=long1
                    cont2+=long2
                else:
                    edg1.append(cont1)
                    edg2.append(cont2)
                    if ind1[cont1].arity>0:
                        copia=copy.deepcopy(ind1)
                        slice1=copia.searchSubtree(cont1)
                        copia[1:]=copia[slice1]
                        long=len(copia)-1
                        cont1+=long
                        cont2+=1
                    elif ind2[cont2].arity>0:
                        copia=copy.deepcopy(ind2)
                        slice1=copia.searchSubtree(cont2)
                        copia[1:]=copia[slice1]
                        long=len(copia)-1
                        cont2+=long
                        cont1+=1
    return edg1,edg2


def crosspoints(tree1, tree2, version):
    nodo=0
    lista_nivel=list()

    if version == 2:
        expr1 = tree1.nodefeat_get()
        expr2 = tree2.nodefeat_get()
    elif version == 3:
        expr1=level_node(tree1)
        expr2=level_node(tree2)

    for ind1 in expr1:
        for ind2 in expr2:
            if ind1==ind2 and ind1[0]==0:
                nodo+=1
                lista_nivel.append(ind1[1])
                break
            elif tot_grpo(expr1, ind1[1])==2 and tot_grpo(expr2, ind1[1])==2 and ind1[1] not in lista_nivel:
                nodo+=2
                lista_nivel.append(ind1[1])
                break
            elif tot_grpo(expr1, ind1[1])<tot_grpo(expr2, ind1[1]) and ind1[1] not in lista_nivel:
                total=tot_grpo(expr1,ind1[1])
                nodo+=total
                if total>0:
                    lista_nivel.append(ind1[1])
                break
            elif tot_grpo(expr1, ind1[1])>tot_grpo(expr2, ind1[1]) and ind1[1] not in lista_nivel:
                total=tot_grpo(expr2,ind1[1])
                nodo+=total
                if total>0:
                    lista_nivel.append(ind1[1])
                break
            elif tot_grpo(expr1, ind1[1])==tot_grpo(expr2, ind1[1]) and ind1[1] not in lista_nivel:
                total=tot_grpo(expr2,ind1[1])
                nodo+=total
                if total>0:
                    lista_nivel.append(ind1[1])
                break
            elif ind1[1] in lista_nivel:
                break
    return nodo, max(lista_nivel)


def grupo(exp,nivel):
    grupo=list()
    for i in exp:
        if i[1]==nivel:
            grupo.append(i)
    return grupo

def tot_grpo(exp,nivel):
    total=0
    for i in exp:
        if i[1]==nivel:
            total+=1
    return total


