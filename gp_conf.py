import copy
import random
import re
import sys
import warnings
import numpy as np
import operator
import funcEval
from collections import defaultdict, deque
from functools import partial, wraps
from inspect import isclass
from operator import eq, lt
from neat_gp import *
from deap import gp
from measure_tree import level_data
######################################
# GP Data structure                  #
######################################
import threading
# Define the name of type for any types.
__type__ = object
class IdGenerator(object):
    def __init__(self):
        self.cur_id = 1
        self.lock = threading.Lock()
    def next_id(self):
        with self.lock:
            result = self.cur_id
            self.cur_id += 1
        return result

newId = IdGenerator()

class PrimitiveTree(gp.PrimitiveTree, neat):
    """Tree spefically formated for optimization of genetic
    programming operations. The tree is represented with a
    list where the nodes are appended in a depth-first order.
    The nodes appended to the tree are required to
    have an attribute *arity* which defines the arity of the
    primitive. An arity of 0 is expected from terminals nodes.
    """

    def __init__(self, content):
        list.__init__(self, content)

        self.id = newId.next_id()
        self.tspecie = None
        self.descendent = None
        self.fitness_h = None
        self.nspecie = None
        self.LS_prob = None
        self.params = None
        self.best_ind = None
        self.ls_ind = None
        self.ls_fitness = None
        self.ls_story = None
        self.off_cx = None
        self.off_mut = None
        self.repr_bin = None
        self.level_bin = None
        self.node_feat = None
        self.intracluster = None
        self.parent_ = None


    def __deepcopy__(self, memo):
        new = self.__class__(self)
        new.__dict__.update(copy.deepcopy(self.__dict__, memo))
        return new

    def __setitem__(self, key, val):
        # Check for most common errors
        # Does NOT check for STGP constraints
        if isinstance(key, slice):
            if key.start >= len(self):
                raise IndexError("Invalid slice object (try to assign a %s"
                    " in a tree of size %d). Even if this is allowed by the"
                    " list object slice setter, this should not be done in"
                    " the PrimitiveTree context, as this may lead to an"
                    " unpredictable behavior for searchSubtree or evaluate."
                     % (key, len(self)))
            total = val[0].arity
            for node in val[1:]:
                total += node.arity - 1
            if total != 0:
                raise ValueError("Invalid slice assignation : insertion of"
                    " an incomplete subtree is not allowed in PrimitiveTree."
                    " A tree is defined as incomplete when some nodes cannot"
                    " be mapped to any position in the tree, considering the"
                    " primitives' arity. For instance, the tree [sub, 4, 5,"
                    " 6] is incomplete if the arity of sub is 2, because it"
                    " would produce an orphan node (the 6).")
        elif val.arity != self[key].arity:
            raise ValueError("Invalid node replacement with a node of a"
                             " different arity.")
        list.__setitem__(self, key, val)

    def __str__(self):
        """Return the expression in a human readable string.
        """
        string = ""
        stack = []
        for node in self:
            stack.append((node, []))
            while len(stack[-1][1]) == stack[-1][0].arity:
                prim, args = stack.pop()
                string = prim.format(*args)
                if len(stack) == 0:
                    break   # If stack is empty, all nodes should have been seen
                stack[-1][1].append(string)

        return string

    @classmethod
    def from_string(cls, string, pset):
        """Try to convert a string expression into a PrimitiveTree given a
        PrimitiveSet *pset*. The primitive set needs to contain every primitive
        present in the expression.

        :param string: String representation of a Python expression.
        :param pset: Primitive set from which primitives are selected.
        :returns: PrimitiveTree populated with the deserialized primitives.
        """
        tokens = re.split("[ \t\n\r\f\v(),]", string)
        expr = []
        ret_types = deque()
        for token in tokens:
            if token == '':
                continue
            if len(ret_types) != 0:
                type_ = ret_types.popleft()
            else:
                type_ = None

            if token in pset.mapping:
                primitive = pset.mapping[token]

                if len(ret_types) != 0 and primitive.ret != type_:
                    raise TypeError("Primitive {} return type {} does not "
                                    "match the expected one: {}."
                                    .format(primitive, primitive.ret, type_))

                expr.append(primitive)
                if isinstance(primitive, Primitive):
                    ret_types.extendleft(reversed(primitive.args))
            else:
                try:
                    token = eval(token)
                except NameError:
                    raise TypeError("Unable to evaluate terminal: {}.".format(token))

                if type_ is None:
                    type_ = type(token)

                if type(token) != type_:
                    raise TypeError("Terminal {} type {} does not "
                                    "match the expected one: {}."
                                    .format(token, type(token), type_))

                expr.append(Terminal(token, False, type_))
        return cls(expr)

    def set_id(self):
        self.set_id_(newId.next_id())

    @property
    def root(self):
        """Root of the tree, the element 0 of the list.
        """
        return self[0]

    def searchSubtree(self, begin):
        """Return a slice object that corresponds to the
        range of values that defines the subtree which has the
        element with index *begin* as its root.
        """
        end = begin + 1
        total = self[begin].arity
        while total > 0:
            total += self[end].arity - 1
            end += 1
        return slice(begin, end)


class Primitive(object):
    """Class that encapsulates a primitive and when called with arguments it
    returns the Python code to call the primitive with the arguments.

        >>> pr = Primitive("mul", (int, int), int)
        >>> pr.format(1, 2)
        'mul(1, 2)'
    """
    __slots__ = ('name', 'arity', 'args', 'ret', 'seq')
    def __init__(self, name, args, ret):
        self.name = name
        self.arity = len(args)
        self.args = args
        self.ret = ret
        args = ", ".join(map("{{{0}}}".format, range(self.arity)))
        self.seq = "{name}({args})".format(name=self.name, args=args)

    def format(self, *args):
        return self.seq.format(*args)

class Terminal(object):
    """Class that encapsulates terminal primitive in expression. Terminals can
    be values or 0-arity functions.
    """
    __slots__ = ('name', 'value', 'ret', 'conv_fct')
    def __init__(self, terminal, symbolic, ret):
        self.ret = ret
        self.value = terminal
        self.name = str(terminal)
        self.conv_fct = str if symbolic else repr

    @property
    def arity(self):
        return 0

    def format(self):
        return self.conv_fct(self.value)

def cxSubtree(ind1, ind2):
    """Randomly select in each individual and exchange each subtree with the
    point as root between each individual.

    :param ind1: First tree participating in the crossover.
    :param ind2: Second tree participating in the crossover.
    :returns: A tuple of two trees.
    """
    if len(ind1) < 2 or len(ind2) < 2:
        # No crossover on single node tree
        return ind1, ind2

    # List all available primitive types in each individual
    types1 = defaultdict(list)
    types2 = defaultdict(list)
    if ind1.root.ret == __type__:
        # Not STGP optimization
        types1[__type__] = xrange(1, len(ind1))
        types2[__type__] = xrange(1, len(ind2))
        common_types = [__type__]
    else:
        for idx, node in enumerate(ind1[1:], 1):
            types1[node.ret].append(idx)
        for idx, node in enumerate(ind2[1:], 1):
            types2[node.ret].append(idx)
    tree1_types = set(types1.keys())
    tree2_types = set(types2.keys())

    #if len(common_types) > 0:
    type1_ = random.choice(list(tree1_types))
    type2_ = random.choice(list(tree2_types))
    index1 = random.choice(types1[type1_])
    index2 = random.choice(types2[type2_])
    slice1 = ind1.searchSubtree(index1)
    slice2 = ind2.searchSubtree(index2)

    if funcEval.LS_flag:
        a=slice1.start
        b=slice1.stop
        c=slice2.start
        d=slice2.stop
        params1=ind1.get_params()
        params2=ind2.get_params()
        params1=params1.tolist()
        params2=params2.tolist()
        temp_p=params1[a+2:b+2]
        params1[a+2:b+2]=params2[c+2:d+2]
        params2[c+2:d+2]=temp_p
        params1=np.asarray(params1)
        params2=np.asarray(params2)
        ind1.params_set(params1)
        ind2.params_set(params2)
    ind1[slice1], ind2[slice2] = ind2[slice2], ind1[slice1]

    return ind1, ind2


def cxOnePoint(ind1, ind2):
    """Randomly select in each individual and exchange each subtree with the
    point as root between each individual.

    :param ind1: First tree participating in the crossover.
    :param ind2: Second tree participating in the crossover.
    :returns: A tuple of two trees.
    """
    if len(ind1) < 2 or len(ind2) < 2:
        # No crossover on single node tree
        return ind1, ind2

    # List all available primitive types in each individual
    types1 = defaultdict(list)
    types2 = defaultdict(list)
    if ind1.root.ret == __type__:
        # Not STGP optimization
        types1[__type__] = xrange(1, len(ind1))
        types2[__type__] = xrange(1, len(ind2))
        common_types = [__type__]
    else:
        for idx, node in enumerate(ind1[1:], 1):
            types1[node.ret].append(idx)
        for idx, node in enumerate(ind2[1:], 1):
            types2[node.ret].append(idx)
        common_types = set(types1.keys()).intersection(set(types2.keys()))

    if len(common_types) > 0:
        type_ = random.choice(list(common_types))
        index1 = random.choice(types1[type_])
        index2 = random.choice(types2[type_])
        slice1 = ind1.searchSubtree(index1)
        slice2 = ind2.searchSubtree(index2)

        if funcEval.LS_flag:
            a=slice1.start
            b=slice1.stop
            c=slice2.start
            d=slice2.stop
            params1=ind1.get_params()
            params2=ind2.get_params()
            params1=params1.tolist()
            params2=params2.tolist()
            temp_p=params1[a+2:b+2]
            params1[a+2:b+2]=params2[c+2:d+2]
            params2[c+2:d+2]=temp_p
            params1=np.asarray(params1)
            params2=np.asarray(params2)
            ind1.params_set(params1)
            ind2.params_set(params2)
        ind1[slice1], ind2[slice2] = ind2[slice2], ind1[slice1]

    return ind1, ind2

def mutUniform(individual, expr, pset):
    """Randomly select a point in the tree *individual*, then replace the
    subtree at that point as a root by the expression generated using method
    :func:`expr`.

    :param individual: The tree to be mutated.
    :param expr: A function object that can generate an expression when
                 called.
    :returns: A tuple of one tree.
    """
    index = random.randrange(len(individual))
    slice_ = individual.searchSubtree(index)
    type_ = individual[index].ret
    xp = expr(pset=pset, type_=type_)
    if funcEval.LS_flag:
            a=slice_.start
            b=slice_.stop
            params1=individual.get_params()
            params1=params1.tolist()
            params2=np.ones(len(xp))
            params1[a+2:b+2]=params2
            params1=np.asarray(params1)
            individual.params_set(params1)
    individual[slice_] = xp #expr(pset=pset, type_=type_)
    return individual,
