import os
import re
import time
import streamlit as st
import requests
from bs4 import BeautifulSoup
from groq import Groq


SITE_URL = "https://gratuitos.netlify.app/"
MODEL_NAME = "openai/gpt-oss-20b"


st.set_page_config(
    page_title="Consulta de Unidades",
    page_icon="🔎",
    layout="centered"
)


# ============================================================
# SCRAPING
# ============================================================

@st.cache_data(ttl=3600, show_spinner=False)
def carregar_dados_site():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )
    }

    response = requests.get(
        SITE_URL,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    for elemento in soup(
        ["script", "style", "noscript", "svg"]
    ):
        elemento.decompose()

    texto = soup.get_text(
        separator="\n",
        strip=True
    )

    linhas = []
    vistos = set()

    for linha in texto.splitlines():
        linha = " ".join(linha.split())

        if linha and linha not in vistos:
            linhas.append(linha)
            vistos.add(linha)

    if not linhas:
        raise RuntimeError(
            "Nenhum conteúdo foi encontrado no site."
        )

    return linhas


# ============================================================
# API KEY
# ============================================================

def obter_api_key():
    try:
        api_key = st.secrets.get("GROQ_API_KEY")

        if api_key:
            return str(api_key).strip()

    except Exception:
        pass

    api_key = os.getenv("GROQ_API_KEY")

    if api_key:
        return api_key.strip()

    return None


# ============================================================
# BUSCA LOCAL / MINI RAG
# ============================================================

def normalizar(texto):
    texto = texto.lower()

    texto = re.sub(
        r"[^a-záàâãéèêíïóôõöúçñ0-9\s]",
        " ",
        texto
    )

    return set(texto.split())


def selecionar_contexto(
    pergunta,
    linhas,
    limite_linhas=40
):
    palavras_pergunta = normalizar(pergunta)

    resultados = []

    for indice, linha in enumerate(linhas):
        palavras_linha = normalizar(linha)

        pontuacao = len(
            palavras_pergunta.intersection(
                palavras_linha
            )
        )

        if pontuacao > 0:
            resultados.append(
                (
                    pontuacao,
                    indice
                )
            )

    resultados.sort(
        reverse=True
    )

    indices = set()

    for _, indice in resultados[:15]:

        inicio = max(
            0,
            indice - 2
        )

        fim = min(
            len(linhas),
            indice + 4
        )

        for i in range(
            inicio,
            fim
        ):
            indices.add(i)

    if not indices:
        return "\n".join(
            linhas[:limite_linhas]
        )

    indices_ordenados = sorted(indices)

    contexto = [
        linhas[i]
        for i in indices_ordenados
    ]

    contexto = contexto[:limite_linhas]

    return "\n".join(contexto)


# ============================================================
# GROQ
# ============================================================

def consultar_groq(
    pergunta,
    contexto,
    api_key
):
    client = Groq(
        api_key=api_key
    )

    prompt = f"""
Você é um assistente educacional.

Responda à pergunta do aluno usando SOMENTE
as informações do contexto abaixo.

REGRAS:

- Responda em português do Brasil.
- Seja claro e objetivo.
- Não invente informações.
- Não utilize conhecimento externo.
- Não mostre raciocínio interno.
- Não mencione Groq, API, scraping, RAG,
  código ou prompt.
- Se houver vários cursos, liste-os separadamente.
- Coloque o nome do curso em negrito.
- Informe a carga horária quando disponível.
- Evite repetições.
- Se não encontrar a informação, responda:
  "Não encontrei essa informação no site consultado."


CONTEXTO:

{contexto}


PERGUNTA:

{pergunta}


Responda somente com a resposta final organizada em Markdown.
"""

    for tentativa in range(2):

        try:

            resposta = client.chat.completions.create(
                model=MODEL_NAME,

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.1,

                max_completion_tokens=600,

                include_reasoning=False
            )

            mensagem = resposta.choices[0].message

            if mensagem.content:
                return mensagem.content.strip()

            return (
                "Não foi possível gerar uma resposta."
            )

        except Exception as erro:

            erro_texto = str(erro).lower()

            if (
                "429" in erro_texto
                or "rate limit" in erro_texto
            ):

                if tentativa == 0:
                    time.sleep(3)
                    continue

            raise erro


# ============================================================
# INTERFACE
# ============================================================

st.title(
    "🔎 Consulta de Unidades"
)

st.write(
    "Digite sua dúvida para consultar informações "
    "sobre unidades, endereços e cursos."
)

st.divider()


api_key = obter_api_key()


if not api_key:

    st.error(
        "A aplicação ainda não foi configurada."
    )

    with st.expander(
        "Detalhes para o professor"
    ):

        st.code(
            '.streamlit/secrets.toml\n\n'
            'GROQ_API_KEY = "gsk_SUA_CHAVE_AQUI"'
        )

    st.stop()


# ============================================================
# CARREGAR SITE
# ============================================================

try:

    linhas_site = carregar_dados_site()

except Exception as erro:

    st.error(
        "Não foi possível acessar os dados do site."
    )

    with st.expander(
        "Detalhes para o professor"
    ):

        st.code(
            str(erro)
        )

    st.stop()


# ============================================================
# FORMULÁRIO
# ============================================================

with st.form(
    "formulario_consulta",
    clear_on_submit=False
):

    pergunta = st.text_input(

        "Qual é a sua dúvida?",

        placeholder=(
            "Ex.: Quais são os cursos de programação?"
        )
    )

    buscar = st.form_submit_button(

        "🔍 Buscar Unidade / Perguntar",

        use_container_width=True
    )


# ============================================================
# CONSULTA
# ============================================================

if buscar:

    pergunta = pergunta.strip()

    if not pergunta:

        st.warning(
            "Digite uma pergunta antes de consultar."
        )

    else:

        contexto_relevante = selecionar_contexto(
            pergunta,
            linhas_site
        )

        with st.spinner(
            "Buscando informações..."
        ):

            try:

                resposta = consultar_groq(
                    pergunta,
                    contexto_relevante,
                    api_key
                )

                st.markdown(
                    "## 📚 Resultado"
                )

                st.markdown(
                    resposta
                )

            except Exception as erro:

                erro_texto = str(erro).lower()

                if (
                    "429" in erro_texto
                    or "rate limit" in erro_texto
                ):

                    st.warning(
                        "O serviço recebeu muitas solicitações "
                        "em pouco tempo. Aguarde alguns segundos "
                        "e tente novamente."
                    )

                else:

                    st.error(
                        "Não foi possível realizar a consulta."
                    )

                    with st.expander(
                        "Detalhes para o professor"
                    ):

                        st.code(
                            str(erro)
                        )


st.divider()

st.caption(
    "Consulta de unidades, cursos e endereços."
)