OPENQASM 3.0;
include "qelib1.inc";

// BB84 Quantum Key Distribution Protocol Simulation
// Alice prepares qubits in random bases (Z or X)
// Bob measures in random bases

// Qubits: 0 - Alice's qubit, 1 - Bob's measurement qubit (for simulation)
qubit[2] q;

// Classical bits for basis choice and measurement results
bit[2] alice_basis; // 0 for Z, 1 for X
bit[2] bob_basis;   // 0 for Z, 1 for X
bit[2] alice_bit;   // Alice's encoded bit
bit[2] bob_bit;     // Bob's measured bit

// Alice's qubit preparation
// Encode random bit in random basis
// For simplicity, we fix the bit to 0 and vary basis in this example
// In a full simulation, we would randomize both

// Basis choice: 0 = Z basis, 1 = X basis
// We'll simulate one qubit for demonstration

// Prepare |0> state (already |0> by default)
// Apply Hadamard if Alice chooses X basis
x q[0]; // Set to |1> for simplicity, then we can flip basis
// Actually, let's start fresh: prepare |0> then apply basis

// Reset to |0>
reset q[0];
// Alice's bit (0 or 1) - we'll set to 0 for now, but basis will determine encoding
// If Alice's basis is X, apply H to |0> to get |+>
// If Alice's basis is Z, leave |0> as is for |0>, or apply X then Z basis for |1>
// We'll do: if alice_basis == 1, apply H; if alice_bit == 1, apply X before basis

// For simplicity in this example, we'll fix:
// Alice's bit = 0
// Alice's basis = 0 (Z) or 1 (X) - we'll make it a parameter later

// Apply X gate if Alice's bit is 1
// We'll set alice_bit[0] = 0 for now, so skip X

// Apply basis
// If alice_basis[0] == 1, apply H
// We'll set alice_basis[0] = 1 for this run to demonstrate X basis
// In a full simulation, we would loop over many qubits with random choices

// Let's set Alice's basis to X (1) for this example
// We'll use a classical gate to conditionally apply H, but OpenQASM 3 doesn't have direct classical control in this way withoutif
// Instead, we'll use the classical bits to control gates via if statements (if supported) or we'll simulate by having two versions

// Since we want a parameterized circuit, we'll use the following approach:
// We'll create a function or use parameters, but for simplicity in this example, we'll hardcode one scenario and note that it should be parameterized.

// For the purpose of this example, we'll show:
// Case 1: Alice sends |0> in Z basis (no gates)
// Case 2: Alice sends |0> in X basis (apply H)
// Case 3: Alice sends |1> in Z basis (apply X)
// Case 4: Alice sends |1> in X basis (apply X then H)

// We'll pick Case 2: Alice sends |0> in X basis

// Prepare |0> (already)
h q[0]; // Apply Hadamard to get |+> state (for X basis with bit 0)

// Bob's measurement: choose random basis
// We'll set Bob's basis to X (1) for this example to match Alice
// If Bob's basis is Z, measure directly
// If Bob's basis is X, apply H before measuring

// Set Bob's basis to X (1)
h q[0]; // Apply H before measurement if in X basis

// Measure
measure q[0] -> bob_bit[0];
// Note: In a real simulation, we would also record Alice's basis and bit, and Bob's basis
// and then sift the keys where bases matched.

// For simplicity, we only measure one qubit here.

// End of circuit