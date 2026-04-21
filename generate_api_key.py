import secrets
import json
from datetime import datetime

def generate_credentials(cluster_name):
    """Generate API credentials for a beta user"""
    
    api_key = f"gpu_opt_{secrets.token_hex(32)}"
    cluster_id = f"{cluster_name}-{secrets.token_hex(4)}"
    
    credentials = {
        "cluster_id": cluster_id,
        "api_key": api_key,
        "created_at": datetime.now().isoformat(),
        "status": "active"
    }
    
    print(f"\n🎫 Credentials for: {cluster_name}")
    print("=" * 60)
    print(f"Cluster ID: {cluster_id}")
    print(f"API Key: {api_key}")
    print("=" * 60)
    print(f"\n📋 Install command for this user:")
    print(f"curl -sSL https://raw.githubusercontent.com/mikebains41-debug/ai-gpu-energy-optimizer-/main/ai-engine/install.sh | bash")
    print(f"\n💾 Save these credentials and send to user!")
    
    # Optionally save to file
    with open(f"beta_user_{cluster_name}.json", 'w') as f:
        json.dump(credentials, f, indent=2)
    print(f"\n💾 Credentials saved to: beta_user_{cluster_name}.json")
    
    return credentials

if __name__ == "__main__":
    name = input("Enter beta user/company name: ").strip().lower().replace(" ", "-")
    generate_credentials(name)
