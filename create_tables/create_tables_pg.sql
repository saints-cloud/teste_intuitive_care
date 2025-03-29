-- Para criar o banco de dados em PostgreSQL, execute (fora deste script):
--   CREATE DATABASE ans_dados;
-- Em seguida, conecte-se a ans_dados (por exemplo, usando psql: \c ans_dados) e execute as instruções abaixo:

DROP TABLE IF EXISTS demonstracoes_contabeis CASCADE;
DROP TABLE IF EXISTS operadoras_ativas CASCADE;

CREATE TABLE operadoras_ativas (
    reg_ans INT NOT NULL,
    cnpj VARCHAR(14),
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf CHAR(2),
    cep VARCHAR(9),
    ddd_telefone VARCHAR(15),
    fax VARCHAR(15),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(255),
    data_registro_ans DATE,
    PRIMARY KEY (reg_ans)
);

CREATE TABLE demonstracoes_contabeis (
    id SERIAL PRIMARY KEY,
    reg_ans INT NOT NULL,
    competencia DATE NOT NULL,
    conta_contabil VARCHAR(255),
    valor DECIMAL(15,2),
    CONSTRAINT fk_operadora FOREIGN KEY (reg_ans) REFERENCES operadoras_ativas(reg_ans)
);
