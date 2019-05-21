import scipy.stats
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.legend_handler import HandlerLine2D
from my_operators import safe_div, mylog, mypower2, mypower3, mysqrt, absolute, negative
from operator import add, sub, mul
from numpy import sin, tan, cos, tanh, asarray, array, arange
import csv

from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
#rcParams['font.sans-serif'] = ['Tahoma']


# Nombre del directorio donde se encuentran mis archivos
directory='Vibraciones'

#  Nombre de los archivos de donde obtenemos los datos
name='DB05_4.csv'
name_='train_5004_23.txt'
name_test='test_5004_23.txt'

# Direcciones de donde se encuentran localizados los archivos previos
direccion="./data_corridas/%s/%s"%(directory,name)
direccion_="./data_corridas/%s/%s"%(directory,name_)
direccion_test="./data_corridas/%s/%s"%(directory,name_test)

# Creacion de listas para almacenar y posteriormente plotear la grafica
datos_x0=list()
datos_x3=list()
datos_x4=list()
datos_x5=list()
datos_x6=list()
datos_x7=list()
datos_x8=list()
datos_x9=list()
datos_x17=list()
datos_y=list()
datos_x0_=list()
datos_x3_=list()
datos_x4_=list()
datos_x5_=list()
datos_x6_=list()
datos_x7_=list()
datos_x9_=list()
datos_x8_=list()
datos_x17_=list()
datos_y_=list()
datos_x0_test=list()
datos_x3_test=list()
datos_x4_test=list()
datos_x5_test=list()
datos_x6_test=list()
datos_x7_test=list()
datos_x8_test=list()
datos_x9_test=list()
datos_x17_test=list()
datos_y_test=list()
soluciones=list()
aptitud=list()

# Abrir los distintos archivos para almacenar la informacion en las listas
with open(direccion) as spambase:
    spamReader = csv.reader(spambase,  delimiter=',', skipinitialspace=False)
    for row in spamReader:
          datos_x0.append(float(row[0]))
          datos_x3.append(float(row[3]))
          datos_x4.append(float(row[4]))
          datos_x5.append(float(row[5]))
          datos_x6.append(float(row[6]))
          datos_x7.append(float(row[7]))
          datos_x8.append(float(row[8]))
          datos_x9.append(float(row[9]))
          datos_x17.append(float(row[17]))
          datos_y.append(float(row[64]))
with open(direccion_) as spambase:
    spamReader = csv.reader(spambase, delimiter=',', skipinitialspace=False)
    for row in spamReader:
        datos_x0_.append(float(row[0]))
        datos_x3_.append(float(row[3]))
        datos_x4_.append(float(row[4]))
        datos_x5_.append(float(row[5]))
        datos_x6_.append(float(row[6]))
        datos_x7_.append(float(row[7]))
        datos_x8_.append(float(row[8]))
        datos_x9_.append(float(row[9]))
        datos_x17_.append(float(row[17]))
        datos_y_.append(float(row[64]))
with open(direccion_test) as spambase:
    spamReader = csv.reader(spambase, delimiter=',', skipinitialspace=False)
    for row in spamReader:
        datos_x0_test.append(float(row[0]))
        datos_x3_test.append(float(row[3]))
        datos_x4_test.append(float(row[4]))
        datos_x5_test.append(float(row[5]))
        datos_x6_test.append(float(row[6]))
        datos_x7_test.append(float(row[7]))
        datos_x8_test.append(float(row[8]))
        datos_x9_test.append(float(row[9]))
        datos_x17_test.append(float(row[17]))
        datos_y_test.append(float(row[64]))

# Funcion para evaluar el individuo deseado
# Unicamente copiar y pegar el string del individuo
def f1(x0, x3, x4, x5, x6, x7, x8, x9, x17):
    #DB05 4
    return eval('(5.667004544013222+(-0.7029684282742611*(4.08041647409489*tanh((4.103058788080642*((0.2537926496551309*((-0.11987389631876491*((-2.393258097156068*x5)-(-8.278182652900979*sin((-0.986702707271094*((0.4703773478789691*x5)-(-7.311826368859693*sin((3.612115923593579*sin((-7.471674861858324*mylog((1.7449226087032266*((-2.9821321372068947*x6)-(-2.3339204874914983*x5)))))))))))))))*(0.11996621976142278*((1.1664432373806368*x5)-(-7.205559736954689*sin((4.135767563667238*sin((-3.751058553252889*mylog((3.427020521355692*((-4.331129328800915*x6)-(1.4310642959704458*((-3.8410279271695607*mysqrt((2.7387410416543996*x6)))-(3.5170918062581067*x6)))))))))))))))-(0.24439610646499454*((-0.22079149612248114*((0.625719793082738*x5)-(-2.3847318877680457*negative((1.4532525125750313*((-5.656101782845092*x6)-(-0.6165083738532093*mysqrt((3.3713760908604016*x6)))))))))*(-0.22548631181766415*((1.242903420502672*((-1.2898997393222023*((0.40507697888649463*x5)-(-1.336526757150619*mylog((-0.03972048384540919*x3)))))*(-1.2796290104492833*((0.4890509687480614*x5)-(-7.311805223135024*sin((3.5084912371633092*sin((-3.2850276464613852*mylog((1.817058918645404*((-2.390159065518245*x6)-(2.3268602346969858*((-4.4196548407551655*mysqrt((3.14545046262026*x6)))-(0.24732905696598162*((-0.17735287148916357*((0.379187149438553*x5)-(-8.274712100748358*sin((0.9881878763162143*x6)))))*(-0.20893747530575701*((1.298423339126998*x5)-(1.3050080750671844*mysqrt((1.1519688743242336*mylog((5.411923240620122*mylog((-3.6476154225775144*x6)))))))))))))))))))))))))-(-7.065784563999727*sin((5.9723043339340665*sin((-3.254021935594174*mylog((3.7884916589333733*((-4.5347017429847565*x6)-(1.2207442134901452*((-3.958413527725648*mysqrt((2.821648492979301*x6)))-(0.37131088882860663*((-0.3147357880169654*((0.11084245283771878*x5)-(-8.296782126155932*sin((2.454814621838861*x6)))))*(-0.33718531694376797*((1.3519478270841525*x5)-(-7.075027352068455*sin((2.880475439520795*sin((-3.2932637954760837*mylog((3.300515647382317*((3.3494301958533157*x6)-(1.4481197422135275*((-4.102441946718701*mysqrt((2.970301509586276*x6)))-(0.673285604831982*x6)))))))))))))))))))))))))))))))))))')
    #DB05 3
    #return eval('(4.084471075487996+(0.6841452994735014*(1.3948802394077242*((1.535076301593911*cos((4.109106393814951*cos((1.469510422266446*cos((-2.5528052037979*cos((1.8564105906779362*cos((-2.590384655808487*cos((1.8790268070631706*cos((-1.26577730656485*cos((-3.190475681232311*mylog((-0.4417277933673267*x4)))))))))))))))))))+(3.433559723528826*tanh((2.09763028415879*sin((2.791748734423277*tanh((0.0004647874163999356*x7)))))))))))')
    #DB05 2
    #corrida 10
    #return eval('(6.346146235029693+(-1.1195698251095612*(-1.851054749987239*sin((3.5073483727423054*negative((-3.433565640327848*mylog((-1.6498520791888995*mylog((0.07603487986219085*mylog((-0.6071633571299084*mylog((-0.13463314990400427*mylog((0.0025013454087226944*x7)))))))))))))))))')
    #corrida 14
    #return eval('(3.715425495539672+(2.317727019374994*(2.317642820700489*mysqrt((1.664663468079458*mylog((1.8464689387706268*((3.475601601839058*mylog((0.2621762636227686*((9.141461063378088*sin((2.53525137921812*mylog((1.4558872168958088*mylog((1.320261867519665*((2.9504514595567652*x5)+(-0.20136393755706475*x5)))))))))+(0.5013206971769213*((-1.6838543809858726*cos((1.4724092346606252*((-11.55804764181868*mylog((3.1812351518255952*sin((-4.795567841765331*x6)))))+(2.96944353983902*sin((4.412998884594957*negative((4.356481827230582*mylog((-5.121528414401795*((0.5406872544364962*x5)+(-7.440892101796221*sin((-0.14155869797917264*x5)))))))))))))))+(0.9928236136042858*cos((2.739078764955872*((2.8193458240945786*((2.8264849201315543*x5)+(3.228272781634312*cos((1.0572981975179028*negative((-11.821880844550815*mylog((0.2689526862421609*x5)))))))))+(3.872160784089117*sin((-4.6668051087001725*sin((0.31191692712079566*x8)))))))))))))))+(-0.5533601729813381*cos((1.8703062721877461*((-11.873467672843832*mylog((-3.967869543027806*sin((0.3558949006837107*x8)))))+(0.7377812890330144*((0.8064367727967767*((-1.1731859850007957*cos((2.262225638195032*((-0.12786522537796607*x5)+(5.082165512260551*sin((1.9166057266247642*cos((2.64675154642179*((-0.3569028306725813*x5)+(3.871996054831353*sin((-4.552993717941499*sin((0.2936623154766057*x8)))))))))))))))+(1.2516912235762643*cos((2.742615798347593*((-0.16566696758720303*x5)+(3.9430852584178506*sin((-4.808392552523442*sin((0.18450524638479537*x8)))))))))))+(1.730534636493207*cos((-0.7895546490084001*cos((1.0497864903340106*x8)))))))))))))))))))')
    #corrida 23
    #return eval('(4.568337986132945+(1.9469326980010258*(-1.3198941744166413*tanh((-4.506551692470262*((-7.701794536821616*mylog((-0.23539254390720293*((-6.460867464232812*mylog((0.19031942019864934*tanh((4.489672774328686*((3.944393560321334*absolute((2.4328844714493747*tanh((3.042382411353075*tanh((2.819446460255401*tanh((-0.30831230997920883*((-6.4541477284969*mylog((0.8141736841210022*tanh((4.590017376563373*((3.979190129552309*absolute((2.4842134620649987*tanh((-0.0393236224758582*x7)))))-(3.2144095469183864*x9)))))))-(0.25744215207756443*cos((3.140716290813789*x9)))))))))))))-(3.114874025846635*x9)))))))-(0.3852966084575941*cos((-4.524147298644425*mylog((1.2763746832400669*cos((3.7562778440903295*mylog((0.10560251472403595*x0)))))))))))))-(-0.0033625316086855974*x7)))))))')
    #DB05 1
    #corrida 26
    #return eval('(4.1153137583359785+(-1.5025545635550832*(2.27340130315149*sin((2.503668728985887*mylog((112.08993540238241*mylog((-0.9772260805376617*mylog((24.640813976491895*mylog((42.921224097956504*x0)))))))))))))')
    #corrida 24
    #return eval('(-22.125717789461003+(8.649432724355668*(8.668756713863054*cos((1.2229442705684703*((-1.395057876946113*cos((0.8473010328241576*cos((-1.5010971333516758*((0.1041851988702618*((-1.0116603349635294*cos((3.2926765928035366*cos((1.0765577309152536*((-1.247607988456013*cos((3.5098496009557585*cos((-3.6798114335816123*((-0.9539980268183248*((-0.4334360997644155*cos((3.5960861002900244*cos((-2.2155870119521492*((-2.75074007533662*cos((-101.8837864103075*x0)))-(-1.6794436231081094*sin((-1.208511867857092*x6)))))))))-(-2.858045598732016*sin((-79.58065078808694*x0)))))-(-4.043891982246664*sin((1.9910998468449292*sin((-1.0863955992186733*mysqrt((12.456543035598596*x0)))))))))))))-(-2.0174391882677685*sin((-1.640722027132485*sin((12.576626182732307*x0)))))))))))-(-2.5467781351103342*sin((-0.1785566561953307*((1.3487438781848662*cos((-1.5548787054009834*x6)))-(2.0813914126926627*sin((3.3834240386778296*x6)))))))))-(-2.3749986959469616*sin((1.5989013537365049*sin((-1.526643355496477*mysqrt((12.519933679607545*x0)))))))))))))-(-2.650351753190927*sin((-0.028636603266624282*((1.3399574251582929*((-0.3021751023127227*cos((3.5555618143528953*cos((-2.4631046846683318*((-0.2569955929749845*cos((-3.4263302265340814*((-4.031859455321255*cos((-1.4786757394950394*cos((0.6634069886931745*cos((-1.455144256829399*((-2.8808187963332768*cos((-85.61481848357745*x0)))-(0.31231491841403114*sin((-3.591638510922045*mysqrt((-2.569586799203569*cos((-90.51504443847243*x0)))))))))))))))-(-0.3719406225152639*sin((2.5410677553369636*sin((4.664876734033632*x6)))))))))-(-3.096979892344788*sin((0.27036648854013584*sin((-1.5254355857708388*((0.11224630323264756*((3.376446398356375*cos((-1.266629112174954*x6)))-(-4.086948046974647*((2.917138747101331*mysqrt((2.1359615013091457*sin((5.94052180903821*sin((-81.83356632690048*x0)))))))-(-2.4533880939560158*sin((1.2581362146709811*x6)))))))-(0.2524359799017055*sin((0.7777779827176817*sin((2.6492751090683155*sin((4.816598612864789*x6)))))))))))))))))))-(-3.0388863465048415*sin((0.04688894098152822*((2.0054968224553718*cos((-1.7647026545470432*x6)))-(2.2676905490527095*sin((3.1963636913773272*x6)))))))))-(1.8213115706850815*sin((-0.15304604885196518*cos((4.197443805540469*cos((-3.378956274076204*((-1.9568618168022442*cos((-3.9818086857605266*((-4.488816724291763*cos((-1.4272091179397375*cos((0.3211142281157919*cos((-1.2657377878456118*((-2.753610491753787*cos((-83.05087315410344*x0)))-(0.5503808277520829*sin((-3.6578063340517013*mysqrt((-2.615861847429114*cos((-89.83738095259262*x0)))))))))))))))-(-0.6089438233010314*sin((0.1246157771017883*sin((3.2650346771060694*x6)))))))))-(-3.3455865311782222*sin((0.7914107392460786*sin((-1.4975586135305348*((0.06586936620296716*((2.537650912896283*cos((1.0233953375765867*cos((2.284863077844796*sin((0.763405977413204*x17)))))))-(-4.656068778565014*((3.1298021512514174*mysqrt((2.281519700137882*sin((5.60042467405026*sin((-82.22889069990715*x0)))))))-(-3.1103078640188397*sin((0.6385527209025934*x6)))))))-(-0.051885854019126404*sin((2.141517458541925*sin((-4.005170464132046*sin((1.9166172856245633*sin((-0.9288155541263042*mysqrt((12.4501091730472*x0)))))))))))))))))))))))))))))))))))')
    #corrida 4
    #return eval('(-11.44170453445937+(1.9506268150505344*(2.3533681821942993*((0.3332639010404149*mylog((4.488482215373239*((15.3260867484336*sin((3.9811346347854504*sin((0.37534036479296107*tan((7.5520047708647855*((1.5745530735481086*sin((0.052908832136063705*mylog((-0.42925010878936853*mylog((4.8002512849255154*((4.6403291191593965*((14.628895104651997*sin((4.382973481081042*x5)))+(-8.166927399353856*x0)))+(11.139685049222019*sin((4.730619404297667*x0)))))))))))+(9.275285306938978*x0)))))))))+(2.843421650793249*x5)))))+(3.5753425666677563*sin((0.8816560205084281*tan((11.154148778883002*sin((4.764530526763361*x0)))))))))))')

# Convertir la lista en numpy array para plotear los datos
# Esta parte puede ser optimizada.
d_x0=asarray(datos_x0)
d_x3=asarray(datos_x3)
d_x4=asarray(datos_x4)
d_x5=asarray(datos_x5)
d_x6=asarray(datos_x6)
d_x7=asarray(datos_x7)
d_x8=asarray(datos_x8)
d_x9=asarray(datos_x9)
d_x17=asarray(datos_x17)
d_y=asarray(datos_y)
d_train_x0=asarray(datos_x0_)
d_train_x3=asarray(datos_x3_)
d_train_x4=asarray(datos_x4_)
d_train_x5=asarray(datos_x5_)
d_train_x6=asarray(datos_x6_)
d_train_x7=asarray(datos_x7_)
d_train_x8=asarray(datos_x8_)
d_train_x9=asarray(datos_x9_)
d_train_x17=asarray(datos_x17_)
d_train_y=asarray(datos_y_)
d_test_x0=asarray(datos_x0_test)
d_test_x3=asarray(datos_x3_test)
d_test_x4=asarray(datos_x4_test)
d_test_x5=asarray(datos_x5_test)
d_test_x6=asarray(datos_x6_test)
d_test_x7=asarray(datos_x7_test)
d_test_x8=asarray(datos_x8_test)
d_test_x9=asarray(datos_x9_test)
d_test_x17=asarray(datos_x17_test)
d_test_y=asarray(datos_y_test)

# primera grafica, ploteo del modelo
# line1,=plt.plot(d_x0,datos_y, label='Target', color= 'blue',linewidth=3.0)
# line2,=plt.plot(d_x0, f1(d_x0, d_x5), linestyle='--',label='Model', color='red')
# plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)}, loc=1, prop={'size': 13})
# plt.annotate('',xy=(d_x0[-1], f1(d_x0[-1])), color=line2.get_color(), size=30)
# plt.yticks(arange(0, 40, step=10), fontweight='bold', size=13)
# plt.xticks(fontweight='bold', size=13)
# plt.ylabel('Vibrations', size=20, fontweight='bold')
# plt.xlabel('Speed (RPM)', size=20, fontweight='bold')
# #plt.grid()
# plt.show()

# Segunda grafica - correlacion
plt.title("DB05_4 ind_c_23")
colors = (0,0,0)
plt.scatter(f1(d_x0, d_x3,  d_x4, d_x5, d_x6, d_x7, d_x8, d_x9, d_x17),d_y, c=colors, alpha=0.5, s=7)
plt.yticks(arange(0, 25, step=5), fontweight='bold', size=13)
plt.xticks(arange(0, 25, step=5),fontweight='bold', size=13)
plt.ylabel('Target output', size=20, fontweight='bold')
plt.xlabel('Model output', size=20, fontweight='bold')
plt.show()

# pearson corr
print scipy.stats.pearsonr(f1(d_x0, d_x3, d_x4, d_x5, d_x6, d_x7, d_x8, d_x9, d_x17), d_y)
print scipy.stats.pearsonr(f1(d_train_x0, d_train_x3, d_train_x4, d_train_x5, d_train_x6, d_train_x7, d_train_x9, d_train_x8,  d_train_x17), d_train_y)
print scipy.stats.pearsonr(f1(d_test_x0, d_test_x3, d_test_x4, d_test_x5, d_test_x6, d_test_x7, d_test_x8, d_test_x9, d_test_x17), d_test_y)