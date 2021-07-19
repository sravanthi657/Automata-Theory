import sys
import json
import re
with open(sys.argv[1]) as f:
    rgx= json.load(f)
nfa = {
    "states": [],
    "letters": [],
    "transition_function": [],
    "start_states": [],
    "final_states": [],
}
def prior_check(ch,stack,postfix,prior_arr):
    if stack !=[]:
        while stack[-1] in prior_arr and prior_arr[stack[-1]] >= prior_arr[ch]:
            postfix.append(stack.pop())
            if len(stack)==0:
                break
    stack.append(ch)
def clos_ope_check(ch,stack,postfix):
    if ch == ")":
        ite=0
        while stack[-1]!="(":
            postfix.append(stack.pop())
            ite+=1
        if(ite==0):
            print(" opening '(' not found")
        stack.pop()
    else:
        stack.append(ch)
def infix_to_postfix(infix,postfix):
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
def help_equal(x,y,y_to):
	if x==y:
		return y_to 
	else:
		return -200
	
def help_or_equal(x,y,z,yz_to):
	if x==y or x==z:
		return yz_to
	else:
		return -200
def allot(y):
    return y
def tsf():
    s,stack,start,end,count,originS,newS,new_tsf=[],[],0,1,-1,0,0,[]
    for i in postfix:
        if i in keys:
            originS,newS=count+1,count+2
            count+=2
            stack.append([originS,newS])
            s.extend([{},{}])
            s[originS][i]=newS
            lis=["Q"+str(originS),i,"Q"+str(newS)]
            new_tsf.append(lis)
        elif i=='*':

            originS,newS=count+1,count+2
            firsT,secT=stack.pop()
            stack.append([originS,newS])
            s.extend([{},{}])
            s[secT]['e']=(firsT,newS);s[originS]['e']=(firsT,newS)
            new_tsf.extend([["Q"+str(secT),'$',"Q"+str(firsT)],["Q"+str(secT),'$',"Q"+str(newS)], ["Q"+str(originS),'$',"Q"+str(firsT)], ["Q"+str(originS),'$',"Q"+str(newS)]])
            res=help_equal(start,firsT,originS)
            if(res!=-200):start=res
            res=help_equal(end,secT,newS)
            if(res!=-200):end=res
            count+=2 
        elif i=='.':

            firsT,secT=stack.pop(),stack.pop()
            s[secT[1]]['e']=firsT[0]
            stack.append([secT[0],firsT[1]])
            new_tsf.append(["Q"+str(secT[1]),"$","Q"+str(firsT[0])])
            res=help_equal(start,firsT[0],secT[0])
            if(res!=-200):start=res 
            res=help_equal(end,secT[1],firsT[1])
            if(res!=-200):end=res

        elif i=='+':

            originS,newS=count+1,count+2
            firsT,secT=stack.pop(),stack.pop()
            stack.append([originS,newS])
            s.extend([{},{}])
            s[originS]['e']=allot((secT[0],firsT[0]))
            s[firsT[1]]['e'],s[secT[1]]['e']= allot(newS),allot(newS)
            new_tsf.extend([["Q"+str(originS),"$","Q"+str(secT[0])],["Q"+str(originS),"$","Q"+str(firsT[0])], ["Q"+str(firsT[1]),"$","Q"+str(newS)], ["Q"+str(secT[1]),"$","Q"+str(newS)]])
            res=help_or_equal(start,firsT[0],secT[0],originS)
            if(res!=-200):start=res
            res= help_or_equal(end,secT[1],firsT[1],newS )
            if(res!=-200):end=res
            count+=2
    return [new_tsf,count,start,end]
def getstates(ts):
    return ["Q"+str(i) for i in range(ts+1)]
def getletters(spce):
    return [i for i in keys if i!="e"]
        
temp,postfix="",""

for i in range(len(rgx["regex"])):
    if i+1<len(rgx["regex"]):
        temp+=rgx["regex"][i]
        if rgx["regex"][i]!='(' and rgx["regex"][i+1]!=')':
            if rgx["regex"][i]!='+'and rgx["regex"][i+1]!='+' and rgx["regex"][i+1]!='*':
                temp+='.'
temp+=rgx["regex"][len(rgx["regex"])-1]
easy_regx,keys=temp,list(set(re.sub('[^A-Za-z0-9]+', '', temp)+'e'))
#regx postfix
postfix =infix_to_postfix(easy_regx,postfix)

nfa["transition_function"],total_states,start,end=tsf()
nfa["states"]=getstates(total_states)
nfa["letters"]=getletters(keys)
nfa["start_states"]=["Q"+str(start)]
nfa["final_states"]=["Q"+str(end)]
with open(sys.argv[2], "w") as f:
    json.dump(nfa, f, indent=4)