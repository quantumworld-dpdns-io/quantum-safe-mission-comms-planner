from fastapi import FastAPI, HTTPException, Depends
from typing import List, Dict, Any
from src.models.schemas import Mission, SimulationResult, CryptoAlgorithm
from src.crypto.pqc import PQCManager
from src.quantum.utils.data_manager import MissionDataManager
from src.quantum.utils.simulator import QuantumCircuitSimulator
import os
import weave

# Initialize Weave
weave.init("quantum-safe-mission-planner")

app = FastAPI(
    title="Quantum-Safe Mission Comms Planner API",
    description="API for planning and simulating quantum-safe mission communications",
    version="0.1.0"
)

# Initialize managers
pqc_manager = PQCManager()
data_manager = MissionDataManager()
quantum_simulator = QuantumCircuitSimulator()

@app.get("/")
async def root():
    return {"message": "Welcome to the Quantum-Safe Mission Comms Planner API"}

@app.get("/algorithms", response_model=Dict[str, List[str]])
async def get_algorithms():
    return pqc_manager.get_available_algorithms()

@app.post("/missions", response_model=Mission)
async def create_mission(mission: Mission):
    try:
        data_manager.add_mission(mission.dict())
        return mission
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/missions", response_model=List[Dict[str, Any]])
async def list_missions():
    df = data_manager.get_missions()
    return df.to_dict(orient="records")

@app.post("/simulate/bb84")
async def simulate_bb84(params: Dict[str, Any]):
    """
    Simulate BB84 protocol
    Expected params: alice_bits, alice_bases, bob_bases
    """
    try:
        result = quantum_simulator.analyze_bb84_protocol(
            params['alice_bits'],
            params['alice_bases'],
            params['bob_bases']
        )
        
        # Save result if mission_id is provided
        if 'mission_id' in params:
            sim_result = {
                'mission_id': params['mission_id'],
                'algorithm_used': 'BB84',
                'success': result['error_rate'] < 0.15,  # Threshold for success
                'performance_metrics': {
                    'error_rate': result['error_rate'],
                    'key_length': result['key_length']
                },
                'details': f"Sifted key: {result['sifted_key_alice']}"
            }
            data_manager.add_simulation_result(sim_result)
            
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/results/{mission_id}", response_model=List[Dict[str, Any]])
async def get_results(mission_id: str):
    df = data_manager.get_simulation_results(mission_id)
    return df.to_dict(orient="records")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
