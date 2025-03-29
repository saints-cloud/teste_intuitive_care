import os
import pandas as pd
import tabula
from zipfile import ZipFile

def main():
    pdf_path = "Anexo_I.pdf"
    csv_filename = "rol_de_procedimentos.csv"
    seu_nome = "LaysPinheiro"
    zip_filename = f"Teste_{seu_nome}.zip"
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {pdf_path}")
    use_lattice = True
    use_stream = False
    use_guess = True 
    
    print(f"Extraindo tabelas do PDF usando lattice={use_lattice}, stream={use_stream}, guess={use_guess}...")
    

    tabelas = tabula.read_pdf(
        pdf_path,
        pages="all",
        multiple_tables=True,
        lattice=use_lattice,
        stream=use_stream,
        guess=use_guess
    )
    
    if isinstance(tabelas, list):
        df = pd.concat(tabelas, ignore_index=True)
    else:
        df = tabelas
    
    print("Extração concluída!")
    print("Colunas encontradas:", df.columns.tolist())
    
    df.rename(columns={
        "OD": "Seg. Odontológica",
        "AMB": "Seg. Ambulatorial"
    }, inplace=True)
    
    print("Colunas após substituição:", df.columns.tolist())
    
    df.to_csv(csv_filename, index=False, encoding="utf-8")
    print(f"Dados salvos em CSV: {csv_filename}")
    
    with ZipFile(zip_filename, "w") as zipf:
        zipf.write(csv_filename, os.path.basename(csv_filename))
    print(f"CSV compactado em: {zip_filename}")

if __name__ == "__main__":
    main()
