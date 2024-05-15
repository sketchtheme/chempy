"""
DECISION TREE REPRASENTATION
"""
import re
import math
from some import elements



# def get_valences(reaction):
#     lefts, rights = parse(reaction)
#     left_valences = []
#     for i in lefts:
#         for j in elements:
#             if not i[0] == j[0]:
#                 continue
#             left_valences.append(j)
#     right_valences = []    
#     for i in rights:
#         for j in elements:
#             if not i[0] == j[0]:
#                 continue
#             right_valences.append(j)
#     return left_valences, right_valences


# def divisorGen(n):
#     factors = list(factorGenerator(n))
#     nfactors = len(factors)
#     f = [0] * nfactors
#     while True:
#         yield reduce(lambda x, y: x*y, [factors[x][0]**f[x] for x in range(nfactors)], 1)
#         i = 0
#         while True:
#             f[i] += 1
#             if f[i] <= factors[i][1]:
#                 break
#             f[i] = 0
#             i += 1
#             if i >= nfactors:
#                 return

def parse(reaction):
    pattern = r"([A-Z][a-z]*)(\d*)"
    lefts, rights = reaction.split('+')
    left = re.findall(pattern, lefts);right = re.findall(pattern, rights)
    return left, right


def divisorGenerator(n):
    large_divisors = []
    for i in range(2, int(math.sqrt(n) + 1)):
        if n % i == 0:
            yield i
            if i*i != n:
                large_divisors.append(n / i)
    for divisor in reversed(large_divisors):
        yield divisor


def get_product(reaction):
    lefts, rights = parse(reaction=reaction)
    left_valences = [j for i in lefts for j in elements if i[0] == j[0]]
    right_valences = [j for i in rights for j in elements if i[0] == j[0]]
    
    # if left_valences.count() == 0 and right_valences.count() == 0:
    #     return False
    if len(left_valences) == 1 and len(right_valences) == 1:
        x, y = int(left_valences[0][1]), int(right_valences[0][1])
        if abs(x) > abs(y) and x%y == 0:
            z = 1
            t = abs(x/y)
            # z = (x/max_value) if max_value !=0 else 1
            # t = (y/max_value) if max_value !=0 else 1    
            return [[int(z), int(t)]]
        elif abs(x) < abs(y) and y%x == 0:
            z = abs(y/x)
            t = 1
            return [[int(z), int(t)]]
        elif abs(x) > abs(y) and x%y != 0:
            divisors = list(divisorGenerator(abs(x)))
            for i in divisors:
                if x%i == 0 and y%i == 0:
                    z, t= x//i, y//i
                    return [[abs(z), abs(t)]]
            return [[abs(y), abs(x)]]
        elif abs(x) < abs(y) and y%x != 0:
            divisors = list(divisorGenerator(abs(y)))
            for i in divisors:
                if x%i == 0 and y%i == 0:
                    z, t= x//i, y//i
                    return [[abs(z), abs(t)]]
            return [[abs(y), abs(x)]]
        else:
            return [[abs(x//y), abs(y//y)]]


def join(reaction):
    left, right = parse(reaction=reaction)
    prefix = get_product(reaction=reaction)
    if len(prefix) == 1 and (len(left)==1 and len(right)==1):
        return f"{left[0][0]}{prefix[0][0]}{right[0][0]}{prefix[0][1]}"


print(join('Ca + O2'))
