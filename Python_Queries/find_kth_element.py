# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 23:54:02 2019

@author: victo
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# return k-th element and its nearest sup and inf in the same interval
# if sup or inf is None, it means the interval length is 1 or 2

def find_k(a, k):
    l = a
    sup_nb_base, inf_nb_base = 0, 0
    while True:
        x = len(l)
        ini = int(x/2)
        pivot = l[ini]
        
        sup, inf = None, None
        sup_nb, inf_nb = 0, 0
        
        print(l)
        
        sup_pool = []
        inf_pool = []
        mid_pool = []
        
        for i in range(x):

            if l[i] > pivot:
                if sup is None or sup > l[i]: sup = l[i]
                sup_pool.append(l[i])
                
            elif l[i] < pivot:
                if inf is None or inf < l[i]: inf = l[i]
                inf_pool.append(l[i])
                
            else:
                mid_pool.append(l[i])
                
        inf_nb = inf_nb_base + len(inf_pool)
        mid_nb = len(mid_pool)
        
        if inf_nb + mid_nb < k:
            l = sup_pool
            inf_nb_base += (len(inf_pool) + mid_nb)
            continue
        
        elif inf_nb +mid_nb == k:
            if mid_nb > 1: return pivot, pivot, sup, "INF THIS SUP"
            else: return inf, pivot, sup, "INF THIS SUP"
            
        elif inf_nb + mid_nb > k and sup_nb + mid_nb > k:
            return pivot, pivot, pivot, "INF THIS SUP"
        
        elif sup_nb + mid_nb == k:
            if mid_nb > 1: return inf, pivot, pivot, "INF THIS SUP"
            else: return inf, pivot, sup, "INF THIS SUP"
            
        else:
            l = inf_pool
            sup_nb_base += (mid_nb + len(sup_pool))

if __name__ == "__main__":
    
    #a = [7, 10, 4, 3, 20, 15]
    #k = 4
    a = [1, 3, 4, 2, 6, 5, 8, 7]
    k = 4
    print(find_k(a,k))
        
                    
                
