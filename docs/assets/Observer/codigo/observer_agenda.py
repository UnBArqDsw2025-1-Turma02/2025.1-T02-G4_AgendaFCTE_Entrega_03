from abc import ABC, abstractmethod
from datetime import datetime
import logging

#Interface Observer
class Observer(ABC):
    @abstractmethod
    def update(self, subject):
        pass

class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self)

#Sujeito Concreto 
class Evento(Subject):
    def __init__(self, nome):
        super().__init__()
        self._nome = nome
        self._estado = None
    
    @property
    def estado(self):
        return self._estado
    
    @estado.setter
    def estado(self, value):
        self._estado = value
        self.notify()  #Notifica todos os observers
    
    @property
    def nome(self):
        return self._nome

#Observador de Log
class LogNotifier(Observer):
    def __init__(self, log_file='agenda_fcte.log'):
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S'
        )
    
    def update(self, subject):
        logging.info(
            f"Evento '{subject.nome}' alterado para estado: {subject.estado}"
        )
        print(f"[LOG] Registro salvo em arquivo: Evento '{subject.nome}' -> {subject.estado}")

#Observador de Email 
class EmailNotifier(Observer):
    def update(self, subject):
        print(f"[EMAIL] Notificação enviada: Evento '{subject.nome}' está agora '{subject.estado}'")

if __name__ == "__main__":
    #Criar um evento
    reuniao = Evento("Reunião de Planejamento")
    
    #Criar e registrar os observers
    logger = LogNotifier()
    email_notifier = EmailNotifier()
    
    reuniao.attach(logger)
    reuniao.attach(email_notifier)
    
    #Simular mudanças de estado
    print("\n--- Primeira Alteração ---")
    reuniao.estado = "Agendado"
    
    print("\n--- Segunda Alteração ---")
    reuniao.estado = "Adiado"
    
    #Remover um observer 
    reuniao.detach(email_notifier)
    
    print("\n--- Terceira Alteração (apenas log) ---")
    reuniao.estado = "Confirmado"