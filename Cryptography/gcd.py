def gcd(n:int, m: int)->int:
    while m !=0:
        n, m = m, n%m
    return n


print(gcd(192,78))