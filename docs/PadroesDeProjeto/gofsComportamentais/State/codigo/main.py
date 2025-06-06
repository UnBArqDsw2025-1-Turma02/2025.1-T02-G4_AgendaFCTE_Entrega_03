from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from datetime import datetime
from abc import ABC, abstractmethod
import uvicorn


app = FastAPI(title="Agenda FCTE - API de Eventos")

# --- State Design Pattern ---

class EventoState(ABC):
    @abstractmethod
    def inscrever(self, evento):
        pass

    @abstractmethod
    def cancelar(self, evento):
        pass

    @abstractmethod
    def favoritar(self, evento):
        pass


class EventoAberto(EventoState):
    def inscrever(self, evento):
        if evento.vagas > 0:
            evento.vagas -= 1
            msg = "Inscrição realizada com sucesso!"
            if evento.vagas == 0:
                evento.state = EventoEncerrado()
            return msg
        else:
            evento.state = EventoEncerrado()
            return evento.inscrever()

    def cancelar(self, evento):
        evento.vagas += 1
        evento.state = EventoAberto()
        return "Inscrição cancelada com sucesso!"

    def favoritar(self, evento):
        return "Evento favoritado com sucesso!"


class EventoEncerrado(EventoState):
    def inscrever(self, evento):
        return "Evento encerrado! Não é possível se inscrever."

    def cancelar(self, evento):
        return "Evento encerrado. Não há inscrição para cancelar."

    def favoritar(self, evento):
        return "Você pode favoritar, mas não se inscrever (evento encerrado)."


class EventoFinalizado(EventoState):
    def inscrever(self, evento):
        return "Evento finalizado. Não é possível se inscrever."

    def cancelar(self, evento):
        return "Evento já aconteceu. Não há inscrição para cancelar."

    def favoritar(self, evento):
        return "Você pode favoritar para futuras referências."


class EventoCancelado(EventoState):
    def inscrever(self, evento):
        return "Evento cancelado. Não é possível se inscrever."

    def cancelar(self, evento):
        return "Evento cancelado. Não há inscrição para cancelar."

    def favoritar(self, evento):
        return "Você não pode favoritar eventos cancelados."


# --- Classe Evento ---

class Evento:
    def __init__(self, nome, vagas, data):
        self.nome = nome
        self.vagas = vagas
        self.data = data
        self.cancelado = False
        self.state = EventoAberto()

    def atualizar_estado(self):
        if self.cancelado:
            self.state = EventoCancelado()
        elif self.data < datetime.now():
            self.state = EventoFinalizado()
        elif self.vagas == 0:
            self.state = EventoEncerrado()
        else:
            self.state = EventoAberto()

    def inscrever(self):
        self.atualizar_estado()
        return self.state.inscrever(self)

    def cancelar(self):
        self.atualizar_estado()
        return self.state.cancelar(self)

    def favoritar(self):
        self.atualizar_estado()
        return self.state.favoritar(self)

    def cancelar_evento(self):
        self.cancelado = True
        self.state = EventoCancelado()

    def get_estado(self):
        return self.state.__class__.__name__

# --- Banco de dados simples ---

eventos_db: Dict[str, Evento] = {}

# --- Models ---

class EventoInput(BaseModel):
    nome: str
    vagas: int
    data: str  # Formato YYYY-MM-DD


# --- Endpoints ---

@app.post("/evento")
def criar_evento(evento: EventoInput):
    data = datetime.strptime(evento.data, "%Y-%m-%d")
    novo_evento = Evento(evento.nome, evento.vagas, data)
    eventos_db[evento.nome] = novo_evento
    return {"mensagem": "Evento criado com sucesso!", "evento": evento.nome}


@app.get("/evento")
def listar_eventos():
    return {
        nome: {
            "vagas": ev.vagas,
            "data": ev.data.strftime("%Y-%m-%d"),
            "estado": ev.get_estado(),
            "cancelado": ev.cancelado
        }
        for nome, ev in eventos_db.items()
    }


@app.post("/evento/{nome}/inscrever")
def inscrever(nome: str):
    evento = eventos_db.get(nome)
    if not evento:
        return {"erro": "Evento não encontrado."}
    msg = evento.inscrever()
    return {
        "evento": nome,
        "mensagem": msg,
        "vagas_restantes": evento.vagas,
        "estado_atual": evento.get_estado()
    }


@app.post("/evento/{nome}/cancelar-inscricao")
def cancelar_inscricao(nome: str):
    evento = eventos_db.get(nome)
    if not evento:
        return {"erro": "Evento não encontrado."}
    msg = evento.cancelar()
    return {
        "evento": nome,
        "mensagem": msg,
        "vagas_restantes": evento.vagas,
        "estado_atual": evento.get_estado()
    }


@app.post("/evento/{nome}/favoritar")
def favoritar(nome: str):
    evento = eventos_db.get(nome)
    if not evento:
        return {"erro": "Evento não encontrado."}
    msg = evento.favoritar()
    return {
        "evento": nome,
        "mensagem": msg,
        "estado_atual": evento.get_estado()
    }


@app.post("/evento/{nome}/cancelar-evento")
def cancelar_evento(nome: str):
    evento = eventos_db.get(nome)
    if not evento:
        return {"erro": "Evento não encontrado."}
    evento.cancelar_evento()
    return {
        "evento": nome,
        "mensagem": "Evento foi cancelado!",
        "estado_atual": evento.get_estado()
    }


# --- Rodar a API ---
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
