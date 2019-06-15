import sys


def readNetlist(file):
    nets = int(file.readline())
    inputs = file.readline().split()
    inputs.sort()
    outputs = file.readline().split()
    outputs.sort()

    # read mapping
    mapping = {}
    while True:
        line = file.readline().strip()
        if not line:
            break

        net, name = line.split()
        mapping[name] = int(net)

    # read gates
    gates = []
    for line in file.readlines():
        bits = line.split()
        gate = bits.pop(0)
        #ports = map(int, bits)
        ports = [int(port) for port in bits]
        gates.append((gate, ports))

    return inputs, outputs, mapping, gates


# read netlists
inputs1, outputs1, mapping1, gates1 = readNetlist(open(sys.argv[1], "r"))
inputs2, outputs2, mapping2, gates2 = readNetlist(open(sys.argv[2], "r"))

# add your code here!

#Goto Run>EditConfig to change file inputs


#Create 2 Databases
ITE1 = []
ITE2 = []
DB1 = {}
DB2 = {}

#Create ITE func
#Within ITE function call use Cofactors function.

def ite1(f,g,h):
    ITE1.append((f,g,h))
#    bdd1(f,g,h)
    if f is True:
        temp = g
        bdd1(temp)

    elif f is False:
        temp = h
        bdd1(temp)

    elif g == h:
        temp = g
        bdd1(temp)

    elif g is True and h is False:
        temp = f
        bdd1(temp)

    else:
        cofactors(f,g,h)

def ite2(f,g,h):
    ITE2.append((f,g,h))
#    bdd2(f,g,h)
    if f is True:
        temp = g
        bdd2(temp)

    elif f is False:
        temp = h
        bdd2(temp)

    elif g == h:
        temp = g
        bdd2(temp)

    elif g is True and h is False:
        temp = f
        bdd2(temp)

    else:
         cofactors(f, g, h)


#Create BDD func
#For bdds which have bdd as var, use ITE function call.
#for db in db.keys():
#accessing elements of db
#for a,b in db.items():
#accessing key and value

#db.get(bdd,0) :returns 0 if bdd is not in dict
#https://www.youtube.com/watch?v=JUxmCUlZoi8
def bdd1(f,g,h):

    if (g == h):
        return g

    else:
        if (f, g, h) in DB1:
            return f, g, h
        else:
            DB1[(f, g, h)] = (f, g, h)
            return 0

def bdd2(f,g,h):

    if(g == h):
        return g

    else:
        if (f,g,h) in DB2:
            return f, g, h
        else:
            DB2[(f, g, h)] = (f, g, h)
            return 0
#Create co factors func


def cofactors(f, g, h):
    return 0
#
#     if f in DB1:
#         dummy, f0, f1 = DB1[f]
#
#     if g in DB1:
#         dummy, g0, g1 = DB1[g]
#
#     if h in DB1:
#         dummy, h0, h1 = DB1[f]
#
#     bdd1(f0, g0, h0)
#     bdd1(f1, g1, h1)

#Go through all gates and create BDDs
def read_gates1(inputs1, outputs1, mapping1, gates1):

    # Call bdd function for all inputs
    for input in inputs1:
        bdd1(input,True,False)


    # gates_temp = [gate_x for (gate_x,port_x) in gates]
    # port_temp = [port_x for (gate_x,port_x) in gates]
    #def gatemap(gates.gate, inputs1[2])



    # for gate in gates:
    #     print(gate[0])
    #     print(gate[1])
    #     print(gate[1][0])
    for gate_s in gates1:

            # gate_s for (gate_s,port_s) in gates1 if gate_s != '':
        if gate_s[0] == 'and':
            ite1(gate_s[1][0], gate_s[1][1], False)
            #bdd of and gate
            # bdd1(gate_s[1][0], gate_s[1][1], False)
            #print('(port_temp[gate_s][0],port_temp[gate_s][1],0)')
            #How to access port?
            print('and')


        elif  gate_s[0] == 'or':
            ite1(gate_s[1][0], True, gate_s[1][1])
            # bdd of or gate
            # bbdd1(gate_s[1][0], True, gate_s[1][1])
            #DB.append((a,1,b))
            print('or')

        elif  gate_s[0] == 'inv':
            ite1(gate_s[1][0], False, True)
            # bdd of not gate
            # bdd1(gate_s[1][0], False, True)
            #DB.append((a,0,1))
            print('inv')

        elif gate_s[0] == 'xor':
            ite1(gate_s[1][0], (gate_s[1][1], False, True), (gate_s[1][1], True, False))
            # bdd of xor gate
            # bdd1(gate_s[1][0], (gate_s[1][1], False, True), (gate_s[1][1], True, False))
            #DB.append((a,(b,0,1),(b,1,0)))
            print('xor')

def read_gates2(inputs2, outputs2, mapping2, gates2):

    # Call bdd function for all inputs
    for input in inputs2:
        bdd2(input,True,False)

    for gate_s in gates2:

        if gate_s[0] == 'and':
            ite2(gate_s[1][0], gate_s[1][1], False)
            #bdd of and gate
            # bdd2(gate_s[1][0], gate_s[1][1], False)
            #print('(port_temp[gate_s][0],port_temp[gate_s][1],0)')
            #How to access port?
            print('and')


        elif  gate_s[0] == 'or':
            ite2(gate_s[1][0], True, gate_s[1][1])
            # bdd of or gate
            # bdd2(gate_s[1][0], True, gate_s[1][1])
            #DB.append((a,1,b))
            print('or')

        elif  gate_s[0] == 'inv':
            ite2(gate_s[1][0], False, True)
            # bdd of not gate
            # bdd2(gate_s[1][0], False, True)
            #DB.append((a,0,1))
            print('inv')

        elif gate_s[0] == 'xor':
            ite2(gate_s[1][0], (gate_s[1][1], False, True), (gate_s[1][1], True, False))
            # bdd of xor gate
            # bdd2(gate_s[1][0], (gate_s[1][1], False, True), (gate_s[1][1], True, False))
            #DB.append((a,(b,0,1),(b,1,0)))
            print('xor')

read_gates1(inputs1, outputs1, mapping1, gates1)
read_gates2(inputs2, outputs2, mapping2, gates2)
#Check bdd rules
bdd1('b', True, False)

print(DB1)
print(DB2)
print(ITE1)
print(ITE2)



#Compare the outputs1 and outputs2
#if you compare outputs with nets, may not match! Compare with variables
# for output in outputs:
#     if DB1[output] ==DB2[output]:
#         print('ok')
#     else:
#         print('not ok')
#

