from abc import ABC, abstractmethod
from django.contrib.auth.models import User

class EventService(ABC):
    @abstractmethod
    def create_event(self, user: User, event_data: dict) -> dict:
        pass
    
    @abstractmethod
    def edit_event(self, user: User, event_id: int, event_data: dict) -> dict:
        pass
    
    @abstractmethod
    def delete_event(self, user: User, event_id: int) -> bool:
        pass


class EventReal(EventService):
    def create_event(self, user: User, event_data: dict) -> dict:
        print("EventReal: Criando evento no banco de dados")
        #criação de evento
        return {"id": 1, "name": event_data.get("name"), "status": "created"}
    
    def edit_event(self, user: User, event_id: int, event_data: dict) -> dict:
        print(f"EventReal: Editando evento {event_id}")
        #edição de evento
        return {"id": event_id, "name": event_data.get("name"), "status": "updated"}
    
    def delete_event(self, user: User, event_id: int) -> bool:
        print(f"EventReal: Deletando evento {event_id}")
        #exclusão de evento
        return True


#serviço de autenticação e autorização
class AuthService:
    def is_authenticated(self, user: User) -> bool:
        return user.is_authenticated
    
    def is_authorized(self, user: User, permission: str) -> bool:
        #verificação de permissões
        if permission == "admin":
            return user.is_staff
        return True


#logging
class Logger:
    def log_action(self, user: User, action: str, details: str):
        print(f"LOG: Usuário {user.username} executou '{action}' - {details}")


#proxy que controla o acesso ao serviço real
class EventProxy(EventService):
    def __init__(self):
        self._real_service = EventReal()
        self._auth_service = AuthService()
        self._logger = Logger()
    
    def create_event(self, user: User, event_data: dict) -> dict:
        # 1. Verificar autenticação
        if not self._auth_service.is_authenticated(user):
            raise PermissionError("Usuário não autenticado")
        
        # 2. Verificar autorização
        if not self._auth_service.is_authorized(user, "admin"):
            raise PermissionError("Usuário não autorizado")
        
        # 3. Delegar para o serviço real
        result = self._real_service.create_event(user, event_data)
        
        # 4. Registrar a operação
        self._logger.log_action(user, "create_event", f"Criou o evento: {result['name']}")
        
        return result
    
    def edit_event(self, user: User, event_id: int, event_data: dict) -> dict:
        if not self._auth_service.is_authenticated(user):
            raise PermissionError("Usuário não autenticado")
        
        if not self._auth_service.is_authorized(user, "admin"):
            raise PermissionError("Usuário não autorizado")
        
        result = self._real_service.edit_event(user, event_id, event_data)
        
        self._logger.log_action(user, "edit_event", f"Editou o evento {event_id}")
        
        return result
    
    def delete_event(self, user: User, event_id: int) -> bool:
        if not self._auth_service.is_authenticated(user):
            raise PermissionError("Usuário não autenticado")
        
        if not self._auth_service.is_authorized(user, "admin"):
            raise PermissionError("Usuário não autorizado")
        
        result = self._real_service.delete_event(user, event_id)
        
        self._logger.log_action(user, "delete_event", f"Deletou o evento {event_id}")
        
        return result
