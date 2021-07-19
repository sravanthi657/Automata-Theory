import json
import sys

if len(sys.argv)<=2:
    print("error: `python3 q<no>.py arg1 arg2` \n  \targ1: path to the input JSON file \n  \targ2: path to the output JSON file")
    exit(0)
with open(sys.argv[1]) as f:
    dfa = json.load(f)
minzdfa = {
    "states": [],
    "letters": dfa["letters"],
    "transition_function": [],
    "start_states": [],
    "final_states": [],
}

def setup(table,mapstates,tarr):
    for i in dfa["states"]:
        table[i] = dict()
        mapstates[i] = 0
        tarr[i] = dict()
    for i in dfa["transition_function"]:
        tarr[i[0]][i[1]] = i[2]
    for i in range(len(dfa["states"])):
        for j in range(len(dfa["states"])):
            table[dfa["states"][i]][dfa["states"][j]]= [0,i,j]
def inx(k,ar):
    return k in ar
def ninx(k,ar):
    return k not in ar
def modifi_table(table):
    for sta in dfa["states"]:
            for stb in dfa["states"]:
                t2=table[sta][stb][1]
                t3=table[sta][stb][2]
                t1=table[sta][stb][0]
                if sta!=stb:
                    if (( t2> t3) and ((inx(sta,dfa["final_states"]) and ninx(stb,dfa["final_states"])) or (ninx(sta,dfa["final_states"]) and inx(stb,dfa["final_states"])) or (t1==1) or (t1==1))):
                            table[sta][stb][0]=1
                    elif ((t2 < t3) and ((inx(sta,dfa["final_states"]) and ninx(stb,dfa["final_states"])) or (ninx(stb,dfa["final_states"]) and inx(sta,dfa["final_states"])) or (t1==1) or (t1==1))):                        
                            table[sta][stb][0]=1
   
def helper1(sta,stb,met,tarr,table):
    for symb in dfa["letters"]:
        if ((((tarr[sta][symb] in dfa["final_states"]) and (tarr[stb][symb] not in dfa["final_states"]))) or ((tarr[sta][symb] not in dfa["final_states"]) and (tarr[stb][symb] in dfa["final_states"])) or (table[tarr[sta][symb]][tarr[stb][symb]][0]==1) or (table[tarr[stb][symb]][tarr[sta][symb]][0]==1)):
            table[sta][stb][0]=1
            met = met + 1
    return met
def helper2(sta,stb,met,tarr,table):
    for symb in dfa["letters"]:
        if ((((tarr[sta][symb] in dfa["final_states"]) and (tarr[stb][symb] not in dfa["final_states"]))) or ((tarr[stb][symb] not in dfa["final_states"]) and (tarr[sta][symb] in dfa["final_states"])) or (table[tarr[sta][symb]][tarr[stb][symb]][0]==1) or (table[tarr[stb][symb]][tarr[sta][symb]][0]==1)):
            table[sta][stb][0]=1
            met = met + 1
    return met
def minModify(tarr,table):
    met = 0
    for sta in dfa["states"]:
        for stb in dfa["states"]:
            t2=table[sta][stb][1]
            t3=table[sta][stb][2]
            t1=table[sta][stb][0]
            if sta!=stb:
                if t2 > t3:
                    if table[sta][stb][0]!=1:
                        met=helper1(sta,stb,met,tarr,table)
                elif t2 < t3:
                    if table[stb][sta][0]!=1:
                        met=helper2(sta,stb,met,tarr,table)
    return met
def combine_cond(arrunset):
    cond,flg = 0,0
    setvar=set([])
    for i in range(len(arrunset)):
        temp,flg,i1,i2 = [],0,-1,-1
        for j in range(i+1,len(arrunset)):
            for k in range(len(arrunset[i])):
                arik=arrunset[i][k]
                for l in range(len(arrunset[j])):
                    arjl=arrunset[j][l]
                    if arik==arjl :
                        cond,flg,setvar = 1,1,set([])
                        setvar ={ m for m in  arrunset[i]}
                        setvar2={m for m in arrunset[j]}
                        setvar=setvar.union(setvar2)
                    if flg:
                        break
                if flg:
                    break
                    
            if flg:
                i1,i2 = i,j
                break
        if flg == 1:
            break
    return [flg,cond,setvar,i1,i2]
def combinestates(table):
    arr,arrunset,finalarr,temp = [],[],[],[]
    for i in dfa["states"]:
        for j in dfa["states"]:
            t3=table[i][j][2]
            t2=table[i][j][1]
            if t2 > t3:
                t1,temp=table[i][j][0],[]
                if t1 == 0:
                    temp.extend([i,j])
                    arr.append(temp)
                    arrunset.append(temp)
    cond = 1
    while cond !=0:
        flg,cond,setvar,i1,i2 = combine_cond(arrunset)
        if flg:
            vara,varb  = arrunset[i1],arrunset[i2]
            arrunset.remove(vara)
            arrunset.remove(varb)
            arrunset.append(list(setvar))
    
    
    for i in dfa["states"]:
        for j in dfa["states"]:
            t3=table[i][j][2]
            t2=table[i][j][1]
            if t3 < t2:
                t1=table[i][j][0]
                if t1 == 0:
                    mapstates[i],mapstates[j] = 1,1
    for i in arrunset:
        finalarr.append(i)
    for i in dfa["states"]:
        if mapstates[i] == 0:
            makelist = []
            makelist.append(i)
            finalarr.append(makelist)
    return finalarr

def  S_F_states(finalarr):
    new_finalstate,new_startstate = [],[]
    for i in finalarr:
        flg = 0
        for j in i:
            if ((j in dfa["final_states"]) and (i not in new_finalstate)):
                new_finalstate.append(i)
            if ((j in dfa["start_states"]) and (i not in new_startstate)):
                new_startstate.append(i)
            if flg :
                break
    minzdfa["start_states"]=new_startstate
    minzdfa["final_states"]=new_finalstate

def tsf(finalarr,transition,fin_tarr):
    for i in finalarr:
        ind=tuple(i)
        for j in i:
            for symb in dfa["letters"]:
                transfer,flg = transition[j][symb],0
                for k in finalarr:
                    for t in k:
                        if transfer in t:
                            fin_tarr[ind][symb] = k
                            break
    minzdfa["states"]=finalarr
table=dict()
mapstates=dict()
tarr=dict()
fin_tarr=dict()
setup(table,mapstates,tarr)
modifi_table(table)
met=1
while met:
    met=minModify(tarr,table)
finalarr = combinestates(table)
S_F_states(finalarr)
for i in finalarr:
    fin_tarr[tuple(i)] = {}
tsf(finalarr,tarr,fin_tarr)
for i in finalarr:
    temp = []
    for symb in dfa["letters"]:
        local,final = [],fin_tarr[tuple(i)][symb]
        local.extend([i,symb,final])
        temp.append(local)
        minzdfa["transition_function"].append(local)

with open(sys.argv[2], "w") as f:
    json.dump(minzdfa, f, indent=4)
