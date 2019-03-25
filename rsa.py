from math import gcd, ceil
from sympy import isprime
from random import randint
import time


def find_e(limit):
    for i in range(2, limit):
        if gcd(i, limit) == 1:
            return i
    return 1


def find_d(e, phi_n):
    k = 1
    while True:
        d = (k * phi_n + 1) / e
        if d % 1 == 0:
            return int(d)
        k += 1


def generate(p, q):
    if not isprime(p):
        raise ValueError('Not prime value p = ' + str(p))
    if not isprime(q):
        raise ValueError('Not prime value q = ' + str(q))
    product = p * q
    phi_n = (p - 1) * (q - 1)
    e = find_e(phi_n)
    d = find_d(e, phi_n)
    return (e, product), (d, product)


p = 270343
q = 109297

print("p: ", p)
print("q: ", q)

open_key, secret_key = generate(p, q)

print("Open key: ", open_key)
print("Secret key: ", secret_key)


def encrypt(value, key):
    return pow(value, key[0], key[1])


def decrypt(value, key):
    return pow(value, key[0], key[1])


def decrypt_cust(value):
    return value ** secret_key[0] % secret_key[1]


to_crypt = 111111
print("Original value: ", to_crypt)
enc = encrypt(to_crypt, open_key)
print("Encrypted value: ", enc)
start = time.time()
dec = decrypt(enc, secret_key)
end = time.time()
print("Decrypted value: ", dec)
print("Decrypted in: {} ms".format(end - start))

# ----- Hacking ----
print("----- Hacking ----")
print()


def ferma_factorise(n):
    start = time.time()
    s = ceil(n ** (1 / 2))
    for k in range(1, n):
        sk = s + k
        y = sk ** 2 - n
        root_y = y ** (1 / 2)
        if root_y == int(root_y):
            a = int(sk + root_y)
            b = int(sk - root_y)
            if isprime(a) and isprime(b):
                end = time.time()
                print("Ferma factorisation a = {0} , b = {1} , found in {2} iterations in {3} ms".format(a, b,
                                                                                                         k,
                                                                                                         end - start))
                return int(a), int(b)
    return None


# could be paralelised
def ro_pollard_factorisation(n):
    start_ = time.time()
    x = randint(2, n - 2)
    y = 1
    i = 0
    stage = 2
    while gcd(n, abs(x - y)) == 1:
        if i == stage:
            y = x
            stage = stage * 2
        x = (x ** 2 - 1) % n
        i = i + 1
    a = gcd(n, abs(x - y))
    b = n / a
    end_ = time.time()
    print("Ro-pollard factorisation a = {0} , b = {1} , found in {2} iterations in {3} ms".format(int(a), int(b), i,
                                                                                                  end_ - start_))
    return int(a), int(b)


o_k, s_k = generate(p, q)
N = o_k[1]
print("factorizing: ", N)
print()

p_hacked, q_hacked = ferma_factorise(N)
_, secret_key_hacked = generate(p_hacked, q_hacked)
print("Hacked with ferma: {0}".format(decrypt(enc, secret_key_hacked)))
print()

p_hacked, q_hacked = ro_pollard_factorisation(N)
_, secret_key_hacked = generate(p_hacked, q_hacked)
print("Hacked with ro-pollard: {0}".format(decrypt(enc, secret_key_hacked)))
