#python3 -m pip install redis
#------------------------------------------------------------------
import redis
import json
import time
from datetime import datetime, timedelta
from .config import redis_client

class RedisManager:
    def __init__(self):
        self.redis = redis_client
        self.session_timeout = 3600  # 1 hour in seconds
        self.cart_timeout = 86400    # 24 hours in seconds
    
    def test_connection(self):
        """Test Redis connection"""
        try:
            self.redis.ping()
            return True, "Redis connection successful"
        except Exception as e:
            return False, f"Redis connection failed: {str(e)}"
    
    # User Authentication and Session Management
    def create_user_session(self, user_id, user_data):
        """Create a user session in Redis"""
        try:
            session_key = f"session:{user_id}"
            session_data = {
                "user_id": user_id,
                "user_data": user_data,
                "created_at": datetime.now().isoformat(),
                "last_activity": datetime.now().isoformat()
            }
            
            # Store session data (convert dict to JSON string)
            session_data["user_data"] = json.dumps(user_data)
            self.redis.hset(session_key, mapping=session_data)
            self.redis.expire(session_key, self.session_timeout)
            
            # Store active sessions
            self.redis.sadd("active_sessions", user_id)
            
            return True, "Session created successfully"
        except Exception as e:
            return False, f"Error creating session: {str(e)}"
    
    def get_user_session(self, user_id):
        """Get user session data"""
        try:
            session_key = f"session:{user_id}"
            session_data = self.redis.hgetall(session_key)
            
            if not session_data:
                return False, "Session not found"
            
            # Update last activity
            self.redis.hset(session_key, "last_activity", datetime.now().isoformat())
            self.redis.expire(session_key, self.session_timeout)
            
            return True, session_data
        except Exception as e:
            return False, f"Error getting session: {str(e)}"
    
    def update_user_session(self, user_id, user_data):
        """Update user session data"""
        try:
            session_key = f"session:{user_id}"
            if not self.redis.exists(session_key):
                return False, "Session not found"
            
            # Update user data and last activity
            self.redis.hset(session_key, "user_data", json.dumps(user_data))
            self.redis.hset(session_key, "last_activity", datetime.now().isoformat())
            self.redis.expire(session_key, self.session_timeout)
            
            return True, "Session updated successfully"
        except Exception as e:
            return False, f"Error updating session: {str(e)}"
    
    def delete_user_session(self, user_id):
        """Delete user session"""
        try:
            session_key = f"session:{user_id}"
            self.redis.delete(session_key)
            self.redis.srem("active_sessions", user_id)
            return True, "Session deleted successfully"
        except Exception as e:
            return False, f"Error deleting session: {str(e)}"
    
    def is_user_logged_in(self, user_id):
        """Check if user is logged in"""
        try:
            session_key = f"session:{user_id}"
            return self.redis.exists(session_key)
        except Exception as e:
            return False
    
    # Cart Management
    def save_user_cart(self, user_id, cart_data):
        """Save user cart to Redis"""
        try:
            cart_key = f"cart:{user_id}"
            cart_data["updated_at"] = datetime.now().isoformat()
            
            self.redis.hset(cart_key, mapping={
                "items": json.dumps(cart_data.get("items", [])),
                "total": str(cart_data.get("total", 0)),
                "updated_at": cart_data["updated_at"]
            })
            self.redis.expire(cart_key, self.cart_timeout)
            
            return True, "Cart saved successfully"
        except Exception as e:
            return False, f"Error saving cart: {str(e)}"
    
    def get_user_cart(self, user_id):
        """Get user cart from Redis"""
        try:
            cart_key = f"cart:{user_id}"
            cart_data = self.redis.hgetall(cart_key)
            
            if not cart_data:
                return True, {"items": [], "total": 0, "updated_at": None}
            
            # Parse items from JSON
            items = json.loads(cart_data.get("items", "[]"))
            total = float(cart_data.get("total", 0))
            updated_at = cart_data.get("updated_at")
            
            return True, {
                "items": items,
                "total": total,
                "updated_at": updated_at
            }
        except Exception as e:
            return False, f"Error getting cart: {str(e)}"
    
    def add_item_to_cart(self, user_id, product_data, quantity):
        """Add item to user cart"""
        try:
            # Get current cart
            success, cart_data = self.get_user_cart(user_id)
            if not success:
                return False, cart_data
            
            items = cart_data.get("items", [])
            
            # Check if product already exists in cart
            for item in items:
                if item.get("codProduto") == product_data.get("codProduto"):
                    item["quantidade"] += quantity
                    item["subtotal"] = item["preco"] * item["quantidade"]
                    break
            else:
                # Add new item
                new_item = {
                    "codProduto": product_data.get("codProduto"),
                    "descricao": product_data.get("descricao"),
                    "preco": product_data.get("preco"),
                    "quantidade": quantity,
                    "subtotal": product_data.get("preco") * quantity
                }
                items.append(new_item)
            
            # Calculate total
            total = sum(item.get("subtotal", 0) for item in items)
            
            # Save updated cart
            updated_cart = {
                "items": items,
                "total": total
            }
            
            return self.save_user_cart(user_id, updated_cart)
        except Exception as e:
            return False, f"Error adding item to cart: {str(e)}"
    
    def remove_item_from_cart(self, user_id, cod_produto):
        """Remove item from user cart"""
        try:
            # Get current cart
            success, cart_data = self.get_user_cart(user_id)
            if not success:
                return False, cart_data
            
            items = cart_data.get("items", [])
            
            # Remove item
            items = [item for item in items if item.get("codProduto") != cod_produto]
            
            # Calculate total
            total = sum(item.get("subtotal", 0) for item in items)
            
            # Save updated cart
            updated_cart = {
                "items": items,
                "total": total
            }
            
            return self.save_user_cart(user_id, updated_cart)
        except Exception as e:
            return False, f"Error removing item from cart: {str(e)}"
    
    def clear_user_cart(self, user_id):
        """Clear user cart"""
        try:
            cart_key = f"cart:{user_id}"
            self.redis.delete(cart_key)
            return True, "Cart cleared successfully"
        except Exception as e:
            return False, f"Error clearing cart: {str(e)}"
    
    def get_cart_summary(self, user_id):
        """Get cart summary"""
        try:
            success, cart_data = self.get_user_cart(user_id)
            if not success:
                return False, cart_data
            
            items = cart_data.get("items", [])
            total = cart_data.get("total", 0)
            
            summary = {
                "item_count": len(items),
                "total_items": sum(item.get("quantidade", 0) for item in items),
                "total_value": total,
                "items": items
            }
            
            return True, summary
        except Exception as e:
            return False, f"Error getting cart summary: {str(e)}"
    
    # Utility methods
    def get_active_sessions(self):
        """Get all active sessions"""
        try:
            return self.redis.smembers("active_sessions")
        except Exception as e:
            return set()
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        try:
            active_sessions = self.get_active_sessions()
            expired_sessions = []
            
            for user_id in active_sessions:
                if not self.is_user_logged_in(user_id):
                    expired_sessions.append(user_id)
            
            if expired_sessions:
                self.redis.srem("active_sessions", *expired_sessions)
            
            return True, f"Cleaned up {len(expired_sessions)} expired sessions"
        except Exception as e:
            return False, f"Error cleaning up sessions: {str(e)}"

# Create global Redis manager instance
redis_manager = RedisManager()

# Test connection on import
if __name__ == "__main__":
    success, message = redis_manager.test_connection()
    print(f"Redis Connection: {message}")
    
    if success:
        print("Redis is ready for use!")
    else:
        print("Please check your Redis configuration.")


