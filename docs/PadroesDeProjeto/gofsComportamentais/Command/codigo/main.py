# main.py

from abc import ABC, abstractmethod
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List

# ==============================
# Modelos (Usuario e Evento)
# ==============================

class Usuario(BaseModel):
    id: int
    nome: str

class Evento:
    def __init__(self, evento_id: int, nome: str):
        self.id = evento_id
        self.nome = nome

    def confirmar_presenca(self, usuario: Usuario):
        print(f"{usuario.nome} confirmou presença no evento {self.nome}")

    def curtir(self, usuario: Usuario):
        print(f"{usuario.nome} curtiu o evento {self.nome}")

    def favoritar(self, usuario: Usuario):
        print(f"{usuario.nome} favoritou o evento {self.nome}")

    def indicar_desinteresse(self, usuario: Usuario):
        print(f"{usuario.nome} demonstrou desinteresse pelo evento {self.nome}")

    def requisitar_participacao(self, usuario: Usuario):
        print(f"{usuario.nome} requisitou participação no evento {self.nome}")

    def comentar_evento(self, usuario: Usuario, comentario: str):
        print(f"{usuario.nome} comentou no evento {self.nome}: \"{comentario}\"")

    def denunciar_evento(self, usuario: Usuario, motivo: str):
        print(f"{usuario.nome} denunciou o evento {self.nome} pelo motivo: \"{motivo}\"")


# ==============================
# Interface Command
# ==============================

class Comando(ABC):
    @abstractmethod
    def executar(self) -> None:
        pass


# ==============================
# Concrete Commands
# ==============================

class ConfirmarPresencaCommand(Comando):
    def __init__(self, usuario: Usuario, evento: Evento):
        self.usuario = usuario
        self.evento = evento

    def executar(self) -> None:
        self.evento.confirmar_presenca(self.usuario)


class CurtirEventoCommand(Comando):
    def __init__(self, usuario: Usuario, evento: Evento):
        self.usuario = usuario
        self.evento = evento

    def executar(self) -> None:
        self.evento.curtir(self.usuario)


class FavoritarEventoCommand(Comando):
    def __init__(self, usuario: Usuario, evento: Evento):
        self.usuario = usuario
        self.evento = evento

    def executar(self) -> None:
        self.evento.favoritar(self.usuario)


class DesinteresseEventoCommand(Comando):
    def __init__(self, usuario: Usuario, evento: Evento):
        self.usuario = usuario
        self.evento = evento

    def executar(self) -> None:
        self.evento.indicar_desinteresse(self.usuario)


class RequisitarParticipacaoCommand(Comando):
    def __init__(self, usuario: Usuario, evento: Evento):
        self.usuario = usuario
        self.evento = evento

    def executar(self) -> None:
        self.evento.requisitar_participacao(self.usuario)


class ComentarEventoCommand(Comando):
    def __init__(self, usuario: Usuario, evento: Evento, comentario: str):
        self.usuario = usuario
        self.evento = evento
        self.comentario = comentario

    def executar(self) -> None:
        self.evento.comentar_evento(self.usuario, self.comentario)


class DenunciarEventoCommand(Comando):
    def __init__(self, usuario: Usuario, evento: Evento, motivo: str):
        self.usuario = usuario
        self.evento = evento
        self.motivo = motivo

    def executar(self) -> None:
        self.evento.denunciar_evento(self.usuario, self.motivo)


# ==============================
# Invoker: GerenciadorDeComandos
# ==============================

class GerenciadorDeComandos:
    def __init__(self):
        self.fila: List[Comando] = []

    def set_command(self, comando: Comando) -> None:
        self.fila.append(comando)

    def executar_comandos(self) -> None:
        for cmd in self.fila:
            cmd.executar()
        self.fila.clear()


# ==============================
# Cliente: FastAPI
# ==============================

app = FastAPI()
manager = GerenciadorDeComandos()

# Simulação de storage em memória
eventos = {
    1: Evento(1, "Festa Junina"),
    2: Evento(2, "Palestra de Python")
}

usuarios = {
    1: Usuario(id=1, nome="Alice"),
    2: Usuario(id=2, nome="Bob")
}

@app.post("/eventos/{evento_id}/confirmar-presenca/")
def confirmar_presenca(evento_id: int, usuario_id: int):
    evento = eventos.get(evento_id)
    usuario = usuarios.get(usuario_id)
    if not evento or not usuario:
        raise HTTPException(status_code=404, detail="Evento ou usuário não encontrado")
    cmd = ConfirmarPresencaCommand(usuario, evento)
    manager.set_command(cmd)
    manager.executar_comandos()
    return {"status": "presença confirmada"}

@app.post("/eventos/{evento_id}/curtir/")
def curtir_evento(evento_id: int, usuario_id: int):
    evento = eventos.get(evento_id)
    usuario = usuarios.get(usuario_id)
    if not evento or not usuario:
        raise HTTPException(status_code=404, detail="Evento ou usuário não encontrado")
    cmd = CurtirEventoCommand(usuario, evento)
    manager.set_command(cmd)
    manager.executar_comandos()
    return {"status": "evento curtido"}

@app.post("/eventos/{evento_id}/favoritar/")
def favoritar_evento(evento_id: int, usuario_id: int):
    evento = eventos.get(evento_id)
    usuario = usuarios.get(usuario_id)
    if not evento or not usuario:
        raise HTTPException(status_code=404, detail="Evento ou usuário não encontrado")
    cmd = FavoritarEventoCommand(usuario, evento)
    manager.set_command(cmd)
    manager.executar_comandos()
    return {"status": "evento favoritado"}

@app.post("/eventos/{evento_id}/desinteresse/")
def indicar_desinteresse(evento_id: int, usuario_id: int):
    evento = eventos.get(evento_id)
    usuario = usuarios.get(usuario_id)
    if not evento or not usuario:
        raise HTTPException(status_code=404, detail="Evento ou usuário não encontrado")
    cmd = DesinteresseEventoCommand(usuario, evento)
    manager.set_command(cmd)
    manager.executar_comandos()
    return {"status": "desinteresse indicado"}

@app.post("/eventos/{evento_id}/requisitar-participacao/")
def requisitar_participacao(evento_id: int, usuario_id: int):
    evento = eventos.get(evento_id)
    usuario = usuarios.get(usuario_id)
    if not evento or not usuario:
        raise HTTPException(status_code=404, detail="Evento ou usuário não encontrado")
    cmd = RequisitarParticipacaoCommand(usuario, evento)
    manager.set_command(cmd)
    manager.executar_comandos()
    return {"status": "participação requisitada"}

# Modelos de requisição para endpoints que recebem JSON
class ComentarioRequest(BaseModel):
    comentario: str

class DenunciaRequest(BaseModel):
    motivo: str

@app.post("/eventos/{evento_id}/comentar/")
def comentar_evento(
    evento_id: int,
    usuario_id: int,
    payload: ComentarioRequest = Body(...),
):
    evento = eventos.get(evento_id)
    usuario = usuarios.get(usuario_id)
    if not evento or not usuario:
        raise HTTPException(status_code=404, detail="Evento ou usuário não encontrado")
    cmd = ComentarEventoCommand(usuario, evento, payload.comentario)
    manager.set_command(cmd)
    manager.executar_comandos()
    return {"status": "comentário adicionado"}

@app.post("/eventos/{evento_id}/denunciar/")
def denunciar_evento(
    evento_id: int,
    usuario_id: int,
    payload: DenunciaRequest = Body(...),
):
    evento = eventos.get(evento_id)
    usuario = usuarios.get(usuario_id)
    if not evento or not usuario:
        raise HTTPException(status_code=404, detail="Evento ou usuário não encontrado")
    cmd = DenunciarEventoCommand(usuario, evento, payload.motivo)
    manager.set_command(cmd)
    manager.executar_comandos()
    return {"status": "denúncia registrada"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True)
