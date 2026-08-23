<div align="center">

# 🔎 Consulta de Unidades com IA

### Aplicação para consultar unidades, cursos e endereços usando linguagem natural

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-Web%20Scraping-4B8BBE?style=for-the-badge)
![RAG](https://img.shields.io/badge/Mini_RAG-8E75B2?style=for-the-badge)

</div>

---

## 📌 O que a aplicação faz

A aplicação permite consultar informações disponíveis em um site através de perguntas em linguagem natural.

Ela pode responder dúvidas sobre:

- 📚 cursos disponíveis;
- 🏢 unidades;
- 📍 endereços;
- ⏱️ carga horária;
- ℹ️ outras informações presentes na página consultada.

Exemplos de perguntas:

```text
Quais são os cursos de programação?
```

```text
Existe curso de Python?
```

```text
Qual é o endereço da unidade?
```

---

## 🧠 Como funciona

```text
👤 Usuário faz uma pergunta
          ↓
🖥️ Streamlit recebe a consulta
          ↓
🌐 O sistema acessa o site
          ↓
🔎 BeautifulSoup extrai o conteúdo
          ↓
🧠 O sistema seleciona os trechos mais relevantes
          ↓
🤖 A Groq processa o contexto
          ↓
📚 A resposta é exibida de forma organizada
```

---

## 🔍 Mini RAG

A aplicação utiliza uma abordagem simples inspirada em **RAG (Retrieval-Augmented Generation)**.

Em vez de enviar todo o conteúdo do site para o modelo de IA, o sistema primeiro identifica os trechos mais relacionados à pergunta.

Depois, somente esse contexto é enviado para o modelo.

Isso ajuda a:

- reduzir a quantidade de tokens;
- melhorar a relevância da resposta;
- evitar informações desnecessárias;
- diminuir a chance de respostas inventadas.

---

## 🌐 Web Scraping

O conteúdo da página é coletado usando:

```python
requests
BeautifulSoup
```

Durante o processamento, elementos como:

```text
script
style
noscript
svg
```

são removidos para manter apenas o conteúdo útil.

---

## ⚡ Cache

Os dados do site ficam armazenados temporariamente por até **1 hora**:

```python
@st.cache_data(ttl=3600)
```

Isso evita novas requisições ao site a cada pergunta.

---

## 🤖 Inteligência Artificial

A aplicação utiliza a **Groq API** com o modelo:

```text
openai/gpt-oss-20b
```

O modelo recebe apenas:

- a pergunta do usuário;
- o contexto encontrado no site.

Ele é instruído a responder somente com base nas informações disponíveis na fonte consultada.

---

## 🛡️ Controle de respostas

A aplicação orienta a IA a:

- responder em português;
- não inventar informações;
- não utilizar conhecimento externo;
- organizar cursos separadamente;
- informar carga horária quando disponível;
- avisar quando uma informação não for encontrada.

Quando não há informação suficiente, a resposta esperada é:

```text
Não encontrei essa informação no site consultado.
```

---

## 🚦 Tratamento de erros

Se ocorrer um erro de limite da API:

```text
429 - Rate Limit
```

o sistema aguarda alguns segundos e realiza uma nova tentativa.

Caso o problema continue, uma mensagem amigável é exibida ao usuário.

---

## 🔐 Segurança

A chave da Groq não fica exposta diretamente no código.

A aplicação utiliza:

```python
st.secrets.get("GROQ_API_KEY")
```

ou:

```python
os.getenv("GROQ_API_KEY")
```

para carregar a chave com segurança.

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Função |
|---|---|
| **Python** | Linguagem principal |
| **Streamlit** | Interface web |
| **Requests** | Requisições HTTP |
| **BeautifulSoup** | Extração do conteúdo da página |
| **Groq API** | Processamento com IA |
| **GPT-OSS 20B** | Modelo de linguagem |
| **Regex** | Normalização do texto |
| **Streamlit Cache** | Cache dos dados |

---

<div align="center">

### 🌐 Site → 🔍 Busca → 🤖 IA → 📚 Resposta

</div>
