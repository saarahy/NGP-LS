import numpy as np
import random
import funcEval
from tree_subt import add_subt_cf
from minpack_conf import curve_fit_2
from tree2func import tree2f
from eval_str import eval_
from g_address import get_address
from speciation import ind_specie, specie_gpo

def eval_prob(population):
    n_nodes = []
    for ind in population:
        n_nodes.append(len(ind))
    nn_nodes = np.asarray(n_nodes)
    av_size = np.mean(nn_nodes)
    c = 1.5
    for ind in population:
        ind.LS_probability(0.0)
        ratio=(len(ind)/av_size)
        y = c-ratio
        if len(ind) < (0.5 * av_size):
            ind.LS_probability(1.)
        elif (len(ind) >= (0.5 * av_size)) and (len(ind) <= (1.5 * av_size)):
            ind.LS_probability(y)


def best_pop(population):
    orderbyfit=list()
    orderbyfit = sorted(population, key=lambda ind:ind.fitness.values)
    return orderbyfit[0]

def best_set_pop(population):
    orderbyfit=list()
    orderbyfit = sorted(population, key=lambda ind:ind.fitness.values)
    selected=len(population)*.10
    p_sel=int(np.round(selected,0))
    return orderbyfit[:p_sel]

def bestrand_set_pop(population):
    orderbyfit=list()
    orderbyfit = sorted(population, key=lambda ind:ind.fitness.values)
    selected=len(population)*.10
    p_sel=int(np.round(selected,0))
    ind_sel=orderbyfit[:p_sel]
    ind_list=list()
    for ind in ind_sel:
        coin=random.randint(0,1)
        if coin:
            ind_list.append(ind)
    return ind_list

def random_set_pop(population):
    orderbyfit=list()
    for ind in population:
        coin=random.randint(0,1)
        if coin:
            orderbyfit.append(ind)
    return orderbyfit


def ls_bestset(population, p, n, pset, direccion, problem):  # size heuristic
    best_set=best_set_pop(population)
    for ind in best_set:
        strg = ind.__str__()
        args = []
        if len(pset.arguments) > 1:
            for arg in pset.arguments:
                args.append(arg)
        l_strg = add_subt_cf(strg, args)
        c = tree2f()
        cd = c.convert(l_strg)
        xdata, ydata = get_address(p, n, problem, direccion)
        beta_opt, beta_cov, success, nfev = curve_fit_2(eval_,cd , xdata, ydata, p0=ind.get_params(), method='trf', max_nfev=40)
        if not success:
            ind.LS_applied_set(1)
            ind.LS_story_set(1)
        else:
            ind.LS_applied_set(1)
            ind.LS_story_set(1)
            funcEval.cont_evalp += nfev
            ind.params_set(beta_opt)


def ls_random(population, p, n, pset, direccion, problem):  # size heuristic
    random_set=random_set_pop(population)
    for ind in random_set:
        strg = ind.__str__()
        args = []
        if len(pset.arguments) > 1:
            for arg in pset.arguments:
                args.append(arg)
        l_strg = add_subt_cf(strg, args)
        c = tree2f()
        cd = c.convert(l_strg)
        xdata, ydata = get_address(p, n, problem,direccion)
        beta_opt, beta_cov, success, nfev = curve_fit_2(eval_,cd , xdata, ydata, p0=ind.get_params(), method='trf', max_nfev=40)
        if not success:
            ind.LS_applied_set(1)
            ind.LS_story_set(1)
        else:
            ind.LS_applied_set(1)
            ind.LS_story_set(1)
            funcEval.cont_evalp += nfev
            ind.params_set(beta_opt)

def ls_randbestset(population, p, n, pset, direccion, problem):  # size heuristic
    best_set=bestrand_set_pop(population)
    for ind in best_set:
        strg = ind.__str__()
        args = []
        if len(pset.arguments) >= 1:
            for arg in pset.arguments:
                args.append(arg)
        l_strg = add_subt_cf(strg, args)
        c = tree2f()
        cd = c.convert(l_strg)
        xdata, ydata = get_address(p, n,problem,direccion)
        beta_opt, beta_cov, success, nfev = curve_fit_2(eval_,cd , xdata, ydata, p0=ind.get_params(), method='trf', max_nfev=40)
        if not success:
            ind.LS_applied_set(1)
            ind.LS_story_set(1)
        else:
            ind.LS_applied_set(1)
            ind.LS_story_set(1)
            funcEval.cont_evalp += nfev
            ind.params_set(beta_opt)


def trees_h(population, p, n, pset, direccion, problem):  # size heuristic
    eval_prob(population)
    for ind in population:
        if random.random() <= ind.get_LS_prob():
            strg = ind.__str__()
            args = []
            if len(pset.arguments) > 1:
                for arg in pset.arguments:
                    args.append(arg)
            l_strg = add_subt_cf(strg, args)
            c = tree2f()
            cd = c.convert(l_strg)
            xdata, ydata = get_address(p, n, problem, direccion)
            beta_opt, beta_cov, success, nfev = curve_fit_2(eval_,cd , xdata, ydata, p0=ind.get_params(), method='trf', max_nfev=40)
            if not success:
                ind.LS_applied_set(1)
                ind.LS_story_set(1)
            else:
                ind.LS_applied_set(1)
                ind.LS_story_set(1)
                funcEval.cont_evalp += nfev
                ind.params_set(beta_opt)


def trees_h_wo(population, p, n, pset, direccion):  # size heuristic
    eval_prob(population)
    for ind in population:
        if random.random() <= ind.get_LS_prob():
            ind.LS_applied_set(1)
            ind.LS_story_set(1)


def all_pop(population, p, n, pset, direccion):  # size heuristic
    for ind in population:
        strg = ind.__str__()
        args = []
        if len(pset.arguments) > 1:
            for arg in pset.arguments:
                args.append(arg)
        l_strg = add_subt_cf(strg, args)
        c = tree2f()
        cd = c.convert(l_strg)
        xdata, ydata = get_address(p, n, direccion)
        beta_opt, beta_cov, success, nfev = curve_fit_2(eval_,cd , xdata, ydata, p0=ind.get_params(), method='trf', max_nfev=40)
        if not success:
            ind.LS_applied_set(1)
            ind.LS_story_set(1)
        else:
            ind.LS_applied_set(1)
            ind.LS_story_set(1)
            ind.params_set(beta_opt)
            funcEval.cont_evalp+=nfev


def best_pop_ls(population, p,  n, pset, direccion):  # best of the pop
    ind = best_pop(population)
    strg = ind.__str__()
    args = []
    if len(pset.arguments) > 1:
        for arg in pset.arguments:
            args.append(arg)
    l_strg = add_subt_cf(strg, args)
    c = tree2f()
    cd = c.convert(l_strg)
    xdata,ydata = get_address(p, n, direccion)
    beta_opt, beta_cov, success, nfev = curve_fit_2(eval_, cd, xdata, ydata, p0=ind.get_params(), method='trf', max_nfev=40)
    if not success:
        ind.LS_applied_set(1)
        ind.LS_story_set(1)
    else:
        ind.LS_applied_set(1)
        ind.LS_story_set(1)
        ind.params_set(beta_opt)
        funcEval.cont_evalp += nfev


def best_specie(population, p, n, pset, direccion):  # best of each specie
    for ind in population:
       if ind.bestspecie_get()==1:
            strg=ind.__str__()
            args=[]
            if len(pset.arguments) > 0:
                for arg in pset.arguments:
                    args.append(arg)
            l_strg=add_subt_cf(strg, args)
            c = tree2f()
            cd=c.convert(l_strg)
            xdata,ydata=get_address(p, n,direccion)
            beta_opt, beta_cov, success, nfev = curve_fit_2(eval_,cd , xdata, ydata, p0=ind.get_params(), method='trf', max_nfev=40)
            if not success:
                ind.LS_applied_set(1)
                ind.LS_story_set(1)
            else:
                ind.LS_applied_set(1)
                ind.LS_story_set(1)
                ind.params_set(beta_opt)
                funcEval.cont_evalp+=nfev


def specie_h(population, p, n, pset, direccion):  # heuristic applied by specie
    gpo_specie=specie_gpo(population)
    for specie in gpo_specie:
        eval_prob(specie[0])
    for ind in population:
        if ind.bestspecie_get()==1:
            if random.random()<=ind.get_LS_prob():
                strg=ind.__str__()
                args=[]
                if len(pset.arguments) > 0:
                    for arg in pset.arguments:
                        args.append(arg)
                l_strg=add_subt_cf(strg, args)
                c = tree2f()
                cd=c.convert(l_strg)
                xdata,ydata=get_address(p, n,direccion)
                beta_opt, beta_cov, success, nfev = curve_fit_2(eval_,cd , xdata, ydata, p0=ind.get_params(), method='trf', max_nfev=40)
                if not success:
                    ind.LS_applied_set(1)
                    ind.LS_story_set(1)
                else:
                    ind.LS_applied_set(1)
                    ind.LS_story_set(1)
                    ind.params_set(beta_opt)
                    funcEval.cont_evalp += nfev

