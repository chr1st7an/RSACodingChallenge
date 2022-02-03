# Author: Christian Rodriguez
# Date: 02/03/2022
# Title:
import rsa
import random
from math import ceil
from decimal import Decimal

field_size = 10**5


def createKeys():
    # creating set of 1024 bit RSA Key Pair
    (pubkey, privkey) = rsa.newkeys(1024)
    # saving public key into .txt file
    pub = pubkey.save_pkcs1()
    pub = pub.decode('utf-8')
    pubfile = open("keys/Public.txt", "w+")
    pubfile.write(pub)
    pubfile.close()
    return privkey, pubkey


def coefficient(k, secret):
    coeff = [random.randrange(0, field_size) for _ in range(int(k) - 1)]
    coeff.append(secret)
    return coeff


class Keys():

    def __init__(self, private, public, k, n, field):
        self.__k = k
        self.__n = n
        self.__private = private
        self.__public = public
        self.__field_size = field

    def print(self):
        print(self.__private)

    def privateHash(self):
        privHash = hash(self.__private)
        return privHash

    def encryptTxt(self, Msg):
        Msg = Msg.encode('utf8')
        cyphertxt = rsa.encrypt(Msg, self.__public)
        return cyphertxt

    def generateShards(self, secret, coefficients):
        shards = []
        for i in range(1, int(self.__n) + 1):
            x = random.randrange(1, self.__field_size)
            point = 0
            for coef_index, coef_value in enumerate(coefficients[::-1]):
                point += x ** coef_index * coef_value
            shards.append((x, point))
        for i in shards:
            fileName = "keys/Shard" + str(shards.index(i) + 1) + ".txt"
            shard = open(fileName, "w+")
            shard.write(str(i))
            shard.close()
        return shards

    def reconstructKey(self, shardlist):
        sums = 0
        prod_arr = []
        for j, shard_j in enumerate(shardlist):
            xj, yj = shard_j
            prod = Decimal(1)
            for i, shard_i in enumerate(shardlist):
                xi, _ = shard_i
                if i != j:
                    prod *= Decimal(Decimal(xi)/(xi - xj))
            prod *= yj
            sums += Decimal(prod)
        return int(round(Decimal(sums), 0))

    def decryptMsg(self, cypher):
        message = rsa.decrypt(cypher, self.__private)
        message = message.decode('utf8')
        return message
