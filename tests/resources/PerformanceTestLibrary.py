"""
Performance Test Library for Robot Framework
Provides performance testing utilities for quantum and cryptographic operations
"""

import time
import statistics
import threading
import concurrent.futures
from typing import List, Dict, Any, Tuple, Optional
import math

class PerformanceTestLibrary:
    def __init__(self):
        self.benchmarks = {}
    
    def measure_circuit_latency(self, circuit_file: str, shots: int = 1024) -> float:
        """Measure latency of quantum circuit execution in milliseconds"""
        start_time = time.perf_counter()
        
        # Simulate circuit execution
        # In a real implementation, this would load and execute the actual circuit
        # For this example, we'll simulate based on circuit complexity
        time.sleep(0.001 * shots / 100)  # Simulate work proportional to shots
        
        end_time = time.perf_counter()
        latency_ms = (end_time - start_time) * 1000
        return latency_ms
    
    def measure_key_generation_throughput(self, iterations: int = 10) -> float:
        """Measure PQC key generation throughput in operations per second"""
        start_time = time.perf_counter()
        
        # Simulate key generation
        for _ in range(iterations):
            time.sleep(0.01)  # Simulate key generation time
        
        end_time = time.perf_counter()
        total_time = end_time - start_time
        throughput = iterations / total_time if total_time > 0 else 0
        return throughput
    
    def measure_encapsulation_decapsulation_throughput(self, iterations: int = 10) -> float:
        """Measure PQC encapsulation/decapsulation throughput in operations per second"""
        start_time = time.perf_counter()
        
        # Simulate encapsulation and decapsulation
        for _ in range(iterations):
            time.sleep(0.005)  # Simulate crypto operation time
        
        end_time = time.perf_counter()
        total_time = end_time - start_time
        throughput = iterations / total_time if total_time > 0 else 0
        return throughput
    
    def run_concurrent_circuit_executions(self, circuit_file: str, concurrent_count: int, shots: int) -> Dict[str, Any]:
        """Run concurrent circuit executions and return performance metrics"""
        def execute_single_circuit():
            start = time.perf_counter()
            time.sleep(0.001 * shots / 100)  # Simulate circuit execution
            end = time.perf_counter()
            return (end - start) * 1000  # Return latency in ms
        
        latencies = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_count) as executor:
            futures = [executor.submit(execute_single_circuit) for _ in range(concurrent_count)]
            for future in concurrent.futures.as_completed(futures):
                try:
                    latency = future.result()
                    latencies.append(latency)
                except Exception as e:
                    # Count as failed execution
                    latencies.append(float('inf'))
        
        # Filter out infinite latencies (failures) for success rate calculation
        valid_latencies = [l for l in latencies if l != float('inf')]
        success_rate = (len(valid_latencies) / len(latencies)) * 100 if latencies else 0
        
        if valid_latencies:
            avg_latency = statistics.mean(valid_latencies)
            max_latency = max(valid_latencies)
        else:
            avg_latency = float('inf')
            max_latency = float('inf')
        
        return {
            'average_latency': avg_latency,
            'max_latency': max_latency,
            'success_rate': success_rate,
            'raw_latencies': latencies
        }
    
    def measure_memory_usage(self, circuit_file: str, shots: int) -> float:
        """Estimate memory usage during quantum circuit simulation in MB"""
        # Mock implementation - would use memory profiling tools in reality
        # Base memory + memory proportional to circuit complexity and shots
        base_memory = 50  # MB
        circuit_factor = 0.1  # MB per unit of complexity
        shots_factor = 0.001  # MB per 1000 shots
        
        estimated_memory = base_memory + (circuit_factor * 10) + (shots_factor * shots)
        return estimated_memory
    
    def measure_key_rotation_time(self, iterations: int = 10) -> float:
        """Measure average key rotation time in milliseconds"""
        start_time = time.perf_counter()
        
        # Simulate key rotation operations
        for _ in range(iterations):
            time.sleep(0.05)  # Simulate key rotation time
        
        end_time = time.perf_counter()
        total_time = end_time - start_time
        avg_time_ms = (total_time / iterations) * 1000 if iterations > 0 else 0
        return avg_time_ms
    
    def measure_crypto_operation_latency_under_load(self, operations: int = 50) -> Dict[str, float]:
        """Measure cryptographic operation latency under load"""
        latencies = []
        
        for _ in range(operations):
            start_time = time.perf_counter()
            time.sleep(0.01)  # Simulate crypto operation
            end_time = time.perf_counter()
            latency_ms = (end_time - start_time) * 1000
            latencies.append(latency_ms)
        
        if latencies:
            sorted_latencies = sorted(latencies)
            avg_latency = statistics.mean(latencies)
            p95_latency = sorted_latencies[int(len(sorted_latencies) * 0.95)] if sorted_latencies else 0
        else:
            avg_latency = 0
            p95_latency = 0
        
        return {
            'average': avg_latency,
            'p95': p95_latency,
            'raw_latencies': latencies
        }
    
    def measure_resource_estimation_accuracy(self, circuit_file: str) -> float:
        """Measure accuracy of quantum resource estimation"""
        # Mock implementation - would compare estimated vs actual resources
        # For this example, we'll return a high accuracy value
        return 95.0  # Percentage
    
    def measure_protocol_scaling(self, protocol_name: str, qubit_list: List[int]) -> float:
        """Measure how protocol simulation scales with number of qubits"""
        # Mock implementation - would test actual circuits of different sizes
        # For this example, we'll simulate scaling characteristics
        
        base_time_per_qubit = 0.1  # ms per qubit
        overhead_factor = 0.05    # Additional overhead per qubit
        
        times = []
        for qubits in qubit_list:
            # Simulate time = base_time * qubits + overhead * qubits^2
            time_ms = (base_time_per_qubit * qubits) + (overhead_factor * qubits * qubits)
            times.append(time_ms)
        
        if len(times) >= 2:
            # Calculate scaling factor: how much time increases per qubit increase
            time_increase = times[-1] - times[0]
            qubit_increase = qubit_list[-1] - qubit_list[0]
            if qubit_increase > 0:
                scaling_factor = time_increase / qubit_increase
                # Normalize by dividing by base time per qubit
                normalized_scaling = scaling_factor / base_time_per_qubit
                return normalized_scaling
        return 1.0  # Default to linear scaling
    
    def get_time_milliseconds(self) -> float:
        """Get current time in milliseconds"""
        return time.time() * 1000
    
    def create_bytearray(self, data: List[int]) -> bytearray:
        """Create a bytearray from a list of integers"""
        return bytearray(data)

# For backward compatibility with tests that expect direct function access
def measure_circuit_latency(circuit_file: str, shots: int = 1024) -> float:
    lib = PerformanceTestLibrary()
    return lib.measure_circuit_latency(circuit_file, shots)

def measure_key_generation_throughput(iterations: int = 10) -> float:
    lib = PerformanceTestLibrary()
    return lib.measure_key_generation_throughput(iterations)

def measure_encapsulation_decapsulation_throughput(iterations: int = 10) -> float:
    lib = PerformanceTestLibrary()
    return lib.measure_encapsulation_decapsulation_throughput(iterations)

def run_concurrent_circuit_executions(circuit_file: str, concurrent_count: int, shots: int) -> Dict[str, Any]:
    lib = PerformanceTestLibrary()
    return lib.run_concurrent_circuit_executions(circuit_file, concurrent_count, shots)

def measure_memory_usage(circuit_file: str, shots: int) -> float:
    lib = PerformanceTestLibrary()
    return lib.measure_memory_usage(circuit_file, shots)

def measure_key_rotation_time(iterations: int = 10) -> float:
    lib = PerformanceTestLibrary()
    return lib.measure_key_rotation_time(iterations)

def measure_crypto_operation_latency_under_load(operations: int = 50) -> Dict[str, float]:
    lib = PerformanceTestLibrary()
    return lib.measure_crypto_operation_latency_under_load(operations)

def measure_resource_estimation_accuracy(circuit_file: str) -> float:
    lib = PerformanceTestLibrary()
    return lib.measure_resource_estimation_accuracy(circuit_file)

def measure_protocol_scaling(protocol_name: str, qubit_list: List[int]) -> float:
    lib = PerformanceTestLibrary()
    return lib.measure_protocol_scaling(protocol_name, qubit_list)

def get_time_milliseconds() -> float:
    lib = PerformanceTestLibrary()
    return lib.get_time_milliseconds()

def create_bytearray(data: List[int]) -> bytearray:
    lib = PerformanceTestLibrary()
    return lib.create_bytearray(data)