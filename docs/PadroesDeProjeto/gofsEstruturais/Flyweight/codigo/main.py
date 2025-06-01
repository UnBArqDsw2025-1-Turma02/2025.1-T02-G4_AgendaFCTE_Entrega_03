from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import List
import uvicorn

app = FastAPI()

# --- Flyweight classes ---

class LocalFlyweight:
    def __init__(self, nome: str, endereco: str):
        self.nome = nome
        self.endereco = endereco

    def __str__(self):
        return f"{self.nome} - {self.endereco}"

    def to_dict(self):
        return {"nome": self.nome, "endereco": self.endereco}

class LocalFactory:
    _locais = {}

    @classmethod
    def get_local(cls, nome: str, endereco: str):
        key = (nome.strip().lower(), endereco.strip().lower())
        if key not in cls._locais:
            print(f"[Criando novo Local] {nome} - {endereco}")
            cls._locais[key] = LocalFlyweight(nome, endereco)
        else:
            print(f"[Reutilizando Local] {nome} - {endereco}")
        return cls._locais[key]

    @classmethod
    def quantidade_locais(cls):
        return len(cls._locais)


class Evento:
    def __init__(self, nome_evento: str, data: str, local: LocalFlyweight):
        self.nome_evento = nome_evento
        self.data = data
        self.local = local

    def to_dict(self):
        return {
            "nome_evento": self.nome_evento,
            "data": self.data,
            "local": self.local.to_dict()
        }

# Estado global
eventos: List[Evento] = []

# --- Pydantic Models para requisições e respostas ---

class LocalRequest(BaseModel):
    nome: str
    endereco: str

    model_config = ConfigDict(from_attributes=True)

class EventoRequest(BaseModel):
    nome_evento: str
    data: str
    local: LocalRequest

    model_config = ConfigDict(from_attributes=True)

class EventoResponse(BaseModel):
    nome_evento: str
    data: str
    local: LocalRequest

    model_config = ConfigDict(from_attributes=True)

# --- Rotas ---

@app.post("/local")
def criar_local(local_req: LocalRequest):
    local = LocalFactory.get_local(local_req.nome, local_req.endereco)
    return {"local": str(local), "total_locais": LocalFactory.quantidade_locais()}

@app.post("/evento", response_model=EventoResponse)
def criar_evento(evento_req: EventoRequest):
    try:
        local = LocalFactory.get_local(evento_req.local.nome, evento_req.local.endereco)
        evento = Evento(evento_req.nome_evento, evento_req.data, local)
        eventos.append(evento)
        return evento.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Testes via terminal ---

def teste_terminal():
    fabrica = LocalFactory()
    local1 = fabrica.get_local("Auditório A", "Campus FCTE")
    local2 = fabrica.get_local("Auditório A", "Campus FCTE")  # Mesmo local de a de antes, irá reaproveitar
    local3 = fabrica.get_local("Sala 101", "Prédio de Engenharia")
    local4 = fabrica.get_local("Auditório A", "Campus FCTE")  # Mesmo local de a de antes, irá reaproveitar
    local5 = fabrica.get_local("Sala 101", "Prédio de Engenharia")  # Mesmo de a de antes, irá reaproveitar
    local6 = fabrica.get_local("Auditório B", "Campus FCTE")  # Novo local
    
    evento1 = Evento("Palestra sobre IA", "10/06/2025", local1)
    evento2 = Evento("Oficina de Python", "11/06/2025", local2)
    evento3 = Evento("Workshop de Robótica", "12/06/2025", local3)
    evento4 = Evento("Seminário de Dados", "13/06/2025", local4)
    evento5 = Evento("Curso de Arduino", "14/06/2025", local5)
    evento6 = Evento("Hackathon de Inovação", "15/06/2025", local6)
    eventos = [evento1, evento2, evento3, evento4, evento5, evento6]
    print("\n==== Eventos Cadastrados ====")
    for evento in eventos:
        print(evento.to_dict())
    print("\n==== Relatório de Locais ====")
    print(f"Quantidade de locais únicos criados: {fabrica.quantidade_locais()}")
    print("\n==== Teste de Objeto Compartilhado ====")
    print(f"local1 é local2? {local1 is local2}")
    print(f"local1 é local4? {local1 is local4}")
    print(f"local3 é local5? {local3 is local5}")
    print(f"local1 é local6? {local1 is local6}")
    print(f"local2 é local6? {local2 is local6}")
    print(f"local3 é local6? {local3 is local6}")
    print("\n==== Locais Criados ====")
    print("Locais criados:")
    print(local1)
    print(local2)
    print(local3)
    print(local4)
    print(local5)
    print(local6)
    print(f"Locais únicos: {fabrica.quantidade_locais()}") 

# --- Main ---

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        teste_terminal()