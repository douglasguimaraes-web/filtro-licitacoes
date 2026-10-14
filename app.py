import streamlit as st
import pandas as pd

st.set_page_config(page_title="Filtro de Licitações - Bahia", layout="wide")

# Proteção simples por senha
def checar_senha():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.title("🔒 Acesso Restrito")
        senha_digitada = st.text_input("Digite a senha de acesso:", type="password")
        if st.button("Entrar"):
            # VOCÊ PODE MUDAR A SENHA '123456' PARA A SENHA QUE QUISER AQUI ABAIXO:
            if senha_digitada == "123456":
                st.session_state["autenticado"] = True
                st.rerun()
            else:
                st.error("Senha incorreta!")
        return False
    return True

if checar_senha():
    st.title("📋 Filtro de Licitações da Bahia")
    st.write("Faça o upload da planilha do Com Licitação e aplique seus filtros abaixo.")

    # Upload do arquivo
    arquivo = st.file_uploader("Carregue aqui o arquivo baixado (.xlsx ou .csv)", type=["xlsx", "csv"])

    if arquivo is not None:
        try:
            if arquivo.name.endswith('.csv'):
                df = pd.read_csv(arquivo)
            else:
                df = pd.read_excel(arquivo)

            st.success("Arquivo carregado com sucesso!")

            # Filtros por palavras-chave
            st.subheader("🔍 Filtros de Busca")
            palavra_chave = st.text_input("Buscar palavra-chave no Objeto (ex: informática, reforma, limpeza):")

            df_filtrado = df.copy()

            if palavra_chave:
                # Procura a palavra nas colunas de texto
                colunas_texto = df_filtrado.select_dtypes(include=['object']).columns
                mascara = False
                for col in colunas_texto:
                    mascara = mascara | df_filtrado[col].astype(str).str.contains(palavra_chave, case=False, na=False)
                df_filtrado = df_filtrado[mascara]

            st.subheader(f"Resultados Encontrados ({len(df_filtrado)} registros)")
            st.dataframe(df_filtrado, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")
