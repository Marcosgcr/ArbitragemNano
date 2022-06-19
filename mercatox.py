import math
A = 2600
B = 1950
C = 3900
s = math.gcd(A,B,C)
##Como a editora deseja remeter os três pedidos com a mesma quantidade de livros
# e com o maior número de livros possível por pacote, quantos pacotes serão remetidos ao todo?

print(s)
print(A/s)
print(B/s)
print(C/s)
print("Soma é{0}".format(A/s+B/s+C/s))