import csv
from neatGPLS import ensure_dir

def get_data(directory, index_, out):
    data=list()
    #data2=list()
    for i in range(1,2):
        direccion="./Results/%s/bestind_LStr_%d_%d.txt"%(directory,index_,i)
        with open(direccion) as spambase:
            spamReader = csv.reader(spambase,  delimiter=';', skipinitialspace=False)
            cont=1
            for row in spamReader:
                if row != []:
                    cont=cont+1
            cont2 = 1#cont
            cont = 0
        direccion = "./Results/%s/bestind_LStr_%d_%d.txt" % (directory, index_, i)
        with open(direccion) as spambase:
            spamReader2 = csv.reader(spambase, delimiter=';', skipinitialspace=False)
            for row2 in spamReader2:
                if row2 != [] and cont==cont2:
                    data.append(row2[1])
                    #data.append(row2[2])
                cont = cont + 1

    print min(data)
    num = data.index(min(data))+1
    print num

    direccion3="./Results/%s/bestind_LStr_%d_%d.txt"%(directory,index_,num)
    with open(direccion3) as spambase:
        spamReader = csv.reader(spambase, delimiter=';', skipinitialspace=False)
        cont = 0
        for row in spamReader:
            if row != []:
                cont = cont + 1
    with open(direccion3) as spambase:
        spamReader = csv.reader(spambase,  delimiter=';', skipinitialspace=False)
        for row in spamReader:
            if row != [] and row[0]==str(cont):
                #data2.append([num, row[2]])
                print row[2]
                out.write('\n%d;%s;%s;%s' % (index_, num, min(data), row[2]))


d = './Engine3/data_min.txt'
ensure_dir(d)
out = open(d, 'a')
directory = "Engine3"
#for i in (1101):
i = 10121
get_data(directory, i, out)
