import random
import funcEval
import numpy as np
import copy
import os
import time
from deap import tools
from neat_operators import neatGP
from speciation import ind_specie, species, specie_parents_child, count_species
from fitness_sharing import SpeciesPunishment
from ParentSelection import p_selection
from tree_subt import add_subt, add_subt_cf
from tree2func import tree2f
from treesize_h import trees_h, specie_h, best_specie, best_pop_ls, all_pop, trees_h_wo, ls_bestset, ls_random, ls_randbestset
from my_operators import avg_nodes
from measure_tree import level_node, p_bin


def varOr(population, toolbox, cxpb, mutpb):
    assert (cxpb + mutpb) <= 1.0, ("The sum of the crossover and mutation "
        "probabilities must be smaller or equal to 1.0.")

    new_pop = [toolbox.clone(ind) for ind in population]
    offspring = []
    for i in range(1, len(new_pop), 2):
        new_pop[i-1].off_cx_set(0), new_pop[i].off_cx_set(0)
        if random.random() < cxpb and len(ind)>1:
            new_pop[i-1].off_cx_set(1)
            new_pop[i].off_cx_set(1)
            offspring1, offspring2 = toolbox.mate(new_pop[i-1], new_pop[i])
            del offspring1.fitness.values
            del offspring2.fitness.values
            offspring1.bestspecie_set(0), offspring2.bestspecie_set(0)
            offspring1.LS_applied_set(0), offspring2.LS_applied_set(0)
            offspring1.LS_fitness_set(None), offspring2.LS_fitness_set(None)
            offspring1.off_cx_set(1), offspring2.off_cx_set(1)
            offspring1.specie(None), offspring2.specie(None)
            # sizep = len(offspring1)+2
            # param_ones = np.ones(sizep)
            # param_ones[0] = 0
            # offspring1.params_set(param_ones)
            # sizep = len(offspring2)+2
            # param_ones = np.ones(sizep)
            # param_ones[0] = 0
            # offspring2.params_set(param_ones)
            offspring.append(offspring1)
            offspring.append(offspring2)
    for i in range(len(new_pop)):
        if new_pop[i].off_cx_get() != 1:
            if random.random() < (cxpb+mutpb):  # Apply mutation
                offspring1, = toolbox.mutate(new_pop[i])
                del offspring1.fitness.values
                offspring1.bestspecie_set(0)
                offspring1.LS_applied_set(0)
                offspring1.LS_fitness_set(None)
                offspring1.off_mut_set(1)
                #offspring1.specie(None)
                # sizep = len(offspring1)+2
                # param_ones = np.ones(sizep)
                # param_ones[0] = 0
                # offspring1.params_set(param_ones)
                offspring.append(offspring1)

    if len(offspring) < len(population):
        for i in range(len(new_pop)):
            if new_pop[i].off_mut_get() != 1 and new_pop[i].off_cx_get() != 1:
                offspring1 = copy.deepcopy(new_pop[i])
                offspring.append(offspring1)

    return offspring


def varAnd(population, toolbox, cxpb, mutpb):
    """Part of an evolutionary algorithm applying only the variation part
    (crossover **and** mutation). The modified individuals have their
    fitness invalidated. The individuals are cloned so returned population is
    independent of the input population.

    :param population: A list of individuals to vary.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution
                    operators.
    :param cxpb: The probability of mating two individuals.
    :param mutpb: The probability of mutating an individual.
    :returns: A list of varied individuals that are independent of their
              parents.

    The variation goes as follow. First, the parental population
    :math:`P_\mathrm{p}` is duplicated using the :meth:`toolbox.clone` method
    and the result is put into the offspring population :math:`P_\mathrm{o}`.
    A first loop over :math:`P_\mathrm{o}` is executed to mate pairs of consecutive
    individuals. According to the crossover probability *cxpb*, the
    individuals :math:`\mathbf{x}_i` and :math:`\mathbf{x}_{i+1}` are mated
    using the :meth:`toolbox.mate` method. The resulting children
    :math:`\mathbf{y}_i` and :math:`\mathbf{y}_{i+1}` replace their respective
    parents in :math:`P_\mathrm{o}`. A second loop over the resulting
    :math:`P_\mathrm{o}` is executed to mutate every individual with a
    probability *mutpb*. When an individual is mutated it replaces its not
    mutated version in :math:`P_\mathrm{o}`. The resulting
    :math:`P_\mathrm{o}` is returned.

    This variation is named *And* beceause of its propention to apply both
    crossover and mutation on the individuals. Note that both operators are
    not applied systematicaly, the resulting individuals can be generated from
    crossover only, mutation only, crossover and mutation, and reproduction
    according to the given probabilities. Both probabilities should be in
    :math:`[0, 1]`.
    """
    offspring = [toolbox.clone(ind) for ind in population]

    # Apply crossover and mutation on the offspring
    for i in range(1, len(offspring), 2):
        if random.random() < cxpb:
            offspring[i-1], offspring[i] = toolbox.mate(offspring[i-1], offspring[i])
            del offspring[i-1].fitness.values, offspring[i].fitness.values
            offspring[i-1].bestspecie_set(0), offspring[i].bestspecie_set(0)
            offspring[i-1].LS_applied_set(0), offspring[i].LS_applied_set(0)
            offspring[i-1].LS_fitness_set(None), offspring[i].LS_fitness_set(None)
            offspring[i-1].off_cx_set(1), offspring[i].off_cx_set(1)

    for i in range(len(offspring)):
        if random.random() < mutpb:
            offspring[i], = toolbox.mutate(offspring[i])
            del offspring[i].fitness.values
            offspring[i].bestspecie_set(0)
            offspring[i].LS_applied_set(0)
            offspring[i].LS_fitness_set(None)
            offspring[i].off_mut_set(1)

    return offspring

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def neat_GP_LS(population, toolbox, cxpb, mutpb, ngen, neat_alg, neat_cx, neat_h,neat_pelit, LS_flag, LS_select, cont_evalf,
               num_salto, SaveMatrix, GenMatrix, pset,n_corr, num_p, params, direccion, problem, testing, version, benchmark_flag, beta,
               stats=None, halloffame=None, verbose=__debug__):
    """This algorithm reproduce the simplest evolutionary algorithm as
    presented in chapter 7 of [Back2000]_.

    :param population: A list of individuals.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution
                    operators.
    :param cxpb: The probability of mating two individuals.
    :param mutpb: The probability of mutating an individual.
    :param ngen: The number of generation.
    :param neat_alg: wheter or not to use species stuff.
    :param neat_cx: wheter or not to use neatGP cx
    :param neat_h: indicate the distance allowed between each specie
    :param neat_pelit: probability of being elitist, it's used in the neat cx and mutation
    :param LS_flag: wheter or not to use LocalSearchGP
    :param LS_select: indicate the kind of selection to use the LSGP on the population.
    :param cont_evalf: contador maximo del numero de evaluaciones
    :param n_corr: run number just to wirte the txt file
    :param p: problem number just to wirte the txt file
    :param params:indicate the params for the fitness sharing, the diffetent
                    options are:
                    -DontPenalize(str): 'best_specie' or 'best_of_each_specie'
                    -Penalization_method(int):
                        1.without penalization
                        2.penalization fitness sharing
                        3.new penalization
                    -ShareFitness(str): 'yes' or 'no'
    :param stats: A :class:`~deap.tools.Statistics` object that is updated
                  inplace, optional.
    :param halloffame: A :class:`~deap.tools.HallOfFame` object that will
                       contain the best individuals, optional.
    :param verbose: Whether or not to log the statistics.
    :returns: The final population.

    It uses :math:`\lambda = \kappa = \mu` and goes as follow.
    It first initializes the population (:math:`P(0)`) by evaluating
    every individual presenting an invalid fitness. Then, it enters the
    evolution loop that begins by the selection of the :math:`P(g+1)`
    population. Then the crossover operator is applied on a proportion of
    :math:`P(g+1)` according to the *cxpb* probability, the resulting and the
    untouched individuals are placed in :math:`P'(g+1)`. Thereafter, a
    proportion of :math:`P'(g+1)`, determined by *mutpb*, is
    mutated and placed in :math:`P''(g+1)`, the untouched individuals are
    transferred :math:`P''(g+1)`. Finally, those new individuals are evaluated
    and the evolution loop continues until *ngen* generations are completed.
    Briefly, the operators are applied in the following order ::

        evaluate(population)
        for i in range(ngen):
            offspring = select(population)
            offspring = mate(offspring)
            offspring = mutate(offspring)
            evaluate(offspring)
            population = offspring

    This function expects :meth:`toolbox.mate`, :meth:`toolbox.mutate`,
    :meth:`toolbox.select` and :meth:`toolbox.evaluate` aliases to be
    registered in the toolbox.

    .. [Back2000] Back, Fogel and Michalewicz, "Evolutionary Computation 1 :
       Basic Algorithms and Operators", 2000.
    """

    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    #creating files to save data.
    d = './Results/%s/pop_file_%d_%d.txt' % (problem, num_p, n_corr)
    ensure_dir(d)
    pop_file = open(d, 'a')

    d = './Results/%s/bestind_%d_%d.txt' % (problem, num_p, n_corr)
    ensure_dir(d)
    best = open(d, 'w')  # save data

    d = './Results/%s/bestind_str_%d_%d.txt' % (problem, num_p, n_corr)
    ensure_dir(d)
    out = open(d, 'w')

    d='./Timing/%s/pop_file_%d_%d.txt' % (problem, num_p, n_corr)
    ensure_dir(d)
    time_file = open(d, 'w')

    d = './Timing/%s/specie_%d_%d.txt' % (problem, num_p, n_corr)
    ensure_dir(d)
    time_specie = open(d, 'w')

    d = './Timing/%s/cruce_s_%d_%d.txt' % (problem, num_p, n_corr)
    ensure_dir(d)
    time_cx = open(d, 'w')

    d = './Specie/%s/specieind_%d_%d.txt' % (problem, num_p, n_corr)
    ensure_dir(d)
    specie_file = open(d, 'w')

    d = './Specie/%s/specist_%d_%d.txt' % (problem, num_p, n_corr)
    ensure_dir(d)
    specie_statis = open(d, 'w')

    d = './Results/%s/bestind_LStr_%d_%d.txt' % (problem, num_p, n_corr)
    ensure_dir(d)
    bestind = open(d, 'w')

    d = './Matrix/%s/' % (problem)
    ensure_dir(d)

    begin=time.time()

    if SaveMatrix:  # Saving data in matrix
        num_r = 11
        num_r_sp=2
        if GenMatrix:
            num_salto=1
            num_c=ngen+1
            Matrix= np.empty((num_c, num_r,))
            Matrix_specie = np.empty((num_c, num_r_sp,), dtype=object)
            vector = np.arange(0, num_c, num_salto)
        else:
            num_c = (cont_evalf/num_salto) + 1
            num_c_sp = (cont_evalf / num_salto) + 1
            Matrix = np.empty((num_c, num_r,))
            Matrix_specie = np.empty((num_c_sp, num_r_sp,), dtype=object)
            vector = np.arange(1, cont_evalf+num_salto, num_salto)
        for i in range(len(vector)):
            Matrix[i, 0] = vector[i]
            Matrix_specie[i, 0] = vector[i]
        Matrix[:, 6] = 0.

    begin_sp = time.time()

    if neat_alg:
        if version == 1:
            for ind in population:
                bit = p_bin(ind)
                ind.binary_rep_set(bit)
        elif version != 1:
            for ind in population:
                level_info = level_node(ind)
                ind.nodefeat_set(level_info)

        species(population,neat_h, version, beta)
        #ind_specie(population)

    end_sp = time.time()
    time_specie.write('\n%s;%s;%s;%s' % (0, begin_sp, end_sp, str(round(end_sp - begin_sp, 2))))

    for ind in population:
        specie_file.write('\n%s;%s;%s;%s' % (0, ind.get_specie(),ind,version))

    if funcEval.LS_flag:
        for ind in population:
            sizep = len(ind)+2
            param_ones = np.ones(sizep)
            param_ones[0] = 0
            ind.params_set(param_ones)

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        funcEval.cont_evalp += 1
        ind.fitness.values = fit

    best_ind = best_pop(population)  # best individual of the population
    if testing:
        fitnesst_best = toolbox.map(toolbox.evaluate_test, [best_ind])
        best_ind.fitness_test.values = fitnesst_best[0]
    if testing:
        best.write('\n%s;%s;%s;%s;%s;%s' % (0, funcEval.cont_evalp, best_ind.fitness_test.values[0], best_ind.fitness.values[0], len(best_ind), avg_nodes(population)))
    else:
        best.write('\n%s;%s;%s;%s;%s;%s' % (
        0, funcEval.cont_evalp, None, best_ind.fitness.values[0], len(best_ind),
        avg_nodes(population)))
    data_pop=avg_nodes(population)
    if SaveMatrix:
        idx = 0
        Matrix[idx, 1] = best_ind.fitness.values[0]
        if testing:
            Matrix[idx, 2] = best_ind.fitness_test.values[0]
        else:
            Matrix[idx, 2] = None
        Matrix[idx, 3] = len(best_ind)
        Matrix[idx, 4] = data_pop[0]
        Matrix[idx, 5] = 0.
        Matrix[idx, 6] = 1  # just an id to know if the current row is full
        Matrix[idx, 7] = data_pop[1]  # max size
        Matrix[idx, 8] = data_pop[2]  # min size
        Matrix[idx, 9] = ind.get_specie() # max number of species in the current population
        Matrix[idx, 10] = max(ind_specie(population), key=lambda x: x[0])[0]  # max number of species in the current population

        np.savetxt('./Matrix/%s/idx_%d_%d.txt' % (problem,num_p, n_corr), Matrix, delimiter=",", fmt="%s")

    if neat_alg:
        SpeciesPunishment(population,params,neat_h)

    if funcEval.LS_flag == 1:
        strg = best_ind.__str__()
        l_strg = add_subt_cf(strg, args=[])
        c = tree2f()
        cd = c.convert(l_strg)
        out.write('\n%s;%s;%s;%s;%s;%s' % (0, len(best_ind), best_ind.LS_applied_get(), best_ind.get_params(), cd, best_ind))
    else:
        out.write('\n%s;%s;%s' % (0, len(best_ind), best_ind))

    for ind in population:
        pop_file.write('\n%s;%s;%s'%(0,ind.fitness.values[0], ind))

    ls_type = ''
    if LS_select == 1:
        ls_type = 'LSHS'
    elif LS_select == 2:
        ls_type = 'Best-Sp'
    elif LS_select == 3:
        ls_type = 'LSHS-Sp'
    elif LS_select == 4:
        ls_type = 'Best-Pop'
    elif LS_select == 5:
        ls_type = 'All-Pop'
    elif LS_select == 6:
        ls_type = 'LSHS-test'
    elif LS_select == 7:
        ls_type = 'Best set'
    elif LS_select == 8:
        ls_type = 'Random set'
    elif LS_select == 9:
        ls_type = "Best-Random set"

    print '---- Generation %d -----' % (0)
    print 'Problem: ', problem
    print 'Problem No.: ', num_p
    print 'Run No.: ', n_corr
    print 'neat-GP:', neat_alg
    print 'neat-cx:', neat_cx
    print 'Local Search:', funcEval.LS_flag
    if funcEval.LS_flag:
        print 'Local Search Heuristic: %s (%s)' % (LS_select,ls_type)
    print 'Best Ind.:', best_ind
    print 'Best Fitness:', best_ind.fitness.values[0]
    if testing:
        print 'Test fitness:', best_ind.fitness_test.values[0]
    print 'Avg Nodes:', avg_nodes(population)
    print 'Evaluations: ', funcEval.cont_evalp
    end_t=time.time()

    if SaveMatrix:
        idx=0
        Matrix_specie[idx,1]=ind_specie(population)
    #specie_statis.write('\n%s;%s' % (0, ind_specie(population)))
        np.savetxt('./Specie/%s/specist_%d_%d.txt' % (problem, num_p, n_corr), Matrix_specie, delimiter=";", fmt="%s")
    if testing:
        time_file.write('\n%s;%s;%s;%s;%s;%s' % (0, begin,end_t, str(round(end_t - begin, 2)), best_ind.fitness.values[0], best_ind.fitness_test.values[0]))
    else:
        time_file.write('\n%s;%s;%s;%s;%s' % (
        0, begin, end_t, str(round(end_t - begin, 2)), best_ind.fitness.values[0]))

    # Begin the generational process
    for gen in range(1, ngen+1):

        if not GenMatrix:
            if funcEval.cont_evalp > cont_evalf:
                break

        begin=time.time()
        print '---- Generation %d -----' % (gen)
        print 'Problem: ', problem
        print 'Problem No.: ', num_p
        print 'Run No.: ', n_corr
        print 'neat-GP:', neat_alg
        print 'neat-cx:', neat_cx
        print 'Local Search:', funcEval.LS_flag
        if funcEval.LS_flag:
            print 'Local Search Heuristic: %s (%s)' % (LS_select, ls_type)

        best_ind = copy.deepcopy(best_pop(population))
        if neat_alg:
            parents = p_selection(population, survival_p = 0.5)
        else:
            parents = toolbox.select(population, len(population))

        begin_cx = time.time()
        if neat_alg:  # neat-Crossover neat_cx and
            n = len(parents)
            mut = 1
            cx = 1
            offspring = neatGP(toolbox, parents, cxpb, mutpb, n, mut, cx, neat_pelit, neat_cx)
        else:
            offspring = varOr(parents, toolbox, cxpb, mutpb)
        end_cx = time.time()
        time_specie.write('\n%s;%s;%s;%s' % (0, begin_cx, end_cx, str(round(end_sp - begin_sp, 2))))

        if neat_alg:  # Speciation of the descendants
            begin_sp = time.time()

            if version ==1:
                for ind in offspring:
                    if ind.binary_rep_get() == None:
                        bit = p_bin(ind)
                        ind.binary_rep_set(bit)

            elif version == 2:
                for ind in offspring:
                    if ind.nodefeat_get() == None:
                        level_info = level_node(ind)
                        ind.nodefeat_set(level_info)

            specie_parents_child(parents,offspring, neat_h, version)
            offspring[:] = parents+offspring
            #ind_specie(offspring)
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)

            for ind, fit in zip(invalid_ind, fitnesses):
                funcEval.cont_evalp += 1
                ind.fitness.values = fit

            end_sp = time.time()
            time_specie.write('\n%s;%s;%s;%s' % (gen, begin_sp, end_sp, str(round(end_sp - begin_sp, 2))))

        else:
            invalid_ind = [ind for ind in offspring]
            if funcEval.LS_flag:
                new_invalid_ind = []
                for ind in invalid_ind:
                    strg = ind.__str__()
                    l_strg = add_subt(strg, ind)
                    c = tree2f()
                    cd = c.convert(l_strg)
                    new_invalid_ind.append(cd)
                fitness_ls = toolbox.map(toolbox.evaluate, new_invalid_ind)
                for ind, ls_fit in zip(invalid_ind, fitness_ls):
                    funcEval.cont_evalp += 1
                    ind.fitness.values = ls_fit
            else:
                fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
                for ind, fit in zip(invalid_ind, fitnesses):
                    funcEval.cont_evalp += 1
                    ind.fitness.values = fit

            orderbyfit = sorted(offspring, key=lambda ind:ind.fitness.values)
            print len(orderbyfit),len(best_ind)

            if best_ind.fitness.values[0] <= orderbyfit[0].fitness.values[0]:
                offspring[:] = [best_ind]+orderbyfit[:len(population)-1]
        print 'End Specie'

        if neat_alg:
            SpeciesPunishment(offspring, params, neat_h)

        if SaveMatrix:
            if GenMatrix:
                idx_aux = np.searchsorted(Matrix[:, 0], gen)
                Matrix_specie[idx_aux, 1] = ind_specie(offspring)
            else:
                #num_c_sp -= 1
                idx_aux = np.searchsorted(Matrix_specie[:, 0], funcEval.cont_evalp)
                try:
                    Matrix_specie[idx_aux, 1] = ind_specie(offspring)
                except IndexError:
                    Matrix_specie[-1, 1] = ind_specie(offspring)
            #specie_statis.write('\n%s;%s' % (gen, ind_specie(offspring)))
            np.savetxt('./Specie/%s/specist_%d_%d.txt' % (problem, num_p, n_corr), Matrix_specie, delimiter=";",
                       fmt="%s")

        population[:] = offspring  # population update

        if neat_alg:
            for ind in population:
                specie_file.write('\n%s;%s;%s;%s' % (gen,ind.get_specie(), ind, version))


        cond_ind = 0
        cont_better=0
        if funcEval.LS_flag:
            for ind in population:
                ind.LS_applied_set(0)

            if   LS_select == 1:
                trees_h(population, num_p, n_corr,  pset, direccion, problem, benchmark_flag)
            elif LS_select == 2:
                best_specie(population, num_p, n_corr, pset, direccion, problem, benchmark_flag)
            elif LS_select == 3:
                specie_h(population, num_p, n_corr, pset, direccion, problem, benchmark_flag)
            elif LS_select == 4:
                best_pop_ls(population, num_p, n_corr, pset, direccion, problem, benchmark_flag)
            elif LS_select == 5:
                all_pop(population, num_p, n_corr, pset, direccion, problem, benchmark_flag)
            elif LS_select == 6:
                trees_h_wo(population, num_p, n_corr, pset, direccion, problem, benchmark_flag)
            elif LS_select == 7:
                ls_bestset(population, num_p, n_corr, pset, direccion, problem, benchmark_flag)
            elif LS_select == 8:
                ls_random(population, num_p, n_corr, pset, direccion, problem, benchmark_flag)
            elif LS_select == 9:
                ls_randbestset(population, num_p, n_corr, pset, direccion, problem, benchmark_flag)
            #
            invalid_ind = [ind for ind in population]
            new_invalid_ind = []
            for ind in population:
                strg = ind.__str__()
                l_strg = add_subt(strg, ind)
                c = tree2f()
                cd = c.convert(l_strg)
                new_invalid_ind.append(cd)
            fitness_ls = toolbox.map(toolbox.evaluate, new_invalid_ind)
            print 'Fitness comp.:',
            for ind, ls_fit in zip(invalid_ind, fitness_ls):
                if ind.LS_applied_get() == 1:
                    cond_ind += 1
                    if ind.fitness.values[0] < ls_fit:
                        print '-',
                    elif ind.fitness.values[0] > ls_fit:
                        cont_better += 1
                        print '+',
                    elif ind.fitness.values[0] == ls_fit:
                        print '=',
                funcEval.cont_evalp += 1
                ind.fitness.values = ls_fit
            print ''


            for ind in population:
                pop_file.write('\n%s;%s;%s;%s;%s'%(gen, ind.fitness.values[0], ind.LS_applied_get(), ind, [x for x in ind.get_params()]))
        else:

            for ind in population:
                pop_file.write('\n%s;%s;%s;%s;%s;%s;%s'%(gen, ind.fitness.values[0], ind.LS_applied_get(),ind.LS_story_get(),ind.off_cx_get(),ind.off_mut_get(), ind))

        best_ind = best_pop(population)
        if funcEval.LS_flag:
            strg = best_ind.__str__()
            l_strg = add_subt(strg, best_ind)
            c = tree2f()
            cd = c.convert(l_strg)
            new_invalid_ind.append(cd)
            bestind.write('\n%s;%s;%s' % (gen, best_ind.fitness.values[0],cd))
            if testing:
                fit_best = toolbox.map(toolbox.evaluate_test, [cd])
                best_ind.fitness_test.values = fit_best[0]

                best.write('\n%s;%s;%s;%s;%s;%s;%s' % (gen, funcEval.cont_evalp,  best_ind.fitness.values[0], best_ind.LS_fitness_get(), best_ind.fitness_test.values[0], len(best_ind), avg_nodes(population)))
            else:
                best.write('\n%s;%s;%s;%s;%s;%s;%s' % (
                gen, funcEval.cont_evalp, best_ind.fitness.values[0], best_ind.LS_fitness_get(),
                None, len(best_ind), avg_nodes(population)))
            out.write('\n%s;%s;%s;%s;%s;%s' % (gen, len(best_ind), best_ind.LS_applied_get(), best_ind.get_params(), cd, best_ind))
        else:
            if testing:
                fitnesses_test = toolbox.map(toolbox.evaluate_test, [best_ind])
                best_ind.fitness_test.values = fitnesses_test[0]
                best.write('\n%s;%s;%s;%s;%s;%s' % (gen, funcEval.cont_evalp, best_ind.fitness_test.values[0], best_ind.fitness.values[0], len(best_ind), avg_nodes(population)))
            else:
                best.write('\n%s;%s;%s;%s;%s;%s' % (
                gen, funcEval.cont_evalp, None, best_ind.fitness.values[0], len(best_ind),
                avg_nodes(population)))
            bestind.write('\n%s;%s;%s' % (gen, best_ind.fitness.values[0], best_ind))
            out.write('\n%s;%s;%s' % (gen, len(best_ind), best_ind))

        if funcEval.LS_flag:
            print 'Num. LS:', cond_ind
            print 'Ind. Improvement:', cont_better
            print 'Best Ind. LS:', best_ind.LS_applied_get()

        print 'Best Ind.:', best_ind
        print 'Best Fitness:', best_ind.fitness.values[0]
        if testing:
            print 'Test fitness:',best_ind.fitness_test.values[0]
        print 'Avg Nodes:', avg_nodes(population)
        print 'Evaluations: ', funcEval.cont_evalp

        if SaveMatrix:
            data_pop=avg_nodes(population)
            if GenMatrix:
                idx_aux = np.searchsorted(Matrix[:, 0], gen)
                Matrix[idx_aux, 1] = best_ind.fitness.values[0]
                if testing:
                    Matrix[idx_aux, 2] = best_ind.fitness_test.values[0]
                else:
                    Matrix[idx_aux, 2] = None
                Matrix[idx_aux, 3] = len(best_ind)
                Matrix[idx_aux, 4] = data_pop[0]
                Matrix[idx_aux, 5] = gen
                Matrix[idx_aux, 6] = 1
                Matrix[idx_aux, 7] = data_pop[1]  # max nodes
                Matrix[idx_aux, 8] = data_pop[2]  # min nodes
                if neat_alg:
                    Matrix[idx_aux, 9] = best_ind.get_specie()
                    Matrix[idx_aux, 10] = max(ind_specie(population), key=lambda x: x[0])[0]
            else:
                if funcEval.cont_evalp >= cont_evalf:
                    num_c -= 1
                    idx_aux=num_c
                    Matrix[num_c, 1] = best_ind.fitness.values[0]
                    if testing:
                        Matrix[num_c, 2] = best_ind.fitness_test.values[0]
                    else:
                        Matrix[num_c, 2] = None
                    Matrix[num_c, 3] = len(best_ind)
                    Matrix[num_c, 4] = data_pop[0]
                    Matrix[num_c, 5] = gen
                    Matrix[num_c, 6] = 1
                    Matrix[num_c, 7] = data_pop[1]  #max_nodes
                    Matrix[num_c, 8] = data_pop[2]  #min nodes
                    if neat_alg:
                        Matrix[num_c, 9] = max(ind_specie(population), key=lambda x: x[0])[0]

                else:
                    idx_aux = np.searchsorted(Matrix[:, 0], funcEval.cont_evalp)
                    Matrix[idx_aux, 1] = best_ind.fitness.values[0]
                    if testing:
                        Matrix[idx_aux, 2] = best_ind.fitness_test.values[0]
                    else:
                        Matrix[idx_aux, 2] = None
                    Matrix[idx_aux, 3] = len(best_ind)
                    Matrix[idx_aux, 4] = data_pop[0]
                    Matrix[idx_aux, 5] = gen
                    Matrix[idx_aux, 6] = 1
                    Matrix[idx_aux, 7] = data_pop[1]  #max nodes
                    Matrix[idx_aux, 8] = data_pop[2]  #min nodes
                    if neat_alg:
                        Matrix[idx_aux, 9] = max(ind_specie(population), key=lambda x: x[0])[0]

                id_it = idx_aux-1
                id_beg = 0
                flag = True
                flag2 = False
                while flag:
                    if Matrix[id_it, 6] == 0:
                        id_it -= 1
                        flag2 = True
                    else:
                        id_beg = id_it
                        flag = False
                if flag2:
                    x = Matrix[id_beg, 1:8]
                    Matrix[id_beg:idx_aux, 1:] = Matrix[id_beg, 1:]

            np.savetxt('./Matrix/%s/idx_%d_%d.txt' % (problem, num_p, n_corr), Matrix, delimiter=",", fmt="%s")

        end_t=time.time()
        if testing:
            time_file.write('\n%s;%s;%s;%s;%s;%s' % (gen, begin, end_t, str(round(end_t - begin, 2)), best_ind.fitness.values[0], best_ind.fitness_test.values[0]))
        else:
            time_file.write('\n%s;%s;%s;%s;%s' % (
            gen, begin, end_t, str(round(end_t - begin, 2)), best_ind.fitness.values[0]))
    return population, logbook


def best_pop(population):
    orderbyfit=list()
    orderbyfit=sorted(population, key=lambda ind:ind.fitness.values)
    return orderbyfit[0]