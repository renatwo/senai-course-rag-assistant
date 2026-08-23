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

- 📚 cursos disponíveis
- 🏢 unidades
- 📍 endereços
- ⏱️ carga horária
- ℹ️ outras informações presentes na página consultada

### Exemplos

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

Em vez de enviar todo o conteúdo do site para o modelo de IA, o sistema identifica primeiro os trechos mais relacionados à pergunta e envia apenas esse contexto.

Isso ajuda a:

- reduzir a quantidade de tokens
- melhorar a relevância da resposta
- evitar informações desnecessárias
- diminuir a chance de respostas inventadas

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Função |
|---|---|
| **Python** | Linguagem principal |
| **Streamlit** | Interface web |
| **Requests** | Acesso ao site |
| **BeautifulSoup** | Extração do conteúdo |
| **Groq API** | Processamento com IA |
| **GPT-OSS 20B** | Modelo de linguagem |
| **Regex** | Normalização do texto |
| **Streamlit Cache** | Cache dos dados |

---

## 🔐 Segurança

A chave da Groq não fica escrita diretamente no código.

A aplicação utiliza `st.secrets` ou a variável de ambiente `GROQ_API_KEY`.

---

<div align="center">

### 🌐 Site → 🔍 Busca → 🤖 IA → 📚 Resposta

</div>
