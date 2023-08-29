import os, time, json
from hashlib import sha256

class NoBlock:
    def __init__(self, seed, nonce=0, d=2):
        self.seed = seed
        self.nonce = nonce
        self.difficulty = d

    def compute_hash(self):
        # A function that return the hash of the block contents.
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest() #Devuelve el hash del bloque

    def proof_of_work(self):
        # Function that tries different values of nonce to get a hash
        # that satisfies our difficulty criteria.

        computed_hash = self.compute_hash()
        while not computed_hash.startswith('0'*self.difficulty):
            self.nonce += 1
            computed_hash = self.compute_hash()

        return computed_hash
    
 
b = NoBlock(seed='La semilla que quiera', nonce=0)
h = b.compute_hash()
print(h)
print(b.proof_of_work())
print(b.nonce)

# Considerando el programa noblock.py, realizar un programa que lance dos procesos hijos 
# que intenten encontrar el nonce para un No-Bloque con una dificultad dada. 
# El hijo que lo encuentre primero debe comunicarse con el padre mediante una señal 
# guardando el nonce en una fifo para que el padre pueda leerla. 
# Hacer otra versión pero utilizando pipes.

def hackear(hijos=2):
    os.mkfifo("data")
    block = NoBlock()

    for n in range(hijos):
        pip = os.fork()
        if pip==0:
            data = b.proof_of_work()
            with open("data") as p:
                p.write(data)
            exit()
    
    while open("date") == "":
        time.sleep(1)
    

if __name__ == "__main__":
    pass    