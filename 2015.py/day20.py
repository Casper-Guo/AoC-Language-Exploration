"""
let X = (a1 ^ b1) + (a2 ^ b2) ... + (an ^ bn)
let the sum of X's factors be f(X)
then f(X) = (a1^0 + a1^1 ... + a1^b1) + (a2^0 + a2^1... +a2^b2) + ... + (an^0 + an^1... + an^bn)

Some other observations"
If X = a * b and a and b are relatively prime, then f(X) = f(a) * f(b)
If X = a^n and a is prime, then f(X) = a^0 + a^1 + ... a^n
"""

from itertools import product
from math import prod


def list_factors(prime_factorization: dict[int, int]) -> list[int]:
    """Given the prime factorization of a number, list all its factors."""
    prime_factors = list(prime_factorization.keys())
    exponents = [list(range(i + 1)) for i in prime_factorization.values()]

    factors = []

    for exponent_set in product(*exponents):
        factors.append(
            prod([factor ** exponent_set[idx] for idx, factor in enumerate(prime_factors)])
        )

    return factors


def multiply_factors(prime_factorization: dict[int, int]) -> int:
    """Use the prime factorization to find the original number."""
    terms = [key**value for key, value in prime_factorization.items()]

    return prod(terms)


def sum_factors(prime_factorization: dict[int, int]) -> int:
    """Calculate the sum of all factors given its prime factorization."""
    # part 1
    # terms = []
    # for factor, freq in prime_factorization.items():
    #     term = 0
    #     for i in range(freq + 1):
    #         term += factor ** i
    #     terms.append(term)

    # return prod(terms)

    # part 2
    factors = list_factors(prime_factorization)
    original_number = multiply_factors(prime_factorization)

    return sum([factor for factor in factors if factor * 50 >= original_number])


def merge_factors(left: dict[int, int], right: dict[int, int]) -> dict[int, int]:
    """
    Merge two dictionaries, values of common keys are added.

    Caveat: the value is always 1 for key value 1
    """
    new_dict = {}

    for key, value in left.items():
        if key in right:
            new_dict[key] = value + right[key]
        else:
            new_dict[key] = value

    for key, value in right.items():
        if key not in new_dict:
            new_dict[key] = value

    return new_dict


prime_factorization = {}
factor_sums = {1: 1}
current = 2

# part 1
upper_bound = 3600000

# part 2
upper_bound = 36000000 // 11 + 1

while True:
    if current not in prime_factorization:
        # i must be prime
        prime_factorization[current] = {current: 1}
        factor_sums[current] = current + 1

    if factor_sums[current] > upper_bound:
        print(current)
        break

    for i in range(2, current + 1):
        considering = i * current
        if considering in prime_factorization:
            continue

        prime_factorization[considering] = merge_factors(
            prime_factorization[i], prime_factorization[current]
        )

        factors_sum = sum_factors(prime_factorization[considering])
        factor_sums[considering] = factors_sum

        if factors_sum > upper_bound:
            # too big
            break

    current += 1
