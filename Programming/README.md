# Programming Assignment | Automata Theory 
## Roll.No: 2019101101
### One drive link for the q1,q2,q4 submission :
> https://iiitaphyd-my.sharepoint.com/:v:/g/personal/stella_sravanthi_students_iiit_ac_in/EQ_zuJA9fz9Nh-jI7i9ZTd0Bec2YDT_wao0vSpDF9MNFHw?e=t7trMv

#### Question1: **Regular expression to NFA**

* Firstly after loading the regular expression simplifying that on inserting '.' for normal multiplication.
> for i in range(len(rgx["regex"])):
    if i+1<len(rgx["regex"]):
        temp+=rgx["regex"][i]
        if rgx["regex"][i]!='(' and rgx["regex"][i+1]!=')':
            if rgx["regex"][i]!='+'and rgx["regex"][i+1]!='+' and rgx["regex"][i+1]!='*':
                temp+='.'
temp+=rgx["regex"][len(rgx["regex"])-1]
* To make the expression constant for all, convert the given expression into postfix. 
> def infix_to_postfix(infix,postfix):
    stack ,postfix  = [],[]
    for ch in infix:
        prior_arr={ "+":1,".":2,"*":3}
        if ch in prior_arr:
            prior_check(ch,stack,postfix,prior_arr)
        elif ch in ["(", ")"]:
            clos_ope_check(ch,stack,postfix)              
        else:
            postfix.append(ch)
    crct_exp=reversed(stack)
    for elem in crct_exp:
        if elem in prior_arr:
            postfix.extend(elem)
    postfix=''.join(postfix)
    return postfix
* Now to construct the NFA fill the states and transition function **tsf()** that returns transition function array, no.of states in NFA, start an end states respectively.
* tsf mainly invloves solving the expression using characters of it, operators includes star,union and concaternation .
> def getstates(ts):
    return ["Q"+str(i) for i in range(ts+1)]
  def getletters(spce):
    return [i for i in keys if i!="e"]
- finally filled the nfa
> nfa["transition_function"],total_states,start,end=tsf()
  nfa["states"]=getstates(total_states)
  nfa["letters"]=getletters(keys)
  nfa["start_states"]=["Q"+str(start)]
  nfa["final_states"]=["Q"+str(end)]
    with open(sys.argv[2], "w") as f:
        json.dump(nfa, f, indent=4)


#### Question2: **Converting NFA to DFA**
* Firstly we know the start state and alphabets remain same for both autmata. Thats why I've set the varaibles in the beginning.
> with open(sys.argv[1]) as f:
    nfa = json.load(f)
    nfa["final_states"] = set(nfa["final_states"])
* used in getting final states of dfa for intersection of set purpose.
* Initialised empty list for states,transition function and final states as they differ in each other.
> dfa = {
    "states": [],
    "letters": nfa["letters"],
    "transition_function": [],
    "start_states": [nfa["start_states"]],
    "final_states": [],
}

### **dfa states**
* DFA may have up to 2 power n states (n is number if states in nfa) so created the power set on considering the possbile combinations of nfa states for all i from 1 to len(iterable) .
> def powerset(iterable):
    return chain.from_iterable(combinations(convo(iterable), leng) for leng in range(len(convo(iterable)) + 1)) #from empty state to total elements all possible combinations 
>def dstates():
    dfa_stateSets=powerset(nfa["states"])
    for pstate_arr in dfa_stateSets:
        dfa["states"].append(convo(pstate_arr)) 
* Every element  in powerset is considered as dfa state and appended to dfa["states"]
### **transition function**
> def fun_tsf():
    whole_tsf=[]
    for originS_arr in dfa["states"]:
        for symb in dfa["letters"]:
            newS_arr=set_next_state(originS_arr,symb)
            whole_tsf.append([originS_arr, symb, newS_arr])
    dfa["transition_function"]=whole_tsf
* Every state in state array is mapped to respective letter and searched in  nfa transitons, if mappedd then append to get a single transition 
>  new_state=tsf[2] if tsf[0]==ostate and tsf[1]==symb and tsf[2] not in newS_arr else -100
            if(new_state!=-100):
                newS_arr.append(new_state)
    *refer def set_next_state(originS_arr,symb):*
### **final states**
> def get_finS(pstate_arr):
    dfa_finS=[]
    if nfa["final_states"] & set(pstate_arr):
        dfa["final_states"].append(convo(pstate_arr))
* for every lement in powerset we check for finalstates of nfa
* DFA state q is a final state if q ∩ F is not equal to ∅, where F is the set of NFA final states.
-> Thus printed the final output is resulted
> with open(sys.argv[2], "w") as f:
    json.dump(dfa, f, indent=4)
