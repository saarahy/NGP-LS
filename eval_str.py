from numpy import sin, cos, divide, division, seterr, tanh, tan
from my_operators import safe_div, mylog, mysqrt, mypower2, mypower3, myexp, negexp, negative, absolute
from operator import add, sub, mul


def eval_(strg, x, *p):
    seterr(divide='ignore', invalid='ignore')
    try:
        x_r = eval(strg)
    except TypeError:
        print 'Error.', strg
    except NameError:
        print strg

    return x_r

