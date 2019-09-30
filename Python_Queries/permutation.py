def f(A):
    if len(A) > 1:
        per_list = []
        for a in A:
            per_list += add_list(a, f([b for b in A if b != a]))
        return per_list
    else: return [A]

def add_list(ele, list_list):
    return [[ele] + l for l in list_list]

print(f([1,2,3,4,5,6,7,8,9]))