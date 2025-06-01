# Modelagem do Banco de Dados

## Introdução

O desenvolvimento de um sistema de banco de dados envolve diferentes etapas de modelagem que visam representar os dados e suas relações de maneira progressivamente mais detalhada. As três principais fases são: **modelagem conceitual, modelagem lógica e modelagem física.** Cada uma possui um papel fundamental na construção de uma base de dados eficiente, bem estruturada e aderente aos requisitos do sistema.

## Metodologia

A modelagem do sistema AgendaFCTE foi elaborada com base nos requisitos funcionais e não funcionais identificados na [Entrega 1](https://unbarqdsw2025-1-turma02.github.io/2025.1-T02-_G4_AgendaFCTE_Entrega_01/#/./Base/1.5.3.PriorizacaoMosCoW). As modelagens conceitual e lógica foram feitas pelo [BR Modelo Web](https://www.brmodeloweb.com/), um site feito para a construção desses modelos. 
A seguir, segue cada um dos três modelos (**conceitual, lógica e física**) com suas respectivas explicações.

## Modelagem Conceitual

A modelagem conceitual é a primeira etapa do processo. Nela, busca-se representar os requisitos do negócio de forma abstrata, sem se preocupar com aspectos técnicos ou específicos de um SGBD (Sistema Gerenciador de Banco de Dados).
A principal ferramenta utilizada é o modelo entidade-relacionamento (MER), que descreve:

- **Entidades**: os objetos principais do sistema;
- **Atributos**: as informações que caracterizam as entidades;
- **Relacionamentos**: as interações entre as entidades;
- **Cardinalidade**: expressa a quantidade mínima e máxima de vezes que uma entidade pode participar de um relacionamento com outra
O foco da modelagem conceitual é compreender e organizar o domínio do problema, promovendo um entendimento claro entre os envolvidos no projeto (desenvolvedores, analistas, clientes etc.).

### Elementos da Modelagem

#### Entidades

A modelagem conceitual da AgendaFCTE contempla as seguintes entidades principais:

- **Usuário**: Representa os participantes do sistema, podendo ser organizadores ou apenas inscritos em eventos. Possui atributos como nome, email, senha, data_cadastro, entre outros.
- **Evento**: Representa os eventos organizados e gerenciados na plataforma. Inclui informações como data, hora, descrição, limite de vagas, link de inscrição, entre outros.
- **Notificação**: Guarda mensagens que são enviadas aos usuários. Inclui título e mensagem, sendo associada à entidade usuário.
- **Categoria**: Classifica os eventos em diferentes grupos temáticos (como oficinas, palestras, cursos etc.).
- **Tag**: Palavras-chave associadas aos eventos, permitindo melhor indexação e busca.
- **Mídia do Evento**: Representa arquivos multimídia (imagens, vídeos) relacionados aos eventos. Contém atributos como tipo, URL do arquivo e descrição.
- **Seguir**: Entidade responsável por representar o relacionamento de usuários com eventos ou organizadores que desejam acompanhar.

#### Relacionamentos

A modelagem inclui relacionamentos importantes que permitem capturar as interações entre os usuários e os eventos, conforme descrito a seguir:

- **Organiza**: Relacionamento entre usuário (organizador) e evento, com atributo data_criacao.
- **Inscreve**: Representa a inscrição de usuários em eventos. Inclui atributos como data_inscricao, status (confirmado, pendente etc.) e codigo da inscrição.
- **Comenta**: Usuários podem comentar nos eventos, sendo registrada a mensagem e data_postagem.
- **Gera**: Relacionamento entre evento e certificado, com os atributos data_emissao e url_pdf.
- **Avalia**: Usuários podem avaliar os eventos, registrando uma nota e um comentário.
- **Favorita**: Indica os eventos marcados como favoritos pelos usuários.
- **Possui**: O evento pode estar associado a uma ou mais categorias, tags e mídias. Há múltiplas instâncias deste relacionamento na modelagem.
- **Recebe**: Representa as notificações recebidas por usuários.
- **Rel**: Generalização que permite especializar o relacionamento de “seguir” em seguir_evento e seguir_organizador.

#### Modelagem

<iframe 
    frameborder="0"
    style="width:100%;height:453px;"
    src="https://app.brmodeloweb.com/#!/publicview/683bac6c4ae4596e44f5fcc5"
    allowtransparency="true">
</iframe>

## Modelagem Lógica

A modelagem lógica do banco de dados visa representar, em um nível mais técnico, as entidades, atributos e relacionamentos definidos na etapa conceitual, de forma que possa ser posteriormente convertida em um modelo físico implementável em um SGBD relacional.

1. **Entidade usuario**:

A tabela **usuario** armazena os dados dos participantes e organizadores da plataforma. Cada usuário possui:

- **pkusuario**: chave primária (identificador único);
- **nome, email, senha**: dados de login e identificação;
- **foto_perfil**: imagem de perfil;
- **data_cadastro**: data de criação do usuário no sistema;
- **organizador**: atributo booleano que define se o usuário é organizador de eventos.

A entidade se relaciona com diversas outras entidades, como evento, inscricao_evento, avaliacao, entre outras.

2. **Entidade evento**:

Representa os eventos cadastrados na plataforma. Seus principais atributos incluem:

- **pkevento**: chave primária;
- **dataevento, horaevento, localevento, descricaoevento, contato**: detalhamento do evento;
- **link_inscricao**: URL para inscrição;
- **possui_certificado**: booleano que indica se o evento oferece certificado;
- **limite_vagas**: número máximo de participantes;
- **fkcategoria**: chave estrangeira para a entidade categoria.

A tabela **evento** possui relacionamentos com várias tabelas associativas que representam interações de usuários com eventos.

3. **Entidade categoria:**

Contém as categorias que classificam os eventos:

- **pkcategoria**: chave primária;
- **categoria**: descrição textual da categoria.

Cada **evento** pertence a uma única categoria.

4. **Entidade midia_evento:**

Armazena arquivos de mídia (imagens, vídeos) relacionados aos eventos:

- **pkmidia**: chave primária;
- **fkevento**: chave estrangeira para evento;
- **tipo, url_arquivo, descricao**: informações sobre a mídia.

5. **Entidade tag e rel_evento_tag:**

A entidade tag representa palavras-chave associáveis aos eventos. Como a relação entre eventos e tags é do tipo muitos-para-muitos, utiliza-se a tabela intermediária rel_evento_tag, que contém:

- **fkevento** e **fktag**: chaves estrangeiras que formam uma chave composta.

6. **Entidade rel_seguir_evento:**

Tabela associativa que registra os usuários que seguem eventos específicos:

- **fkusuario** e **fkevento**: chaves estrangeiras (compõem a chave primária).

7. **Entidade rel_seguir_organizador:**

Registra os usuários que seguem organizadores:

- **pksesguir_organizador**: chave primária;
- **fkusuario** e **fkorganizador**: chaves estrangeiras.

8. **Entidade rel_organizador_evento:**

Relaciona organizadores com os eventos criados por eles:

- **fkorganizador**, **fkevento**: chaves estrangeiras (compõem a chave primária);
- **data_criacao**: data de criação do evento.

9. **Entidade rel_inscricao_evento:**

Controla as inscrições dos usuários nos eventos:

- **fkusuario**, **fkevento**: chaves estrangeiras (compõem a chave primária);
- **data_inscricao**, **status**, **codigo_inscricao**: dados da inscrição.

10. **Entidade rel_avaliacao:**

Registra avaliações de usuários sobre eventos:

- **fkusuario**, **fkevento**: chaves estrangeiras (compõem a chave primária);
- **avaliacao**: nota;
- **comentario**: observação textual.

11. **Entidade rel_favoritado:**

Controla quais eventos foram favoritados pelos usuários:

- **fkusuario**, **fkevento**: chaves estrangeiras (compõem a chave primária);
- **favoritado**: valor booleano.

12. **Entidade rel_forum_evento:**

Armazena mensagens de fórum (comentários) associadas a eventos:

- **fkevento**, **fkusuario**: chaves estrangeiras (compõem a chave primária);
- **mensagem**, **data_postagem**: conteúdo e data da mensagem.

13. **Entidade rel_certificado:**

Relaciona o usuário a certificados emitidos por participação:

- **fkevento**, **fkusuario**: chaves estrangeiras (compõem a chave primária);
- **data_emissao**, **url_pdf**: informações do certificado.

14. **Entidades notificacao e rel_notificacao_usuario:**

- **notificacao**: define o conteúdo da notificação, com pknotificacao, titulo e mensagem.
- **notificacao_usuario**: associa a notificação a um usuário, contendo:
- **fkusuario**, **fknotificacao**: chaves estrangeiras;
- **data_envio**, **lida**: data e status da leitura.

#### Modelagem

<iframe
    frameborder="0"
    style="width:100%;height:453px;"
    src="https://app.brmodeloweb.com/#!/publicview/683baed44ae4596e44f5fd07"
    allowtransparency="true">
</iframe>

## Modelagem Física

A modelagem física é a etapa final do processo de modelagem de dados, responsável por traduzir o modelo lógico para uma estrutura concreta que será implementada no Sistema Gerenciador de Banco de Dados (SGBD) escolhido. Nessa fase, são definidos os nomes das tabelas e colunas, os tipos de dados específicos, os índices, chaves primárias e estrangeiras, além de outras restrições de integridade que garantem o correto funcionamento e desempenho do banco de dados.

Cada entidade lógica do modelo anterior foi convertida em uma tabela física com os respectivos atributos e relacionamentos. As tabelas foram criadas com nomes simples e descritivos, respeitando a convenção de nomes claros e sem ambiguidade.

Componentes:

- **Chaves Primárias (PK)** foram atribuídas a todos os registros como identificadores únicos, geralmente com nomes como pkusuario, pkevento, pkcategoria, etc.
- **Chaves Estrangeiras (FK)** foram utilizadas para representar relacionamentos entre entidades, garantindo a integridade referencial entre os dados. Por exemplo, fkusuario e fkevento são largamente utilizadas nas tabelas relacionais para vincular registros de usuario e evento.
- Os tipos de dados foram atribuídos de acordo com a natureza de cada atributo:
  - Campos como nome, email, titulo, mensagem usam VARCHAR com limites definidos.
  - Datas como data_evento, data_cadastro, data_postagem utilizam o tipo DATE.
  - Atributos booleanos como organizador, favoritado, possui_certificado, lida usam o tipo BOOLEAN.
  - Identificadores primários geralmente utilizam INT com AUTO_INCREMENT para facilitar a geração automática de chaves únicas.

#### Código SQL

É possível também verificar o código seguindo essa estrutura dentro do repositório no caminho `docs/PadroesDeProjeto/iniciativasExtras/modelagem_banco/banco.sql`.

```SQL
create table usuario (
    pkusuario serial primary key,
    nome varchar(100) not null,
    email varchar(100) not null,
    senha varchar(100) not null,
    foto_perfil varchar(255),
    data_cadastro date not null,
    organizador boolean default false,
    unique (nome)
);

create table categoria (
    pkcategoria serial primary key,
    categoria varchar(100) not null,
    unique (categoria)
);

create table evento (
    pkevento serial primary key,
    dataevento date not null,
    horaevento time not null,
    localevento varchar(150) not null,
    descricaoevento varchar(500) not null,
    contato varchar(100),
    link_inscricao varchar(200),
    possui_certificado boolean not null,
    fkcategoria int not null,
    limite_vagas int,
    foreign key (fkcategoria) references categoria(pkcategoria)
);

create table tag (
    pktag serial primary key,
    tag varchar(100) not null,
    unique (tag)
);

create table rel_evento_tag (
    fkevento int,
    fktag int,
    primary key (fkevento, fktag),
    foreign key (fkevento) references evento(pkevento),
    foreign key (fktag) references tag(pktag)
);

create table avaliacao (
    fkevento int,
    fkusuario int,
    avaliacao int not null,
    comentario varchar(300),
    primary key (fkevento, fkusuario),
    foreign key (fkevento) references evento(pkevento),
    foreign key (fkusuario) references usuario(pkusuario)
);

create table favoritado (
    fkusuario int,
    fkevento int,
    favoritado boolean,
    primary key (fkusuario, fkevento),
    foreign key (fkusuario) references usuario(pkusuario),
    foreign key (fkevento) references evento(pkevento)
);

create table organizador_evento (
    fkorganizador int,
    fkevento int,
    data_criacao date not null,
    primary key (fkorganizador, fkevento),
    foreign key (fkorganizador) references usuario(pkusuario),
    foreign key (fkevento) references evento(pkevento)
);

create table notificacao (
    pknotificacao serial primary key,
    titulo varchar(100) not null,
    mensagem varchar(500) not null
);

create table notificacao_usuario (
    fkusuario int,
    fknotificacao int,
    data_envio date not null,
    lida boolean default false,
    primary key (fkusuario, fknotificacao),
    foreign key (fkusuario) references usuario(pkusuario),
    foreign key (fknotificacao) references notificacao(pknotificacao)
);

create table inscricao_evento (
    fkusuario int,
    fkevento int,
    data_inscricao date not null,
    status varchar(1), -- C - confirmado, E - em andamento, A - anulado
    codigo_inscricao int not null unique,
    primary key (fkusuario, fkevento),
    foreign key (fkusuario) references usuario(pkusuario),
    foreign key (fkevento) references evento(pkevento)
);

create table certificado (
    fkevento int,
    fkusuario int,
    data_emissao date not null,
    url_pdf varchar(255) not null,
    primary key (fkevento, fkusuario),
    foreign key (fkevento) references evento(pkevento),
    foreign key (fkusuario) references usuario(pkusuario)
);

create table forum_evento (
    fkevento int,
    fkusuario int,
    mensagem varchar(500) not null,
    data_postagem date not null,
    primary key (fkevento, fkusuario),
    foreign key (fkevento) references evento(pkevento),
    foreign key (fkusuario) references usuario(pkusuario)
);

create table midia_evento (
    pkmidia serial primary key,
    fkevento int not null,
    tipo varchar(1) not null, -- I - imagem / V - vídeo
    url_arquivo varchar(255) not null,
    descricao varchar(255),
    foreign key (fkevento) references evento(pkevento)
);

create table rel_seguir_evento (
    fkusuario int,
    fkevento int,
    primary key (fkusuario, fkevento),
    foreign key (fkusuario) references usuario(pkusuario),
    foreign key (fkevento) references evento(pkevento)
);

create table seguir_organizador (
    pkseguir_organizador serial primary key,
    fkusuario int not null,
    fkorganizador int not null,
    foreign key (fkusuario) references usuario(pkusuario),
    foreign key (fkorganizador) references usuario(pkusuario)
);

create trigger trigger_inscricao_evento_status
before insert or update on inscricao_evento
for each row
execute function inscricao_evento_tratamento();

create or replace function inscricao_evento_tratamento() returns trigger as
$$
begin
-- status
  if length(coalesce(new.status, '')) > 0 then
    if new.status not in ('C', 'E', 'A') then
      raise exception 'Status inválido: % (use apenas C, E ou A)', new.status;
    end if;
  end if;
  return new;
end;
$$ language 'plpgsql' stable;

create trigger trigger_midia_evento_tipo
before insert or update on midia_evento
for each row
execute function midia_evento_tratamento();

create or replace function midia_evento_tratamento() returns trigger as
$$
begin
-- tipo
  if length(coalesce(new.tipo, '')) > 0 then
    if new.tipo not in ('I', 'V') then
      raise exception 'Tipo inválido: % (use apenas I ou V)', new.tipo;
    end if;
  end if;
  return new;
end;
$$ language 'plpgsql' stable;
```

## Bibliografia

> <a id='ref1' style="text-decoration: none; color: inherit;"> UNIVERSIDADE DE BRASÍLIA. Modelo Conceitual – Parte 1. Disponível em: https://aprender3.unb.br/pluginfile.php/3114408/mod_resource/content/2/aula_modelo_conceitual_parte1.pdf. Acesso em: 31 maio 2025.</a>
>
> <a id='ref2' style="text-decoration: none; color: inherit;"> UNIVERSIDADE DE BRASÍLIA. Cardinalidade. Disponível em: https://aprender3.unb.br/pluginfile.php/3114413/mod_resource/content/2/cardinalidade.pdf. Acesso em: 31 maio 2025.</a>
>
> <a id='ref3' style="text-decoration: none; color: inherit;"> UNIVERSIDADE DE BRASÍLIA. Mapeamento para Tabelas Relacionais. Disponível em: https://aprender3.unb.br/pluginfile.php/3114422/mod_resource/content/5/mapeamento_tabela.pdf. Acesso em: 31 maio 2025.</a>
>
> <a id='ref4' style="text-decoration: none; color: inherit;"> UNIVERSIDADE DE BRASÍLIA. Linguagem SQL – Parte 1. Disponível em: https://aprender3.unb.br/pluginfile.php/3114427/mod_resource/content/2/Linguagem%20SQL%20-%20parte%201.pdf. Acesso em: 31 maio 2025.</a>

## Histórico de Versão

| Versão | Data | Descrição | Autor | Revisor | Comentário do Revisor |
| -- | -- | -- | -- | -- | -- |
| `1.0`  | 31/05/2025 | Adição do código sql | [Manoela Garcia](https://github.com/manu-sgc) | [Thales Euflauzino](https://github.com/thaleseuflauzino) | Parabéns pelo trabalho! |
| `1.1`  | 31/05/2025 | Adição dos textos explicando as modelagens | [Manoela Garcia](https://github.com/manu-sgc) | [Thales Euflauzino](https://github.com/thaleseuflauzino) | Parabéns pelo trabalho! |
| `1.2`  | 01/06/2025 | Adição dos textos introdutórios | [Victor Bernardes](https://github.com/VHbernardes) | [Thales Euflauzino](https://github.com/thaleseuflauzino) | Parabéns pelo trabalho! |
| `1.3`  | 01/06/2025 | Adição das modelagens visuais e código SQL | [Victor Bernardes](https://github.com/VHbernardes) | [Thales Euflauzino](https://github.com/thaleseuflauzino) | Parabéns pelo trabalho! |
