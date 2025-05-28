import java.time.LocalDateTime;
import java.util.List;
import java.util.ArrayList;

class Evento {
    private String titulo;
    private String descricao;
    private String local;
    private LocalDateTime dataHora;
    private String linkInscricao;
    private int vagas;
    private List<String> categorias;

    public Evento(String titulo, String descricao, String local, LocalDateTime dataHora,
        String linkInscricao, int vagas, List<String> categorias) {
        this.titulo = titulo;
        this.descricao = descricao;
        this.local = local;
        this.dataHora = dataHora;
        this.linkInscricao = linkInscricao;
        this.vagas = vagas;
        this.categorias = categorias;
    }

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

class Agenda {
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

public class Main {
    public static void main(String[] args) {
        Agenda agenda1 = Agenda.getInstance();
        Evento evento1 = new Evento(
            "Workshop de Java",
            "Aprenda conceitos avançados de Java",
            "FGA Sala I10",
            LocalDateTime.of(2025, 6, 1, 14, 0),
            "http://inscricao.com/java",
            50,
            List.of("Programação", "Java", "Backend")
        );
        agenda1.addEvento(evento1);
        Agenda agenda2 =  Agenda.getInstance();
        Evento evento2 = new Evento(
            "Introdução ao Spring Boot",
            "Workshop prático sobre desenvolvimento com Spring Boot",
            "FGA Sala S10",
            LocalDateTime.of(2025, 6, 2, 10, 30),
            "http://inscricao.com/springboot",
            40,
            List.of("Java", "Spring", "Desenvolvimento Web")
        );
        agenda2.addEvento(evento2);
        agenda2.listarEventos();
    }
}
