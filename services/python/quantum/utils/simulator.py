"""
Quantum Circuit Simulator for QSCM Planner
Handles loading, simulating, and analyzing OpenQASM circuits
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
import json
import os
import weave
import psutil
import time

try:
    from qiskit import QuantumCircuit, transpile
    try:
        from qiskit_aer import AerSimulator
    except ImportError:
        from qiskit.providers.aer import AerSimulator
    from qiskit.visualization import plot_histogram
    from qiskit.quantum_info import Statevector, partial_trace
    from qiskit.circuit.library import QFT
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    print("Qiskit not available. Install with: pip install qiskit qiskit-aer")

class QuantumCircuitSimulator:
    def __init__(self):
        if not QISKIT_AVAILABLE:
            raise ImportError("Qiskit is required for quantum circuit simulation")
        self.simulator = AerSimulator()
        self.circuits = {}
        
    def load_qasm_file(self, filepath: str) -> QuantumCircuit:
        """Load an OpenQASM 3.0 circuit from file"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"QASM file not found: {filepath}")
        
        with open(filepath, 'r') as f:
            qasm_content = f.read()
        
        circuit = QuantumCircuit.from_qasm_str(qasm_content)
        self.circuits[filepath] = circuit
        return circuit
    
    @weave.op()
    def simulate_circuit(self, circuit: QuantumCircuit, shots: int = 1024) -> Dict:
        """Simulate a quantum circuit and return measurement results"""
        # Transpile for the simulator
        transpiled_circuit = transpile(circuit, self.simulator)
        
        # Run simulation
        job = self.simulator.run(transpiled_circuit, shots=shots)
        result = job.result()
        
        # Get counts
        counts = result.get_counts()
        
        # Get statevector if no measurements (for analysis)
        statevector = None
        if circuit.num_clbits == 0 or all(instr.operation.name != 'measure' for instr in circuit.data):
            statevector = Statevector.from_instruction(circuit)
            
        return {
            'counts': counts,
            'statevector': statevector,
            'transpiled_circuit': transpiled_circuit,
            'shots': shots
        }
    
    @weave.op()
    def analyze_bb84_protocol(self, alice_bits: List[int], alice_bases: List[int], 
                              bob_bases: List[int], shots: int = 1024) -> Dict:
        """Simulate BB84 protocol with given parameters"""
        if len(alice_bits) != len(alice_bases) or len(alice_bases) != len(bob_bases):
            raise ValueError("All input lists must have the same length")
        
        num_qubits = len(alice_bits)
        bob_bits = []
        
        # Simulate each qubit
        for i in range(num_qubits):
            # Create circuit for this qubit
            qc = QuantumCircuit(1, 1)
            
            # Alice's preparation
            if alice_bits[i] == 1:
                qc.x(0)  # |1> state
            if alice_bases[i] == 1:  # X basis
                qc.h(0)
            
            # Bob's measurement
            if bob_bases[i] == 1:  # X basis
                qc.h(0)
            qc.measure(0, 0)
            
            # Simulate
            result = self.simulate_circuit(qc, shots=1)
            measured_bit = int(list(result['counts'].keys())[0])
            bob_bits.append(measured_bit)
        
        # Calculate sifted key (where bases match)
        sifted_key_alice = []
        sifted_key_bob = []
        for i in range(num_qubits):
            if alice_bases[i] == bob_bases[i]:
                sifted_key_alice.append(alice_bits[i])
                sifted_key_bob.append(bob_bits[i])
        
        # Calculate error rate
        errors = sum(1 for a, b in zip(sifted_key_alice, sifted_key_bob) if a != b)
        error_rate = errors / len(sifted_key_alice) if sifted_key_alice else 0
        
        return {
            'alice_bits': alice_bits,
            'alice_bases': alice_bases,
            'bob_bases': bob_bases,
            'bob_bits': bob_bits,
            'sifted_key_alice': sifted_key_alice,
            'sifted_key_bob': sifted_key_bob,
            'error_rate': error_rate,
            'key_length': len(sifted_key_alice)
        }
    
    @weave.op()
    def estimate_quantum_resources(self, circuit: QuantumCircuit) -> Dict:
        """Estimate quantum resources required for a circuit"""
        # Count gates
        gate_counts = {}
        for instruction in circuit.data:
            gate_name = instruction.operation.name
            gate_counts[gate_name] = gate_counts.get(gate_name, 0) + 1
        
        # Calculate depth
        depth = circuit.depth()
        
        # Calculate width (number of qubits)
        width = circuit.num_qubits
        
        # Estimate T-count (important for fault tolerance)
        t_count = gate_counts.get('t', 0) + gate_counts.get('tdg', 0)
        
        return {
            'gate_counts': gate_counts,
            'depth': depth,
            'width': width,
            't_count': t_count,
            'total_gates': sum(gate_counts.values())
        }

# Example usage function
def run_bb84_example():
    """Run a simple BB84 example"""
    if not QISKIT_AVAILABLE:
        print("Qiskit not available, skipping example")
        return
    
    simulator = QuantumCircuitSimulator()
    
    # Example: 10 qubits with random choices
    np.random.seed(42)  # For reproducibility
    num_qubits = 10
    alice_bits = np.random.randint(0, 2, num_qubits).tolist()
    alice_bases = np.random.randint(0, 2, num_qubits).tolist()
    bob_bases = np.random.randint(0, 2, num_qubits).tolist()
    
    result = simulator.analyze_bb84_protocol(alice_bits, alice_bases, bob_bases)
    
    print("BB84 Protocol Simulation Results:")
    print(f"Alice's bits: {alice_bits}")
    print(f"Alice's bases: {alice_bases} (0=Z, 1=X)")
    print(f"Bob's bases: {bob_bases} (0=Z, 1=X)")
    print(f"Bob's bits: {result['bob_bits']}")
    print(f"Sifted key length: {result['key_length']}")
    print(f"Error rate: {result['error_rate']:.2f}")
    print(f"Sifted key (Alice): {result['sifted_key_alice']}")
    print(f"Sifted key (Bob): {result['sifted_key_bob']}")

if __name__ == "__main__":
    run_bb84_example()