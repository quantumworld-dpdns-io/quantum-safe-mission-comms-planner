from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any, Optional
from models.schemas import (
    BB84SimulationParams, 
    KeyPairResponse, 
    EncapsulateRequest, 
    EncapsulateResponse,
    DecapsulateRequest, 
    DecapsulateResponse,
    SignRequest, 
    SignResponse,
    VerifyRequest, 
    VerifyResponse
)
from crypto.pqc import PQCManager
from quantum.utils.simulator import QuantumCircuitSimulator
import os
import weave
import binascii

# Initialize W&B Weave
weave.init("quantum-safe-mission-planner")

app = FastAPI(
    title="Quantum-Safe Mission Comms Worker Service",
    description="Worker service for quantum simulations and PQC operations",
    version="0.2.0"
)

# Initialize managers
pqc_manager = PQCManager()
quantum_simulator = QuantumCircuitSimulator()

@app.get("/")
@weave.op()
async def root():
    return {"message": "Quantum-Safe Mission Comms Worker Service is running"}

@app.get("/algorithms")
@weave.op()
async def get_algorithms():
    return pqc_manager.get_available_algorithms()

@app.post("/simulate/bb84")
@weave.op()
async def simulate_bb84(params: BB84SimulationParams):
    """
    Simulate BB84 protocol
    """
    try:
        result = quantum_simulator.analyze_bb84_protocol(
            params.alice_bits,
            params.alice_bases,
            params.bob_bases,
            params.shots
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/crypto/generate-key", response_model=KeyPairResponse)
@weave.op()
async def generate_key(algorithm: Optional[str] = None):
    try:
        alg = algorithm or pqc_manager.default_kem
        pub, sec = pqc_manager.generate_keypair(alg)
        return KeyPairResponse(
            public_key=binascii.hexlify(pub).decode(),
            secret_key=binascii.hexlify(sec).decode(),
            algorithm=alg
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/crypto/encapsulate", response_model=EncapsulateResponse)
@weave.op()
async def encapsulate(request: EncapsulateRequest):
    try:
        alg = request.algorithm or pqc_manager.default_kem
        pub_key = binascii.unhexlify(request.public_key)
        ciphertext, shared_secret = pqc_manager.encapsulate(pub_key, alg)
        return EncapsulateResponse(
            ciphertext=binascii.hexlify(ciphertext).decode(),
            shared_secret=binascii.hexlify(shared_secret).decode(),
            algorithm=alg
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/crypto/decapsulate", response_model=DecapsulateResponse)
@weave.op()
async def decapsulate(request: DecapsulateRequest):
    try:
        alg = request.algorithm or pqc_manager.default_kem
        ciphertext = binascii.unhexlify(request.ciphertext)
        secret_key = binascii.unhexlify(request.secret_key)
        shared_secret = pqc_manager.decapsulate(ciphertext, secret_key, alg)
        return DecapsulateResponse(
            shared_secret=binascii.hexlify(shared_secret).decode(),
            algorithm=alg
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/crypto/sign", response_model=SignResponse)
@weave.op()
async def sign(request: SignRequest):
    try:
        alg = request.algorithm or pqc_manager.default_sign
        message_bytes = request.message.encode()
        signature, pub, sec = pqc_manager.sign_message(message_bytes, alg)
        return SignResponse(
            signature=binascii.hexlify(signature).decode(),
            public_key=binascii.hexlify(pub).decode(),
            secret_key=binascii.hexlify(sec).decode(),
            algorithm=alg
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/crypto/verify", response_model=VerifyResponse)
@weave.op()
async def verify(request: VerifyRequest):
    try:
        alg = request.algorithm or pqc_manager.default_sign
        message_bytes = request.message.encode()
        signature = binascii.unhexlify(request.signature)
        pub_key = binascii.unhexlify(request.public_key)
        is_valid = pqc_manager.verify_signature(message_bytes, signature, pub_key, alg)
        return VerifyResponse(
            is_valid=is_valid,
            algorithm=alg
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)
