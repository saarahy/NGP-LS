import operator
import random
import csv
import funcEval
import numpy as np
import neatGPLS
import init_conf
import os.path
import time
import yaml
import copy
import smtplib
import socket
from deap import base
from deap import creator
from deap import tools
from deap import gp
import gp_conf as neat_gp
from shutil import copyfile
from conf_primitives import conf_sets, vector_benchmarks


def evalSymbReg_b(individual, points, toolbox, config, type):
    points.flags['WRITEABLE'] = False
    func = toolbox.compile(expr=individual)
    if config["benchmark"]:
        vector = vector_benchmarks(config["problem"], points)
        data_x = copy.deepcopy(np.asarray(points)[:])
    else:
        vector = copy.deepcopy(points[config["num_var"]])
        data_x = copy.deepcopy(np.asarray(points)[:config["num_var"]])
    try:
        vector_x = func(*data_x)
    except TypeError:
        print individual
        print data_x
    with np.errstate(divide='ignore', invalid='ignore'):
        if isinstance(vector_x, np.ndarray):
            for e in range(len(vector_x)):
                if np.isnan(vector_x[e]) or np.isinf(vector_x[e]):
                    vector_x[e] = 0.
    if config["funcion"] == 1:
        d = './Results/%s/best_data_%d_%s.txt' % (config["problem"], config["n_problem"], type)
        neatGPLS.ensure_dir(d)
        best_test = open(d, 'w')
        for item in vector_x:
            best_test.write("%s\n" % item)
        result = np.sum((vector_x - vector)**2)
        return np.sqrt(result/len(points[0])),
    elif config["funcion"] == 2:
        l = len(points[0])
        ME = np.sum(abs((vector_x - vector))) / l
        SD = np.sqrt(np.sum((vector_x - ME) ** 2) / (l))
        try:
            calc = 100 * (SD / ME)
            return calc,
        except ZeroDivisionError:
            return 100,


def evalSymbReg(individual, points, toolbox, config):
    points.flags['WRITEABLE'] = False
    func = toolbox.compile(expr=individual)
    vector_x=[]
    if config["benchmark"]:
        vector = vector_benchmarks(config["problem"], points)
        data_x = copy.deepcopy(np.asarray(points)[:])
    else:
        vector = copy.deepcopy(points[config["num_var"]])
        data_x = copy.deepcopy(np.asarray(points)[:config["num_var"]])
    try:
        vector_x = func(*data_x)
    except TypeError:
        print 'error'
    with np.errstate(divide='ignore', invalid='ignore'):
        if isinstance(vector_x, np.ndarray):
            for e in range(len(vector_x)):
                if np.isnan(vector_x[e]) or np.isinf(vector_x[e]):
                    vector_x[e] = 0.
    if config["funcion"] == 1:
        result = np.sum((vector_x - vector)**2)
        return np.sqrt(result/len(points[0])),
    elif config["funcion"] == 2:
        l = len(points[0])
        ME = np.sum(abs((vector_x - vector))) / l
        SD = np.sqrt(np.sum((vector_x - ME) ** 2) / (l))
        try:
            calc = 100 * (SD / ME)
            return calc,
        except ZeroDivisionError:
            return 100,


def train_test(n_corr, p, problem, name_database, toolbox, config, train_p, test_p):
    n_archivo = './data_corridas/%s/train_%d_%d.txt' % (problem, p, n_corr)
    n_archivot = './data_corridas/%s/test_%d_%d.txt' % (problem, p, n_corr)
    if not (os.path.exists(n_archivo) or os.path.exists(n_archivot)):
        direccion="./data_corridas/%s/%s" %(problem, name_database)
        with open(direccion) as spambase:
            if config["db_name"][-3:]=="txt":
                spamReader = csv.reader(spambase,  delimiter=' ', skipinitialspace=True)
                num_c = sum(1 for line in open(direccion))
                num_r = len(next(csv.reader(open(direccion), delimiter=' ', skipinitialspace=True)))
            else:
                spamReader = csv.reader(spambase, delimiter=',', skipinitialspace=True)
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
            long_train = int(len(Matrix.T) * train_p)
            data_train1 = random.sample(Matrix.T, long_train)
            np.savetxt(n_archivo, data_train1, delimiter=",", fmt="%s")
        if config["test_flag"]:
            if not os.path.exists(n_archivot):
                long_test = int(len(Matrix.T) * test_p)
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
                    print 'Line {r} is corrupt train' , r
                    break
        data_train=Matrix[:]
    if config["test_flag"]:
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
                        print 'Line {r} is corrupt test' , r
                        break
            data_test=Matrix[:]
    toolbox.register("evaluate", evalSymbReg, points=data_train, toolbox=toolbox, config=config)
    toolbox.register("evaluate_best_t", evalSymbReg_b, points=data_train, toolbox=toolbox, config=config, type="train")
    if config["test_flag"]:
        toolbox.register("evaluate_test", evalSymbReg, points=data_test, toolbox=toolbox, config=config)
        toolbox.register("evaluate_best", evalSymbReg_b, points=data_test, toolbox=toolbox, config=config, type="test")



def main(n_corr, p, problem, database_name, pset, config):


    pop_size = config["population_size"]
    cxpb                = config["cxpb"]  # 0.9
    mutpb               = config["mutpb"]  # 0.1
    train_p             = config["train_p"]
    test_p              = config["test_p"]
    tournament_size     = config["tournament_size"]
    ngen                = config["generations"]

    params              = ['best_of_each_specie', 2, 'yes']
    neat_cx             = config["neat_cx"]
    neat_alg            = config["neat_alg"]
    neat_pelit          = config["neat_pelit"]
    neat_h              = config["neat_h"]
    beta                = config["neat_beta"]
    random_speciation   = config["nRandom_speciation"]

    funcEval.LS_flag    = config["ls_flag"]
    LS_select           = config["ls_select"]
    funcEval.cont_evalp = 0
    num_salto           = config["num_salto"]  # 500
    cont_evalf          = config["cont_evalf"]

    SaveMatrix          = config["save_matrix"]
    GenMatrix           = config["gen_matrix"]
    version             = 3
    testing             = config["test_flag"]
    benchmark_flag      = config["benchmark"]


    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("FitnessTest", base.Fitness, weights=(-1.0,))
    creator.create("Individual", neat_gp.PrimitiveTree, fitness=creator.FitnessMin, fitness_test=creator.FitnessTest)

    toolbox = base.Toolbox()

    if neat_cx:
        toolbox.register("expr", gp.genFull, pset=pset, min_=0, max_=3)
    else:
        toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=0, max_=7)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", init_conf.initRepeat, list, toolbox.individual)
    toolbox.register("compile", gp.compile, pset=pset)

    name_database=database_name
    direccion="./data_corridas/%s/train_%d_%d.txt"
    train_test(n_corr,p, problem, name_database, toolbox, config, train_p, test_p)

    toolbox.register("select", tools.selTournament, tournsize=tournament_size)
    toolbox.register("mate", neat_gp.cxSubtree)
    if neat_cx:
        toolbox.register("expr_mut", gp.genFull, min_=0, max_=3)
    else:
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


    pop, log, train_f, test_f = neatGPLS.neat_GP_LS(pop, toolbox, cxpb, mutpb, ngen, neat_alg, neat_cx, neat_h,
                                   neat_pelit, funcEval.LS_flag, LS_select, cont_evalf,
                                   num_salto, SaveMatrix, GenMatrix, pset, n_corr, p,
                                   params, direccion, problem, testing, version, benchmark_flag, beta,
                                   random_speciation, config,stats=mstats, halloffame=hof, verbose=True)

    # Regresa el mejor de las generaciones
    return pop, log, hof, train_f, test_f

if __name__ == "__main__":

    config        = yaml.load(open("conf/conf.yaml"))
    problem       = config["problem"]
    num_var       = config["num_var"]
    database_name = config["db_name"]
    number        = config["n_problem"]

    c_f = './conf_record/%s/' % (problem)
    neatGPLS.ensure_dir(c_f)
    copyfile('./conf/conf.yaml', ('./conf_record/%s/config_%s_%d.yaml'% (problem, problem, number)))

    c_m = './matrix_complete/%s/Matrix_c_%d.csv' % (problem, number)
    neatGPLS.ensure_dir(c_m)
    matrix_complete = open(c_m, 'a')

    c_s = './matrix_complete/%s/stats_train_%d.csv' % (problem, number)
    neatGPLS.ensure_dir(c_s)
    matrix_stats = open(c_s, 'a')

    c_s = './matrix_complete/%s/stats_test_%d.csv' % (problem, number)
    neatGPLS.ensure_dir(c_s)
    matrix_stats_t = open(c_s, 'a')

    d = './Timing/%s/timing_cxneat_%d.txt' % (problem, number)
    neatGPLS.ensure_dir(d)
    time_conc = open(d, 'a')

    pset = conf_sets(num_var)

    instance_name=socket.gethostname()

    n = config["run_begin"]
    train_list = np.empty([config["run_end"]])
    test_list = np.empty([config["run_end"]])
    while n < config["run_end"]:
        begin_p = time.time()
        a=main(n, number, problem, database_name, pset, config)
        train_list[n]= a[3]
        test_list[n] = a[4]
        n += 1
        end_p = time.time()
        time_conc.write('\n%s;%s;%s;%s' % (n, begin_p, end_p, str(round(end_p - begin_p, 2))))
        matrix_complete.write('\n%s,%s' % (a[3],a[4]))
    matrix_stats.write('\n%s,%s,%s,%s,%s,%s' % (np.min(train_list), np.max(train_list),np.mean(train_list), np.median(train_list), np.std(train_list), train_list.argmin()))
    matrix_stats_t.write('\n%s,%s,%s,%s,%s,%s' % (
    np.min(test_list), np.max(test_list), np.mean(test_list), np.median(test_list), np.std(test_list),test_list.argmin()))