# Quantum-Safe Mission Communications Planner

> A production-ready polyglot microservices platform for planning, simulating, and analyzing quantum-safe mission communications.

## 🏗️ Architecture

The system is built using a modern microservices architecture to ensure scalability, performance, and maintainability:

- **Frontend (Next.js)**: A responsive, high-fidelity dashboard built with React, TypeScript, and Tailwind CSS. Located in `frontend/`.
- **Core Backend (Go)**: A high-concurrency gateway built with Gin, managing mission state (DuckDB) and security policies (Chroma Vector DB). Located in `services/go-core/`.
- **Simulation Microservice (Python)**: A specialized worker service for quantum simulations (Qiskit), post-quantum cryptography (liboqs), and ML observability (W&B Weave). Located in `services/python/`.

## 🚀 Key Features

### 🔬 Quantum Computing & Cryptography
- **Protocol Simulations**: Native support for BB84, E91, and custom OpenQASM 3.0 circuits.
- **PQC Algorithm Integration**: Kyber, Dilithium, Falcon, NTRU via liboqs.
- **Hybrid Cryptography**: Combining classical and post-quantum approaches for transition security.
- **Resource Analysis**: Quantum resource estimation (gate count, depth, width).

### 🧠 AI & Data Intelligence
- **Semantic Search**: AI-powered security policy management using **ChromaDB**.
- **Analytical Insights**: Local analytical SQL engine (**DuckDB**) for mission metrics and log archival.
- **Observability**: Trace and evaluate every quantum operation with **Weights & Biases Weave**.

### 🧪 Comprehensive Testing & Security
- **Robot Framework**: Keyword-driven functional and end-to-end testing.
- **OWASP Top 10 Security**: Dedicated security test suite covering common web and cryptographic vulnerabilities.
- **CI/CD Pipeline**: Polyglot pipeline for linting, security scanning, and automated testing across Go, Python, and Next.js.

## 📦 Project Structure

```
quantum-safe-mission-comms-planner/
├── frontend/               # Next.js Frontend (React, TS, Tailwind)
├── services/
│   ├── go-core/            # Go Core Backend (Gin, DuckDB, Chroma)
│   └── python/             # Python Worker (FastAPI, Qiskit, liboqs, Weave)
├── data/                   # Shared data storage (DuckDB, Chroma)
├── tests/                  # Root E2E and Functional tests (Robot Framework)
├── .github/                # Polyglot CI/CD Workflows
└── README.md
```

## 🛠️ Getting Started

### Prerequisites
- Go 1.21+
- Python 3.11+
- Node.js 18+
- liboqs (system dependency)

### Installation

```bash
# Clone the repository
git clone https://github.com/quantumworld-dpdns-io/quantum-safe-mission-comms-planner.git
cd quantum-safe-mission-comms-planner

# 1. Setup Python Worker
cd services/python
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Setup Go Core
cd ../go-core
go mod download

# 3. Setup Frontend
cd ../../frontend
npm install
```

### Running the Platform

```bash
# Start Python Worker (Port 8082)
cd services/python && python api/main.py

# Start Go Core (Port 8080)
cd services/go-core && go run main.go

# Start Frontend (Port 3000)
cd frontend && npm run dev
```

## 🧪 Testing

### Functional & Security Tests (Robot Framework)
```bash
# Ensure services are running, then:
robot --outputdir reports/functional tests/robot/functional/
robot --outputdir reports/security tests/robot/security/
```

## 🛡️ Security

This project implements comprehensive security testing aligned with the **OWASP Top 10**, including automated security scanning (Bandit, Safety, GoSec) in the CI/CD pipeline and dedicated runtime protection strategies.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Built as part of the [quantumworld-dpdns-io](https://github.com/quantumworld-dpdns-io) initiative.*
