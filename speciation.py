from deap import base, creator, gp, tools
from random import choice
from numpy import average

from measure_tree import *
#Inicializa las poblacion con una sola especie
def init_species(population):
    for ind in population:
        ind.specie(1)


def count_species(population):
    """
    This method counts the total number of species
    in the population
    :param population: a set of individuals
    :return: The number of species
    """

    specie = list()

    for ind in population:
        if ind.get_specie() is not None and ind.get_specie() not in specie:
            specie.append(ind.get_specie())
    if not specie:
        return 0
    else:
        return len(specie)


def list_species(population):
    """
    This method return a list of the species
    in the population
    :param population: a set of individuals
    :return: A list of species
    """

    specie = list()

    for ind in population:
        if ind.get_specie() is not None and ind.get_specie() not in specie:
            specie.append(ind.get_specie())
    if not specie:
        return 0
    else:
        return specie


def ind_specie(population):
    """
    This method count the individuals of each specie
    :param population: a set of individuals
    :return: A list with the specie and the total number of individuals in it.
    """
    specie2 = list()
    num = list()
    for ind in population:
        specie2.append(ind.get_specie())
    specie = sorted(specie2)
    if specie.count(specie[0]) == len(population):
        num.append([specie[0], specie.count(specie[0])])
    else:
        for i in range(len(specie)):
            if specie[i] != specie[i-1]:
                num.append([specie[i], specie.count(specie[i])])
    for ind in population:
        set_numind(ind, num)
    return num


def specie_gpo(population):
    """
    This method return groups of individuals by specie
    :param population: a set of individuals
    :return: A list with the individuals grouped by specie
    """
    specie2 = list()
    gpos = list()
    orderbyfit = list()
    orderbyfit = sorted(population, key=lambda ind: ind.get_specie())
    for i in range(1, len(orderbyfit)):
        if orderbyfit[i-1].get_specie() == orderbyfit[i].get_specie():
            specie2.append(orderbyfit[i-1])
            if i==len(orderbyfit)-1:
                specie2.append(orderbyfit[i])
                gpos.append([specie2])
        else:
            specie2.append(orderbyfit[i-1])
            gpos.append([specie2])
            specie2 = list()
            if i == len(orderbyfit)-1:
                specie2.append(orderbyfit[i])
                gpos.append([specie2])
    return gpos


def get_specie_ind(individual, population):
    """
    This method return the number of individuals in a given specie
    :param individual: This individual will bring the number of specie to search
    :param population: The list of individuals to compare
    :return: A number of total individuals
    """
    cont = 0
    specie = individual.get_specie()
    for ind in population:
        if ind.get_specie() == specie:
            cont += 1
    return cont


def get_ind_specie(n_specie, population):
    """
    This method return a group of individuals from a given specie
    :param n_specie: The number of the specie
    :param population: The list of individuals to compare
    :return: A list of total individuals
    """
    specie = n_specie
    list_ind = []
    for ind in population:
        if ind.get_specie() == specie:
            list_ind.append(ind)
    return list_ind


def set_numind(ind, species):
    """
    This method assign to an individual the number of individuals in the specie of his kind. 
    :param ind: This individual will bring the number of specie to search
    :param species:
    """
    for i in range(len(species)):
        if species[i][0] == ind.get_specie() and ind.num_specie is not None:
            ind.num_specie(species[i][1])

def intracluster(gpo_specie):
    """
    Upgrade: May 11th
    This method calculates the intracluster distance in a specie. 
    :param gpo_specie: The specie to calculate the intracluster
    """
    list_distance = []
    for ind in gpo_specie:
        list_d = []
        for e_ind in range(0, len(gpo_specie)):
            if len(ind) == 1 and len(gpo_specie[e_ind]) == 1:
                d = 0
            else:
                d = distance(ind, gpo_specie[e_ind], version = 3, beta = 0.5)
            list_d.append(d)
        try:
            list_distance.append(min(list_d))
        except ValueError:
            print list_distance
    avg_distance = average(list_distance)
    for ind in gpo_specie:
        ind.set_intracluster(avg_distance)
    return avg_distance

def calc_intracluster(population):
    """
    Upgrade: May 11th
    This method calculates the intracluster distance in each specie. 
    :param population: all the individuals
    """
    list_s = list_species(population)
    for specie in list_s:
        list_ind = get_ind_specie(specie, population)
        if len(list_ind) >= 2:
            intracluster(list_ind)


def species_random(population, h, version, beta):
    """
    Upgrade: May 10th
    This is the speciation method.
    This method compare each individual without specie with the rest of the
    individual, selecting one random individual of the specie and calculating the distance to compare.

    :param population: set of individuals without specie
    :param h: distance measure
    :param version: the way of comparasion between the individuals
        1: Binary comparasion
        2: Modify method
        3: Original method
    :param beta: measure to give a weight in the comparasion between number of nodes and
                depth.
    :return: a population with specie
    """
    num_specie = count_species(population)
    if num_specie >= 1:
        for ind in population:
            if ind.get_specie() is None:
                if len(ind) == 1:
                    ind.specie(1)
                else:
                    list_s = list_species(population)
                    for specie in list_s:
                        list_ind = get_ind_specie(specie, population)
                        r_ind = choice(list_ind)
                        if distance(ind, r_ind, version, beta) <= h:
                            ind.specie(r_ind.get_specie())
                            break
                    if ind.get_specie() is None:
                        ind.specie(num_specie+1)
                        num_specie += 1
    else:
        population[0].specie(1)
        species_random(population, h, version, beta)
    return population


def species(population, h, version, beta):
    """
    This is the speciation method.
    This method compare each individual with the rest
    of the population to assign it a specie.

    :param population: set of individuals without specie
    :param h: distance measure
    :param version: the way of comparasion between the individuals
        1: Binary comparasion
        2: Modify method
        3: Original method
    :return: a population with specie
    """
    num_specie = count_species(population)

    for ind in population:
        if ind.get_specie() is None:
            if len(ind) == 1:
                ind.specie(1)
            else:
                for ind1 in population:
                    if ind1.get_specie() is not None:

                        # if distance(ind, ind1, 1) != distance(ind, ind1, 3):
                        #     print 'ind:', ind
                        #     print 'ind2:', ind1
                        #     print 'D1:', distance(ind, ind1, 1)
                        #     print ind.binary_rep_get()
                        #     print ind1.binary_rep_get()
                        #     print 'D2:', distance(ind, ind1, 3)

                        if distance(ind, ind1, version, beta) <= h:
                            ind.specie(ind1.get_specie())
                            break

                if ind.get_specie() is None:
                    ind.specie(num_specie+1)
                    num_specie += 1
    return population


def specie_ind(population,ind, h):
    """
    This method assign a specie to an specific individual
    :param population: set of individuals
    :param ind: the individual to assign the specie
    :param h: the distance measure
    :return: The individual with a specie
    """
    if (len(ind)==1):
        ind.specie(1)
    else:
        for ind_p in population:
            if ind_p.get_specie()!=None:
                if distance(ind, ind_p, version=3)<=h:
                    ind.specie(ind_p.get_specie())
                    break
        if ind.get_specie()==None:
            num_specie=count_species(population)
            ind.specie(num_specie+1)
    return ind


def specie_parents_child(parents, offspring, h, version, beta):
    """
    This method assign the specie to each children.
    The assignation of the specie depends of the specie of the parent.
    :param parents: set of parents
    :param offspring: set of descendents without specie
    :param h: distace to compare, deafult .15
    :return: A set of descendent with specie.
    """
    n_esp = count_species(parents)
    for ind in offspring:
        if ind.get_specie() is None:
            if len(ind) == 1:
                ind.specie(1)
            else:
                for parent in parents:
                    if parent.get_specie() is not None:
                        if distance(ind, parent, version, beta) <= h:
                            ind.specie(parent.get_specie())
                            break
                if ind.get_specie() is None:
                    ind.specie(n_esp+1)
                    n_esp += 1
    return offspring


def specie_offspring_random(parents, offspring, h, version, beta):
    """
    Modified May 10th
    This method assign the specie to each children.
    The assignation of the specie depends of the specie of the parent.
    :param parents: set of parents
    :param offspring: set of descendents without specie
    :param h: distace to compare, deafult .15
    :return: A set of descendent with specie.
    """
    n_esp = count_species(parents)
    if n_esp >= 1:
        for ind in offspring:
            if ind.get_specie() is None:
                if len(ind) == 1:
                    ind.specie(1)
                else:
                    list_s = list_species(parents)
                    for specie in list_s:
                        list_ind = get_ind_specie(specie, parents)
                        r_ind = choice(list_ind)
                        if distance(ind, r_ind, version, beta) <= h:
                            ind.specie(r_ind.get_specie())
                            break
                    if ind.get_specie() is None:
                        ind.specie(n_esp+1)
                        n_esp += 1
    else:
        print ("Error en las especies de los padres/descencientes")
    return offspring


