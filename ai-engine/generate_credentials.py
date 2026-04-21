import secrets

def generate_credentials(user_name):
    """Generate credentials for a beta user"""
    cluster_id = f"{user_name}-{secrets.token_hex(4)}"
    api_key = f"gpu_opt_{secrets.token_hex(32)}"
    
    print(f"\n🎫 Credentials for: {user_name}")
    print("=" * 60)
    print(f"Cluster ID: {cluster_id}")
    print(f"API Key: {api_key}")
    print("=" * 60)
    print(f"\n📋 Send these to the user!")
    
    return cluster_id, api_key

if __name__ == "__main__":
    name = input("Enter user/company name: ").strip().lower().replace(" ", "-")
    generate_credentials(name)
