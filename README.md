# Quantum-Safe Mission Communications Planner

> Quantum-safe mission communications planner – maps cryptographic dependencies and simulates key rotations for long-life space missions

This repository implements a comprehensive quantum-safe communications planning system for space missions, featuring OpenQASM-based quantum circuit simulations, post-quantum cryptography, comprehensive testing frameworks (including OWASP Top 10 security tests), and robust CI/CD pipelines.

## Overview

The Quantum-Safe Mission Communications Planner is designed to address the cryptographic challenges posed by quantum computing to long-duration space missions. It provides tools for:

- Simulating quantum key distribution protocols (BB84, E91) using OpenQASM
- Implementing and testing post-quantum cryptographic algorithms
- Modeling cryptographic dependencies for mission planning
- Simulating key rotation strategies under quantum threat models
- Comprehensive security testing aligned with OWASP Top 10
- Performance benchmarking and validation
- Automated CI/CD pipelines with security gates

## Features

### 🔬 Quantum Computing Integration
- **OpenQASM 3.0 Support**: Native support for quantum circuit specification and simulation
- **Protocol Simulations**: BB84 and E91 quantum key distribution protocols
- **Attack Modeling**: Eavesdropping attack simulations (intercept-resend)
- **Resource Estimation**: Quantum resource analysis (gate count, depth, width)
- **Multiple Backends**: Compatible with Qiskit, Cirq, and other quantum simulators

### 🔐 Post-Quantum Cryptography
- **PQC Algorithm Integration**: Kyber, Dilithium, Falcon, NTRU, and more via liboqs
- **Hybrid Cryptography**: Combining classical and post-quantum approaches
- **Key Management**: Automated key generation, encapsulation, and decapsulation
- **Digital Signatures**: PQC-based message authentication and integrity

### 🧪 Comprehensive Testing Framework
- **Robot Foundation**: Keyword-driven testing for maintainability
- **Functional Tests**: Quantum protocol validation and correctness
- **Security Tests**: Full OWASP Top 10 coverage:
  - A01: Broken Access Control
  - A02: Cryptographic Failures
  - A03: Injection
  - A04: Insecure Design
  - A05: Security Misconfiguration
  - A06: Vulnerable Components
  - A07: Identification & Authentication Failures
  - A08: Software & Data Integrity Failures
  - A09: Security Logging & Monitoring Failures
  - A10: Server-Side Request Forgery
- **Performance Tests**: Latency, throughput, scalability, and resource usage

### 🔄 Robust CI/CD Pipeline
- **Multi-Stage Pipeline**: Build, test, security, performance, and deployment
- **Security Gates**: Automated vulnerability scanning with Bandit, Safety, and OWASP ZAP
- **Performance Benchmarking**: Regression detection and optimization tracking
- **Container Security**: Trivy-based image scanning
- **Automated Documentation**: MKDocs-based documentation generation
- **Release Management**: Automated versioning and GitHub releases

### 📦 Software-Tools Integration
- **Cloud-Native Security**: Cilium Tetragon for runtime protection
- **Data Lakehouse**: Apache Arrow/Pandas for efficient cryptographic metadata handling
- **Vector Databases**: Weaviate/Qdrant for semantic cryptographic dependency graphs
- **AI-Assisted Development**: Integration with Claude Code and other AI agents

## Project Structure

```
quantum-safe-mission-comms-planner/
├── src/
│   ├── quantum/              # Quantum computing components
│   │   ├── circuits/         # OpenQASM 3.0 circuit definitions
│   │   ├── protocols/        # Quantum protocol implementations (BB84, E91)
│   │   └── utils/            # Quantum simulation utilities
│   ├── crypto/               # Cryptographic components
│   │   └── pqc.py            # Post-quantum cryptography implementations
│   ├── models/               # Cryptographic dependency models
│   └── api/                  # REST/gRPC service interfaces
├── tests/
│   ├── robot/                # Robot Framework test suites
│   │   ├── functional/       # Functional validity tests
│   │   ├── security/         # OWASP Top 10 security tests
│   │   └── performance/      # Performance and load tests
│   ├── unit/                 # Unit tests
│   └── integration/          # Integration tests
├── docs/
│   ├── openqasm/             # OpenQASM specifications and usage guides
│   ├── architecture/         # System design documents
│   └── api/                  # API documentation
├── .github/
│   └── workflows/
│       ├── ci.yml            # Enhanced CI/CD pipeline
│       ├── security.yml      # Dedicated security scanning
│       └── release.yml       # Release management
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
└── robot-framework.yaml      # Robot Framework configuration
```

## Getting Started

### Prerequisites
- Python 3.11+
- C compiler (for building some dependencies)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/quantumworld-dpdns-io/quantum-safe-mission-comms-planner.git
cd quantum-safe-mission-comms-planner

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install system-level dependencies for quantum libraries
# On Ubuntu/Debian:
# sudo apt-get install -y build-essential cmake libgmp-dev libssl-dev
```

### Running Tests

#### Unit Tests
```bash
python -m pytest tests/unit/ -v
```

#### Functional Tests (Robot Framework)
```bash
robot --outputdir reports/functional tests/robot/functional/
```

#### Security Tests (OWASP Top 10)
```bash
robot --outputdir reports/security tests/robot/security/
```

#### Performance Tests
```bash
robot --outputdir reports/performance tests/robot/performance/
```

#### Full Test Suite
```bash
# Run all test types
robot --outputdir reports/ tests/robot/
```

### Usage Examples

#### Quantum Circuit Simulation
```python
from src.quantum.utils.simulator import QuantumCircuitSimulator

simulator = QuantumCircuitSimulator()
circuit = simulator.load_qasm_file("src/quantum/circuits/bb84.qasm")
results = simulator.simulate_circuit(circuit, shots=1024)
print(f"Measurement results: {results['counts']}")
```

#### Post-Quantum Cryptography
```python
from src.crypto.pqc import PQCManager

pqc = PQCManager()
public_key, secret_key = pqc.generate_keypair()
ciphertext, shared_secret = pqc.encapsulate(public_key)
decrypted_secret = pqc.decapsulate(ciphertext, secret_key)
assert shared_secret == decrypted_secret
```

#### BB84 Protocol Simulation
```python
from src.quantum.utils.simulator import QuantumCircuitSimulator

simulator = QuantumCircuitSimulator()
# Alice sends bit 0 in X basis, Bob measures in X basis
result = simulator.analyze_bb84_protocol(
    alice_bits=[0],
    alice_bases=[1],  # 1 = X basis
    bob_bases=[1],    # 1 = X basis
    shots=1024
)
print(f"Sifted key length: {result['key_length']}")
print(f"Error rate: {result['error_rate']:.2f}")
```

## Configuration

### Environment Variables
- `QSCM_PQC_DEFAULT_KEM`: Default KEM algorithm (default: Kyber768)
- `QSCM_PQC_DEFAULT_SIGN`: Default signature algorithm (default: Dilithium3)
- `QSCM_QUANTUM_SHOTS`: Default number of shots for quantum simulation (default: 1024)
- `QSCM_SECURITY_LOG_LEVEL`: Security logging level (default: INFO)

### Robot Framework Configuration
See `robot-framework.yaml` for test execution settings, library imports, and variable files.

## API Documentation

API documentation is available in the `docs/api/` directory and can be generated locally with:

```bash
mkdocs serve
```

Then visit http://localhost:8000

## Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) before submitting pull requests.

We welcome contributions that:
- Improve quantum circuit simulations
- Add new PQC algorithm support
- Enhance security test coverage
- Optimize performance
- Improve documentation
- Fix bugs

## Security

### Security Testing
This project implements comprehensive security testing aligned with the OWASP Top 10:
- Automated security scanning in CI/CD pipeline
- Regular dependency vulnerability checks
- Runtime protection mechanisms
- Secure coding practices

### Reporting Security Issues
Please report security vulnerabilities through GitHub Security Advisories or contact the maintainers directly.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built as part of the [quantumworld-dpdns-io](https://github.com/quantumworld-dpdns-io) Wild SaaS & Tech Development initiative
- Uses OpenQASM 3.0 standard for quantum circuit representation
- Integrates with liboqs for post-quantum cryptographic algorithms
- Leverages Robot Framework for comprehensive testing
- Inspired by quantum-safe communication protocols for space applications

## Roadmap

See [docs/roadmap.md](docs/roadmap.md) for planned features and enhancements.

---
*Last updated: $(date)*
*Version: 1.0.0-dev*