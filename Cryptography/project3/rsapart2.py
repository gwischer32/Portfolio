from jacobi import jacobi
from gcd import gcd
from chinatheorem import extended_gcd, mod_inverse
from exponential_mod import expo_mod
import random

lower_bound = (2**(1023))+1
upper_bound = (2**(1024))
def prime_test(n:int)->bool:
    trials = 55
    for _ in range(trials):
        tester = random.randrange(2, n-1)
        criterion = expo_mod(tester, (n-1)//2,n)
        symbol = jacobi(tester, n)
        if symbol == 0 or (symbol == -1 and criterion != n-1) or (symbol != -1 and symbol != criterion):
            return False
        
    return True

def get_key():
    counter = 1  
    number = random.randrange(lower_bound, upper_bound,2)
    while not prime_test(number):
        counter+=1
        number = random.randrange(lower_bound, upper_bound,2)
    print('')
    print(counter, "number of odds were tested")

    second = random.randrange(lower_bound, upper_bound,2)
    counter = 1
    while not prime_test(second):
        counter+=1
        second = random.randrange(lower_bound, upper_bound,2)
    print(counter, "number of odds were tested")

    public_final = number*second
    phi_the_number= (number-1)*(second-1)
    coprime = random.randrange(2,phi_the_number-1)
    while gcd(coprime,phi_the_number)!=1:
        coprime = random.randrange(2,phi_the_number-1)

    modular_inverse = mod_inverse(coprime,phi_the_number)

    with open('RSA_Project_3_public.txt','w')as public:
        public.write(f'{public_final}')
        public.write(f'{coprime}')

    with open ('RSA_Project_3_private.txt', 'w') as private:
        private.write(f'{modular_inverse}')
        private.write(f'\n{number}')
        private.write(f'\n{second}')

    
    print(f'\n55 numbers less than the current prime were chosen,\nThis means that there is a 1 in 100 trillion chance that these numbers are not prime\n')
    print(f'public key (n):\n{public_final}\n\ncoprime (e):\n{coprime} ')
    print(f'\nprivate (d):\n{modular_inverse}\n')

def main():
    get_key()

if __name__ == "__main__":
    main()