from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class BB84SimulationParams(BaseModel):
    alice_bits: List[int]
    alice_bases: List[int]
    bob_bases: List[int]
    shots: int = 1024

class KeyPairResponse(BaseModel):
    public_key: str  # hex encoded
    secret_key: str  # hex encoded
    algorithm: str

class EncapsulateRequest(BaseModel):
    public_key: str  # hex encoded
    algorithm: Optional[str] = None

class EncapsulateResponse(BaseModel):
    ciphertext: str  # hex encoded
    shared_secret: str  # hex encoded
    algorithm: str

class DecapsulateRequest(BaseModel):
    ciphertext: str  # hex encoded
    secret_key: str  # hex encoded
    algorithm: Optional[str] = None

class DecapsulateResponse(BaseModel):
    shared_secret: str  # hex encoded
    algorithm: str

class SignRequest(BaseModel):
    message: str  # base64 or plain string
    algorithm: Optional[str] = None

class SignResponse(BaseModel):
    signature: str  # hex encoded
    public_key: str  # hex encoded
    secret_key: str  # hex encoded
    algorithm: str

class VerifyRequest(BaseModel):
    message: str
    signature: str  # hex encoded
    public_key: str  # hex encoded
    algorithm: Optional[str] = None

class VerifyResponse(BaseModel):
    is_valid: bool
    algorithm: str

class CryptoAlgorithm(BaseModel):
    name: str
    type: str  # 'KEM' or 'Signature'
    category: str  # 'Lattice-based', 'Isogeny-based', etc.
    security_level: int  # NIST level 1-5
    is_quantum_safe: bool = True

class Mission(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    assets: List[str] = []
    security_requirements: Dict[str, str] = {}

class SimulationResult(BaseModel):
    mission_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    algorithm_used: str
    success: bool
    performance_metrics: Dict[str, float]
    details: Optional[str] = None
