import numpy as np
import yaml
from neatGPLS import ensure_dir
config        = yaml.load(open("conf/conf.yaml"))
def random_floats(low, high, size):
    return [np.random.uniform(low, high) for _ in xrange(size)]

low=-1
high=1
size=20

low_test=-1
high_test=1
size_test=20

problem=config["problem"]
num_v=config["num_var"]
num_p=config["n_problem"]
num_corr=int(config["run_end"])-int(config["run_begin"])+1

d = './data_corridas/%s/' % (problem)
ensure_dir(d)

for n_corr in range(1,num_corr):
    np.savetxt('./data_corridas/%s/train_%d_%d.txt'%(problem,num_p, n_corr), np.vstack( [np.random.uniform(low, high) for _ in xrange(size)] for i in range(num_v) ).T, delimiter=",")
    #np.savetxt('./data_corridas/%s/train_%d_%d.txt'%(problem,num_p, n_corr),samples,delimiter=',')

for n_corr in range(1, num_corr):
    np.savetxt('./data_corridas/%s/test_%d_%d.txt' % (problem, num_p, n_corr),
               np.vstack([np.random.uniform(low, high) for _ in xrange(size)] for i in range(num_v)).T, delimiter=",")