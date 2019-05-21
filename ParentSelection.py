from deap import gp
import numpy as np
from speciation import *


def p_selection(population, survival_p):
        survival = survival_p  # 0.5
        prom_ap_penal = avg(population)

        #Penalize the average, if the average is too big.
        if prom_ap_penal>10:
            prom_ap_penal=10

        for ind in population:
            ndesc = num_desc(ind, prom_ap_penal)
            if ndesc>(len(population)*0.10):
                ind.descendents(len(population)*0.10)
            else:
                ind.descendents(ndesc)

        q=population

        #obtener numero de especies
        specie=ind_specie(q)

        #crear grupos auxilares
        gpo_specie=list()
        parents=list()
        gparents=list()
        gsparents=list()
        contador=0
        for e in specie:
            for ind in q:
                if ind.get_specie()==e[0]:
                    contador+=1
                    gpo_specie.append(ind)
                if contador==e[1]:
                    parents.append(penalizar_ind(gpo_specie,survival))
                    gpo_specie=list()
                    contador=0
        for especie in parents:
            for ind in especie:
                gparents.append([ind,ind.fitness.values, ind.get_fsharing(), ind.get_descendents(), ind.get_specie()])
        gsparents=sorted(gparents, key=lambda ind:(ind[1], ind[2]))

        gparents=list()
        indice=int(round(len(gsparents)-(len(gsparents)*survival)))
        for ind in range(indice):
            gparents.append(gsparents[ind][0])
        return gparents

def num_desc(ind, avg):
    """
    Method to calculate the number of descendants of each individual
    :param ind:
    :param avg:
    :return: a number that indicate the amount of descendants
    """
    int1=ind.get_fsharing()
    if int1==0.0:
        int1=1
    numd=round(avg/int1)
    if np.isnan(numd):
        print avg
        print int1
    return int(numd)


def avg(population):
    """
    Method tha calculates the average of the fitness on the population
    :param population:
    :return: a value that indicates the average fitness population
    """
    suma=0
    for ind in population:
        if np.isnan(ind.get_fsharing()):
            fshre=999999999.99
        else:
            fshre=ind.get_fsharing()
        suma+=fshre
    promedio=suma/len(population)
    return promedio

def sort_fitness(population): #ordena la poblacion y regresa una lista con el ind y sus dos aptitudes
    allpotfit=list()
    orderbyfit=list()
    for ind in population:
        allpotfit.append([ind, ind.fitness.values, ind.get_fsharing()])
    orderbyfit=sorted(allpotfit, key=lambda ind: ind[1], reverse=True)
    return orderbyfit

def sort_fitnessvalues(population): #ordena la poblacion y regresa la poblacion ordenada
    orderbyfit=list()
    orderbyfit=sorted(population, key=lambda ind:ind.fitness.values)
    return orderbyfit

def eliminar_ind(gpo_specie, survival):
    sort_gpo=sort_fitness(gpo_specie)
    indice=int(round(len(sort_gpo)-(len(sort_gpo)*survival)))
    reverse_gpo=sorted(sort_gpo, key=lambda ind:ind[2],reverse=True)
    for i in range(indice):
       del reverse_gpo[0]
    sort_gpo=sorted(reverse_gpo, key=lambda ind:ind[2])
    parnt=list()
    for i in range(len(sort_gpo)):
        parnt.append(sort_gpo[i][0])
    return parnt

def penalizar_ind(gpo_specie, survival):
    sort_gpo=sort_fitness(gpo_specie)
    indice=int(round(len(sort_gpo)-(len(sort_gpo)*survival)))
    #reverse_gpo=sorted(sort_gpo, key=lambda ind:ind[1],reverse=True)
    reverse_gpo=sort_gpo
    if len(reverse_gpo)>1:
        for i in range(indice):
            reverse_gpo[i][0].fitness.values=999999999.00,
            reverse_gpo[i][1]=999999999.00
            reverse_gpo[i][2]=999999999.00
    sort_gpo=sorted(reverse_gpo, key=lambda ind:ind[1])
    parnt=list()
    for i in range(len(sort_gpo)):
        parnt.append(sort_gpo[i][0])
    return parnt
