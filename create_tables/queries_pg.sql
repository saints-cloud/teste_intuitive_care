-- Certifique-se de estar conectado ao banco de dados ans_dados

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
