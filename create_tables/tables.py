import os

# Caminhos absolutos dos arquivos conforme informado:
demo_files = [
    r"C:\\Users\\pinhe\\OneDrive\Documentos\\intuitive_care\\create_tables\dados\1T2023.csv",
    r"C:\\Users\\pinhe\\OneDrive\Documentos\\intuitive_care\\create_tables\dados\1T2024.csv",
    r"C:\\Users\\pinhe\\OneDrive\Documentos\\intuitive_care\\create_tables\dados\2t2023.csv",
    r"C:\\Users\\pinhe\\OneDrive\Documentos\\intuitive_care\\create_tables\dados\2T2024.csv",
    r"C:\\Users\\pinhe\\OneDrive\Documentos\\intuitive_care\\create_tables\dados\3T2023.csv",
    r"C:\\Users\\pinhe\\OneDrive\Documentos\\intuitive_care\\create_tables\dados\3T2024.csv",
    r"C:\\Users\\pinhe\\OneDrive\Documentos\\intuitive_care\\create_tables\dados\4T2023.csv",
    r"C:\\Users\\pinhe\\OneDrive\Documentos\\intuitive_care\\create_tables\dados\4T2024.csv"
]

operadoras_file = r"C:\\Users\\pinhe\\OneDrive\Documentos\\intuitive_care\\create_tables\dados\\Relatorio_cadop.csv"

def write_create_tables_sql_pg():
    create_tables = """-- Para criar o banco de dados em PostgreSQL, execute (fora deste script):
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
"""
    with open("create_tables_pg.sql", "w", encoding="utf-8") as f:
        f.write(create_tables)

def convert_path_for_pg(path):
    # Converte barras invertidas para barras normais
    return path.replace("\\", "/")

def write_load_data_sql_pg(demo_files, operadoras_file):
    # Em PostgreSQL usamos o comando COPY para importar CSVs.
    load_data = ""
    
    # Importação dos dados cadastrais das operadoras ativas:
    operadoras_path = convert_path_for_pg(operadoras_file)
    load_data += f"""-- Importa dados das operadoras ativas
COPY operadoras_ativas(reg_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, complemento, bairro, cidade, uf, cep, ddd_telefone, fax, endereco_eletronico, representante, cargo_representante, data_registro_ans)
FROM '{operadoras_path}'
WITH (
    FORMAT csv,
    DELIMITER ';',
    HEADER true,
    QUOTE '\"',
    ENCODING 'UTF8'
);
\n
"""
    # Importação dos arquivos de demonstrações contábeis:
    for file in demo_files:
        file_path = convert_path_for_pg(file)
        base_name = os.path.basename(file)
        load_data += f"""-- Importa dados do arquivo {base_name}
COPY demonstracoes_contabeis(reg_ans, competencia, conta_contabil, valor)
FROM '{file_path}'
WITH (
    FORMAT csv,
    DELIMITER ';',
    HEADER true,
    QUOTE '\"',
    ENCODING 'UTF8'
);
\n
"""
    with open("load_data_pg.sql", "w", encoding="utf-8") as f:
        f.write(load_data)

def write_queries_sql_pg():
    queries = """-- Certifique-se de estar conectado ao banco de dados ans_dados

-- Query 1: Top 10 operadoras com maiores despesas no último trimestre
-- Exemplo: período de 01/10/2024 a 31/12/2024
SELECT 
    dc.reg_ans,
    oa.razao_social,
    SUM(dc.valor) AS total_despesa
FROM demonstracoes_contabeis dc
JOIN operadoras_ativas oa ON dc.reg_ans = oa.reg_ans
WHERE dc.conta_contabil = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
  AND dc.competencia BETWEEN '2024-10-01' AND '2024-12-31'
GROUP BY dc.reg_ans, oa.razao_social
ORDER BY total_despesa DESC
LIMIT 10;

-- Query 2: Top 10 operadoras com maiores despesas no último ano (exemplo: 2024)
SELECT 
    dc.reg_ans,
    oa.razao_social,
    SUM(dc.valor) AS total_despesa
FROM demonstracoes_contabeis dc
JOIN operadoras_ativas oa ON dc.reg_ans = oa.reg_ans
WHERE dc.conta_contabil = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
  AND EXTRACT(YEAR FROM dc.competencia) = 2024
GROUP BY dc.reg_ans, oa.razao_social
ORDER BY total_despesa DESC
LIMIT 10;
"""
    with open("queries_pg.sql", "w", encoding="utf-8") as f:
        f.write(queries)

def main():
    print("Gerando scripts SQL para PostgreSQL...")
    write_create_tables_sql_pg()
    write_load_data_sql_pg(demo_files, operadoras_file)
    write_queries_sql_pg()
    print("Scripts gerados com sucesso:")
    print(" - create_tables_pg.sql")
    print(" - load_data_pg.sql")
    print(" - queries_pg.sql")
    print("\nOBS: Certifique-se de que os caminhos dos arquivos nos comandos COPY estão corretos para o seu ambiente.")

if __name__ == "__main__":
    main()
