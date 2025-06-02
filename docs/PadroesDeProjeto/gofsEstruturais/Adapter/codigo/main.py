class CadastroEvento:
    def cadastrar_evento(self, evento):
        raise NotImplementedError("Método deve ser implementado pelas subclasses")


class SistemaExternoEventos:
    def registrar(self, dados_evento):
        print(f"[SistemaExterno] Evento registrado: {dados_evento}")


class RepositorioEventos:
    def salvar_evento(self, evento):
        print(f"[RepositorioInterno] Evento salvo: {evento}")


class AdapterSistemaExterno(CadastroEvento):
    def __init__(self, sistema_externo):
        self.sistema_externo = sistema_externo

    def cadastrar_evento(self, evento):
        dados_evento = self._preparar_dados(evento)
        self.sistema_externo.registrar(dados_evento)

    def _preparar_dados(self, evento):
        return {
            "titulo": evento["titulo"],
            "data": evento["data"],
            "local": evento["local"]
        }


class AdapterRepositorioInterno(CadastroEvento):
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def cadastrar_evento(self, evento):
        self.repositorio.salvar_evento(evento)


def main():
    evento = {
        "titulo": "Feira de Ciências",
        "data": "2025-06-15",
        "local": "Auditório FCTE"
    }

    sistema_externo = SistemaExternoEventos()
    adapter_externo = AdapterSistemaExterno(sistema_externo)
    adapter_externo.cadastrar_evento(evento)

    repositorio = RepositorioEventos()
    adapter_interno = AdapterRepositorioInterno(repositorio)
    adapter_interno.cadastrar_evento(evento)


if __name__ == "__main__":
    main()
