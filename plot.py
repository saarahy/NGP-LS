import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.legend_handler import HandlerLine2D
from matplotlib import colors as mcolors
from my_operators import safe_div, mylog, mypower2, mypower3, mysqrt
from operator import add, sub, mul
from numpy import sin, tan, cos, tanh, asarray, array
import csv
#directory='PierrickData22'
directory='Engine3'
#id_number=22
#name='patient1.csv'
#name='data_engine_delayed.csv'
name='train_10125_1.txt'
#name='LooTrain0.txt'
direccion="./data_corridas/Engine3/%s"%(name)
datos_x0=list()
datos_x1=list()
datos_y=list()
soluciones=list()
aptitud=list()
with open(direccion) as spambase:
    spamReader = csv.reader(spambase,  delimiter=',', skipinitialspace=False)
    for row in spamReader:
          datos_x0.append(float(row[0]))
          datos_x1.append(float(row[1]))
          datos_y.append(float(row[2]))
#print datos_x
#print datos_y

direccion2="./Engine3/data_min.txt"
with open(direccion2) as spambase:
    spamReader = csv.reader(spambase,  delimiter=';', skipinitialspace=False)
    for row in spamReader:
        if row!=[]:
          aptitud.append(float(str(round(float(row[2]),4))))
          soluciones.append(row[3])

data_save = []
def f1(x0, x1,soluciones): #neat-GP-LS neat-cx
    data_save.append(eval(soluciones[0]))
    return eval(soluciones[0])
        #( -0.0761271041432+(1.02740569219*(1.03230000973*sin((1.08298943136*mypower2((1.48210014838*tanh((0.848365007676*((0.831833272197*((0.816663211963*tan((1.09679734743*mypower2((1.01855459792*cos((0.824814137784*((0.819724629441*mysqrt((0.912215387816*((1.21287819779*((1.21646575703*safe_div((1.21646586662*tan((1.33162809574*x0))),(0.727406626443*((1.10678749263*0.0072188738240202)+(0.552492950003*x0)))))+(0.995311711743*((0.995311498524*tanh((0.99573199271*0.3144124528547403)))*(0.995329863212*tan((0.889792319857*x0)))))))+(0.82701511239*x0)))))-(1.00717109048*((0.935738402436*((1.1004653473*x0)-(0.826658801183*0.8079620242135872)))-(1.06195882185*((1.17416005179*-0.7866760625277252)+(0.875890742844*x0)))))))))))))-(1.36658148587*((0.389185009363*mysqrt((0.757329601481*((-0.637308551876*0.8170259759945775)+(1.09620553813*x0)))))-(1.56110854635*0.298983274862731)))))*(0.726629578039*mysqrt((0.598596750718*x0)))))))))))))
        #(0.477531795381+(0.780248680079*(-0.670603543862*cos((39.1404274404*mylog((3.5781628264*((4.15196405592*sin((0.231521719825*tanh((-0.554778873027*x0)))))+(0.0244766786864*((1.07338336566*((1.65501629247*((1.65655977208*mysqrt((1.48369001757*0.6964399313009428)))*(1.64709233114*((0.0335343080799*x0)+(2.05957973029*((3.13191488634*tanh((-3.872647815*safe_div((-3.87299276604*-0.5566328854900306),(3.20875991817*x0)))))-(0.0333287826495*cos((8.52062456569*cos((1.28012381436*x0)))))))))))+(0.0780811385369*-0.44699669945380704)))-(0.816294475322*tan((-0.183838741048*0.4745393623931202)))))))))))))

# def f2(x0, soluciones): #neat-GP-LS sub-cx
#     return eval(soluciones[1])
#     #(-0.22826115416+(1.03337422978*(1.03010733484*mypower2((1.06140383126*((1.05892678937*cos((0.850476228648*tanh((1.00405208557*sin((1.01937078261*tanh((1.15085353566*sin((0.918535459898*((1.01310778999*mypower2((1.02747128451*mylog((1.25694449105*((1.25694444796*sin((1.14158519074*tanh((0.948696713312*x0)))))*(1.25694451822*((1.25694445922*((1.0*mysqrt((1.0*mypower3((1.0*-0.7034515998091746)))))-(1.25694445775*((1.25694464996*mysqrt((1.13530877324*0.4407630643852565)))*(1.25694445766*((1.25694453489*-0.12031532013441892)*(1.25694453124*x0)))))))*(1.25694449408*tanh((1.65131804185*-0.4919469068738478)))))))))))-(0.905024182961*((1.00502118685*((0.932252524795*((0.932252524061*((0.670537043176*tanh((0.803320345055*0.9310926750236095)))-(1.20001975553*tan((1.00110424308*x0)))))*(0.932252674726*((0.932252684753*tanh((0.943541878983*0.5361463166781837)))*(0.93225255909*((0.977134501336*sin((0.977261573386*mypower2((0.954231963085*mylog((1.05603077354*mypower3((1.1632833293*0.7297650800528548)))))))))+(0.955990298348*mylog((0.910659444291*mylog((0.987406306336*mypower3((0.96233806198*mylog((0.981455570777*x0)))))))))))))))+(1.0683405834*-0.12031532013441892)))-(0.899753297904*((0.899754326946*((1.0*mysqrt((1.0*mypower3((1.0*-0.7034515998091746)))))-(0.899754025606*((0.899753686254*mysqrt((0.951135468776*0.4407630643852565)))*(0.899753746567*((0.899754073413*-0.12031532013441892)*(0.899754151583*x0)))))))*(0.89975361449*tanh((0.931771387434*((0.931771037617*tanh((1.00047914275*x0)))*(0.931771398108*mysqrt((0.966460091047*0.7220172409489254)))))))))))))))))))))))*(1.06136180442*sin((1.64991756452*mylog((1.58130418859*((1.69429101197*tanh((1.56244643829*-0.4919469068738478)))+(0.811157175576*((0.369120622653*x0)+(1.23282509281*-0.2562376790774876)))))))))))))))
#         #(-0.0654612081332+(1.03401317534*(1.0318053369*mypower2((1.10978268154*tanh((1.03309957576*mypower2((1.16689676854*cos((2.05341104802*tanh((3.61548191735*mylog((0.216922262144*((0.112211646525*sin((4.36364555242*sin((0.979156350622*sin((0.846132308291*x0)))))))-(1.1451623118*mysqrt((1.03773208345*x0)))))))))))))))))))
#
# def f3(x0, soluciones):
#     return eval(soluciones[2])
#     # sin(mypower3(mysqrt(mysqrt(safe_div(mul(mypower2(mysqrt(mypower3(mypower3(mysqrt(mypower3(sin(mylog(x0)))))))), mysqrt(mylog(x0))), 0.45539649740621724)))))
#         #mypower2(mysqrt(sin(add(mypower3(mypower3(0.30899127844295204)), sin(sub(mul(0.5551064362586127, -0.9438254262210319), mysqrt(x0)))))))
#
# def f4(x0, soluciones):
#     return eval(soluciones[3])
#     #mysqrt(mypower3(sin(mylog(mypower3(safe_div(add(safe_div(sub(x0, sin(mul(-0.5651506197132945, x0))), cos(0.19190074600463114)), cos(add(tan(mul(x0, 0.19190074600463114)), -0.061221103402531174))), -0.061221103402531174))))))
#         #mul(tanh(mypower3(mul(add(mul(cos(tanh(add(mypower3(safe_div(-0.6110502801523747, -0.414938063367555)), sin(add(add(-0.6110502801523747, x0), mypower3(0.8565422444914368)))))), x0), mul(x0, -0.3426307293351998)), cos(mylog(x0))))), tanh(mypower3(mylog(sub(mysqrt(mysqrt(add(x0, x0))), x0)))))


d_x=asarray(datos_x0)
# datos_x1=asarray(datos_x1)
# datos_y1=asarray(datos_y)
import numpy as np
# from cycler import cycler
# time=np.arange(250000)
# plt.rc('lines', linewidth=4)
# plt.rc('lines', prop_cycle=(cycler('color', ['r', 'g']) +
#                             cycler('linestyle', ['-', '--'])))
# line1,=plt.plot(time,datos_y1,'ro',label='Original data', c='tomato')
#strng=
# line2,=plt.plot(time, f1(d_x, datos_x1, soluciones), 'ro', label='neat-GP-LS neat-cx (%s)' % aptitud[0],c='wheat')
# line3,=plt.plot(d_x, f2(d_x, soluciones), linestyle='--',label='neat-GP-LS sub-cx (%s)' % aptitud[1])
# line4,=plt.plot(d_x, f3(d_x, soluciones), label='neat-GP sub-cx (%s)' % aptitud[2])
# line5,=plt.plot(d_x, f4(d_x, soluciones), label='neat-GP neat-cx (%s)'% aptitud[3])

vec_y1=f1(asarray(datos_x0),asarray(datos_x1), soluciones)

result = np.sum((vec_y1 - datos_y)**2)
print np.sqrt(result/len(datos_y)),

np.savetxt('./Engine3/data_vector.csv', vec_y1, delimiter=",", fmt="%s")

# plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)}, loc=4)
#plt.annotate(aptitud[0], xy=(time[-1]-30000, f1(d_x[-1], datos_x1[-1], soluciones)+0.3), color=line2.get_color(), size=13)
# plt.annotate(aptitud[1], xy=(d_x[-1], f2(d_x[-1], soluciones)-0.03), color=line3.get_color(), size=13)
# plt.annotate(aptitud[2], xy=(d_x[-1], f3(d_x[-1], soluciones)), color=line4.get_color(), size=13)
# plt.annotate(aptitud[3], xy=(d_x[-1], f4(d_x[-1], soluciones)), color=line5.get_color(), size=13)


# plt.title('data_engine.csv', size=20)
# plt.xlabel('Time', size=20)
# plt.ylabel('Model output', size=20)
# plt.grid()
# plt.show()
