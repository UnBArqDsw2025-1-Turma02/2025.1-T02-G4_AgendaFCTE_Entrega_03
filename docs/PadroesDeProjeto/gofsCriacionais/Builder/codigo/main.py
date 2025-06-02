from datetime import datetime

# "Product"
class Evento:
    def __init__(self):
        self.titulo = ""
        self.descricao = ""
        self.local = ""
        self.data_hora = None
        self.link_inscricao = ""
        self.vagas = 0
        self.categorias = []

    def __str__(self):
        return (
            f"Evento: {self.titulo}\n"
            f"Descrição: {self.descricao}\n"
            f"Local: {self.local}\n"
            f"Data e Hora: {self.data_hora}\n"
            f"Link de Inscrição: {self.link_inscricao}\n"
            f"Vagas: {self.vagas}\n"
            f"Categorias: {self.categorias}\n"
        )

# "Abstract Builder"
class EventoBuilder:
    def __init__(self):
        self.evento = Evento()

    def get_evento(self):
        return self.evento

    def build_titulo(self):
        raise NotImplementedError

    def build_descricao(self):
        raise NotImplementedError

    def build_local(self):
        raise NotImplementedError

    def build_data_hora(self):
        raise NotImplementedError

    def build_link_inscricao(self):
        raise NotImplementedError

    def build_vagas(self):
        raise NotImplementedError

    def build_categorias(self):
        raise NotImplementedError

# "ConcreteBuilder 1"
class EventoAcademicoBuilder(EventoBuilder):
    def build_titulo(self):
        self.evento.titulo = "Palestra sobre IA na Educação"

    def build_descricao(self):
        self.evento.descricao = "Discussão sobre aplicações de IA no ambiente universitário."

    def build_local(self):
        self.evento.local = "Auditório FCTE"

    def build_data_hora(self):
        self.evento.data_hora = datetime(2025, 6, 12, 14, 0)

    def build_link_inscricao(self):
        self.evento.link_inscricao = "https://fcte.unb.br/ia-na-educacao"

    def build_vagas(self):
        self.evento.vagas = 150

    def build_categorias(self):
        self.evento.categorias = ["Acadêmico", "Tecnologia"]

# "ConcreteBuilder 2"
class EventoCulturalBuilder(EventoBuilder):
    def build_titulo(self):
        self.evento.titulo = "Sarau Cultural"

    def build_descricao(self):
        self.evento.descricao = "Espaço aberto para apresentações artísticas da comunidade."

    def build_local(self):
        self.evento.local = "Pátio Central"

    def build_data_hora(self):
        self.evento.data_hora = datetime(2025, 6, 20, 18, 30)

    def build_link_inscricao(self):
        self.evento.link_inscricao = "https://fcte.unb.br/sarau"

    def build_vagas(self):
        self.evento.vagas = 80

    def build_categorias(self):
        self.evento.categorias = ["Cultura", "Arte"]

# "Director"
class Organizador:
    def __init__(self):
        self.evento_builder = None

    def set_evento_builder(self, builder):
        self.evento_builder = builder

    def get_evento(self):
        return self.evento_builder.get_evento()

    def construir_evento(self):
        self.evento_builder.build_titulo()
        self.evento_builder.build_descricao()
        self.evento_builder.build_local()
        self.evento_builder.build_data_hora()
        self.evento_builder.build_link_inscricao()
        self.evento_builder.build_vagas()
        self.evento_builder.build_categorias()

# "Client"
if __name__ == "__main__":
    organizador = Organizador()

    # Evento Acadêmico
    builder_academico = EventoAcademicoBuilder()
    organizador.set_evento_builder(builder_academico)
    organizador.construir_evento()
    evento1 = organizador.get_evento()
    print(evento1)

    # Evento Cultural
    builder_cultural = EventoCulturalBuilder()
    organizador.set_evento_builder(builder_cultural)
    organizador.construir_evento()
    evento2 = organizador.get_evento()
    print(evento2)
