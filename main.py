#!/usr/bin/env python3
"""
Enhanced Menu Launcher
Runs the enhanced menu system with Redis authentication and cart management
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def main():
    """Main application entry point"""
    try:
        print("🚀 Starting Enhanced Mercado Livre System...")
        print("   With Redis Authentication & Cart Management")
        print("="*60)
        
        # Test database connections first
        from src.config import client
        client.admin.command('ping')
        print("✅ MongoDB conectado com sucesso!")
        
        # Seed admin user
        print("\n🌱 Seeding admin user...")
        from src.seed_admin_user import create_admin_user
        create_admin_user()
        
        from src.myredis import redis_manager
        redis_success, redis_message = redis_manager.test_connection()
        if redis_success:
            print(f"✅ {redis_message}")
        else:
            print(f"❌ {redis_message}")
            print("Continuando sem Redis...")
        
        # Import and start enhanced menu
        from src.enhanced_menu import EnhancedMenu
        menu = EnhancedMenu()
        menu.main_menu()
        
    except Exception as e:
        print(f"❌ Erro ao iniciar o sistema: {e}")
        print("Verifique sua conexão com a internet e tente novamente.")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
