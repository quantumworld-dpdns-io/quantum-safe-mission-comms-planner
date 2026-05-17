import duckdb
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional
import os

class MissionDataManager:
    def __init__(self, db_path: str = "data/mission_planner.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = duckdb.connect(self.db_path)
        self._initialize_tables()

    def _initialize_tables(self):
        """Initialize DuckDB tables for missions and simulation results"""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS missions (
                id VARCHAR PRIMARY KEY,
                name VARCHAR,
                description TEXT,
                start_date TIMESTAMP,
                end_date TIMESTAMP,
                assets JSON,
                security_requirements JSON
            )
        """)
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS simulation_results (
                mission_id VARCHAR,
                timestamp TIMESTAMP,
                algorithm_used VARCHAR,
                success BOOLEAN,
                performance_metrics JSON,
                details TEXT
            )
        """)

    def add_mission(self, mission_data: Dict[str, Any]):
        """Add a mission to the database"""
        import json
        self.conn.execute("""
            INSERT OR REPLACE INTO missions VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [
            mission_data['id'],
            mission_data['name'],
            mission_data.get('description'),
            mission_data['start_date'],
            mission_data['end_date'],
            json.dumps(mission_data.get('assets', [])),
            json.dumps(mission_data.get('security_requirements', {}))
        ])

    def add_simulation_result(self, result: Dict[str, Any]):
        """Add a simulation result to the database"""
        import json
        self.conn.execute("""
            INSERT INTO simulation_results VALUES (?, ?, ?, ?, ?, ?)
        """, [
            result['mission_id'],
            result.get('timestamp', datetime.now()),
            result['algorithm_used'],
            result['success'],
            json.dumps(result.get('performance_metrics', {})),
            result.get('details')
        ])

    def get_missions(self) -> pd.DataFrame:
        """Get all missions as a Pandas DataFrame"""
        return self.conn.execute("SELECT * FROM missions").df()

    def get_simulation_results(self, mission_id: Optional[str] = None) -> pd.DataFrame:
        """Get simulation results, optionally filtered by mission_id"""
        if mission_id:
            return self.conn.execute("SELECT * FROM simulation_results WHERE mission_id = ?", [mission_id]).df()
        return self.conn.execute("SELECT * FROM simulation_results").df()

    def close(self):
        self.conn.close()
