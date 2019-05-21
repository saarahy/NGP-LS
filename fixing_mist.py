import csv
import numpy as np
import converting
num_p=4310
n_corr_max=10#11
problem='Yacht'



# for i in range(1,2):
#     direccion='./Results/wastewater/pop_file_%d_%d.txt'%(num_p,i)
#     with open(direccion) as spambase:
#         spamReader = csv.reader(spambase, delimiter=';', skipinitialspace=True)
#         for row in spamReader:
#             print ', '.join(row)
#

# for n_corr in range(30,n_corr_max+1):
#     print 'corrida:', n_corr
#     direccion='./Results/Housing2/pop_file_%d_%d.txt'%(num_p,n_corr)
#     with open(direccion, 'r') as f:
#         data = f.read().splitlines()
#         Matrix = list()#np.zeros([200100, 2]) #np.empty([200000, 2])#np.empty([100100, 2]) #np.empty([200000, 2])
#         contador=1
#         cont=0
#         c = converting.convert()
#         for line in data:
#             if line=='':
#                 print 'null'
#             else:
#                 strg=line.split(";")
#                 if strg[0] == '0':
#                     Matrix.append([strg[0],c.cont(strg[2])])
#                     #Matrix[cont,0]=strg[0]
#                     #Matrix[cont, 1] = c.cont(strg[2])
#                 else:
#                     Matrix.append([strg[0], c.cont(strg[6])])
#                     #Matrix[cont, 0] = strg[0]
#                     #Matrix[cont, 1] = c.cont(strg[6])
#         np.savetxt('./data_graph/%s/%s_%d_%d.txt' % (problem, problem,num_p, n_corr), Matrix, delimiter=",", fmt="%s")


for n_corr in range(1,n_corr_max+1):
    print 'corrida:', n_corr
    direccion = '/media/treelab/84DF-9E7F/Datos/Results/Yacht/pop_file_%d_%d.txt' % (num_p, n_corr)
    #direccion='./Results/wastewater/pop_file_%d_%d.txt'%(num_p,n_corr)
    with open(direccion, 'r') as f:
        data = f.read().splitlines()
        print len(data)

        # cont=0
        # for i in range(202000,len(data)):
        #     print cont,i,data[i]
        #     cont+=1

        Matrix =  np.zeros([210000, 2])#np.empty([200000, 2]) #np.empty([100100, 2])
        contador=1
        cont=0
        c = converting.convert()
        for line in range(0,len(data)-1):
            if data[line]=='':
                print 'null'
            else:
                if '----------------------------------------' in data[line]:
                    contador+=1
                    #print 'cont:',contador
                else:
                    strg = data[line].split(";")
                    #if len(strg) < 3:
                    if contador==1:
                        #print 'no'
                        #strg=line.split(";")
                        #print c.cont(strg[1])
                        Matrix[cont,0]=contador
                        #print strg[1]
                        Matrix[cont, 1] = c.cont(strg[1])
                        cont+=1
                    else:
                        #c = converting.convert()
                            # print c.cont(strg[1])
                            Matrix[cont, 0] = contador
                            #print strg[5]
                            try:
                                #print strg[5]
                                Matrix[cont, 1] = c.cont(strg[5])
                                cont += 1
                            except IndexError:
                                print strg
                                #print Matrix[cont-1]
                                #print(cont+contador)
                                Matrix[cont, 1]=123.
                                cont = cont + 1

        #print 'lineas',cont
        #np.savetxt('./data_graph/%s/%s_%d_%d.txt' % (problem, problem,num_p, n_corr), Matrix, delimiter=",", fmt="%s")
        np.savetxt('/media/treelab/84DF-9E7F/archivos_graficas/GraficasConvergenciaNGPLS_1/data_graph/%s/%s_%d_%d.txt' % (problem, problem, num_p, n_corr), Matrix, delimiter=",", fmt="%s")