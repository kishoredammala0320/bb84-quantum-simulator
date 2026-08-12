import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

def simulate_bb84(num_bits, eavesdropping):
    backend = Aer.get_backend('qasm_simulator')
    
    # Alice's setup
    alice_bits = np.random.randint(2, size=num_bits)
    alice_bases = np.random.randint(2, size=num_bits)
    bob_bases = np.random.randint(2, size=num_bits)
    bob_results = []

    for i in range(num_bits):
        qc = QuantumCircuit(1, 1)
        if alice_bits[i] == 1: qc.x(0)
        if alice_bases[i] == 1: qc.h(0)
        
        if eavesdropping:
            # Eve intercepts
            eve_basis = np.random.randint(2)
            if eve_basis == 1: qc.h(0)
            qc.measure(0, 0)
            qc.reset(0) # State is disturbed
            
        if bob_bases[i] == 1: qc.h(0)
        qc.measure(0, 0)
        
        job = backend.run(transpile(qc, backend), shots=1, memory=True)
        bob_results.append(int(job.result().get_memory()[0]))

    # Sifting (finding matching bases)
    alice_key = []
    bob_key = []
    for i in range(num_bits):
        if alice_bases[i] == bob_bases[i]:
            alice_key.append(alice_bits[i])
            bob_key.append(bob_results[i])
            
    qber = 0
    if len(alice_key) > 0:
        matches = sum([1 for a, b in zip(alice_key, bob_key) if a == b])
        qber = 1 - (matches / len(alice_key))
        
    return alice_key, bob_key, qber, alice_bits, alice_bases, bob_bases