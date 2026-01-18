#!/usr/bin/env python3
"""
Generate a secure API key for Vector Storage Service
"""
import secrets
import os

def generate_api_key(length=32):
    """Generate a cryptographically secure API key"""
    return secrets.token_hex(length)

def create_env_file(api_key):
    """Create .env file with the API key"""
    env_content = f"""# Vector Storage Service Configuration
# Generated: {os.popen('date').read().strip()}

# Security - IMPORTANT!
API_KEY={api_key}

# CORS (Optional - comma separated origins)
# ALLOWED_ORIGINS=https://your-express-app.com,https://your-frontend.com

# Server Configuration (Optional)
# PORT=8000
# HOST=0.0.0.0
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")
    print(f"📁 Location: {os.path.abspath('.env')}")

def main():
    print("🔐 Vector Storage Service - API Key Generator")
    print("=" * 50)
    
    # Check if .env already exists
    if os.path.exists('.env'):
        response = input("\n⚠️  .env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("❌ Cancelled. Existing .env file kept.")
            return
    
    # Generate API key
    print("\n🔑 Generating secure API key...")
    api_key = generate_api_key()
    
    # Create .env file
    create_env_file(api_key)
    
    print("\n" + "=" * 50)
    print("🎉 Setup Complete!")
    print("=" * 50)
    print(f"\n📋 Your API Key:")
    print(f"   {api_key}")
    print("\n⚠️  Keep this key secret! Don't commit to Git.")
    print("\n📝 Next steps:")
    print("   1. Add .env to .gitignore (if not already)")
    print("   2. Set API_KEY on Railway/Cloud Run deployment")
    print("   3. Add API key to your Express server .env:")
    print(f"      VECTOR_STORAGE_API_KEY={api_key}")
    print("\n🚀 Ready to deploy!")
    print("\n📖 See INTEGRATION-GUIDE.md for usage examples")

if __name__ == "__main__":
    main()
