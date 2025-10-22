"""
Test script for Redis functionality
"""

from myredis import redis_manager
from auth import auth_manager
from cart_manager import cart_manager

def test_redis_connection():
    """Test Redis connection"""
    print("=== TESTING REDIS CONNECTION ===")
    success, message = redis_manager.test_connection()
    print(f"Redis Connection: {message}")
    return success

def test_session_management():
    """Test session management"""
    print("\n=== TESTING SESSION MANAGEMENT ===")
    
    # Test user data
    test_user_data = {
        "nome": "Teste",
        "sobrenome": "Usuario",
        "cpf": "12345678901",
        "enderecos": ["Rua Teste, 123"],
        "mongo_id": "test_id_123"
    }
    
    # Test session creation
    success, message = redis_manager.create_user_session("test_user_123", test_user_data)
    print(f"Session Creation: {message}")
    
    if success:
        # Test session retrieval
        success, session_data = redis_manager.get_user_session("test_user_123")
        print(f"Session Retrieval: {'Success' if success else session_data}")
        
        # Test session update
        updated_user_data = test_user_data.copy()
        updated_user_data["nome"] = "Teste Atualizado"
        success, message = redis_manager.update_user_session("test_user_123", updated_user_data)
        print(f"Session Update: {message}")
        
        # Test session deletion
        success, message = redis_manager.delete_user_session("test_user_123")
        print(f"Session Deletion: {message}")

def test_cart_management():
    """Test cart management"""
    print("\n=== TESTING CART MANAGEMENT ===")
    
    test_user_id = "test_cart_user_123"
    
    # Test product data
    test_product = {
        "codProduto": "PROD001",
        "descricao": "Produto Teste",
        "preco": 29.99
    }
    
    # Test adding items to cart
    success, message = cart_manager.add_to_cart(test_user_id, "PROD001", 2)
    print(f"Add to Cart: {message}")
    
    if success:
        # Test getting cart
        success, message, cart_data = cart_manager.get_cart(test_user_id)
        print(f"Get Cart: {'Success' if success else message}")
        if success:
            print(f"Cart Items: {len(cart_data.get('items', []))}")
            print(f"Cart Total: R$ {cart_data.get('total', 0):.2f}")
        
        # Test cart summary
        success, summary = cart_manager.get_cart_summary(test_user_id)
        print(f"Cart Summary: {'Success' if success else summary}")
        if success:
            print(f"Total Items: {summary.get('total_items', 0)}")
            print(f"Total Value: R$ {summary.get('total_value', 0):.2f}")
        
        # Test removing item
        success, message = cart_manager.remove_from_cart(test_user_id, "PROD001")
        print(f"Remove from Cart: {message}")
        
        # Test clearing cart
        success, message = cart_manager.clear_cart(test_user_id)
        print(f"Clear Cart: {message}")

def main():
    """Main test function"""
    print("🧪 TESTING REDIS FUNCTIONALITY")
    print("=" * 50)
    
    # Test Redis connection
    if not test_redis_connection():
        print("❌ Redis connection failed. Please check your configuration.")
        return
    
    # Test session management
    test_session_management()
    
    # Test cart management
    test_cart_management()
    
    print("\n✅ All tests completed!")
    print("Redis is ready for use in your application.")

if __name__ == "__main__":
    main()
