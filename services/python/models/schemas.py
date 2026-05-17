from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

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
    assets: List[str] = []  # List of satellite/ground station IDs
    security_requirements: Dict[str, str] = {}

class KeyRotationPolicy(BaseModel):
    mission_id: str
    algorithm: str
    rotation_interval_days: int
    last_rotation: Optional[datetime] = None
    next_rotation: Optional[datetime] = None

class SimulationResult(BaseModel):
    mission_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    algorithm_used: str
    success: bool
    performance_metrics: Dict[str, float]
    details: Optional[str] = None
