import numpy as np
import yaml
from neatGPLS import ensure_dir
config        = yaml.load(open("conf/conf.yaml"))
def random_floats(low, high, size):
    return [np.random.uniform(low, high) for _ in xrange(size)]

low=0
high=1
size=20
problem=config["problem"]
num_v=config["num_var"]
num_p=config["n_problem"]
num_corr=int(config["run_end"])-int(config["run_begin"])+1

d = './data_corridas/%s/' % (problem)
ensure_dir(d)

for n_corr in range(1,num_corr):
    samples = random_floats(low,high,size)
    np.savetxt('./data_corridas/%s/train_%d_%d.txt'%(problem,num_p, n_corr),samples,delimiter=',')

for n_corr in range(1, num_corr):
    samples = random_floats(low, high, size)
    np.savetxt('./data_corridas/%s/test_%d_%d.txt' % (problem, num_p, n_corr), samples, delimiter=',')