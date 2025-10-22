#!/usr/bin/env python3
"""
Admin User Seed Script
Creates a default admin user in the database
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def create_admin_user():
    """Create admin user in the database"""
    try:
        from .config import client, db
        from .models.usuario import create_usuario_schema, insert_usuario
        
        print("🌱 Seeding admin user...")
        
        # Check if admin user already exists
        existing_admin = db.usuario.find_one({"nome": "admin"})
        if existing_admin:
            print("✅ Admin user already exists!")
            print(f"   ID: {existing_admin.get('_id')}")
            print(f"   Name: {existing_admin.get('nome')} {existing_admin.get('sobrenome')}")
            print(f"   CPF: {existing_admin.get('cpf')}")
            return True
        
        # Create admin user schema
        admin_data = create_usuario_schema(
            nome="admin",
            sobrenome="system",
            cpf="000.000.000-00",
            enderecos=["Sistema", "Administração"]
        )
        
        # Insert admin user
        success, result = insert_usuario(admin_data)
        
        if success:
            print("✅ Admin user created successfully!")
            print(f"   ID: {result}")
            print(f"   Name: admin system")
            print(f"   CPF: 000.000.000-00")
            print(f"   Addresses: Sistema, Administração")
            return True
        else:
            print(f"❌ Error creating admin user: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Error seeding admin user: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main seed function"""
    print("="*50)
    print("           ADMIN USER SEED SCRIPT")
    print("="*50)
    
    try:
        # Test database connection
        from .config import client
        client.admin.command('ping')
        print("✅ MongoDB connected successfully!")
        
        # Create admin user
        success = create_admin_user()
        
        if success:
            print("\n🎉 Admin user seed completed successfully!")
            print("You can now log in with:")
            print("   Name: admin")
            print("   CPF: 000.000.000-00 (optional)")
        else:
            print("\n❌ Admin user seed failed!")
            
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        print("Please check your MongoDB connection.")

if __name__ == "__main__":
    main()
