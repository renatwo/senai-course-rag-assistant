<div align="center">

🔎 Consulta de Unidades com IA

Aplicação para consultar unidades, cursos e endereços usando linguagem natural







</div>

📌 O que a aplicação faz

A aplicação permite que o usuário faça perguntas sobre informações disponíveis no site consultado, como:

unidades;

endereços;

cursos;

carga horária;

informações relacionadas aos cursos disponíveis.

O usuário digita uma pergunta em linguagem natural e recebe uma resposta organizada automaticamente.

Exemplo:

Quais são os cursos de programação?

ou:

Qual é o endereço da unidade?

🧠 Como funciona

A aplicação segue um fluxo simples:

Usuário faz uma pergunta
        ↓
Streamlit recebe a consulta
        ↓
O sistema acessa o site
        ↓
BeautifulSoup extrai o conteúdo
        ↓
O sistema procura os trechos mais relacionados à pergunta
        ↓
Apenas o contexto relevante é enviado para a IA
        ↓
A Groq gera a resposta
        ↓
O resultado é exibido ao usuário

🔍 Mini RAG

O projeto utiliza uma abordagem simples inspirada em RAG (Retrieval-Augmented Generation).

Antes de enviar a pergunta para o modelo de IA, o sistema procura no conteúdo do site quais trechos possuem maior relação com a consulta.

Dessa forma, a IA recebe apenas as informações mais relevantes.

Isso ajuda a:

reduzir o número de tokens enviados;

melhorar a relevância das respostas;

evitar informações desnecessárias;

diminuir a chance de respostas inventadas.

🌐 Web Scraping

A aplicação utiliza:

requests
BeautifulSoup

para acessar o site e extrair seu conteúdo.

Elementos que não são úteis para a consulta, como:

script
style
noscript
svg

são removidos antes do processamento.

⚡ Cache

Os dados coletados do site ficam armazenados em cache por até 1 hora:

@st.cache_data(ttl=3600)

Isso evita que o site precise ser acessado novamente a cada pergunta.

🤖 Inteligência Artificial

A aplicação utiliza a Groq API com o modelo:

openai/gpt-oss-20b

O modelo recebe:

a pergunta do usuário;

somente o contexto selecionado pelo sistema.

Ele é instruído a responder apenas com base nas informações encontradas no site consultado.

🛡️ Controle de respostas

A IA recebe regras para:

responder em português;

não inventar informações;

não utilizar conhecimento externo;

organizar cursos separadamente;

informar carga horária quando disponível;

informar quando determinado dado não foi encontrado.

Quando não existe informação suficiente, a resposta esperada é:

Não encontrei essa informação no site consultado.

🚦 Tratamento de erros

A aplicação também possui tratamento para erros de limite da API.

Caso ocorra um erro:

429 - Rate Limit

o sistema aguarda alguns segundos e realiza uma nova tentativa.

Se o problema continuar, uma mensagem amigável é exibida ao usuário.

🔐 Segurança da API Key

A chave da Groq não fica escrita diretamente no código.

A aplicação procura a chave através de:

st.secrets.get("GROQ_API_KEY")

ou:

os.getenv("GROQ_API_KEY")

Isso evita a exposição da API Key no código público.

🛠️ Tecnologias utilizadas

Tecnologia

Função

Python

Linguagem principal

Streamlit

Interface web

Requests

Acesso ao site

BeautifulSoup

Extração do conteúdo

Groq API

Processamento com IA

GPT-OSS 20B

Modelo de linguagem

Regex

Normalização de texto

Streamlit Cache

Cache dos dados

📚 Resumo

A aplicação transforma uma página com informações em uma interface de consulta inteligente.

Em vez de procurar manualmente no site, o usuário pode fazer perguntas e receber respostas baseadas diretamente no conteúdo disponível na página.

<div align="center">

🌐 Site → 🔍 Busca → 🤖 IA → 📚 Resposta

</div>
