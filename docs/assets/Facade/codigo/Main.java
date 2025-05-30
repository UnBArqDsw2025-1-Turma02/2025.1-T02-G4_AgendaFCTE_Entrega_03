import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

class Usuario {
    private int id;
    private String nome;
    private String email;
    private String senha;
    private List<Notificacao> notificacoes = new ArrayList<>();

    public void adicionarNotificacao(Notificacao notificacao) {
        notificacoes.add(notificacao);
    }

    public String getNome() { return nome; }

    public void setNome(String nome){
        this.nome = nome;
    }
}

class Participante extends Usuario {
    private List<Evento> eventosInscritos = new ArrayList<>();

    public void inscrever(Evento evento) {
        eventosInscritos.add(evento);
    }

    public void setNome(String nome){
        super.setNome(nome);
    }
}

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

    public String getTitulo(){
        return this.titulo;
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

class Notificacao {
    private String mensagem;
    private LocalDateTime dataHora;

    public Notificacao(String mensagem, LocalDateTime dataHora) {
        this.mensagem = mensagem;
        this.dataHora = dataHora;
    }

    public String getMensagem() {
        return mensagem;
    }
}

class EventoFacade {
    public void inscreverUsuarioNoEvento(Usuario usuario, Evento evento) {
        if (!(usuario instanceof Participante)) {
            throw new IllegalArgumentException("Usuário não é um participante.");
        }

        Participante participante = (Participante) usuario;

        participante.inscrever(evento);

        Notificacao notificacao = new Notificacao( "Inscrição realizada com sucesso no evento: " + evento.getTitulo(),  LocalDateTime.now());

        usuario.adicionarNotificacao(notificacao);

        System.out.println("Usuário " + usuario.getNome() + " inscrito no evento " + evento.getTitulo());
        System.out.println("Notificação criada: " + notificacao.getMensagem());
    }
}

public class Main {
    public static void main(String[] args) {
        Participante usuario = new Participante();
        usuario.setNome("Maria");

        Evento evento = new Evento("Workshop de Java", "Workshop de Java para Iniciantes", "FGA Sala I10", LocalDateTime.parse("2025-06-30T15:30:00"), "link.com.br/workshop-java", 50, new ArrayList<>());

        EventoFacade facade = new EventoFacade();
        facade.inscreverUsuarioNoEvento(usuario, evento);
    }
}