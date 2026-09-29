SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS L_Tech DEFAULT CHARACTER SET utf8 ;
SHOW WARNINGS;
USE l_tech ;
SELECT * FROM produto;
CREATE TABLE pedido_saida (
    idsaida INT AUTO_INCREMENT PRIMARY KEY,
    produto VARCHAR(100),
    quantidade INT,
    data_saida DATE
);
USE l_tech;
SHOW TABLES;
CREATE TABLE fornecedor (
    idfornecedor INT AUTO_INCREMENT PRIMARY KEY,
    nome_fornecedor VARCHAR(150) NOT NULL,
    cnpj VARCHAR(20),
    telefone VARCHAR(20),
    email VARCHAR(120),
    produto_fornecido VARCHAR(120),
    endereco VARCHAR(200)
);

CREATE TABLE agenda (
    idagenda INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100),
    descricao TEXT,
    data_evento DATE
);

ALTER TABLE fornecedor ADD COLUMN produto_fornecido VARCHAR(100);

-- -----------------------------------------------------
-- Table cliente
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS cliente (
  idcliente INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(45) NOT NULL,
  cpf VARCHAR(11) NULL,
  email VARCHAR(50) NULL,
  telefone VARCHAR(11) NULL,
  PRIMARY KEY (idcliente)
)
ENGINE = InnoDB;

SHOW WARNINGS;
SELECT * FROM pedido_saida ORDER BY idsaida DESC;
ALTER TABLE pedido_saida DROP COLUMN id_localizacao;
DESCRIBE pedido_saida;

select * from pedido_saida;
DESC produto;
select * from pedido_entrada;
SELECT * FROM pedido_entrada ORDER BY identrada DESC;
SELECT * FROM pedido_saida ORDER BY idsaida DESC;
ALTER TABLE pedido_entrada ADD COLUMN produto_id INT;
DESCRIBE pedido_entrada;
DESCRIBE pedido_saida;
ALTER TABLE pedido_entrada DROP COLUMN produto;
ALTER TABLE pedido_saida DROP COLUMN produto;
DESCRIBE pedido_saida;
SELECT * FROM pedido_saida;
DESCRIBE produto;
SELECT * FROM produto;
ALTER TABLE produtos ADD estoque INT DEFAULT 0;
SHOW TABLES;

USE l_tech;
DESCRIBE pedido_saida;
CREATE TABLE pedido_entrada (
    identrada INT AUTO_INCREMENT PRIMARY KEY,
    produto VARCHAR(100),
    quantidade INT,
    data_entrada DATE
);
-- -----------------------------------------------------
-- Table produto
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS produto (
  idproduto INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(45) NULL,
  preco DECIMAL(10,2) NULL,
  estoqueatual VARCHAR(45) NULL,
  quantidade VARCHAR(45) NULL,
  limite_maximo INT NOT NULL DEFAULT 100,
  datasaida DATE NULL,
  PRIMARY KEY (idproduto)
)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table fornecedor
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS fornecedor (
  idfornecedor INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(45) NOT NULL,
  cnpj VARCHAR(14) NULL,
  telefone VARCHAR(45) NULL,
  PRIMARY KEY (idfornecedor)
)
ENGINE = InnoDB;

SHOW WARNINGS;

select * from fornecedor;

-- -----------------------------------------------------
-- Table pedidofornecedor
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS pedidofornecedor (
  idpedidofornecedor INT NOT NULL AUTO_INCREMENT,
  datapedido DATE NULL,
  fonecedor_idfonecedor INT NOT NULL,
  PRIMARY KEY (idpedidofornecedor),
  CONSTRAINT fk_pedidofornecedor_fonecedor
    FOREIGN KEY (fonecedor_idfonecedor)
    REFERENCES fonecedor (idfonecedor)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table localizcaopedidointerna
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS localizcaopedidointerna (
  idlocalizcaopedido INT NOT NULL AUTO_INCREMENT,
  setor VARCHAR(45) NULL,
  prateleira VARCHAR(45) NULL,
  corredor VARCHAR(45) NULL,
  produto_idproduto INT NOT NULL,
  PRIMARY KEY (idlocalizcaopedido),
  CONSTRAINT fk_localizcaopedido_produto1
    FOREIGN KEY (produto_idproduto)
    REFERENCES produto (idproduto)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table entrada
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS entrada (
  identrada INT NOT NULL AUTO_INCREMENT,
  quantidade VARCHAR(45) NULL,
  dataentrada DATE NULL,
  pedidofornecedor_idpedidofornecedor INT NOT NULL,
  produto_idproduto INT NOT NULL,
  PRIMARY KEY (identrada),
  CONSTRAINT fk_entrada_pedidofornecedor1
    FOREIGN KEY (pedidofornecedor_idpedidofornecedor)
    REFERENCES pedidofornecedor (idpedidofornecedor)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_entrada_produto1
    FOREIGN KEY (produto_idproduto)
    REFERENCES produto (idproduto)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table localizacaopedido
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS localizacaopedido (
  idlocalizacaopedido INT NOT NULL,
  cep VARCHAR(45) NULL,
  rua VARCHAR(45) NULL,
  bairro VARCHAR(45) NULL,
  produto_idproduto INT NOT NULL,
  PRIMARY KEY (idlocalizacaopedido),
  CONSTRAINT fk_localizacaopedido_produto1
    FOREIGN KEY (produto_idproduto)
    REFERENCES produto (idproduto)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table saida
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS saida (
  idsaida INT NOT NULL AUTO_INCREMENT,
  quantidade VARCHAR(45) NULL,
  datasaida DATE NULL,
  produto_idproduto INT NOT NULL,
  localizacaopedido_idlocalizacaopedido INT NOT NULL,
  PRIMARY KEY (idsaida),
  CONSTRAINT fk_saida_produto1
    FOREIGN KEY (produto_idproduto)
    REFERENCES produto (idproduto)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_saida_localizacaopedido1
    FOREIGN KEY (localizacaopedido_idlocalizacaopedido)
    REFERENCES localizacaopedido (idlocalizacaopedido)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table pedidocliente
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS pedidocliente (
  idpedidocliente INT NOT NULL AUTO_INCREMENT,
  datapedido DATE NULL,
  cliente_idcliente INT NOT NULL,
  saida_idsaida INT NOT NULL,
  PRIMARY KEY (idpedidocliente),
  CONSTRAINT fk_pedidocliente_cliente1
    FOREIGN KEY (cliente_idcliente)
    REFERENCES cliente (idcliente)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_pedidocliente_saida1
    FOREIGN KEY (saida_idsaida)
    REFERENCES saida (idsaida)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table pagamento
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS pagamento (
  idpagamento INT NOT NULL AUTO_INCREMENT,
  valor DECIMAL(10,2) NULL,
  formadepagamento VARCHAR(45) NOT NULL,
  pedidocliente_idpedidocliente INT NOT NULL,
  PRIMARY KEY (idpagamento, formadepagamento),
  CONSTRAINT fk_pagamento_pedidocliente1
    FOREIGN KEY (pedidocliente_idpedidocliente)
    REFERENCES pedidocliente (idpedidocliente)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table entrega
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS entrega (
  identrega INT NOT NULL AUTO_INCREMENT,
  entregacol VARCHAR(45) NULL,
  pagamento_idpagamento INT NOT NULL,
  pagamento_formadepagamento VARCHAR(45) NOT NULL,
  PRIMARY KEY (identrega),
  CONSTRAINT fk_entrega_pagamento1
    FOREIGN KEY (pagamento_idpagamento, pagamento_formadepagamento)
    REFERENCES pagamento (idpagamento, formadepagamento)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
)
ENGINE = InnoDB;
CREATE DATABASE IF NOT EXISTS l_tech;
RENAME TABLE entrada TO pedido_entrada;
USE l_tech;

SHOW TABLES;
SELECT * FROM produto;
SELECT * FROM fornecedor;
SELECT * FROM cliente;
ALTER TABLE cliente CHANGE id idcliente INT AUTO_INCREMENT;
DESCRIBE cliente;
ALTER TABLE pedido_saida
MODIFY localizacaopedido_idlocalizacaopedido INT NULL;
SELECT idproduto FROM produto;
USE l_tech;
SHOW TABLES;
CREATE DATABASE l_tech;
SHOW WARNINGS;



USE l_tech;
SHOW TABLES;
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL
);
DESCRIBE usuarios;

CREATE TABLE produto (
    idproduto INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    preco DECIMAL(10,2),
    estoqueatual INT,
    datasaida DATE,
    limite_maximo INT NOT NULL DEFAULT 100
);
DESCRIBE produto;

INSERT INTO produto (nome, preco, estoqueatual, datasaida)
VALUES ('Teste', 10.00, 5, '2026-01-01');

USE l_tech;

CREATE TABLE pedido_entrada (
    identrada INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT,
    quantidade INT,
    data_entrada DATETIME,

    FOREIGN KEY (produto_id)
    REFERENCES produto(idproduto)
);
USE l_tech;

SHOW COLUMNS FROM pedido_saida;
USE l_tech;

CREATE TABLE agenda (
    idagenda INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descricao VARCHAR(255),
    data_evento DATETIME NOT NULL
);

USE l_tech;

DESCRIBE fornecedor;

USE l_tech;

DESC pedido_entrada;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;



-- RF.1 - Definição de limite máximo de estoque
-- Execute este comando uma única vez em um banco l_tech já existente.
ALTER TABLE produto ADD COLUMN limite_maximo INT NOT NULL DEFAULT 100;
