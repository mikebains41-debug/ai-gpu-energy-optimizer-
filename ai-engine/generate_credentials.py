// PROPRIETARY AND CONFIDENTIAL
// Copyright (c) 2026 Mike Bains. All Rights Reserved.
// Contact: Mikebains41@gmail.com
// Unauthorized use prohibited.

#!/usr/bin/env python3
"""
Credential Generator for AI GPU Energy Optimizer Beta Program
Generates secure Cluster IDs and API Keys for beta partners
"""

import secrets
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, Optional

class CredentialGenerator:
    def __init__(self, storage_file: str = "beta_credentials.json"):
        self.storage_file = storage_file
        self.credentials = self.load_credentials()
    
    def load_credentials(self) -> Dict:
        """Load existing credentials from storage file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("⚠️ Credentials file corrupted. Creating new one.")
                return {}
        return {}
    
    def save_credentials(self):
        """Save credentials to storage file"""
        with open(self.storage_file, 'w') as f:
            json.dump(self.credentials, f, indent=2)
        print(f"✅ Credentials saved to {self.storage_file}")
    
    def generate_cluster_id(self, user_name: str) -> str:
        """Generate unique cluster ID"""
        # Sanitize user name
        clean_name = user_name.lower().strip().replace(" ", "-")
        # Remove special characters except hyphens
        clean_name = ''.join(c for c in clean_name if c.isalnum() or c == '-')
        # Truncate to 20 chars
        clean_name = clean_name[:20]
        # Add random suffix
        suffix = secrets.token_hex(4)
        return f"{clean_name}-{suffix}"
    
    def generate_api_key(self) -> str:
        """Generate secure API key"""
        # Format: gpu_opt_[64 hex chars]
        return f"gpu_opt_{secrets.token_hex(32)}"
    
    def generate_credentials(self, user_name: str, email: str = "", company: str = "") -> Dict:
        """Generate complete credentials for a beta user"""
        
        # Check if user already exists
        existing = None
        for cred in self.credentials.values():
            if cred.get('user_name') == user_name or cred.get('email') == email:
                existing = cred
                break
        
        if existing:
            print(f"⚠️ User already exists: {existing['user_name']}")
            print(f"   Cluster ID: {existing['cluster_id']}")
            print(f"   API Key: {existing['api_key']}")
            response = input("Regenerate new credentials? (y/N): ").lower()
            if response != 'y':
                return existing
        
        # Generate new credentials
        cluster_id = self.generate_cluster_id(user_name)
        api_key = self.generate_api_key()
        
        # Set expiration (90 days from now for beta)
        expires_at = (datetime.now() + timedelta(days=90)).isoformat()
        
        credentials = {
            cluster_id: {
                "user_name": user_name,
                "email": email,
                "company": company,
                "cluster_id": cluster_id,
                "api_key": api_key,
                "created_at": datetime.now().isoformat(),
                "expires_at": expires_at,
                "is_active": True,
                "usage_count": 0,
                "notes": ""
            }
        }
        
        self.credentials.update(credentials)
        self.save_credentials()
        
        return credentials[cluster_id]
    
    def validate_api_key(self, api_key: str) -> Optional[Dict]:
        """Validate an API key and return user info if valid"""
        for cluster_id, cred in self.credentials.items():
            if cred['api_key'] == api_key:
                # Check if expired
                expires_at = datetime.fromisoformat(cred['expires_at'])
                if expires_at < datetime.now():
                    print(f"⚠️ API key expired for {cred['user_name']}")
                    return None
                
                # Check if active
                if not cred.get('is_active', True):
                    print(f"⚠️ API key disabled for {cred['user_name']}")
                    return None
                
                # Increment usage count
                cred['usage_count'] = cred.get('usage_count', 0) + 1
                self.save_credentials()
                
                return cred
        return None
    
    def list_credentials(self):
        """List all active credentials"""
        if not self.credentials:
            print("No credentials found.")
            return
        
        print("\n" + "="*80)
        print(f"{'User':<20} {'Cluster ID':<30} {'Created':<20} {'Expires':<20} {'Active':<8}")
        print("="*80)
        
        for cluster_id, cred in self.credentials.items():
            created = cred['created_at'][:10] if 'created_at' in cred else 'Unknown'
            expires = cred['expires_at'][:10] if 'expires_at' in cred else 'Unknown'
            active = "✅" if cred.get('is_active', True) else "❌"
            
            print(f"{cred['user_name']:<20} {cluster_id:<30} {created:<20} {expires:<20} {active:<8}")
        
        print("="*80)
    
    def revoke_credentials(self, cluster_id: str):
        """Revoke credentials by cluster ID"""
        if cluster_id in self.credentials:
            self.credentials[cluster_id]['is_active'] = False
            self.save_credentials()
            print(f"✅ Revoked credentials for {self.credentials[cluster_id]['user_name']}")
        else:
            print(f"❌ Cluster ID {cluster_id} not found")
    
    def delete_credentials(self, cluster_id: str):
        """Delete credentials by cluster ID"""
        if cluster_id in self.credentials:
            user_name = self.credentials[cluster_id]['user_name']
            del self.credentials[cluster_id]
            self.save_credentials()
            print(f"✅ Deleted credentials for {user_name}")
        else:
            print(f"❌ Cluster ID {cluster_id} not found")

def main():
    generator = CredentialGenerator()
    
    print("\n🔐 AI GPU Energy Optimizer - Credential Manager")
    print("="*50)
    print("1. Generate new credentials")
    print("2. List all credentials")
    print("3. Validate API key")
    print("4. Revoke credentials")
    print("5. Delete credentials")
    print("6. Exit")
    print("="*50)
    
    while True:
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            print("\n📝 New Beta User Registration")
            name = input("User/Company name: ").strip()
            email = input("Email (optional): ").strip()
            company = input("Company name (optional): ").strip()
            
            if not name:
                print("❌ Name is required")
                continue
            
            cred = generator.generate_credentials(name, email, company)
            
            print("\n" + "="*60)
            print("🎫 BETA CREDENTIALS - SAVE THESE")
            print("="*60)
            print(f"Cluster ID: {cred['cluster_id']}")
            print(f"API Key:    {cred['api_key']}")
            print("="*60)
            print(f"\n📧 Send these to the user: {cred['email'] or name}")
            print(f"⏰ Credentials expire: {cred['expires_at'][:10]}")
            print("\nInstall command for user:")
            print(f'curl -sSL https://raw.githubusercontent.com/mikebains41-debug/ai-gpu-energy-optimizer-/main/ai-engine/install.sh | bash')
            
        elif choice == '2':
            generator.list_credentials()
            
        elif choice == '3':
            api_key = input("Enter API key to validate: ").strip()
            result = generator.validate_api_key(api_key)
            if result:
                print(f"✅ Valid API key for: {result['user_name']}")
                print(f"   Cluster ID: {result['cluster_id']}")
                print(f"   Expires: {result['expires_at'][:10]}")
            else:
                print("❌ Invalid API key")
                
        elif choice == '4':
            cluster_id = input("Enter Cluster ID to revoke: ").strip()
            generator.revoke_credentials(cluster_id)
            
        elif choice == '5':
            cluster_id = input("Enter Cluster ID to delete: ").strip()
            confirm = input(f"Delete {cluster_id}? This is permanent. Type 'yes' to confirm: ")
            if confirm.lower() == 'yes':
                generator.delete_credentials(cluster_id)
            else:
                print("Cancelled")
                
        elif choice == '6':
            print("👋 Goodbye")
            break
        else:
            print("Invalid choice. Select 1-6")

if __name__ == "__main__":
    main()
