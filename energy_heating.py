import operator
import random
import csv
import cProfile
import funcEval
import numpy as np
import neatGPLS
import init_conf
import os.path
import time
from deap import base
from deap import creator
from deap import tools
from deap import gp
from deap import algorithms
import gp_conf as neat_gp
from my_operators import safe_div, mylog, mypower2, mypower3, mysqrt, myexp


pset = gp.PrimitiveSet("MAIN", 8)
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
pset.renameArguments(ARG0='x0',ARG1='x1', ARG2='x2', ARG3='x3', ARG4='x4', ARG5='x5', ARG6='x6', ARG7='x7')


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("FitnessTest", base.Fitness, weights=(-1.0,))
creator.create("Individual", neat_gp.PrimitiveTree, fitness=creator.FitnessMin, fitness_test=creator.FitnessTest)

toolbox = base.Toolbox()
#toolbox.register("expr", gp.genFull, pset=pset, min_=0, max_=3)
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=0, max_=6)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", init_conf.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)


def evalSymbReg(individual, points):
    func = toolbox.compile(expr=individual)
    vector = points[8]
    data_x=np.asarray(points)[:8]
    vector_x=func(*data_x)
    with np.errstate(divide='ignore', invalid='ignore'):
        if isinstance(vector_x, np.ndarray):
            for e in range(len(vector_x)):
                if np.isnan(vector_x[e]) or np.isinf(vector_x[e]):
                    vector_x[e] = 0.
    result = np.sum((vector_x - vector)**2)
    return np.sqrt(result/len(points[0])),

def energy_coolng(n_corr, num_p, problem, name_database):
    n_archivot='./data_corridas/%s/test_%d_%d.txt' % (problem, num_p, n_corr)
    n_archivo='./data_corridas/%s/train_%d_%d.txt' % (problem, num_p, n_corr)
    if not (os.path.exists(n_archivo) or os.path.exists(n_archivot)):
        direccion="./data_corridas/%s/%s.csv" % (problem, name_database)
        with open(direccion) as spambase:
            spamReader = csv.reader(spambase,  delimiter=',', skipinitialspace=True)
            num_c = sum(1 for line in open(direccion))
            num_r = len(next(csv.reader(open(direccion), delimiter=',', skipinitialspace=True)))
            Matrix = np.empty((num_r, num_c,))
            for row, c in zip(spamReader, range(num_c)):
                for r in range(num_r):
                    try:
                        Matrix[r, c] = row[r]
                    except ValueError:
                        print 'Line {r} is corrupt', r
                        break
        if not os.path.exists(n_archivo):
            long_train=int(len(Matrix.T)*.7)
            data_train1 = random.sample(Matrix.T, long_train)
            np.savetxt(n_archivo, data_train1, delimiter=",", fmt="%s")
        if not os.path.exists(n_archivot):
            long_test=int(len(Matrix.T)*.3)
            data_test1 = random.sample(Matrix.T, long_test)
            np.savetxt(n_archivot, data_test1, delimiter=",", fmt="%s")
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
    toolbox.register("evaluate", evalSymbReg, points=data_train)
    toolbox.register("evaluate_test", evalSymbReg, points=data_test)


def main(n_corr, num_p, problem):
    #problem = "EnergyHeatingBin"
    name_database="energy_efficiency_Heat"
    direccion="./data_corridas/%s/train_%d_%d.txt"
    energy_coolng(n_corr, num_p, problem, name_database)

    pop_size = 100
    toolbox.register("select", tools.selTournament, tournsize=7)
    toolbox.register("mate", neat_gp.cxSubtree)
    #toolbox.register("expr_mut", gp.genFull, min_=0, max_=3) #3
    toolbox.register("expr_mut", gp.genHalfAndHalf, min_=0, max_=6)
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
    cxpb = 0.9#0.7
    mutpb = 0.1#0.3
    ngen = 100
    params = ['best_of_each_specie', 2, 'yes']
    neat_cx = False
    neat_alg = True
    neat_pelit = 0.5
    neat_h = 0.15
    funcEval.LS_flag =True
    LS_select = 8
    funcEval.cont_evalp = 0
    num_salto = 1
    cont_evalf = 100000
    SaveMatrix = True
    GenMatrix = True
    testing=True
    version=3
    pop, log = neatGPLS.neat_GP_LS(pop, toolbox, cxpb, mutpb, ngen, neat_alg, neat_cx,
                                   neat_h, neat_pelit, funcEval.LS_flag, LS_select,
                                   cont_evalf, num_salto, SaveMatrix, GenMatrix,
                                   pset,n_corr, num_p, params, direccion,problem,
                                   testing, version,
                                   stats=mstats, halloffame=hof, verbose=True)

    return pop, log, hof


def run(number, problem):
    n = 1
    while n <= number:
        main(n, problem)
        n += 1

if __name__ == "__main__":
    problem='EHeating'
    number = 1108
    d = './Timing/%s/timing_cxneat_%d.txt'%(problem,number)
    neatGPLS.ensure_dir(d)
    time_conc = open(d, 'a')

    n = 1
    while n < 31:
        begin_p = time.time()
        main(n, number, problem)
        n += 1
        end_p = time.time()
        time_conc.write('\n%s;%s;%s;%s' % (n, begin_p, end_p, str(round(end_p - begin_p, 2))))
