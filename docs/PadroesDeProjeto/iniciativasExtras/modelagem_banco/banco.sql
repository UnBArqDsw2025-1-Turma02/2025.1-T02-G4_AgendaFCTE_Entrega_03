CREATE TABLE usuario 
( 
 pkusuario INT PRIMARY KEY,  
 nome CHAR(n) NOT NULL,  
 email CHAR(n) NOT NULL,  
 senha CHAR(n) NOT NULL,  
 foto_perfil CHAR(n),  
 data_cadastro DATE NOT NULL,  
 organizador: BOOL CHAR(n) DEFAULT 'false',  
 UNIQUE (nome,email)
); 

CREATE TABLE evento 
( 
 pkevento INT PRIMARY KEY AUTO_INCREMENT,  
 dataevento DATE NOT NULL,  
 horaevento DATE NOT NULL,  
 localevento CHAR(n) NOT NULL,  
 descricaoevento CHAR(n) NOT NULL,  
 contato CHAR(n),  
 link_inscricao CHAR(n) NOT NULL,  
 possui_certificado: BOOL VARCHAR(n) NOT NULL DEFAULT 'False',  
 fkcategoria INT NOT NULL,  
 limite_vagas INT,  
); 

CREATE TABLE categoria 
( 
 pkcategoria INT PRIMARY KEY AUTO_INCREMENT,  
 categoria CHAR(n) NOT NULL,  
 UNIQUE (categoria)
); 

CREATE TABLE tag 
( 
 pktag INT PRIMARY KEY AUTO_INCREMENT,  
 tag CHAR(n) NOT NULL,  
 UNIQUE (tag)
); 

CREATE TABLE rel_evento_tag 
( 
 fkevento INT PRIMARY KEY,  
 fktag INT PRIMARY KEY,  
); 

CREATE TABLE avaliacao 
( 
 avaliacao CHAR(n) NOT NULL,  
 fkevento INT PRIMARY KEY,  
 fkusuario INT PRIMARY KEY NOT NULL,  
 comentario CHAR(n),  
); 

CREATE TABLE favoritado 
( 
 fkusuario INT PRIMARY KEY NOT NULL,  
 fkevento INT PRIMARY KEY NOT NULL,  
 favoritado: BOOL INT DEFAULT 'true',  
); 

CREATE TABLE organizador_evento 
( 
 fkorganizador INT PRIMARY KEY NOT NULL,  
 fkevento INT PRIMARY KEY NOT NULL,  
 data_criacao DATE NOT NULL,  
); 

CREATE TABLE notificacao_usuario 
( 
 fkusuario INT NOT NULL,  
 fknotificacao INT NOT NULL,  
 data_envio DATE NOT NULL,  
 lida: BOOL INT DEFAULT 'false',  
); 

CREATE TABLE notificacao 
( 
 pknotificacao INT PRIMARY KEY AUTO_INCREMENT,  
 titulo CHAR(n) NOT NULL,  
 mensagem CHAR(n) NOT NULL,  
); 

CREATE TABLE sugestao_evento 
( 
 fkusuario INT PRIMARY KEY,  
 fkevento INT PRIMARY KEY,  
); 

CREATE TABLE inscricao_evento 
( 
 fkusuario INT PRIMARY KEY NOT NULL,  
 fkevento INT PRIMARY KEY NOT NULL,  
 data_inscricao DATE NOT NULL,  
 status VARCHAR(n) DEFAULT 'C',  
 codigo_inscricao INT NOT NULL,  
 UNIQUE (codigo_inscricao)
); 

CREATE TABLE certificado 
( 
 fkevento INT PRIMARY KEY NOT NULL,  
 fkusuario INT PRIMARY KEY NOT NULL,  
 data_emissao DATE NOT NULL,  
 url_pdf CHAR(n) NOT NULL,  
); 

CREATE TABLE forum_evento 
( 
 fkevento INT PRIMARY KEY NOT NULL,  
 fkusuario INT PRIMARY KEY NOT NULL,  
 mensagem CHAR(n) NOT NULL,  
 data_postagem DATE NOT NULL,  
); 

CREATE TABLE midia_evento 
( 
 pkmidia INT PRIMARY KEY AUTO_INCREMENT,  
 fkevento INT NOT NULL,  
 tipo VARCHAR(n) NOT NULL,  
 url_arquivo CHAR(n) NOT NULL,  
 descricao CHAR(n),  
); 

CREATE TABLE rel_seguir_evento 
( 
 fkusuario INT PRIMARY KEY NOT NULL,  
 fkevento INT PRIMARY KEY NOT NULL,  
); 

CREATE TABLE seguir_organizador 
( 
 pkseguir_organizador INT PRIMARY KEY AUTO_INCREMENT,  
 fkusuario INT NOT NULL,  
 fkorganizador INT NOT NULL,  
); 

ALTER TABLE evento ADD FOREIGN KEY(pkevento) REFERENCES undefined (pkevento)
ALTER TABLE evento ADD FOREIGN KEY(fkcategoria) REFERENCES categoria (fkcategoria)
ALTER TABLE rel_evento_tag ADD FOREIGN KEY(fkevento) REFERENCES evento (fkevento)
ALTER TABLE rel_evento_tag ADD FOREIGN KEY(fktag) REFERENCES tag (fktag)
ALTER TABLE avaliacao ADD FOREIGN KEY(fkevento) REFERENCES evento (fkevento)
ALTER TABLE avaliacao ADD FOREIGN KEY(fkusuario) REFERENCES usuario (fkusuario)
ALTER TABLE favoritado ADD FOREIGN KEY(fkusuario) REFERENCES usuario (fkusuario)
ALTER TABLE favoritado ADD FOREIGN KEY(fkevento) REFERENCES evento (fkevento)
ALTER TABLE organizador_evento ADD FOREIGN KEY(fkorganizador) REFERENCES usuario (fkorganizador)
ALTER TABLE organizador_evento ADD FOREIGN KEY(fkevento) REFERENCES evento (fkevento)
ALTER TABLE notificacao_usuario ADD FOREIGN KEY(fkusuario) REFERENCES usuario (fkusuario)
ALTER TABLE notificacao_usuario ADD FOREIGN KEY(fknotificacao) REFERENCES notificacao (fknotificacao)
ALTER TABLE sugestao_evento ADD FOREIGN KEY(fkusuario) REFERENCES usuario (fkusuario)
ALTER TABLE sugestao_evento ADD FOREIGN KEY(fkevento) REFERENCES evento (fkevento)
ALTER TABLE inscricao_evento ADD FOREIGN KEY(fkusuario) REFERENCES usuario (fkusuario)
ALTER TABLE inscricao_evento ADD FOREIGN KEY(fkevento) REFERENCES evento (fkevento)
ALTER TABLE certificado ADD FOREIGN KEY(fkevento) REFERENCES evento (fkevento)
ALTER TABLE certificado ADD FOREIGN KEY(fkusuario) REFERENCES usuario (fkusuario)
ALTER TABLE forum_evento ADD FOREIGN KEY(fkevento) REFERENCES evento (fkevento)
ALTER TABLE forum_evento ADD FOREIGN KEY(fkusuario) REFERENCES usuario (fkusuario)
ALTER TABLE midia_evento ADD FOREIGN KEY(fkevento) REFERENCES evento (fkevento)
ALTER TABLE rel_seguir_evento ADD FOREIGN KEY(fkusuario) REFERENCES usuario (fkusuario)
ALTER TABLE rel_seguir_evento ADD FOREIGN KEY(fkevento) REFERENCES evento (fkevento)
ALTER TABLE seguir_organizador ADD FOREIGN KEY(fkusuario) REFERENCES usuario (fkusuario)
ALTER TABLE seguir_organizador ADD FOREIGN KEY(fkorganizador) REFERENCES usuario (fkorganizador)