from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime

app = FastAPI(title="Bridge Pattern – Integrações")

# ----------------------------
# Models / Enums
# ----------------------------
class EventoModel(BaseModel):
    titulo: str
    data: datetime
    local: str
    descricao: str

class ResultadoModel(BaseModel):
    sucesso: bool
    mensagem: str

class IntegracaoType(str, Enum):
    calendario = "calendario"
    social    = "social"
    mapas     = "mapas"

class PlataformaType(str, Enum):
    google       = "google"
    outlook      = "outlook"
    facebook     = "facebook"
    whatsapp     = "whatsapp"
    instagram    = "instagram"
    google_maps  = "google_maps"

class RequestIntegracao(BaseModel):
    tipo: IntegracaoType
    plataforma: PlataformaType
    evento: EventoModel

# ----------------------------
# Bridge Implementor
# ----------------------------
class Integrador(ABC):
    @abstractmethod
    def integrar(self, evento: EventoModel) -> ResultadoModel:
        ...

# Calendário
class GoogleCalendarIntegrator(Integrador):
    def integrar(self, evento: EventoModel) -> ResultadoModel:
        return ResultadoModel(sucesso=True, mensagem=f"'{evento.titulo}' adicionado ao Google Calendar")

class OutlookCalendarIntegrator(Integrador):
    def integrar(self, evento: EventoModel) -> ResultadoModel:
        return ResultadoModel(sucesso=True, mensagem=f"'{evento.titulo}' adicionado ao Outlook Calendar")

# Social
class FacebookShareIntegrator(Integrador):
    def integrar(self, evento: EventoModel) -> ResultadoModel:
        return ResultadoModel(sucesso=True, mensagem=f"'{evento.titulo}' compartilhado no Facebook")

class WhatsAppShareIntegrator(Integrador):
    def integrar(self, evento: EventoModel) -> ResultadoModel:
        return ResultadoModel(sucesso=True, mensagem=f"'{evento.titulo}' enviado via WhatsApp")

class InstagramShareIntegrator(Integrador):
    def integrar(self, evento: EventoModel) -> ResultadoModel:
        return ResultadoModel(sucesso=True, mensagem=f"'{evento.titulo}' compartilhado no Instagram")

# Mapas
class GoogleMapsIntegrator(Integrador):
    def integrar(self, evento: EventoModel) -> ResultadoModel:
        return ResultadoModel(sucesso=True, mensagem=f"Local '{evento.local}' aberto no Google Maps")

# ----------------------------
# Bridge Abstraction
# ----------------------------
class Integracao(ABC):
    def __init__(self, integrador: Integrador):
        self._integrador = integrador

    @abstractmethod
    def executar(self, evento: EventoModel) -> ResultadoModel:
        ...

class CalendarIntegracao(Integracao):
    def executar(self, evento: EventoModel) -> ResultadoModel:
        # Aqui você poderia validar data, checar disponibilidade, etc.
        return self._integrador.integrar(evento)

class SocialMediaIntegracao(Integracao):
    def executar(self, evento: EventoModel) -> ResultadoModel:
        # Aqui você poderia montar texto, hashtags, etc.
        return self._integrador.integrar(evento)

class MapsIntegracao(Integracao):
    def executar(self, evento: EventoModel) -> ResultadoModel:
        # Aqui você poderia geocodar o endereço, etc.
        return self._integrador.integrar(evento)

# ----------------------------
# Factories
# ----------------------------
def factory_integrador(tipo: IntegracaoType, plataforma: PlataformaType) -> Integrador:
    # Calendário
    if tipo == IntegracaoType.calendario:
        if plataforma == PlataformaType.google:  return GoogleCalendarIntegrator()
        if plataforma == PlataformaType.outlook: return OutlookCalendarIntegrator()
    # Social
    if tipo == IntegracaoType.social:
        if plataforma == PlataformaType.facebook:  return FacebookShareIntegrator()
        if plataforma == PlataformaType.whatsapp:  return WhatsAppShareIntegrator()
        if plataforma == PlataformaType.instagram: return InstagramShareIntegrator()
    # Mapas
    if tipo == IntegracaoType.mapas and plataforma == PlataformaType.google_maps:
        return GoogleMapsIntegrator()
    raise HTTPException(400, "Tipo ou plataforma inválidos")

def factory_abstracao(tipo: IntegracaoType, integrador: Integrador) -> Integracao:
    if tipo == IntegracaoType.calendario: return CalendarIntegracao(integrador)
    if tipo == IntegracaoType.social:     return SocialMediaIntegracao(integrador)
    if tipo == IntegracaoType.mapas:      return MapsIntegracao(integrador)
    raise HTTPException(500, "Tipo de integração desconhecido")

# ----------------------------
# Endpoint
# ----------------------------
@app.post("/integrar", response_model=ResultadoModel)
def integrar_bridge(req: RequestIntegracao):
    integrador = factory_integrador(req.tipo, req.plataforma)
    bridge    = factory_abstracao(req.tipo, integrador)
    return bridge.executar(req.evento)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)