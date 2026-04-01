def expo_mod( b: int, e: int, m: int ) :
    new_b = b%m 
    answer = 1
    while e > 0 :
        if e % 2 == 1 :
            answer = (answer*new_b)%m
        new_b = (new_b**2)%m
        e = e//2

    return answer


