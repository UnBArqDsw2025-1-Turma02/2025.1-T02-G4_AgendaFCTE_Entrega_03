import java.time.LocalDateTime;
import java.util.List;

public class Evento {
    private String titulo;
    private String descricao;
    private String local;
    private LocalDateTime dataHora;
    private String linkInscricao;
    private int vagas;
    private List<String> categorias;

    public void setTitulo(String titulo) {
        this.titulo = titulo;
    }

    public void setDescricao(String descricao) {
        this.descricao = descricao;
    }

    public void setLocal(String local) {
        this.local = local;
    }

    public void setDataHora(LocalDateTime dataHora) {
        this.dataHora = dataHora;
    }

    public void setLinkInscricao(String linkInscricao) {
        this.linkInscricao = linkInscricao;
    }

    public void setVagas(int vagas) {
        this.vagas = vagas;
    }

    public void setCategorias(List<String> categorias) {
        this.categorias = categorias;
    }

    @Override
    public String toString() {
        return "Evento: " + titulo + "\n" +
               "Descrição: " + descricao + "\n" +
               "Local: " + local + "\n" +
               "Data e Hora: " + dataHora + "\n" +
               "Link de Inscrição: " + linkInscricao + "\n" +
               "Vagas: " + vagas + "\n" +
               "Categorias: " + categorias + "\n";
    }
}

public class Agenda {
    private static Agenda instancia;

    private List<Evento> eventos;

    private Agenda() {
        this.eventos = new ArrayList<>();
    }

    public static Agenda getInstance() {
        if (instancia == null) {
            instancia = new Agenda();
        }
        return instancia;
    }

    public void addEvento(Evento evento) {
        eventos.add(evento);
    }

    public void listarEventos() {
        if (eventos.isEmpty()) {
            System.out.println("Nenhum evento na agenda.");
        } else {
            for (Evento evento : eventos) {
                System.out.println(evento);
            }
        }
    }
}