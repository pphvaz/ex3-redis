"""
Authentication and Session Management Module
Handles user login, logout, and session management using Redis
"""

import json
from datetime import datetime
from ..models import usuario
from ..myredis import redis_manager

class AuthManager:
    def __init__(self):
        self.redis = redis_manager
    
    def login_user(self, nome, cpf=None):
        """
        Login user by name and optionally CPF
        Returns (success, message, user_data)
        """
        try:
            # Find user in MongoDB
            usuarios = usuario.find_usuario(nome)
            if not usuarios:
                return False, "Usuário não encontrado", None
            
            # If multiple users with same name, ask for CPF
            if len(usuarios) > 1:
                if not cpf:
                    return False, "Múltiplos usuários encontrados. Por favor, informe o CPF.", None
                
                # Find user by name and CPF
                user_found = None
                for user in usuarios:
                    if user.get('cpf') == cpf:
                        user_found = user
                        break
                
                if not user_found:
                    return False, "Usuário não encontrado com o CPF informado.", None
            else:
                user_found = usuarios[0]
            
            # Create user session in Redis
            user_id = str(user_found.get('_id'))
            user_data = {
                "nome": user_found.get('nome'),
                "sobrenome": user_found.get('sobrenome'),
                "cpf": user_found.get('cpf'),
                "enderecos": user_found.get('end', []),
                "mongo_id": str(user_found.get('_id'))
            }
            
            success, message = self.redis.create_user_session(user_id, user_data)
            if not success:
                return False, f"Erro ao criar sessão: {message}", None
            
            return True, f"Login realizado com sucesso! Bem-vindo, {user_found.get('nome')}!", user_data
            
        except Exception as e:
            return False, f"Erro no login: {str(e)}", None
    
    def logout_user(self, user_id):
        """
        Logout user and clear session
        Returns (success, message)
        """
        try:
            success, message = self.redis.delete_user_session(user_id)
            if success:
                return True, "Logout realizado com sucesso!"
            else:
                return False, f"Erro no logout: {message}"
        except Exception as e:
            return False, f"Erro no logout: {str(e)}"
    
    def get_current_user(self, user_id):
        """
        Get current logged in user data
        Returns (success, message, user_data)
        """
        try:
            if not self.redis.is_user_logged_in(user_id):
                return False, "Usuário não está logado", None
            
            success, session_data = self.redis.get_user_session(user_id)
            if not success:
                return False, f"Erro ao obter sessão: {session_data}", None
            
            # Parse user data from session
            user_data = json.loads(session_data.get('user_data', '{}'))
            return True, "Usuário logado", user_data
            
        except Exception as e:
            return False, f"Erro ao obter usuário: {str(e)}", None
    
    def is_user_logged_in(self, user_id):
        """
        Check if user is logged in
        Returns boolean
        """
        return self.redis.is_user_logged_in(user_id)
    
    def get_user_display_name(self, user_data):
        """
        Get user display name from user data
        """
        if not user_data:
            return "Usuário"
        
        nome = user_data.get('nome', '')
        sobrenome = user_data.get('sobrenome', '')
        return f"{nome} {sobrenome}".strip()
    
    def get_user_id_from_name(self, nome):
        """
        Get user ID from name (for backward compatibility)
        Returns (success, user_id)
        """
        try:
            usuarios = usuario.find_usuario(nome)
            if not usuarios:
                return False, None
            
            # Return first user's ID
            user_id = str(usuarios[0].get('_id'))
            return True, user_id
        except Exception as e:
            return False, None

# Create global auth manager instance
auth_manager = AuthManager()
