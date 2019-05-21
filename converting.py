import operator
import random
import numpy as np
from deap import base
from deap import creator
from deap import tools
from deap import gp
import gp_conf as neat_gp
from my_operators import safe_div, mylog, mypower2, mypower3, mysqrt, myexp, absolute, negative, negexp

class convert():
    def cont(self,str_ind):
        pset = gp.PrimitiveSet("MAIN", 25)
        pset.addPrimitive(operator.add, 2)
        pset.addPrimitive(operator.sub, 2)
        pset.addPrimitive(operator.mul, 2)
        pset.addPrimitive(safe_div, 2)
        pset.addPrimitive(np.cos, 1)
        pset.addPrimitive(np.sin, 1)
        pset.addPrimitive(myexp, 1)
        pset.addPrimitive(mylog, 1)
        pset.addPrimitive(mypower2, 1)
        pset.addPrimitive(mypower3, 1)
        pset.addPrimitive(mysqrt, 1)
        pset.addPrimitive(np.tan, 1)
        pset.addPrimitive(np.tanh, 1)
        pset.addPrimitive(absolute, 1)
        pset.addPrimitive(negative, 1)
        pset.addPrimitive(negexp, 1)
        #pset.addEphemeralConstant("rand101", lambda: random.uniform(-1, 1))
        #pset.renameArguments(ARG0='x0',ARG1='x1', ARG2='x2', ARG3='x3', ARG4='x4', ARG5='x5', ARG6='x6', ARG7='x7',  ARG8='x8', ARG9='x9',  ARG10='x10',  ARG11='x11',  ARG12='x12')
        pset.renameArguments(ARG0='x0', ARG1='x1', ARG2='x2', ARG3='x3', ARG4='x4', ARG5='x5', ARG6='x6', ARG7='x7',
                             ARG8='x8', ARG9='x9', ARG10='x10', ARG11='x11', ARG12='x12', ARG13='x13', ARG14='x14',
                             ARG15='x15', ARG16='x16', ARG17='x17', ARG18='x18', ARG19='x19', ARG20='x20', ARG21='x21',
                             ARG22='x22', ARG23='x23', ARG24='x24')

        creator.create("Individual", gp.PrimitiveTree)

        toolbox = base.Toolbox()
        #toolbox.register("expr", gp.genFull, pset=pset, min_=1, max_=3)
        toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=6)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
        toolbox.register("compile", gp.compile, pset=pset)


        #Aqui pones el string que tienes del individuo.
        cade = str_ind

        #Esta linea convierte el string a individuo. Tienes que mandarle el conjunto de parametros
        expr1 = neat_gp.PrimitiveTree.from_string(cade, pset)
        return len(expr1)


c = convert()
#tokens = re.split("[ \t\n\r\f\v(),]", string)
test = c.cont("tanh(absolute(sub(sub(x0, sin(mysqrt(absolute(mypower2(sin(sub(x0, sin(sub(x0, mylog(absolute(cos(mylog(absolute(-0.5673465831480815)))))))))))))), mylog(safe_div(sin(sub(mypower2(sin(sub(x0, mylog(absolute(-0.5673465831480815))))), mylog(absolute(-0.5673465831480815)))), mylog(mypower2(cos(-0.5673465831480815))))))))")
#tokens = re.split("[ \t\n\r\f\v(),]", string)
#test = c.cont("mul(cos(power3(x6)),sub(sub(mul(mylog(x6 ),sqrt(x4)), x3), mul(tan(x1 ),safe_div(tan(x0), tan(x4)))))")

