# ID: 28900057
# Name: Chong Kah Ying

import math
import random
import sys

COMPOSITE = "Composite"
PROBABLY_PRIME = "probably_prime"

def millerRabin(n,k):
    if n%2 == 0:
        return COMPOSITE
    t = n-1
    s = 0
    while t%2 == 0:
        s += 1
        t = t//2
    if n-2 > 2: 
        for _ in range(k):
            random_int = random.randint(2,n-2)
            prev = random_int
            #compute a^(2^0)*t = a*t 
            for _ in range(1,t):
                current = (prev*prev)%n
                prev = current
            #compute a^(2^1)*t...a^(2^s)*t
            for _ in range(1,s):
                current = (prev*prev)%n
                if (current == 1 and not(prev == 1 or prev == n-1)) or (current == 0):
                    return COMPOSITE
                elif current == 1 and (prev == 1 or prev == n-1):
                    break
                prev = current 
    return PROBABLY_PRIME

def write_result_to_file(three_primes):
    # three_primes is in descending order
    # simply get the last element from the end of the list to produce a sequence of numbers in ascending order
    three_primes_string = ""
    print(three_primes)
    if len(three_primes) > 0:
        three_primes_string += str(three_primes.pop())

    while len(three_primes) > 0:
        three_primes_string += " " + str(three_primes.pop())

    f = open("output_threeprimes.txt", "w")
    f.write(three_primes_string)
    f.close()

def _find_remaining_primes(n, current, prime_list):
    # current might not be odd 
    if len(prime_list) == 3 or current < 3:
        return prime_list
    k = round(1/math.log(current))
    while millerRabin(current,k) == COMPOSITE and current >= 3:
        k = round(1/math.log(n))
        current -= 1 

    if sum(prime_list)+current <= n:
        prime_list.append(current)
    else:
        current -= 2
    return _find_remaining_primes(n, current, prime_list)

def find_three_primes(n):
    # n is a odd number
    # the largest prime number in the three prime numbers that will add up to n 
    # must be smaller than n, and must be a prime, but a prime number must be odd
    # so start looking for the largest prime number from n-2 onwards 
    current = n-2
    primes = []
    k = round(1/math.log(n))
    # the least odd prime number is 3 
    while current >= 3:
        # reduce the number 
        while millerRabin(current,k) == COMPOSITE and current > 2:
            k = round(1/math.log(n))
            current -= 2
        if current > 0 and n-current >= 2:
            for start in range(n-current, 2, -1):
                #look for the next 2 prime numbers that will add up to n-current
                primes = _find_remaining_primes(n,start,[current])
                # terminate if conditions are fulfilled
                if len(primes) == 3 and sum(primes) == n:
                    return primes
        else:
            return primes
       
        current -= 2
        
    return primes

def main(n):
    found = False
    if n > 7 and n % 2 != 0:
        primes = find_three_primes(n)
        if len(primes) == 3 and sum(primes) == n:
            found = True
    if found:
        write_result_to_file(primes)
    else:
        write_result_to_file([])

if __name__ == "__main__":
    n = int(sys.argv[1])
    main(n)
