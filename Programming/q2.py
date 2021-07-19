import json
import sys
from itertools import chain, combinations

if len(sys.argv)<=2:
    print("error: `python3 q<no>.py arg1 arg2` \n  \targ1: path to the input JSON file \n  \targ2: path to the output JSON file")
    exit(0)

with open(sys.argv[1]) as f:
    nfa = json.load(f)
    nfa["final_states"] = set(nfa["final_states"])

dfa = {
    "states": [],
    "letters": nfa["letters"],
    "transition_function": [],
    "start_states": [nfa["start_states"]],
    "final_states": [],
}
def convo(x):
    return list(x)
def powerset(iterable):
    return chain.from_iterable(combinations(convo(iterable), leng) for leng in range(len(convo(iterable)) + 1)) #from empty state to total elements all possible combinations 
def set_next_state(originS_arr,symb):
    newS_arr=[]
    for ostate in originS_arr:
        for tsf in nfa["transition_function"]:
            new_state=tsf[2] if tsf[0]==ostate and tsf[1]==symb and tsf[2] not in newS_arr else -100
            if(new_state!=-100):
                newS_arr.append(new_state)
    newS_arr=sorted(newS_arr)
    return newS_arr
def get_finS(pstate_arr):
    dfa_finS=[]
    if nfa["final_states"] & set(pstate_arr):
        dfa["final_states"].append(convo(pstate_arr))
def dstates():
    dfa_stateSets=powerset(nfa["states"])
    for pstate_arr in dfa_stateSets:
        dfa["states"].append(convo(pstate_arr)) 
        get_finS(pstate_arr)
def fun_tsf():
    whole_tsf=[]
    for originS_arr in dfa["states"]:
        for symb in dfa["letters"]:
            newS_arr=set_next_state(originS_arr,symb)
            whole_tsf.append([originS_arr, symb, newS_arr])
    dfa["transition_function"]=whole_tsf

dstates()
fun_tsf()
with open(sys.argv[2], "w") as f:
    json.dump(dfa, f, indent=4)
