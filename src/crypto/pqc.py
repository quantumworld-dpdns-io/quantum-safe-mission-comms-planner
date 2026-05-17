"""
Post-Quantum Cryptography Integration for QSCM Planner
Using liboqs for quantum-resistant algorithms
"""

import oqs
from typing import Tuple, Optional
import hashlib
import hmac
import json
import weave

class PQCManager:
    def __init__(self):
        # Initialize available algorithms
        self.kem_algorithms = oqs.KeyEncapsulation.get_enabled_kem_mechanisms()
        self.sign_algorithms = oqs.Signature.get_enabled_sig_mechanisms()
        
        # Default algorithms (prioritizing NIST candidates)
        self.default_kem = self._select_default_kem()
        self.default_sign = self._select_default_sign()
    
    def _select_default_kem(self) -> str:
        """Select a default KEM algorithm (Kyber preferred)"""
        preferred = ['Kyber512', 'Kyber768', 'Kyber1024', 'NTRU', 'Saber']
        for alg in preferred:
            if alg in self.kem_algorithms:
                return alg
        return self.kem_algorithms[0] if self.kem_algorithms else ''
    
    def _select_default_sign(self) -> str:
        """Select a default signature algorithm (Dilithium preferred)"""
        preferred = ['Dilithium2', 'Dilithium3', 'Dilithium5', 'Falcon-512', 'Falcon-1024']
        for alg in preferred:
            if alg in self.sign_algorithms:
                return alg
        return self.sign_algorithms[0] if self.sign_algorithms else ''
    
    @weave.op()
    def generate_keypair(self, algorithm: Optional[str] = None) -> Tuple[bytes, bytes]:
        """Generate a keypair for the specified KEM algorithm"""
        alg = algorithm or self.default_kem
        if not alg:
            raise ValueError("No KEM algorithms available")
        
        with oqs.KeyEncapsulation(alg) as kem:
            public_key = kem.generate_keypair()
            secret_key = kem.export_secret_key()
            return public_key, secret_key
    
    def encapsulate(self, public_key: bytes, algorithm: Optional[str] = None) -> Tuple[bytes, bytes]:
        """Encapsulate a shared secret using the public key"""
        alg = algorithm or self.default_kem
        if not alg:
            raise ValueError("No KEM algorithms available")
        
        with oqs.KeyEncapsulation(alg) as kem:
            kem.public_key = public_key
            ciphertext, shared_secret = kem.encap_secret()
            return ciphertext, shared_secret
    
    def decapsulate(self, ciphertext: bytes, secret_key: bytes, algorithm: Optional[str] = None) -> bytes:
        """Decapsulate a shared secret using the secret key"""
        alg = algorithm or self.default_kem
        if not alg:
            raise ValueError("No KEM algorithms available")
        
        with oqs.KeyEncapsulation(alg) as kem:
            kem.secret_key = secret_key
            shared_secret = kem.decap_secret(ciphertext)
            return shared_secret
    
    def sign_message(self, message: bytes, algorithm: Optional[str] = None) -> Tuple[bytes, bytes, bytes]:
        """Sign a message and return signature, public key, and secret key"""
        alg = algorithm or self.default_sign
        if not alg:
            raise ValueError("No signature algorithms available")
        
        with oqs.Signature(alg) as sig:
            public_key = sig.generate_keypair()
            secret_key = sig.export_secret_key()
            signature = sig.sign(message)
            return signature, public_key, secret_key
    
    def verify_signature(self, message: bytes, signature: bytes, public_key: bytes, algorithm: Optional[str] = None) -> bool:
        """Verify a signature"""
        alg = algorithm or self.default_sign
        if not alg:
            raise ValueError("No signature algorithms available")
        
        with oqs.Signature(alg) as sig:
            sig.public_key = public_key
            return sig.verify(message, signature)
    
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

# Hybrid encryption: combine ECC and PQC for transitional security
class HybridCrypto:
    def __init__(self):
        self.pqc = PQCManager()
        # In a full implementation, we would also have traditional ECC (e.g., using cryptography library)
        # For now, we focus on PQC and note where hybrid would be used.
    
    def encrypt_hybrid(self, plaintext: bytes, pqc_public_key: bytes) -> dict:
        """
        Encrypt using hybrid approach:
        1. Generate a random symmetric key
        2. Encrypt the symmetric key with PQC KEM
        3. Encrypt the plaintext with the symmetric key (AES-GCM)
        4. Return ciphertext, encapsulated key, and IV
        """
        # Step 1: Generate symmetric key
        import os
        symmetric_key = os.urandom(32)  # AES-256 key
        
        # Step 2: Encapsulate symmetric key with PQC
        ciphertext, encapsulated_key = self.pqc.encapsulate(pqc_public_key)
        
        # Step 3: Encrypt plaintext with symmetric key (AES-GCM)
        # We'll use cryptography library for AES-GCM in a real implementation
        # For now, we'll simulate by returning the key and note that encryption would happen
        # In a full implementation:
        # from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        # aesgcm = AESGCM(symmetric_key)
        # iv = os.urandom(12)
        # ciphertext = aesgcm.encrypt(iv, plaintext, None)
        
        # For this example, we'll just return the components
        return {
            'pqc_ciphertext': ciphertext,
            'encapsulated_key': encapsulated_key,
            'symmetric_key': symmetric_key,  # In reality, this would be kept secret and not returned
            'note': 'In production, symmetric key is used for AES-GCM encryption of plaintext'
        }
    
    def decrypt_hybrid(self, encrypted_data: dict, pqc_secret_key: bytes) -> bytes:
        """
        Decrypt using hybrid approach:
        1. Decapsulate the symmetric key using PQC
        2. Decrypt the ciphertext using the symmetric key (AES-GCM)
        """
        # Step 1: Decapsulate symmetric key
        try:
            symmetric_key = self.pqc.decapsulate(
                encrypted_data['pqc_ciphertext'], 
                pqc_secret_key
            )
        except Exception as e:
            raise ValueError(f"Failed to decapsulate symmetric key: {e}")
        
        # Step 2: Decrypt with symmetric key (AES-GCM)
        # In a full implementation:
        # from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        # aesgcm = AESGCM(symmetric_key)
        # plaintext = aesgcm.decrypt(encrypted_data['iv'], encrypted_data['ciphertext'], None)
        
        # For this example, we'll just return the symmetric key as a placeholder
        # and note that actual decryption would happen
        return symmetric_key  # Placeholder

# Example usage
def run_pqc_example():
    """Run a simple PQC example"""
    pqc = PQCManager()
    
    print("Available KEM algorithms:", pqc.kem_algorithms[:5])  # Show first 5
    print("Available signature algorithms:", pqc.sign_algorithms[:5])  # Show first 5
    
    # Key encapsulation example
    print("\n--- Key Encapsulation ---")
    public_key, secret_key = pqc.generate_keypair()
    print(f"Generated keypair for {pqc.default_kem}")
    print(f"Public key length: {len(public_key)} bytes")
    print(f"Secret key length: {len(secret_key)} bytes")
    
    ciphertext, shared_secret = pqc.encapsulate(public_key)
    print(f"Encapsulated key length: {len(ciphertext)} bytes")
    print(f"Shared secret length: {len(shared_secret)} bytes")
    
    # Decapsulate
    decrypted_secret = pqc.decapsulate(ciphertext, secret_key)
    print(f"Decapsulated shared secret matches: {shared_secret == decrypted_secret}")
    
    # Signature example
    print("\n--- Digital Signature ---")
    message = b"Quantum-safe mission communication test"
    signature, pub_key, sec_key = pqc.sign_message(message)
    print(f"Signed message with {pqc.default_sign}")
    print(f"Signature length: {len(signature)} bytes")
    
    # Verify
    is_valid = pqc.verify_signature(message, signature, pub_key)
    print(f"Signature valid: {is_valid}")

if __name__ == "__main__":
    run_pqc_example()