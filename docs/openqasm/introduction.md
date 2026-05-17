# OpenQASM Introduction

This document provides an introduction to OpenQASM 3.0 usage in the Quantum-Safe Mission Communications Planner.

## What is OpenQASM?

Open Quantum Assembly Language (OpenQASM) is an intermediate representation for quantum instructions. Version 3.0 introduces significant improvements including:

- Classical computation integration
- Unified quantum-classical control flow
- Support for heterogeneous quantum systems
- Improved modularity and composability

## Usage in QSCM Planner

In this project, OpenQASM is used to:

1. **Define Quantum Protocols**: BB84, E91, and other QKD protocols
2. **Simulate Attacks**: Model eavesdropping and other quantum threats
3. **Estimate Resources**: Calculate gate counts, depth, and qubit requirements
4. **Validate Circuits**: Ensure correctness before execution on quantum hardware

## Circuit Directory Structure

```
src/quantum/circuits/
├── bb84.qasm              # BB84 protocol implementation
├── e91.qasm               # E91 protocol implementation  
├── bb84_with_eavesdropping.qasm  # BB84 with intercept-resend attack
└── templates/             # Reusable circuit components
```

## Example: Basic BB84 Circuit

```qasm
OPENQASM 3.0;
include "qelib1.inc";

// Alice prepares qubit in |0> or |1> state
// Then applies Hadamard if using X basis
qubit[1] q;
bit[1] c;

// Prepare |0> state (default)
// Apply X if sending |1>
// Apply H if using X basis

// Measurement
measure q[0] -> c[0];
```

## Validation

All OpenQASM files are validated in the CI pipeline to ensure:
- Proper OPENQASM 3.0 header
- Valid QASM syntax
- Compatibility with target simulators
- Security checks for malicious content

For more information, see the [OpenQASM 3.0 specification](https://openqasm.com/language/).