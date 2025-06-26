import os
import json
import hashlib
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class PinManager:
    def __init__(self, pin_file=None):
        if pin_file is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            pin_file = os.path.join(script_dir, "..", "Security", "ds_pins.dat")
        self.pin_file = pin_file
        self.master_password = "DrillSergeantAccess2025"
        self._ensure_pin_file_exists()
    
    def _generate_key(self, password: str, salt: bytes) -> bytes:
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def _encrypt_data(self, data: dict) -> bytes:

        salt = os.urandom(16)

        key = self._generate_key(self.master_password, salt)
        fernet = Fernet(key)

        json_data = json.dumps(data).encode()
        encrypted_data = fernet.encrypt(json_data)

        return salt + encrypted_data
    
    def _decrypt_data(self, encrypted_bytes: bytes) -> dict:
        
        try:

            salt = encrypted_bytes[:16]
            encrypted_data = encrypted_bytes[16:]

            key = self._generate_key(self.master_password, salt)
            fernet = Fernet(key)

            decrypted_data = fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            print(f"Error decrypting PIN data: {e}")
            return {}
    
    def _hash_pin(self, pin: str) -> str:
        
        return hashlib.sha256(pin.encode()).hexdigest()
    
    def _ensure_pin_file_exists(self):
        
        if not os.path.exists(self.pin_file):

            default_accounts = {
                "DS Smith": self._hash_pin("1234"),
                "DS Johnson": self._hash_pin("2345"),
                "DS Williams": self._hash_pin("3456"),
                "DS Brown": self._hash_pin("4567"),
                "DS Davis": self._hash_pin("5678")
            }

            encrypted_data = self._encrypt_data(default_accounts)
            with open(self.pin_file, 'wb') as f:
                f.write(encrypted_data)
            
            print(f"Created default PIN file: {self.pin_file}")
            print("Default DS accounts created with PINs:")
            print("  DS Smith: 1234")
            print("  DS Johnson: 2345")
            print("  DS Williams: 3456")
            print("  DS Brown: 4567")
            print("  DS Davis: 5678")
    
    def verify_pin(self, ds_name: str, pin: str) -> bool:
        
        try:

            with open(self.pin_file, 'rb') as f:
                encrypted_data = f.read()
            
            pin_data = self._decrypt_data(encrypted_data)

            if ds_name in pin_data:
                hashed_pin = self._hash_pin(pin)
                return pin_data[ds_name] == hashed_pin
            
            return False
            
        except Exception as e:
            print(f"Error verifying PIN: {e}")
            return False
    
    def add_ds(self, ds_name: str, pin: str) -> bool:
        
        try:

            with open(self.pin_file, 'rb') as f:
                encrypted_data = f.read()
            
            pin_data = self._decrypt_data(encrypted_data)

            pin_data[ds_name] = self._hash_pin(pin)

            encrypted_data = self._encrypt_data(pin_data)
            with open(self.pin_file, 'wb') as f:
                f.write(encrypted_data)
            
            return True
            
        except Exception as e:
            print(f"Error adding DS: {e}")
            return False
    
    def remove_ds(self, ds_name: str) -> bool:
        
        try:

            with open(self.pin_file, 'rb') as f:
                encrypted_data = f.read()
            
            pin_data = self._decrypt_data(encrypted_data)

            if ds_name in pin_data:
                del pin_data[ds_name]

                encrypted_data = self._encrypt_data(pin_data)
                with open(self.pin_file, 'wb') as f:
                    f.write(encrypted_data)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"Error removing DS: {e}")
            return False
    
    def list_ds_names(self) -> list:
        
        try:
            with open(self.pin_file, 'rb') as f:
                encrypted_data = f.read()
            
            pin_data = self._decrypt_data(encrypted_data)
            return list(pin_data.keys())
            
        except Exception as e:
            print(f"Error listing DS names: {e}")
            return []
    
    def change_pin(self, ds_name: str, old_pin: str, new_pin: str) -> bool:

        if not self.verify_pin(ds_name, old_pin):
            return False
        
        try:

            with open(self.pin_file, 'rb') as f:
                encrypted_data = f.read()
            
            pin_data = self._decrypt_data(encrypted_data)

            pin_data[ds_name] = self._hash_pin(new_pin)

            encrypted_data = self._encrypt_data(pin_data)
            with open(self.pin_file, 'wb') as f:
                f.write(encrypted_data)
            
            return True
            
        except Exception as e:
            print(f"Error changing PIN: {e}")
            return False

if __name__ == "__main__":
    pin_manager = PinManager()

    print("\nTesting PIN verification:")
    print(f"DS Smith with PIN 1234: {pin_manager.verify_pin('DS Smith', '1234')}")
    print(f"DS Smith with PIN 0000: {pin_manager.verify_pin('DS Smith', '0000')}")
    print(f"Unknown DS: {pin_manager.verify_pin('DS Unknown', '1234')}")

    print(f"\nAll DS names: {pin_manager.list_ds_names()}")