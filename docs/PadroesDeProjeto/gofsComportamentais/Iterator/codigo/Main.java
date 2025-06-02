import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Arrays;
import java.util.List;

interface Iterator {
   public boolean hasNext();
   public Object next();
}

interface Container {
   public Iterator getIterator();
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

    public String getDescricao() {
        return this.descricao;
    }

    public String getLocal() {
        return this.local;
    }

    public LocalDateTime getDataHora() {
        return this.dataHora;
    }
}

class EventoRepository implements Container {
   public Evento eventos[] = {
        new Evento(
            "Tech Conference 2025",
            "Conferência anual sobre as principais tendências em tecnologia e inovação.",
            "Centro de Convenções de São Paulo",
            LocalDateTime.of(2025, 9, 15, 10, 0),
            "https://techconf2025.com/inscricao",
            300,
            Arrays.asList("Tecnologia", "Inovação", "Negócios")
        ),
        new Evento(
            "Workshop de Inteligência Artificial",
            "Aprenda na prática os fundamentos e aplicações da IA.",
            "Campus da Universidade Federal de Minas Gerais",
            LocalDateTime.of(2025, 10, 5, 14, 30),
            "https://workshopia.com/inscricao",
            50,
            Arrays.asList("IA", "Machine Learning", "Educação")
        ),
        new Evento(
            "Encontro Nacional de Startups",
            "Networking, pitches e oportunidades para startups de todo o Brasil.",
            "Expo Center Norte, São Paulo",
            LocalDateTime.of(2025, 11, 20, 9, 0),
            "https://startups2025.com/inscricao",
            500,
            Arrays.asList("Empreendedorismo", "Startups", "Investimento")
        )
    };

    @Override
    public Iterator getIterator() {
      return new NameIterator();
    }

    private class NameIterator implements Iterator {

        int index;

        @Override
        public boolean hasNext() {
        
            if(index < eventos.length){
                return true;
            }
            return false;
        }

        @Override
        public Object next() {      
            if(this.hasNext()){
                return eventos[index++];
            }
            return null;
        }		
   }
}

public class Main {
    public static void main(String[] args) {
        EventoRepository eventoRepository = new EventoRepository();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm");
        for(Iterator iter = eventoRepository.getIterator(); iter.hasNext();){
                Evento evento = (Evento)iter.next();
                System.out.println("Nome do Evento: '" + evento.getTitulo() + "'; Descrição do Evento: '" + evento.getDescricao() + "'; Local do Evento: '" + evento.getLocal() + "'; Data e Hora do Evento: " +  evento.getDataHora().format(formatter));
        } 	
    }
}