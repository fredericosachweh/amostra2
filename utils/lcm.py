from fractions import gcd

def lcm(numbers):
    return reduce(lambda x, y: (x*y)/gcd(x,y), numbers, 1)
