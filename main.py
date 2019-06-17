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
ITE1 = {}
ITE2 = {}
DB1 = {}
DB2 = {}

#Create ITE func
#Within ITE function call use Cofactors function.

def ite1(f,g,h):
    #    bdd1(f,g,h)
    if f is True:
        return g

    elif f is False:
        return h

    elif g == h:
        return g

    elif g is True and h is False:
        return f

    else:
        cofactors1(f,inputs1[0])

def ite2(f,g,h):
    #    bdd2(f,g,h)
    if f is True:
        return g

    elif f is False:
        return h

    elif g == h:
        return g

    elif g is True and h is False:
        return f

    else:
         cofactors2(f,inputs2[0])


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
            return DB1[(f,g,h)]
        else:
            DB1[(f, g, h)] = (f, g, h)
            return DB1[(f,g,h)]

def bdd2(f,g,h):

    if(g == h):
        return g

    else:
        if (f, g, h) in DB2:
            return DB2[(f,g,h)]
        else:
            DB2[(f, g, h)] = (f, g, h)
            return DB2[(f,g,h)]

#Create co factors func

def cofactors1(f, x):
    if f is True:
        return (True,True)
    elif f is False:
        return (False,False)
    else:
        tempf = f[0]
        if tempf[0] == x:
            return (tempf[1],tempf[2])
        elif f[0] > x:
            return (f[0],f[0])
        else:
            f1_1,f1_0 = cofactors1(f[1],x)
            f0_1,f0_0 = cofactors1(f[2],x)
            bddf1 = bdd1(x,f1_1,f0_1)
            bddf0 = bdd1(x,f1_0,f0_0)
            return (bddf1,bddf0)

def cofactors2(f, x):
    if f is True:
        return (True,True)
    elif f is False:
        return (False,False)
    else:
        if f[0] == x:
            return (f[1],f[2])
        elif f[0] > x:
            return (f[0],f[0])
        else:
            f1_1,f1_0 = cofactors2(f[1],x)
            f0_1,f0_0 = cofactors2(f[2],x)
            bddf1 = bdd2(x,f1_1,f0_1)
            bddf0 = bdd2(x,f1_0,f0_0)
            return (bddf1,bddf0)

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

signal_bdd_relation1 = {}
signal_bdd_relation2 = {}

#Go through all gates and create BDDs
def read_gates1(inputs1, outputs1, mapping1, gates1):

    # Call bdd function for all inputs
    for input in inputs1:
        bdd = bdd1(input,True,False)
        signal_number = mapping1[input]
        signal_bdd_relation1[signal_number] = bdd

    # gates_temp = [gate_x for (gate_x,port_x) in gates]
    # port_temp = [port_x for (gate_x,port_x) in gates]
    #def gatemap(gates.gate, inputs1[2])

    for gate_s in gates1:

            # gate_s for (gate_s,port_s) in gates1 if gate_s != '':
        if gate_s[0] == 'and':
            if gate_s[1][0] not in signal_bdd_relation1 or gate_s[1][1] not in signal_bdd_relation1:
                continue
            signal_bdd_relation1[gate_s[1][2]] = ite1(gate_s[1][0], gate_s[1][1], False)
            print('and')

        elif gate_s[0] == 'or':
            if gate_s[1][0] not in signal_bdd_relation1 or gate_s[1][1] not in signal_bdd_relation1:
                continue
            signal_bdd_relation1[gate_s[1][2]] = ite1(gate_s[1][0], True, gate_s[1][1])
            print('or')

        elif gate_s[0] == 'inv':
            if gate_s[1][0] not in signal_bdd_relation1:
                continue
            signal_bdd_relation1[gate_s[1][1]] = ite1(gate_s[1][0], False, True)
            print('inv')

        elif gate_s[0] == 'xor':
            if gate_s[1][0] not in signal_bdd_relation1 or gate_s[1][1] not in signal_bdd_relation1:
                continue
            signal_bdd_relation1[gate_s[1][2]] = ite1(gate_s[1][0], (gate_s[1][1], False, True), (gate_s[1][1], True, False))
            print('xor')

def read_gates2(inputs2, outputs2, mapping2, gates2):

    # Call bdd function for all inputs
    for input in inputs2:
        bdd = bdd2(input, True, False)
        signal_number = mapping2[input]
        signal_bdd_relation2[signal_number] = bdd

        # gates_temp = [gate_x for (gate_x,port_x) in gates]
        # port_temp = [port_x for (gate_x,port_x) in gates]
        # def gatemap(gates.gate, inputs1[2])

    for gate_s in gates2:

        # gate_s for (gate_s,port_s) in gates1 if gate_s != '':
        if gate_s[0] == 'and':
            if gate_s[1][0] not in signal_bdd_relation2 or gate_s[1][1] not in signal_bdd_relation2:
                continue
            signal_bdd_relation2[gate_s[1][2]] = ite2(gate_s[1][0], gate_s[1][1], False)
            print('and')

        elif gate_s[0] == 'or':
            if gate_s[1][0] not in signal_bdd_relation2 or gate_s[1][1] not in signal_bdd_relation2:
                continue
            signal_bdd_relation2[gate_s[1][2]] = ite2(gate_s[1][0], True, gate_s[1][1])
            print('or')

        elif gate_s[0] == 'inv':
            if gate_s[1][0] not in signal_bdd_relation2:
                continue
            signal_bdd_relation2[gate_s[1][1]] = ite2(gate_s[1][0], False, True)
            print('inv')

        elif gate_s[0] == 'xor':
            if gate_s[1][0] not in signal_bdd_relation2 or gate_s[1][1] not in signal_bdd_relation2:
                continue
            signal_bdd_relation2[gate_s[1][2]] = ite2(gate_s[1][0], (gate_s[1][1], False, True), (gate_s[1][1], True, False))
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

