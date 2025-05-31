from abc import ABC, abstractmethod
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
import uvicorn

# --- models ---

class Evento:
    def __init__(self, nome, descricao, data, hora, tipo, local=None, link=None):
        self.nome = nome
        self.descricao = descricao
        self.data = data
        self.hora = hora
        self.tipo = tipo
        self.local = local
        self.link = link

    def detalhes(self):
        if self.tipo == 'Presencial':
            return f"Local: {self.local}"
        elif self.tipo == 'Online':
            return f"Link: {self.link}"
        elif self.tipo == 'Híbrido':
            return f"Local: {self.local} | Link: {self.link}"
        return "Sem detalhes"

    def to_dict(self):
        return {
            "nome": self.nome,
            "descricao": self.descricao,
            "data": self.data,
            "hora": self.hora,
            "tipo": self.tipo,
            "local": self.local,
            "link": self.link,
            "detalhes": self.detalhes()
        }


# --- Classes para Factory Method ---

class EventoFactory(ABC):
    @abstractmethod
    def criar_evento(self, **kwargs) -> Evento:
        pass


class EventoPresencialFactory(EventoFactory):
    def criar_evento(self, nome, descricao, data, hora, local):
        return Evento(
            nome=nome,
            descricao=descricao,
            data=data,
            hora=hora,
            tipo='Presencial',
            local=local
        )


class EventoOnlineFactory(EventoFactory):
    def criar_evento(self, nome, descricao, data, hora, link):
        return Evento(
            nome=nome,
            descricao=descricao,
            data=data,
            hora=hora,
            tipo='Online',
            link=link
        )


class EventoHibridoFactory(EventoFactory):
    def criar_evento(self, nome, descricao, data, hora, local, link):
        return Evento(
            nome=nome,
            descricao=descricao,
            data=data,
            hora=hora,
            tipo='Híbrido',
            local=local,
            link=link
        )


# --- Função para os testes do terminal (opcional) ---

def exibir_evento(evento):
    cores = {
        'Presencial': '\033[42m',
        'Online': '\033[44m',
        'Híbrido': '\033[43m',
    }
    reset = '\033[0m'
    cor = cores.get(evento.tipo, '')

    print(f"{cor}{' '*50}{reset}")
    print(f"{cor}  Evento: {evento.nome:<39}{reset}")
    print(f"{cor}  Tipo: {evento.tipo:<42}{reset}")
    print(f"{cor}  Data: {evento.data} às {evento.hora:<26}{reset}")
    print(f"{cor}  Descrição: {evento.descricao:<33}{reset}")
    print(f"{cor}  Detalhes: {evento.detalhes():<35}{reset}")
    print(f"{cor}{' '*50}{reset}")
    print()

eventos: List[Evento] = []

# --- FastAPI ---

app = FastAPI()

# --- Pydantic models para entrada e saída ---

class EventoRequest(BaseModel):
    nome: str
    descricao: str
    data: str
    hora: str
    tipo: str 
    local: Optional[str] = None
    link: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class EventoResponse(EventoRequest):
    detalhes: str


@app.post("/evento", response_model=EventoResponse)
def criar_evento(evento_req: EventoRequest):
    tipo = evento_req.tipo.lower()

    if tipo == 'presencial':
        if not evento_req.local:
            raise HTTPException(status_code=400, detail="Local é obrigatório para evento presencial")
        factory = EventoPresencialFactory()
        evento = factory.criar_evento(
            nome=evento_req.nome,
            descricao=evento_req.descricao,
            data=evento_req.data,
            hora=evento_req.hora,
            local=evento_req.local
        )

    elif tipo == 'online':
        if not evento_req.link:
            raise HTTPException(status_code=400, detail="Link é obrigatório para evento online")
        factory = EventoOnlineFactory()
        evento = factory.criar_evento(
            nome=evento_req.nome,
            descricao=evento_req.descricao,
            data=evento_req.data,
            hora=evento_req.hora,
            link=evento_req.link
        )

    elif tipo == 'híbrido' or tipo == 'hibrido':
        if not evento_req.local or not evento_req.link:
            raise HTTPException(status_code=400, detail="Local e Link são obrigatórios para evento híbrido")
        factory = EventoHibridoFactory()
        evento = factory.criar_evento(
            nome=evento_req.nome,
            descricao=evento_req.descricao,
            data=evento_req.data,
            hora=evento_req.hora,
            local=evento_req.local,
            link=evento_req.link
        )

    else:
        raise HTTPException(status_code=400, detail="Tipo de evento inválido. Use: Presencial, Online ou Híbrido.")

    eventos.append(evento)
    return evento.to_dict()


@app.get("/eventos", response_model=List[EventoResponse])
def listar_eventos():
    return [evento.to_dict() for evento in eventos]


# --- Função para executar no terminal ---

def executar_terminal():
    presencial_factory = EventoPresencialFactory()
    online_factory = EventoOnlineFactory()
    hibrido_factory = EventoHibridoFactory()

    evento1 = presencial_factory.criar_evento(
        nome="Workshop de Robótica",
        descricao="Aprenda robótica na prática.",
        data="2025-06-10",
        hora="14:00",
        local="Auditório FCTE"
    )

    evento2 = online_factory.criar_evento(
        nome="Palestra sobre IA",
        descricao="Inteligência Artificial no futuro.",
        data="2025-06-12",
        hora="19:00",
        link="https://meet.google.com/abc-xyz"
    )

    evento3 = hibrido_factory.criar_evento(
        nome="Simpósio de Tecnologia",
        descricao="Encontro de profissionais da área.",
        data="2025-06-15",
        hora="09:00",
        local="Sala 101 FCTE",
        link="https://zoom.us/simp-tec"
    )

    lista_eventos = [evento1, evento2, evento3]

    print("\n\033[1mAGENDA FCTE - LISTA DE EVENTOS\033[0m\n")
    for evento in lista_eventos:
        exibir_evento(evento)
    print("\033[1mFIM DA AGENDA\033[0m")
    print("\033[1mObrigado por usar a Agenda FCTE!\033[0m")

# --- Execução do FastAPI ou Terminal ---

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        executar_terminal()
