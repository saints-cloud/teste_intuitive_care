-- Importa dados das operadoras ativas
COPY operadoras_ativas(reg_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, complemento, bairro, cidade, uf, cep, ddd_telefone, fax, endereco_eletronico, representante, cargo_representante, data_registro_ans)
FROM 'C://Users//pinhe//OneDrive/Documentos//intuitive_care//create_tables/dados//Relatorio_cadop.csv'
WITH (
    FORMAT csv,
    DELIMITER ';',
    HEADER true,
    QUOTE '"',
    ENCODING 'UTF8'
);


-- Importa dados do arquivo 1T2023.csv
COPY demonstracoes_contabeis(reg_ans, competencia, conta_contabil, valor)
FROM 'C://Users//pinhe//OneDrive/Documentos//intuitive_care//create_tables/dados/1T2023.csv'
WITH (
    FORMAT csv,
    DELIMITER ';',
    HEADER true,
    QUOTE '"',
    ENCODING 'UTF8'
);


-- Importa dados do arquivo 1T2024.csv
COPY demonstracoes_contabeis(reg_ans, competencia, conta_contabil, valor)
FROM 'C://Users//pinhe//OneDrive/Documentos//intuitive_care//create_tables/dados/1T2024.csv'
WITH (
    FORMAT csv,
    DELIMITER ';',
    HEADER true,
    QUOTE '"',
    ENCODING 'UTF8'
);


-- Importa dados do arquivo 2t2023.csv
COPY demonstracoes_contabeis(reg_ans, competencia, conta_contabil, valor)
FROM 'C://Users//pinhe//OneDrive/Documentos//intuitive_care//create_tables/dados/2t2023.csv'
WITH (
    FORMAT csv,
    DELIMITER ';',
    HEADER true,
    QUOTE '"',
    ENCODING 'UTF8'
);


-- Importa dados do arquivo 2T2024.csv
COPY demonstracoes_contabeis(reg_ans, competencia, conta_contabil, valor)
FROM 'C://Users//pinhe//OneDrive/Documentos//intuitive_care//create_tables/dados/2T2024.csv'
WITH (
    FORMAT csv,
    DELIMITER ';',
    HEADER true,
    QUOTE '"',
    ENCODING 'UTF8'
);


-- Importa dados do arquivo 3T2023.csv
COPY demonstracoes_contabeis(reg_ans, competencia, conta_contabil, valor)
FROM 'C://Users//pinhe//OneDrive/Documentos//intuitive_care//create_tables/dados/3T2023.csv'
WITH (
    FORMAT csv,
    DELIMITER ';',
    HEADER true,
    QUOTE '"',
    ENCODING 'UTF8'
);


-- Importa dados do arquivo 3T2024.csv
COPY demonstracoes_contabeis(reg_ans, competencia, conta_contabil, valor)
FROM 'C://Users//pinhe//OneDrive/Documentos//intuitive_care//create_tables/dados/3T2024.csv'
WITH (
    FORMAT csv,
    DELIMITER ';',
    HEADER true,
    QUOTE '"',
    ENCODING 'UTF8'
);


-- Importa dados do arquivo 4T2023.csv
COPY demonstracoes_contabeis(reg_ans, competencia, conta_contabil, valor)
FROM 'C://Users//pinhe//OneDrive/Documentos//intuitive_care//create_tables/dados/4T2023.csv'
WITH (
    FORMAT csv,
    DELIMITER ';',
    HEADER true,
    QUOTE '"',
    ENCODING 'UTF8'
);


-- Importa dados do arquivo 4T2024.csv
COPY demonstracoes_contabeis(reg_ans, competencia, conta_contabil, valor)
FROM 'C://Users//pinhe//OneDrive/Documentos//intuitive_care//create_tables/dados/4T2024.csv'
WITH (
    FORMAT csv,
    DELIMITER ';',
    HEADER true,
    QUOTE '"',
    ENCODING 'UTF8'
);


