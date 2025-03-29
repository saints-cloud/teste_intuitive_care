from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI(
    title="API de Busca de Operadoras",
    description="Busca textual nos cadastros de operadoras a partir do CSV.",
    version="1.0"
)

# Configuração do CORS para permitir acesso de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja para os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

csv_path = "Relatorio_cadop.csv"
df_operadoras = pd.read_csv(csv_path, delimiter=";", encoding="utf-8")

# Endpoint de busca
@app.get("/search")
def search_operadoras(q: str = Query(..., description="Texto de busca")):
    try:
        q_lower = q.lower()
        
        # Criar máscara para buscar o termo em todas as colunas
        mask = df_operadoras.astype(str).apply(
            lambda row: row.str.lower().str.contains(q_lower, na=False).any(), axis=1
        )
        
        results = df_operadoras[mask].head(10)
        
        processed_results = [
            {k: (v if pd.notna(v) else None) for k, v in record.items()}
            for record in results.to_dict(orient='records')
        ]
        
        return processed_results
    
    except Exception as e:
        print(f"Erro durante a busca: {str(e)}")
        return {"error": "Ocorreu um erro durante a busca"}, 500


# Rota raiz para verificar se a API está funcionando
@app.get("/")
def read_root():
    return {
        "message": "API de Busca de Operadoras está funcionando",
        "version": app.version,
        "docs": "/docs"
    }


# Para rodar localmente: uvicorn server:app --reload