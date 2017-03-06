import csv
import numpy as np
import converting
num_p=5210
n_corr_max=11#11
problem='Housing'
# for i in range(1,2):
#     direccion='./Results/wastewater/pop_file_%d_%d.txt'%(num_p,i)
#     with open(direccion) as spambase:
#         spamReader = csv.reader(spambase, delimiter=';', skipinitialspace=True)
#         for row in spamReader:
#             print ', '.join(row)
#
for n_corr in range(1,n_corr_max):
    print 'corrida:', n_corr
    direccion='./Results/Housing/pop_file_%d_%d.txt'%(num_p,n_corr)
    with open(direccion, 'r') as f:
        data = f.read().splitlines()
        Matrix = np.zeros([200100, 2]) #np.empty([200000, 2])#np.empty([100100, 2]) #np.empty([200000, 2])
        contador=1
        cont=0
        c = converting.convert()
        for line in data:
            if line=='':
                print 'null'
            else:
                if line=='----------------------------------------' or '----------------------------------------' in line:
                    contador+=1
                    print contador
                else:
                    if contador==1:
                        strg=line.split(";")
                        #print c.cont(strg[1])
                        Matrix[cont,0]=contador
                        Matrix[cont, 1] = c.cont(strg[1])
                        cont+=1
                    else:
                        c = converting.convert()
                        strg = line.split(";")
                        # print c.cont(strg[1])
                        Matrix[cont, 0] = contador
                        try:
                            Matrix[cont, 1] = c.cont(strg[5])
                            cont += 1
                        except IndexError:
                            print len(data),strg
                            np.savetxt('./data_graph/%s/%s_%d_%d.txt' % (problem, problem, num_p, n_corr), Matrix,
                                       delimiter=",", fmt="%s")
                            break
        np.savetxt('./data_graph/%s/%s_%d_%d.txt' % (problem, problem,num_p, n_corr), Matrix, delimiter=",", fmt="%s")
# for n_corr in range(9,n_corr_max):
#     print 'corrida:', n_corr
#     direccion='./Results/wastewater/pop_file_%d_%d.txt'%(num_p,n_corr)
#     with open(direccion, 'r') as f:
#         data = f.read().splitlines()
#         print len(data)
#
#         # cont=0
#         # for i in range(202000,len(data)):
#         #     print cont,i,data[i]
#         #     cont+=1
#
#         Matrix =  np.zeros([100000, 2])#np.empty([200000, 2]) #np.empty([100100, 2])
#         contador=1
#         cont=0
#         c = converting.convert()
#         for line in range(202000,len(data)-1):
#             if data[line]=='':
#                 print 'null'
#             else:
#                 if '----------------------------------------' in data[line]:
#                     contador+=1
#                     print 'cont:',contador
#                 else:
#                     strg = data[line].split(";")
#                     #if len(strg) < 3:
#                     if contador==1:
#                         #print 'no'
#                         #strg=line.split(";")
#                         #print c.cont(strg[1])
#                         Matrix[cont,0]=contador
#                         Matrix[cont, 1] = c.cont(strg[1])
#                         cont+=1
#                     else:
#                         #c = converting.convert()
#                             # print c.cont(strg[1])
#                             Matrix[cont, 0] = contador
#                             #print strg[5]
#                             try:
#                                 print strg
#                                 Matrix[cont, 1] = c.cont(strg[2])
#                                 cont += 1
#                             except IndexError:
#                                 print strg
#                                 print Matrix[cont-1]
#                                 print(cont+contador)
#                                 Matrix[cont, 1]=123.
#                                 cont = cont + 1
#
#         #print 'lineas',cont
#         np.savetxt('./data_graph/%s/%s_%d_%d.txt' % (problem, problem,num_p, n_corr), Matrix, delimiter=",", fmt="%s")