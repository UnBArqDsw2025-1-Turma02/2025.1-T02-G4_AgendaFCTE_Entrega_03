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