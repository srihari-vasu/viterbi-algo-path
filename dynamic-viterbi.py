from collections import defaultdict
import numpy as np
from math import log

def viterbi_algorithm(State_File, Symbol_File, Query_File):
    with open(State_File) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    States = content[1:int(content[0])+1]
    State_trans = [[int(x) for x in i.split(' ')] for i in content[int(content[0])+1:]]
    with open(Symbol_File) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    Symbols = content[1:int(content[0])+1]
    Symbol_trans = [[int(x) for x in i.split(' ')] for i in content[int(content[0])+1:]]
    with open(Query_File) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    Querries = []
    for i in range(len(content)):
        A = []
        a = 0
        #print(content[i])
        for j in range(len(content[i])):
            if content[i][j]==',' or content[i][j] == '(' or content[i][j] == ')' or content[i][j] == '/' or content[i][j] == '-' or content[i][j] == '&' or content[i][j] == ' ':
                if content[i][a:j] != '':
                    A.append(content[i][a:j].strip())
                    if content[i][j] != ' ':
                        A.append(content[i][j])
                    a = j + 1
        if content[i][a:] != '':
            A.append(content[i][a:])
        Querries.append(A)
    Querries_symb = []
    for i in range(len(Querries)):
        A = []
        for j in range(len(Querries[i])):
            if Querries[i][j] in Symbols:
                A.append(Symbols.index(Querries[i][j]))
            else:
                A.append(-1)
        Querries_symb.append(A)

    states_n = len(States)
    symbols_n = len(Symbols)
    States_n = [0] * states_n
    States_n_pair = defaultdict(int)
    for i in range(len(State_trans)):
        States_n[State_trans[i][0]] += State_trans[i][2]
        States_n_pair[(State_trans[i][0],State_trans[i][1])] = State_trans[i][2]
    Symbols_n = [0] * states_n
    Symbols_n_pair = defaultdict(int)
    for i in range(len(Symbol_trans)):
        Symbols_n[Symbol_trans[i][0]] += Symbol_trans[i][2]
        Symbols_n_pair[(Symbol_trans[i][0],Symbol_trans[i][1])] = Symbol_trans[i][2]

    gate = States.index('BEGIN')
    final = []
    for i in Querries_symb:
        path_a = [[gate] for _ in range(states_n-2)]
        path_b = list(path_a)
        prod_a = [0] * states_n
        prod_b = list(prod_a)
        for j in range(len(i)):
            if j == 0:
                prod_a = (np.array([((States_n_pair[(gate,x)] + 1)/(States_n[gate] + states_n - 1))*((Symbols_n_pair[(x,i[j])]+1)/(Symbols_n[x] + symbols_n + 1)) for x in range(states_n-2)]))
                [path_a[k].append(k) for k in range(states_n-2)]
                #print(path_a)
            else:
                for state in range(states_n-2):
                    temp = (np.array([((States_n_pair[(x,state)] + 1)/(States_n[x] + states_n - 1))*((Symbols_n_pair[(state,i[j])]+1)/(Symbols_n[state] + symbols_n + 1)) for x in range(states_n-2)]))
                    #print(prod_a)
                    #print(prod_b)
                    temp = temp * prod_b
                    opt = np.amax(temp)
                    #print(prod_a)
                    #print(opt)
                    ind = list(temp).index(opt)
                    #print(ind)
                    path_a[state] = path_b[ind][:] + [state]
                    #print(path_a)
                    prod_a[state] = opt
            path_b = path_a[:]
            prod_b = list(prod_a)
        [path_a[k].append(States.index('END')) for k in range(states_n-2)]
        prod_a *= np.array([(States_n_pair[(x,States.index('END'))]+1)/(States_n[x] + states_n -1) for x in range(states_n-2)])
        opt = np.amax(prod_a)
        sol = list(prod_a).index(opt)
        final.append(path_a[sol] + [log(prod_a[sol])])
    return final
        
        

def top_k_viterbi(State_File, Symbol_File, Query_File, k):
    with open(State_File) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    States = content[1:int(content[0])+1]
    State_trans = [[int(x) for x in i.split(' ')] for i in content[int(content[0])+1:]]
    with open(Symbol_File) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    Symbols = content[1:int(content[0])+1]
    Symbol_trans = [[int(x) for x in i.split(' ')] for i in content[int(content[0])+1:]]
    with open(Query_File) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    Querries = []
    for i in range(len(content)):
        A = []
        a = 0
        #print(content[i])
        for j in range(len(content[i])):
            if content[i][j]==',' or content[i][j] == '(' or content[i][j] == ')' or content[i][j] == '/' or content[i][j] == '-' or content[i][j] == '&' or content[i][j] == ' ':
                if content[i][a:j] != '':
                    A.append(content[i][a:j].strip())
                    if content[i][j] != ' ':
                        A.append(content[i][j])
                    a = j + 1
        if content[i][a:] != '':
            A.append(content[i][a:])
        Querries.append(A)
    Querries_symb = []
    for i in range(len(Querries)):
        A = []
        for j in range(len(Querries[i])):
            if Querries[i][j] in Symbols:
                A.append(Symbols.index(Querries[i][j]))
            else:
                A.append(-1)
        Querries_symb.append(A)

    states_n = len(States)
    symbols_n = len(Symbols)
    States_n = [0] * states_n
    States_n_pair = defaultdict(int)
    for i in range(len(State_trans)):
        States_n[State_trans[i][0]] += State_trans[i][2]
        States_n_pair[(State_trans[i][0],State_trans[i][1])] = State_trans[i][2]
    Symbols_n = [0] * states_n
    Symbols_n_pair = defaultdict(int)
    for i in range(len(Symbol_trans)):
        Symbols_n[Symbol_trans[i][0]] += Symbol_trans[i][2]
        Symbols_n_pair[(Symbol_trans[i][0],Symbol_trans[i][1])] = Symbol_trans[i][2]
    final = []
    gate = States.index('BEGIN')
    for i in Querries_symb:
        matrix = [[[] for _ in range(len(i))] for _ in range(states_n)]
        matrix_path = [[[] for _ in range(len(i))] for _ in range(states_n)]
        for j in range(len(matrix)):
            matrix_path[j][0].append([gate])
            matrix[j][0].append(1)
        for j in range(len(i)):
            if j == 0:
                for state in range(states_n-2):
                    matrix_path[state][0][0].append(state)
                    matrix[state][0][0] = ((States_n_pair[(gate,state)] +1)/(States_n[gate] + states_n - 1)) * ((Symbols_n_pair[(state,i[j])] + 1)/(Symbols_n[state] + symbols_n + 1))
            else:
                for state1 in range(states_n-2):
                    temp = []
                    for state2 in range(states_n-2):
                        for path in range(len(matrix_path[state2][j-1])):
                            value = matrix[state2][j-1][path] * ((States_n_pair[(state2,state1)] + 1)/ (States_n[state2] + states_n - 1)) * ((Symbols_n_pair[(state1,i[j])]  + 1)/(Symbols_n[state1] + symbols_n +1))
                            no = matrix_path[state2][j-1][path][:] + [state1, value]
                            temp.append(no)
                    temp.sort(key = lambda x: x[-1])
                    [(matrix_path[state1][j].append(x[:-1]),matrix[state1][j].append(x[-1])) for x in temp[-k:]]
        top_k = []
        for j in range(states_n-1,-1,-1):
            for l in range(len(matrix[j][len(i) - 1])):
                temp_k = []
                matrix[j][len(i) - 1][l] *= ((States_n_pair[(j, States.index('END'))] + 1)/(States_n[j] + states_n - 1))
                matrix_path[j][len(i) - 1][l].append(states_n - 1)
                temp_k = matrix_path[j][len(i) - 1][l][:] + [log(matrix[j][len(i) - 1][l])]
                top_k.append(temp_k)
        top_k.sort(key= lambda x: x[-1])
        top_k.reverse()
        top_k = top_k[:k]
        #print(top_k)
        [final.append(x) for x in top_k]
    return final