# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 17:18:37 2019

@author: victo
"""

def bfs(adjacent_list):
    idx = 0
    out_list = []
    while idx < len(adjacent_list):
        head = adjacent_list[idx]
        tail = adjacent_list[idx + 1]
        if head not in out_list:
            out_list.append(head)
        if tail not in out_list:
            out_list.append(tail)
        idx += 2
        
    return out_list

class Node:
    def __init__(self, value):
        self.value = value
        self.leaf_list = []
        self.head = None
    def add_leaf(self, leaf):
        self.leaf_list.append(leaf)
    def add_head(self, head):
        self.head = head
        
def dfs(adjacent_list):
    nodes_dict = {}
    idx = 0
    out_list = [0]
    while idx < len(adjacent_list):
        head = adjacent_list[idx]
        tail = adjacent_list[idx + 1]
        node_head = nodes_dict.get(head, Node(head))
        node_leaf = nodes_dict.get(tail, Node(tail))
        node_head.add_leaf(node_leaf)
        node_leaf.add_head(node_head)
        nodes_dict[head] = node_head
        nodes_dict[tail] = node_leaf
        idx += 2
    walk = 0
    while len(nodes_dict[walk].leaf_list) != 0:
        count = 0
        for leaf_node in nodes_dict[walk].leaf_list:
            walk = leaf_node.value
            if walk not in out_list:
                out_list.append(walk)
                count = 1
                break
        if count == 0:
            walk = nodes_dict[walk].head.head
            if walk is not None:
                walk = walk.value
                continue
            else:
                break
        if len(nodes_dict[walk].leaf_list) == 0:
            walk = nodes_dict[walk].head
            if walk is not None:
                walk = walk.value
                continue
            else:
                break
    return out_list

def dijsktra(path_list):
    dict_path = {1:0}
    start = [1]
    reach = []
    start_passed = []
    while len(start) != 0:
        count = 0
        for s in start:
            if s in start_passed:
                continue
            else:
                s_dist = dict_path[s]
                start_passed.append(s)
                if s + 1 in path_list:
                    t = s + 1
                    t_dist = dict_path.get(t, None)
                    reach.append(t)
                    new_dist = s_dist + 1
                    if t_dist is None:
                        dict_path[t] = new_dist
                    elif t_dist > new_dist:
                        dict_path[t] = new_dist
                    count = 1
                if 3 * s in path_list:
                    t = 3 * s
                    t_dist = dict_path.get(t, None)
                    reach.append(t)
                    new_dist = s_dist + 1
                    if t_dist is None:
                        dict_path[t] = new_dist
                    elif t_dist > new_dist:
                        dict_path[t] = new_dist
                    count = 1
        if count == 0:
            break
        else:
            start = reach
            reach = []
            
    print(dict_path)
    return dict_path

def floyd_warshall(matrix):
    n = len(matrix)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if matrix[i][k] + matrix[k][j] < matrix[i][j]:
                    matrix[i][j] = matrix[i][k] + matrix[k][j]
                    
    return matrix

def minimum_spanning_prim(graph_list):
    import numpy as np
    import pandas as pd
    graph_matrix = np.array(graph_list).reshape(-1, 3)
    df_1 = pd.DataFrame(graph_matrix, columns = ['start', 'end', 'weight'])
    df_2 = pd.DataFrame(graph_matrix, columns = ['end', 'start', 'weight'])[['start', 'end', 'weight']]
    df = pd.concat([df_1, df_2], axis = 0)
    passed_set = [graph_list[0]]
    weight_set = []
    while len(passed_set) < len(pd.unique(df[['start','end']].values.flatten())):
        compress_list = list(range(df.shape[0]))
        compress_list = np.compress([True if k in passed_set else False for k in df['start'].tolist()], compress_list)
#        print(compress_list)
        df_part = df.iloc[compress_list.tolist(), :].sort_values(by = ['weight'], ascending = True)
#        print(df_part)
        for i in range(df_part.shape[0]):
            if df_part.iloc[i, 1] not in passed_set: 
                passed_set.append(df_part.iloc[i, 1])
                weight_set.append(df_part.iloc[i, 2])
                break
    print(passed_set)
    return np.sum(weight_set)

def union_find(graph_list):
    import numpy as np
    single = np.unique(graph_list)
    dict_g = {k: k for k in single}
    graph_matrix = np.array(graph_list).reshape(-1,2)
    for i in range(graph_matrix.shape[0]):
        r1 = dict_g[graph_matrix[i][0]]
        r2 = dict_g[graph_matrix[i][1]]
        if r1 != r2:
            dict_g[graph_matrix[i][0]] = max(r1, r1)
            dict_g[graph_matrix[i][1]] = max(r1, r1)
        else:
            return True
    
    return False

def topo_sort(graph_list):
    import numpy as np
    graph_matrix = np.array(graph_list).reshape(-1,2)
    single = np.unique(graph_list)
    tf = [False] * len(single)
    out_list = []
    for i in range(len(single)):
        if len(out_list) < len(single):
            out_list, tf = topo_sort_single(i, graph_matrix, out_list, tf)

    return out_list, tf
    
def topo_sort_single(i, graph_matrix, out_list, tf):
    while len(out_list) < len(tf):
        if not tf[i]:
            tf[i] = True
            out_list.append(i)
            count = 0
            for j in range(graph_matrix.shape[0]):
                if graph_matrix[j][0] == i:
                    count = 1
                    out_list, tf = topo_sort_single(graph_matrix[j][1], graph_matrix, out_list, tf)
            if count == 0:
                break
        else:
            break
            
    return out_list, tf

def boggle_words(words_list, letters_matrix):
    out_list = []
    for w in words_list:
        wl = [l for l in w]
        print(wl)
        count = 0
        for i in range(letters_matrix.shape[0]):
            for j in range(letters_matrix.shape[1]):
                out = []
                if letters_matrix[i][j] == wl[0]:
                    out.append(wl[0])
                    out = boggle(wl[1:], letters_matrix, i, j, out)
                    if len(out) == len(wl):
                        out_list.append(w)
                        count = 1
                        break
            if count == 1:
                 break
            
    return out_list

def boggle(letters, letters_matrix, i, j, out):
    l = letters[0]
    out_back = []
    import itertools
    mnlist = itertools.product([i-1,i,i+1],[j-1,j,j+1])
    for (m,n) in mnlist:
        out_back = []
        if m == i and n == j:
            continue
        if any([m < 0, n < 0, m >= letters_matrix.shape[0], n >= letters_matrix.shape[1]]):
            continue
        if letters_matrix[m][n] == l:
            out_back.append(l)
            if len(letters) == 1:
                return out + out_back
            out_back = boggle(letters[1:], letters_matrix, m, n, out_back)
            if len(out_back) == len(letters):
                break
    
    return out + out_back

def longest_common_subsequence(listA, listB):
    import numpy as np
    cs_matrix = np.array([[''] * len(listB)] * len(listA))
    for i in range(cs_matrix.shape[0]):
        if listA[i] == listB[0]:
            cs_matrix[i : , 0] = listB[0]
            break
        else:
            cs_matrix[i][0] = ''
    for j in range(cs_matrix.shape[1]):
        if listB[j] == listA[0]:
            cs_matrix[0, j : ] = listA[0]
            break
        else:
            cs_matrix[0][j] = ''
    cs_matrix = cs_matrix.tolist()
    for m in range(1, len(listA)):
        for n in range(1, len(listB)):
            l1 = cs_matrix[m-1][n-1] + listA[m] if all([listA[m] == listB[n], listA[m] != '']) else cs_matrix[m-1][n-1]
            l2 = cs_matrix[m-1][n]
            l3 = cs_matrix[m][n-1]
            l = max([l1,l2,l3], key = lambda x: len(x))
            cs_matrix[m][n] = l

    return cs_matrix[-1][-1]

def longest_increasing_sebsequence(list_num):
    nums = [[list_num[0]]]
    for i in list_num:
        count = 0
        for n in nums:
            if i > n[-1]:
                nums.append(n + [i])
                count = 1
        if count == 0:
            nums.append([i])
    return max(nums, key = lambda x: len(x))

def partition_difference(list_num):
    import numpy as np
    sumtot = np.sum(list_num)
    nums = [[list_num[0]],[]]
    out = np.abs(list_num[0] * 2 - sumtot)
    for i in list_num:
        for n in nums:
            if i not in n:
                nums.append(n + [i])
                out = min(np.abs(np.sum(n + [i]) * 2 - sumtot), out)
                
    return out
                
if __name__ == '__main__':
#    test1 = [0,1,0,2,0,3,2,4]
#    test2 = [0, 1, 0, 2]
#    test3 = [0,1,1,2,0,3]
    
#    print(dfs(test1))
#    print(dfs(test2))
#    print(dfs(test3))
    
#    test = list(range(1, 10))
#    print(dijsktra(test))
    
#    test1 = [[0, 25], [1e7, 0]]
#    test2 = [[0,1,43],[1,0,6],[1e7,1e7,0]]
#    print(floyd_warshall(test2))
    
#    test1 = [1,2,5,2,3,3,1,3,1]
#    test2 = [1,2,5]
#    print(minimum_spanning_prim(test1))
#    print(minimum_spanning_prim(test2))
    
#    test = [0,1,0,2,1,3,1,4, 3,4]
#    print(union_find(test))
    
#    test = [5,0,4,0,5,2,2,4,3,1,4,1]
#    print(topo_sort(test)[0])
#    import numpy as np
#    words = ['GEEKS','QUIZ','HELLO','IE']
#    test = np.array([['G', 'I', 'Z'],
#                     ['U', 'E', 'K'],
#                     ['Q', 'S', 'E']])
#    print(boggle_words(words, test))
    
#    test1 = "ABCDGH" 
#    test2 = "AEDFHR"
#    print(longest_common_subsequence(test1, test2))
    
#    test = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
#    print(longest_increasing_sebsequence(test))
    
    test1 = [1, 6, 5, 11]
    test2 = [36, 7, 46, 40]
    print(partition_difference(test1))
    print(partition_difference(test2))
    