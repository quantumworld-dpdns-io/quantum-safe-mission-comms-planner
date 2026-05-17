"""
Security Test Library for Robot Framework
Provides security testing utilities including OWASP Top 10 checks
"""

import os
import json
import base64
import hashlib
import hmac
import secrets
import subprocess
import socket
import ipaddress
import requests
from typing import List, Dict, Any, Tuple, Optional
import urllib.parse
import re

class SecurityTestLibrary:
    def __init__(self):
        self.security_logs = []
        self.alert_config = {
            'failed_login_threshold': 5,
            'alert_email': 'admin@example.com'
        }
        self.test_states = []

    def send_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Send an HTTP request and return a dictionary with status_code and body"""
        capture_response = kwargs.pop('capture_response', True)
        try:
            response = requests.request(method, url, **kwargs)
            result = {
                'status_code': str(response.status_code),
                'headers': dict(response.headers),
            }
            if capture_response:
                try:
                    result['body'] = response.json()
                except:
                    result['body'] = response.text
            
            # For some reason the robot tests expect 'body' to be directly accessible
            # and sometimes they want the whole response object-like dict
            # We also add specific fields that the robot tests use
            if 'access_token' in result.get('body', {}) if isinstance(result.get('body'), dict) else False:
                result['access_token'] = result['body']['access_token']
            
            return result
        except Exception as e:
            return {'status_code': '500', 'body': str(e), 'error': str(e)}

    def log_security_test_state(self):
        """Log the state after a security test"""
        self.test_states.append(self._get_timestamp())

    def run_command(self, command: str, *args) -> str:
        """Run a shell command and return its output"""
        full_command = f"{command} {' '.join(args)}"
        try:
            result = subprocess.check_output(full_command, shell=True, stderr=subprocess.STDOUT)
            return result.decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            return e.output.decode('utf-8').strip()

    def generate_fuzz_payloads(self, fuzz_type: str = 'xss') -> List[str]:
        """Generate a list of fuzzing payloads"""
        if fuzz_type == 'xss':
            return [
                '<script>alert(1)</script>',
                '<img src=x onerror=alert(1)>',
                '"><script>alert(1)</script>',
                "javascript:alert(1)"
            ]
        elif fuzz_type == 'sql':
            return [
                "' OR '1'='1",
                "'; DROP TABLE users; --",
                "1; SELECT * FROM information_schema.tables",
                "' UNION SELECT NULL, NULL, NULL --"
            ]
        return ["test", "fuzz", "1234"]

    # A01: Broken Access Control
    def check_access_control(self, user_role: str, resource: str, action: str) -> bool:
        """Check if a user role can perform an action on a resource"""
        # Mock implementation - in reality would check against policy engine
        access_matrix = {
            'admin': {'*': ['*']},  # Admin can do anything
            'viewer': {'quantum/circuits': ['read'], 'crypto/keys': []},  # Viewer can only read circuits
            'operator': {'quantum/circuits': ['read', 'execute'], 'crypto/keys': ['use']},
        }
        
        if user_role not in access_matrix:
            return False
        
        role_permissions = access_matrix[user_role]
        # Check for wildcard permissions
        if '*' in role_permissions and '*' in role_permissions['*']:
            return True
        
        # Check specific resource
        if resource in role_permissions:
            return action in role_permissions[resource]
        
        # Check for wildcard resource
        if '*' in role_permissions:
            return action in role_permissions['*']
        
        return False
    
    # A02: Cryptographic Failures
    def is_weak_algorithm(self, algorithm: str) -> bool:
        """Check if an algorithm is considered weak or deprecated"""
        weak_algorithms = {
            'RSA': {'key_size': 1024},  # RSA with key size < 2048 is weak
            'DSA': {},  # DSA is deprecated
            'ECDSA': {'hash': 'SHA1'},  # ECDSA with SHA1 is weak
            'HMAC': {'hash': 'MD5'},  # HMAC-MD5 is weak
            'DES': {},  # DES is weak
            '3DES': {},  # 3DES is deprecated
            'RC4': {}   # RC4 is weak
        }
        
        # This is a simplified check - real implementation would be more complex
        for weak_alg, conditions in weak_algorithms.items():
            if weak_alg.upper() in algorithm.upper():
                return True
        return False
    
    def get_pqc_algorithm_security_level(self, algorithm: str) -> int:
        """Get the security level (in bits) of a PQC algorithm"""
        # Approximate security levels for NIST PQC candidates
        security_levels = {
            'Kyber512': 128,
            'Kyber768': 192,
            'Kyber1024': 256,
            'Dilithium2': 128,
            'Dilithium3': 192,
            'Dilithium5': 256,
            'Falcon-512': 128,
            'Falcon-1024': 256,
            'NTRU': 128,
            'Saber': 128
        }
        return security_levels.get(algorithm, 128)  # Default to 128 if unknown
    
    # A03: Injection
    def sanitize_input(self, input_str: str) -> str:
        """Sanitize input to prevent injection attacks"""
        # Remove potential SQL injection patterns
        sql_patterns = [
            r'(?i)\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION)\b',
            r'[\';--]',
            r'/\*.*\*/'
        ]
        sanitized = input_str
        for pattern in sql_patterns:
            sanitized = re.sub(pattern, '', sanitized)
        
        # Remove potential command injection patterns
        cmd_patterns = [
            r'[;&|`$\\]',
            r'\$\{.*\}',
            r'\\(.*\\)'
        ]
        for pattern in cmd_patterns:
            sanitized = re.sub(pattern, '', sanitized)
        
        # Remove potential XSS patterns
        xss_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'on\w+\s*='
        ]
        for pattern in xss_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        return sanitized.strip()
    
    def is_valid_openqasm(self, qasm_str: str) -> Tuple[bool, Optional[str]]:
        """Basic validation of OpenQASM string to prevent injection"""
        # Check for obvious malicious patterns
        malicious_patterns = [
            r'//.*?(rm -rf|del|format)',
            r'/\*.*?(rm -rf|del|format).*?\*/',
            r'(?i)(exec|system|popen|subprocess)',
            r'[\\/\.\.]*[\\\/][\\\/]'
        ]
        
        for pattern in malicious_patterns:
            if re.search(pattern, qasm_str, re.IGNORECASE):
                return False, f"Potentially malicious pattern detected: {pattern}"
        
        # Check that it starts with OPENQASM
        if not qasm_str.strip().startswith('OPENQASM'):
            return False, "Does not start with OPENQASM declaration"
        
        # Check for balanced braces (simple check)
        open_braces = qasm_str.count('{')
        close_braces = qasm_str.count('}')
        if open_braces != close_braces:
            return False, "Unbalanced braces in QASM"
        
        return True, None
    
    # A04: Insecure Design
    def get_key_rotation_policy(self) -> Dict[str, Any]:
        """Get the key rotation policy"""
        # Mock policy - in reality would come from config service
        return {
            'policy': 'rotate_every_90_days',
            'period_days': 90,
            'algorithm': 'Kyber768',
            'require_confirmation': True
        }
    
    # A05: Security Misconfiguration
    def check_default_credentials(self, username: str, password: str) -> bool:
        """Check if credentials are default/common"""
        default_creds = [
            ('admin', 'admin'),
            ('admin', 'password'),
            ('root', 'root'),
            ('test', 'test'),
            ('user', 'user')
        ]
        return (username, password) in default_creds
    
    def get_security_headers(self) -> Dict[str, str]:
        """Get expected security headers"""
        return {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'self'"
        }
    
    # A06: Vulnerable Components
    def check_for_known_vulnerabilities(self, package_name: str, version: str) -> List[Dict[str, Any]]:
        """Check if a package version has known vulnerabilities"""
        # Mock implementation - would use a vulnerability database like NVD or OSV
        known_vulns = {
            'qiskit': [
                {'version': '0.40.0', 'cve': 'CVE-2023-XXXXX', 'severity': 'high'}
            ],
            'liboqs': [
                {'version': '0.7.0', 'cve': 'CVE-2022-YYYYY', 'severity': 'medium'}
            ]
        }
        
        if package_name in known_vulns:
            for vuln in known_vulns[package_name]:
                # Simple version check - real implementation would use semantic versioning
                if vuln['version'] == version:
                    return [vuln]
        return []
    
    # A07: Identification and Authentication Failures
    def check_password_strength(self, password: str) -> Tuple[bool, List[str]]:
        """Check password strength"""
        errors = []
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        
        return len(errors) == 0, errors
    
    def is_rate_limited(self, ip_address: str, attempt_count: int, time_window: int = 300) -> bool:
        """Check if an IP should be rate limited based on failed attempts"""
        # Mock implementation - would use actual request tracking
        return attempt_count > 5 and time_window < 300  # More than 5 attempts in 5 minutes
    
    # A08: Software and Data Integrity Failures
    def verify_file_integrity(self, filepath: str, expected_hash: str, algorithm: str = 'sha256') -> bool:
        """Verify file integrity using hash"""
        if not os.path.exists(filepath):
            return False
        
        hash_func = hashlib.new(algorithm)
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_func.update(chunk)
        
        return hash_func.hexdigest() == expected_hash
    
    def is_world_writable(self, filepath: str) -> bool:
        """Check if a file is world-writable"""
        if not os.path.exists(filepath):
            return False
        return bool(os.stat(filepath).st_mode & 0o002)
    
    # A09: Security Logging and Monitoring Failures
    def log_security_event(self, event_type: str, details: Dict[str, Any], severity: str = 'info'):
        """Log a security event"""
        event = {
            'timestamp': self._get_timestamp(),
            'type': event_type,
            'details': details,
            'severity': severity
        }
        self.security_logs.append(event)
        # In reality, would send to SIEM or logging system
    
    def get_security_logs(self, since: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get security logs since a timestamp"""
        if not since:
            return self.security_logs
        # Mock filtering - would parse since timestamp
        return self.security_logs
    
    def clear_security_logs(self):
        """Clear security logs"""
        self.security_logs = []
    
    def get_alert_configuration(self) -> Dict[str, Any]:
        """Get alert configuration"""
        return self.alert_config
    
    # A10: Server-Side Request Forgery
    def is_safe_url(self, url: str) -> Tuple[bool, Optional[str]]:
        """Check if a URL is safe to fetch (SSRF protection)"""
        try:
            parsed = urllib.parse.urlparse(url)
            
            # Only allow http and https schemes
            if parsed.scheme not in ('http', 'https'):
                return False, f"Scheme {parsed.scheme} not allowed"
            
            # Resolve hostname to IP address
            hostname = parsed.hostname
            if not hostname:
                return False, "No hostname in URL"
            
            try:
                ip_address = socket.gethostbyname(hostname)
            except socket.gaierror:
                return False, f"Could not resolve hostname: {hostname}"
            
            # Check if IP is in private/reserved ranges
            ip_obj = ipaddress.ip_address(ip_address)
            
            # Private IP ranges
            private_ranges = [
                ipaddress.ip_network('10.0.0.0/8'),
                ipaddress.ip_network('172.16.0.0/12'),
                ipaddress.ip_network('192.168.0.0/16'),
                ipaddress.ip_network('127.0.0.0/8'),  # localhost
                ipaddress.ip_network('169.254.0.0/16'),  # link-local
                ipaddress.ip_network('192.0.0.0/24'),  # IETF protocol assignments
                ipaddress.ip_network('192.0.2.0/24'),  # TEST-NET-1
                ipaddress.ip_network('198.51.100.0/24'),  # TEST-NET-2
                ipaddress.ip_network('203.0.113.0/24'),  # TEST-NET-3
                ipaddress.ip_network('224.0.0.0/4'),  # multicast
                ipaddress.ip_network('240.0.0.0/4'),  # reserved
            ]
            
            for private_range in private_ranges:
                if ip_obj in private_range:
                    return False, f"IP address {ip_address} is in private/reserved range {private_range}"
            
            # Additional check for cloud metadata services
            metadata_ips = [
                ipaddress.ip_address('169.254.169.254'),  # AWS, Azure, GCP
                ipaddress.ip_address('169.254.169.250'),  # EC2 metadata
            ]
            
            if ip_obj in metadata_ips:
                return False, f"IP address {ip_address} is a cloud metadata service"
            
            return True, None
        except Exception as e:
            return False, f"URL validation error: {str(e)}"
    
    # Helper methods
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'
    
    def run_dependency_check(self) -> Dict[str, Any]:
        """Run a dependency security check (mock)"""
        # Mock implementation
        return {
            'tool': 'dependency-check',
            'passed': True,
            'vulnerabilities_found': 0,
            'details': 'No known vulnerabilities found in dependencies'
        }
    
    def check_runtime_protection(self) -> bool:
        """Check if runtime protection is enabled (mock)"""
        # Mock - would check for things like SELinux, AppArmor, etc.
        return True
    
    def get_file_permissions(self, filepath: str) -> str:
        """Get file permissions as string"""
        if not os.path.exists(filepath):
            return "File does not exist"
        return oct(os.stat(filepath).st_mode)[-3:]
    
    def check_if_update_signed(self, filename: str) -> bool:
        """Check if an update file is signed (mock)"""
        # Mock implementation
        return filename.endswith('.sig') or 'signed' in filename.lower()
    
    def verify_dependency_integrity(self, package_name: str) -> bool:
        """Verify dependency integrity (mock)"""
        # Mock implementation
        return True

# For backward compatibility with tests that expect direct function access
def check_access_control(user_role: str, resource: str, action: str) -> bool:
    lib = SecurityTestLibrary()
    return lib.check_access_control(user_role, resource, action)

def is_weak_algorithm(algorithm: str) -> bool:
    lib = SecurityTestLibrary()
    return lib.is_weak_algorithm(algorithm)

def sanitize_input(input_str: str) -> str:
    lib = SecurityTestLibrary()
    return lib.sanitize_input(input_str)

def is_valid_openqasm(qasm_str: str) -> Tuple[bool, Optional[str]]:
    lib = SecurityTestLibrary()
    return lib.is_valid_openqasm(qasm_str)

def get_key_rotation_policy() -> Dict[str, Any]:
    lib = SecurityTestLibrary()
    return lib.get_key_rotation_policy()

def check_default_credentials(username: str, password: str) -> bool:
    lib = SecurityTestLibrary()
    return lib.check_default_credentials(username, password)

def get_security_headers() -> Dict[str, str]:
    lib = SecurityTestLibrary()
    return lib.get_security_headers()

def check_for_known_vulnerabilities(package_name: str, version: str) -> List[Dict[str, Any]]:
    lib = SecurityTestLibrary()
    return lib.check_for_known_vulnerabilities(package_name, version)

def check_password_strength(password: str) -> Tuple[bool, List[str]]:
    lib = SecurityTestLibrary()
    return lib.check_password_strength(password)

def is_rate_limited(ip_address: str, attempt_count: int, time_window: int = 300) -> bool:
    lib = SecurityTestLibrary()
    return lib.is_rate_limited(ip_address, attempt_count, time_window)

def verify_file_integrity(filepath: str, expected_hash: str, algorithm: str = 'sha256') -> bool:
    lib = SecurityTestLibrary()
    return lib.verify_file_integrity(filepath, expected_hash, algorithm)

def is_world_writable(filepath: str) -> bool:
    lib = SecurityTestLibrary()
    return lib.is_world_writable(filepath)

def log_security_event(event_type: str, details: Dict[str, Any], severity: str = 'info'):
    lib = SecurityTestLibrary()
    lib.log_security_event(event_type, details, severity)

def get_security_logs(since: Optional[str] = None) -> List[Dict[str, Any]]:
    lib = SecurityTestLibrary()
    return lib.get_security_logs(since)

def clear_security_logs():
    lib = SecurityTestLibrary()
    lib.clear_security_logs()

def get_alert_configuration() -> Dict[str, Any]:
    lib = SecurityTestLibrary()
    return lib.get_alert_configuration()

def is_safe_url(url: str) -> Tuple[bool, Optional[str]]:
    lib = SecurityTestLibrary()
    return lib.is_safe_url(url)

def run_dependency_check() -> Dict[str, Any]:
    lib = SecurityTestLibrary()
    return lib.run_dependency_check()

def check_runtime_protection() -> bool:
    lib = SecurityTestLibrary()
    return lib.check_runtime_protection()

def get_file_permissions(filepath: str) -> str:
    lib = SecurityTestLibrary()
    return lib.get_file_permissions(filepath)

def check_if_update_signed(filename: str) -> bool:
    lib = SecurityTestLibrary()
    return lib.check_if_update_signed(filename)

def verify_dependency_integrity(package_name: str) -> bool:
    lib = SecurityTestLibrary()
    return lib.verify_dependency_integrity(package_name)

def send_request(method: str, url: str, **kwargs) -> Dict[str, Any]:
    lib = SecurityTestLibrary()
    return lib.send_request(method, url, **kwargs)

def log_security_test_state():
    lib = SecurityTestLibrary()
    lib.log_security_test_state()

def run_command(command: str, *args) -> str:
    lib = SecurityTestLibrary()
    return lib.run_command(command, *args)

def generate_fuzz_payloads(fuzz_type: str = 'xss') -> List[str]:
    lib = SecurityTestLibrary()
    return lib.generate_fuzz_payloads(fuzz_type)