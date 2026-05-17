"""
Crypto Test Library for Robot Framework
Provides cryptographic related test utilities
"""

import os
from typing import List, Dict, Any, Tuple, Optional
import hashlib
import hmac
import secrets
import time

# Try to import liboqs and cryptography, provide mock if not available for testing structure
try:
    import oqs
    OQS_AVAILABLE = True
except ImportError:
    OQS_AVAILABLE = False
    print("liboqs not available, using mock for crypto tests")

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False
    print("cryptography not available, using mock for crypto tests")

class PQCManager:
    def __init__(self):
        if OQS_AVAILABLE:
            self.kem_algorithms = oqs.KeyEncapsulation.get_enabled_kem_mechanisms()
            self.sign_algorithms = oqs.Signature.get_enabled_sig_mechanisms()
        else:
            # Mock algorithms for testing
            self.kem_algorithms = ['Kyber512', 'Kyber768', 'Kyber1024']
            self.sign_algorithms = ['Dilithium2', 'Dilithium3', 'Dilithium5']
        
        # Set defaults
        self.default_kem = self.kem_algorithms[0] if self.kem_algorithms else ''
        self.default_sign = self.sign_algorithms[0] if self.sign_algorithms else ''
    
    def generate_keypair(self, algorithm: Optional[str] = None) -> Tuple[bytes, bytes]:
        """Generate a keypair for the specified KEM algorithm"""
        alg = algorithm or self.default_kem
        if not alg:
            raise ValueError("No KEM algorithms available")
        
        if OQS_AVAILABLE:
            with oqs.KeyEncapsulation(alg) as kem:
                public_key = kem.generate_keypair()
                secret_key = kem.export_secret_key()
                return public_key, secret_key
        else:
            # Mock implementation
            public_key = secrets.token_bytes(32)
            secret_key = secrets.token_bytes(32)
            return public_key, secret_key
    
    def encapsulate(self, public_key: bytes, algorithm: Optional[str] = None) -> Tuple[bytes, bytes]:
        """Encapsulate a shared secret using the public key"""
        alg = algorithm or self.default_kem
        if not alg:
            raise ValueError("No KEM algorithms available")
        
        if OQS_AVAILABLE:
            with oqs.KeyEncapsulation(alg) as kem:
                kem.public_key = public_key
                ciphertext, shared_secret = kem.encap_secret()
                return ciphertext, shared_secret
        else:
            # Mock implementation
            ciphertext = secrets.token_bytes(32)
            shared_secret = secrets.token_bytes(32)
            return ciphertext, shared_secret
    
    def decapsulate(self, ciphertext: bytes, secret_key: bytes, algorithm: Optional[str] = None) -> bytes:
        """Decapsulate a shared secret using the secret key"""
        alg = algorithm or self.default_kem
        if not alg:
            raise ValueError("No KEM algorithms available")
        
        if OQS_AVAILABLE:
            with oqs.KeyEncapsulation(alg) as kem:
                kem.secret_key = secret_key
                shared_secret = kem.decap_secret(ciphertext)
                return shared_secret
        else:
            # Mock implementation - just return a deterministic value based on inputs
            # In real scenario, this would fail if ciphertext doesn't match key
            return hashlib.sha256(ciphertext + secret_key).digest()
    
    def sign_message(self, message: bytes, algorithm: Optional[str] = None) -> Tuple[bytes, bytes, bytes]:
        """Sign a message and return signature, public key, and secret key"""
        alg = algorithm or self.default_sign
        if not alg:
            raise ValueError("No signature algorithms available")
        
        if OQS_AVAILABLE:
            with oqs.Signature(alg) as sig:
                public_key = sig.generate_keypair()
                secret_key = sig.export_secret_key()
                signature = sig.sign(message)
                return signature, public_key, secret_key
        else:
            # Mock implementation
            public_key = secrets.token_bytes(32)
            secret_key = secrets.token_bytes(32)
            # Simple mock signature - hash of message + key
            signature = hmac.new(secret_key, message, hashlib.sha256).digest()
            return signature, public_key, secret_key
    
    def verify_signature(self, message: bytes, signature: bytes, public_key: bytes, algorithm: Optional[str] = None) -> bool:
        """Verify a signature"""
        alg = algorithm or self.default_sign
        if not alg:
            raise ValueError("No signature algorithms available")
        
        if OQS_AVAILABLE:
            with oqs.Signature(alg) as sig:
                sig.public_key = public_key
                return sig.verify(message, signature)
        else:
            # Mock implementation
            # In reality, we'd need the secret key to verify, but for mock we'll just check format
            return len(signature) == 32
    
    def get_available_algorithms(self) -> dict:
        """Get list of available KEM and signature algorithms"""
        return {
            'kem': self.kem_algorithms,
            'signature': self.sign_algorithms
        }
    
    def is_algorithm_enabled(self, algorithm: str, is_kem: bool = True) -> bool:
        """Check if an algorithm is enabled"""
        if is_kem:
            return algorithm in self.kem_algorithms
        else:
            return algorithm in self.sign_algorithms

class HybridCrypto:
    def __init__(self):
        self.pqc = PQCManager()
    
    def encrypt_hybrid(self, plaintext: bytes, pqc_public_key: bytes) -> dict:
        """
        Encrypt using hybrid approach:
        1. Generate a random symmetric key
        2. Encrypt the symmetric key with PQC KEM
        3. Encrypt the plaintext with the symmetric key (AES-GCM)
        4. Return ciphertext, encapsulated key, and IV
        """
        # Step 1: Generate symmetric key
        symmetric_key = secrets.token_bytes(32)  # AES-256 key
        
        # Step 2: Encapsulate symmetric key with PQC
        ciphertext, encapsulated_key = self.pqc.encapsulate(pqc_public_key)
        
        # Step 3: Encrypt plaintext with symmetric key (AES-GCM)
        if CRYPTOGRAPHY_AVAILABLE:
            import os
            iv = os.urandom(12)  # GCM recommended IV size
            aesgcm = AESGCM(symmetric_key)
            ciphertext_data = aesgcm.encrypt(iv, plaintext, None)
        else:
            # Mock encryption
            iv = secrets.token_bytes(12)
            # Simple XOR for mock (NOT SECURE - just for testing structure)
            ciphertext_data = bytes(a ^ b for a, b in zip(plaintext, itertools.cycle(iv + symmetric_key)))
            if len(ciphertext_data) < len(plaintext):
                ciphertext_data += secrets.token_bytes(len(plaintext) - len(ciphertext_data))
        
        return {
            'pqc_ciphertext': ciphertext,
            'encapsulated_key': encapsulated_key,
            'iv': iv,
            'ciphertext': ciphertext_data,
            'symmetric_key': symmetric_key  # In reality, this would NOT be returned
        }
    
    def decrypt_hybrid(self, encrypted_data: dict, pqc_secret_key: bytes) -> bytes:
        """
        Decrypt using hybrid approach:
        1. Decapsulate the symmetric key using PQC
        2. Decrypt the ciphertext using the symmetric key (AES-GCM)
        """
        # Extract components
        pqc_ciphertext = encrypted_data.get('pqc_ciphertext')
        iv = encrypted_data.get('iv')
        ciphertext_data = encrypted_data.get('ciphertext')
        
        if not all([pqc_ciphertext, iv, ciphertext_data]):
            raise ValueError("Missing required encryption components")
        
        # Step 1: Decapsulate symmetric key
        try:
            symmetric_key = self.pqc.decapsulate(pqc_ciphertext, pqc_secret_key)
        except Exception as e:
            raise ValueError(f"Failed to decapsulate symmetric key: {e}")
        
        # Step 2: Decrypt with symmetric key (AES-GCM)
        if CRYPTOGRAPHY_AVAILABLE:
            aesgcm = AESGCM(symmetric_key)
            plaintext = aesgcm.decrypt(iv, ciphertext_data, None)
            return plaintext
        else:
            # Mock decryption (reverse of mock encryption)
            # Simple XOR for mock (NOT SECURE - just for testing structure)
            keystream = itertools.cycle(iv + symmetric_key)
            plaintext = bytes(c ^ k for c, k in zip(ciphertext_data, keystream))
            return plaintext

# Mock itertools for the mock crypto above if needed
try:
    import itertools
except ImportError:
    # Very basic mock for cycling
    class itertools:
        @staticmethod
        def cycle(iterable):
            saved = []
            while True:
                for element in iterable:
                    yield element
                    saved.append(element)
                if not saved:
                    raise ValueError("cycle() empty iterator")

# For backward compatibility with tests that expect direct function access
def generate_pqc_keypair(algorithm: Optional[str] = None) -> Tuple[bytes, bytes]:
    pqc = PQCManager()
    return pqc.generate_keypair(algorithm)

def pqc_encapsulate(public_key: bytes, algorithm: Optional[str] = None) -> Tuple[bytes, bytes]:
    pqc = PQCManager()
    return pqc.encapsulate(public_key, algorithm)

def pqc_decapsulate(ciphertext: bytes, secret_key: bytes, algorithm: Optional[str] = None) -> bytes:
    pqc = PQCManager()
    return pqc.decapsulate(ciphertext, secret_key, algorithm)

def sign_message(message: bytes, algorithm: Optional[str] = None) -> Tuple[bytes, bytes, bytes]:
    pqc = PQCManager()
    return pqc.sign_message(message, algorithm)

def verify_signature(message: bytes, signature: bytes, public_key: bytes, algorithm: Optional[str] = None) -> bool:
    pqc = PQCManager()
    return pqc.verify_signature(message, signature, public_key, algorithm)

def encrypt_hybrid(plaintext: bytes, pqc_public_key: bytes) -> dict:
    crypto = HybridCrypto()
    return crypto.encrypt_hybrid(plaintext, pqc_public_key)

def decrypt_hybrid(encrypted_data: dict, pqc_secret_key: bytes) -> bytes:
    crypto = HybridCrypto()
    return crypto.decrypt_hybrid(encrypted_data, pqc_secret_key)