import operator
import random
import csv
import cProfile
import funcEval
import numpy as np
import neatGPLS
import init_conf
import os.path
from deap import base
from deap import creator
from deap import tools
from deap import gp
import gp_conf as neat_gp
from my_operators import safe_div, mylog, mypower2, mypower3, mysqrt


pset = gp.PrimitiveSet("MAIN", 5)
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
pset.renameArguments(ARG0='x0',ARG1='x1', ARG2='x2', ARG3='x3', ARG4='x4')


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("FitnessTest", base.Fitness, weights=(-1.0,))
creator.create("Individual", neat_gp.PrimitiveTree, fitness=creator.FitnessMin, fitness_test=creator.FitnessTest)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, min_=1, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", init_conf.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def selElitistAndTournament(individuals, k_elitist, k_tournament, tournsize):
    return tools.selBest(individuals, k_elitist) + tools.selTournament(individuals, k_tournament, tournsize=3)


def evalSymbReg(individual, test, points):
    func = toolbox.compile(expr=individual)
    vector = points[5]
    try:
        result =np.sum((func(*np.asarray(points)[:5]) - vector)**2)
    except TypeError:
        result = np.sum(np.power((np.subtract(func(*np.asarray(points)[:5]),vector)),2))
    return np.sqrt(result/len(points[0])),

def energy_coolng(problem,n_corr,p):
    p=1
    n_archivot='./data_corridas/%s/test_%d_%d.txt' % (problem, p, n_corr)
    n_archivo='./data_corridas/%s/train_%d_%d.txt' % (problem, p, n_corr)
    if not (os.path.exists(n_archivo) or os.path.exists(n_archivot)):
        print ("generar archivos")
    else:
        with open(n_archivo) as spambase:
            spamReader = csv.reader(spambase,  delimiter=',', skipinitialspace=True)
            num_c = sum(1 for line in open(n_archivo))
            num_r = len(next(csv.reader(open(n_archivo), delimiter=',', skipinitialspace=True)))
            Matrix = np.empty((num_r, num_c,))
            for row, c in zip(spamReader, range(num_c)):
                for r in range(num_r):
                    try:
                        Matrix[r, c] = row[r]
                    except ValueError:
                        print 'Line {r} is corrupt' , r
                        break
            data_train=Matrix[:]
        with open(n_archivot) as spambase:
            spamReader = csv.reader(spambase,  delimiter=',', skipinitialspace=True)
            num_c = sum(1 for line in open(n_archivot))
            num_r = len(next(csv.reader(open(n_archivot), delimiter=',', skipinitialspace=True)))
            Matrix = np.empty((num_r, num_c,))
            for row, c in zip(spamReader, range(num_c)):
                for r in range(num_r):
                    try:
                        Matrix[r, c] = row[r]
                    except ValueError:
                        print 'Line {r} is corrupt' , r
                        break
            data_test=Matrix[:]
    toolbox.register("evaluate", evalSymbReg, test=False, points=data_train)
    toolbox.register("evaluate_test", evalSymbReg,  test=True, points=data_test)


def main(n_corr, p):
    problem = "Korns12"
    direccion="./data_corridas/Korns12/train_%d_%d.txt"
    energy_coolng(problem,n_corr,p)

    pop_size = 100
    toolbox.register("select",selElitistAndTournament, k_elitist=int(0.1*pop_size), k_tournament=pop_size - int(0.1*pop_size), tournsize=3)
    toolbox.register("mate", neat_gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genFull, min_=0, max_=3)
    toolbox.register("mutate", neat_gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
    toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
    toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

    pop = toolbox.population(n=pop_size)
    hof = tools.HallOfFame(3)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", np.mean)
    mstats.register("std", np.std)
    mstats.register("min", np.min)
    mstats.register("max", np.max)
    cxpb = 0.7
    mutpb = 0.3
    ngen = 3000000
    params = ['best_of_each_specie', 2, 'yes']
    neat_cx = True
    neat_alg = True
    neat_pelit = 0.5
    neat_h = 0.15
    funcEval.LS_flag = False
    LS_select = 1
    funcEval.cont_evalp = 0
    num_salto = 5000
    cont_evalf = 2500000
    SaveMatrix = True

    pop, log = neatGPLS.neat_GP_LS(pop, toolbox, cxpb, mutpb, ngen, neat_alg, neat_cx, neat_h, neat_pelit, funcEval.LS_flag, LS_select, cont_evalf, num_salto, SaveMatrix,pset,n_corr, p, params, direccion,problem,stats=mstats, halloffame=hof, verbose=True)


    return pop, log, hof


def run(number, problem):
    n = 1
    while n <= number:
        main(n, problem)
        n += 1


if __name__ == "__main__":
    n = 1
    while n < 6:
        #cProfile.run('print main(n, 93); print')
        main(n, 2)
        n += 1