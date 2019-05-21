import numpy as np
import csv
from conf_primitives import vector_benchmarks


def get_address(p, n, problem, direccion, benchmark_flag):
    flag = True
    try:
        direccion=direccion % (problem,p,n)
    except:
        flag = False
        direccion = direccion % (problem,n)
    if flag:
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
                        print 'Line {r} is corrupt' , r
                        break
            if benchmark_flag:
                xdata = Matrix[:num_r]
                ydata = vector_benchmarks(problem, xdata)
            else:
                xdata = Matrix[:num_r - 1]
                ydata = Matrix[num_r-1]
        return xdata, ydata
    else:
        with open(direccion) as spambase:
            spamReader = csv.reader(spambase, delimiter=' ', skipinitialspace=True)
            num_c = sum(1 for line in open(direccion))
            num_r = len(next(csv.reader(open(direccion), delimiter=' ', skipinitialspace=True)))
            Matrix = np.empty((num_r, num_c,))
            for row, c in zip(spamReader, range(num_c)):
                for r in range(num_r):
                    try:
                        Matrix[r, c] = row[r]
                    except ValueError:
                        print 'Line {r} is corrupt', r
                        break
            if benchmark_flag:
                xdata = Matrix[:num_r]
                ydata = vector_benchmarks(problem, xdata)
            else:
                xdata = Matrix[:num_r - 1]
                ydata = Matrix[num_r - 1]
        return xdata, ydata
