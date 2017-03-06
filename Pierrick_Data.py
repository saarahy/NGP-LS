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


pset = gp.PrimitiveSet("MAIN", 1)
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
pset.renameArguments(ARG0='x0')


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("FitnessTest", base.Fitness, weights=(-1.0,))
creator.create("Individual", neat_gp.PrimitiveTree, fitness=creator.FitnessMin, fitness_test=creator.FitnessTest)

toolbox = base.Toolbox()
#toolbox.register("expr", gp.genFull, pset=pset, min_=0, max_=3)
toolbox.register("expr", gp.genHalfAndHalf, pset=pset,min_=0, max_=7)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", init_conf.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)


def evalSymbReg(individual, points):
    func = toolbox.compile(expr=individual)
    vector = points[1]
    data_x=np.asarray(points)[:1]
    vector_x=func(*data_x)
    with np.errstate(divide='ignore', invalid='ignore'):
        if isinstance(vector_x, np.ndarray):
            for e in range(len(vector_x)):
                if np.isnan(vector_x[e]) or np.isinf(vector_x[e]):
                    vector_x[e] = 0.
    result = np.sum((vector_x - vector)**2)
    return np.sqrt(result/len(points[0])),


def energy_coolng(n_corr, p, directory, file, testing):
    n_archivot='./data_corridas/%s/test_%d_%d.txt'%(directory,p,n_corr)
    n_archivo='./data_corridas/%s/train_%d_%d.txt'%(directory,p,n_corr)
    if not (os.path.exists(n_archivo) or os.path.exists(n_archivot)):
        direccion="./data_corridas/%s/%s"%(directory,file)
        with open(direccion) as spambase:
            spamReader = csv.reader(spambase,  delimiter=',', skipinitialspace=False)
            num_c = sum(1 for line in open(direccion))
            num_r = len(next(csv.reader(open(direccion), delimiter=',', skipinitialspace=False)))
            Matrix = np.empty((num_r, num_c,))
            for row, c in zip(spamReader, range(num_c)):
                for r in range(num_r):
                    try:
                        Matrix[r, c] = row[r]
                    except ValueError:
                        print 'Line {r} is corrupt', r
                        break
        if testing:
            if not os.path.exists(n_archivo):
                long_train=int(len(Matrix.T)*.7)
                data_train1 = random.sample(Matrix.T, long_train)
                np.savetxt(n_archivo, data_train1, delimiter=",", fmt="%s")
            if not os.path.exists(n_archivot):
                long_test=int(len(Matrix.T)*.3)
                data_test1 = random.sample(Matrix.T, long_test)
                np.savetxt(n_archivot, data_test1, delimiter=",", fmt="%s")
        else:
            if not os.path.exists(n_archivo):
                long_train=int(len(Matrix.T))
                data_train1 = random.sample(Matrix.T, long_train)
                np.savetxt(n_archivo, data_train1, delimiter=",", fmt="%s")
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
    if testing:
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
    if testing:
        toolbox.register("evaluate_test", evalSymbReg, points=data_test)


def main(n_corr, p):
    direccion="./data_corridas/PierrickData24/train_%d_%d.txt"
    directory="PierrickData24"
    file="patient4.csv"
    testing=False
    energy_coolng(n_corr, p, directory, file, testing)

    pop_size = 100
    toolbox.register("select", tools.selTournament, tournsize=7)
    toolbox.register("mate", neat_gp.cxSubtree)
    #toolbox.register("expr_mut", gp.genFull, min_=0, max_=3)
    toolbox.register("expr_mut", gp.genHalfAndHalf, min_=0, max_=7)
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
    cxpb = 0.9#.9
    mutpb = 0.1#.1
    ngen = 100
    params = ['best_of_each_specie', 2, 'yes']
    neat_cx = False
    neat_alg = True
    neat_pelit = 0.5
    neat_h = 0.15
    funcEval.LS_flag = False
    LS_select = 9
    funcEval.cont_evalp = 0
    num_salto = 1#500
    cont_evalf = 100000
    SaveMatrix = True
    problem = "PierrickData24"
    GenMatrix = True
    version=3

    pop, log = neatGPLS.neat_GP_LS(pop, toolbox, cxpb, mutpb, ngen, neat_alg, neat_cx, neat_h, neat_pelit, funcEval.LS_flag,
                                   LS_select, cont_evalf, num_salto, SaveMatrix,GenMatrix,pset,n_corr, p, params,
                                   direccion,problem, testing,
                                   version=version,stats=mstats, halloffame=hof, verbose=True)

    return pop, log, hof


def run(number, problem):
    n = 1
    while n <= number:
        main(n, problem)
        n += 1
if __name__ == "__main__":
    number=1000
    d = './Timing/PierrickData24/timing_Concrete_cxneat_%d.txt'%number
    neatGPLS.ensure_dir(d)
    time_conc = open(d, 'a')


    n = 1
    while n < 15:
        begin_p = time.time()
        main(n, number) #1701 cx-sub
        n += 1
        end_p=time.time()
        time_conc.write('\n%s;%s;%s;%s' % (n, begin_p, end_p, str(round(end_p - begin_p, 2))))
#Concrete
#3000 Gp Standar .9 7 .7 H& H
#3510 LSHS
#3570 Bestset
#3580 Random
#3590 BestRandom

#18012 subtree neat GP LS
#17012 subtrie neat
#19012 neat cx GP LS



