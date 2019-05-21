import random
from ParentSelection import sort_fitnessvalues
from speciation import get_specie_ind, ind_specie
from crosspoints import *


def neatGP(toolbox, parents, cxpb, mutpb, n, mut, cx, pelit, neat_cx):
    r = list()
    i = 0
    copy_parent = copy.deepcopy(parents)

    while i < n:
        if n > len(copy_parent):  # if the parent pool is less than the number of child
            copy_parent[:] = copy.deepcopy(parents)
        eflag = random.random()
        if eflag < pelit:
            ind1 = copy_parent[0]  # best ind in the population by fitness
        else:
            ind1 = random.choice(copy_parent)  # random elitism
        if mut == 1 and random.random() < mutpb:  # mutation
            of=copy.deepcopy(ind1)
            offspring=toolbox.mutate(of)
            offspring[0].set_id()
            offspring[0].set_parent([ind1.get_id()])
            offspring[0].descendents(0)
            offspring[0].bestspecie_set(0)
            offspring[0].LS_applied_set(0)
            offspring[0].LS_fitness_set(None)
            offspring[0].fitness_sharing(0)
            offspring[0].specie(None)
            del offspring[0].fitness.values

            if i < n:
                r.append(offspring[0])
                i += 1
            else:
                break

            ind1.descendents(ind1.get_descendents()-1)
        elif cx == 1 and random.random() < (cxpb+mutpb):
            ind_nspecie = get_specie_ind(ind1,copy_parent)
            if ind_nspecie > 1 and eflag<pelit:
                ind2=[]
                for q in range(len(copy_parent)):
                    if copy_parent[q].get_specie() == ind1.get_specie() and copy_parent[q] != ind1:
                        ind2 = copy_parent[q]
                        break
                if ind2 == []:
                    try:  # elitist
                        if eflag:
                            ind2 = elitism_choice(ind1, copy_parent)
                        else:
                            ind2 = random.choice(copy_parent)
                    except:  # random
                        ind2 = random.choice(copy_parent)
            else:
                ind2 = random.choice(copy_parent)

            of1 = copy.deepcopy(ind1)
            of2 = copy.deepcopy(ind2)
            if neat_cx:
                hijo = neatcx(of1, of2, toolbox)
            else:
                hijo, offspring2 = toolbox.mate(of1, of2)
            hijo.set_id()
            hijo.set_parent([ind1.get_id(), ind2.get_id()])
            hijo.descendents(0)
            hijo.fitness_sharing(0)
            hijo.bestspecie_set(None)
            hijo.LS_fitness_set(None)
            hijo.LS_applied_set(0)
            hijo.specie(None)
            del hijo.fitness.values

            if i < n:
                r.append(hijo)
                i += 1
            else:
                break

            ind1.descendents(ind1.get_descendents() - 0.5)
            ind2.descendents(ind2.get_descendents() - 0.5)

            if ind2.get_descendents() <= 0:
                for xi in range(len(copy_parent)):
                    if copy_parent[xi] == ind2:
                        del copy_parent[xi]
                        break
        else:
            offspring1 = copy.deepcopy(ind1)
            offspring1.descendents(0)
            offspring1.fitness_sharing(0)
            offspring1.bestspecie_set(None)
            offspring1.LS_fitness_set(None)
            offspring1.LS_applied_set(0)
            offspring1.specie(None)
            del offspring1.fitness.values
            r.append(offspring1)
            i += 1
            ind1.descendents(ind1.get_descendents() - 1)
        if ind1.get_descendents() <= 0:
            for xi in range(len(copy_parent)):
                if copy_parent[xi] == ind1:
                    del copy_parent[xi]
                    break
    return r


def elitism_choice(ind, parents):
    sort_par=sort_fitnessvalues(parents)
    for i in range(len(sort_par)):
        if sort_par[i]!=ind:
            ind2=sort_par[i]
            break
    return ind2