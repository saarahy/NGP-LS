import operator
import numpy as numpy
import neatGPLS
import init_conf
import funcEval
import time
from scipy import stats
from deap import base
from deap import creator
from deap import tools
from deap import gp
import gp_conf as neat_gp
from ParentSelection import sort_fitnessvalues
from my_operators import safe_div, mylog, mysqrt, myexp

pset = gp.PrimitiveSet("MAIN", 4)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(safe_div, 2)
pset.addPrimitive(numpy.cos, 1)
pset.addPrimitive(numpy.sin, 1)
#pset.addPrimitive(numpy.exp,1)
pset.addPrimitive(mylog,1)
pset.addPrimitive(mysqrt, 1)
pset.addPrimitive(numpy.tan, 1)
pset.addPrimitive(numpy.tanh, 1)
pset.renameArguments(ARG0='x0',ARG1='x1', ARG2='x2', ARG3='x3')

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
    values= points[:,4]
    sqerrors = numpy.sum((func(*points[:,[0,1,2,3]].T) - values)**2)
    return numpy.sqrt(sqerrors / len(points)),

def evalSymbReg_MSE(individual, points):
    func = toolbox.compile(expr=individual)
    values= points[:,4]
    sqerrors = numpy.sum((func(*points[:,[0,1,2,3]].T) - values)**2)
    return sqerrors / len(points),

def evalSymbReg_R2(individual, points):
    func = toolbox.compile(expr=individual)
    values= points[:,4]
    slope, intercept, r_value, p_value, std_err = stats.linregress(func(*points[:,[0,1,2,3]].T),values)
    r=r_value**2
    return r,

def evalSymbReg_MAE(individual, points):
    func = toolbox.compile(expr=individual)
    values= points[:,4]
    sqerrors = numpy.sum(func(*points[:,[0,1,2,3]].T) - values)
    return sqerrors / len(points),

def ww(n_corr):
    direccion="./data_corridas/wastewater/wastewater_test_%d.txt"
    direccion2="./data_corridas/wastewater/wastewater_train_%d.txt"
    my_data = numpy.genfromtxt(direccion % n_corr)
    my_data2 = numpy.genfromtxt(direccion2 % n_corr)
    toolbox.register("evaluate_test", evalSymbReg, points=my_data)
    toolbox.register("evaluate", evalSymbReg, points=my_data2)


def main(n_corr, num_p, problem):
    #problem="wastewater"
    direccion = "./data_corridas/wastewater/wastewater_train_%d.txt"
    ww(n_corr)

    toolbox.register("select", tools.selTournament, tournsize=7)
    toolbox.register("mate", neat_gp.cxSubtree)
    #toolbox.register("expr_mut", gp.genFull, min_=0, max_=3)
    toolbox.register("expr_mut", gp.genHalfAndHalf, min_=0, max_=6)
    toolbox.register("mutate", neat_gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
    toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
    toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(3)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    stats_fit_test=tools.Statistics(lambda i: i.fitness_test.values)
    mstats = tools.MultiStatistics(fitness=stats_fit,size=stats_size, fitness_test=stats_fit_test)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)
    params = ['best_of_each_specie', 2, 'yes']
    cxpb=0.7#.9
    mutpb=0.3#.1
    ngen=50000
    neat_cx = True
    neat_alg = True
    neat_pelit = 0.5
    neat_h = 0.15
    funcEval.LS_flag = False
    LS_select = 3
    funcEval.cont_evalp = 0
    num_salto = 500
    cont_evalf = 100000
    SaveMatrix = True
    GenMatrix=True
    testing = True
    version = 1
    pop, log = neatGPLS.neat_GP_LS(pop, toolbox, cxpb, mutpb, ngen, neat_alg, neat_cx, neat_h,
                                   neat_pelit,funcEval.LS_flag, LS_select, cont_evalf,
                                   num_salto, SaveMatrix, GenMatrix, pset, n_corr, num_p,
                                   params, direccion, problem, testing, version,
                                   stats=mstats, halloffame=hof,verbose=True)
    return pop, log, hof


def run(number,problem):
    n = 1
    while n <= number:
        main(n,problem)
        n += 1


if __name__ == "__main__":
    problem = 'wastewater2'
    number = 1000
    d = './Timing/%s/timing_cxneat_%d.txt' % (problem, number)
    neatGPLS.ensure_dir(d)
    time_conc = open(d, 'a')

    n = 1
    while n < 11:
        begin_p = time.time()
        main(n, number, problem)
        n += 1
        end_p = time.time()
        time_conc.write('\n%s;%s;%s;%s' % (n, begin_p, end_p, str(round(end_p - begin_p, 2))))
