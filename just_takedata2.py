import csv
from neatGPLS import ensure_dir

def get_data(directory, index_, out):
    data=list()
    #data2=list()
    for i in range(1,14):
        direccion="./Results/%s/bestind_LStr_%d_%d.txt"%(directory,index_,i)
        with open(direccion) as spambase:
            spamReader = csv.reader(spambase,  delimiter=';', skipinitialspace=False)
            for row in spamReader:
                if row != [] and row[0]=='100':
                    data.append(row[1])

    print min(data)
    num=data.index(min(data))+1
    print num

    direccion2="./Results/%s/bestind_LStr_%d_%d.txt"%(directory,index_,num)
    with open(direccion2) as spambase:
        spamReader = csv.reader(spambase,  delimiter=';', skipinitialspace=False)
        for row in spamReader:
            if row != [] and row[0]=='100':
                #data2.append([num, row[2]])
                print row[2]
                out.write('\n%d;%s;%s;%s' % (index_, num, min(data), row[2]))


    #print data2


d = './data_pierrick/data_24.txt'
ensure_dir(d)
out = open(d, 'a')
directory = "PierrickData24"
for i in (1110,1010,1000,1100):
    get_data(directory,i, out)
