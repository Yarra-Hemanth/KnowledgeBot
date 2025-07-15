# 💬 KnowledgeBot

**KnowledgeBot** is an intelligent, privacy-focused chatbot powered by a local LLM (Large Language Model). It features chat session history, a user-friendly interface built with Streamlit, and runs completely offline using [Ollama](https://ollama.com/) and a lightweight model like `tinyllama`.

---

## 🚀 Features  

- 🧠 **Offline Chat with LLM** (via Ollama)  
- 💾 **Multi-Session Chat History**  
- 📄 **Downloadable Conversations**  
- 🎨 **Chat-like UI with Typing Animation**  
- ⚡ **Fast, Lightweight, and Local**  

---

## 🛠️ Tech Stack  

- **Frontend/UI**: [Streamlit](https://streamlit.io/)  
- **LLM API**: [Ollama](https://ollama.com/)  
- **Model**: `tinyllama:1.1b` (can be changed)  
- **Language**: Python  

---

## 📦 Setup Instructions  

### 1. Clone the Repository  

git clone https://github.com/Yarra-Hemanth/KnowledgeBot.git  
cd KnowledgeBot

### 2. Set Up Virtual Environment

python -m venv venv  
source venv/bin/activate  # or venv\Scripts\activate on Windows

### 3. Install Depenedncies  
pip install -r requirements.txt

### 4. Install Ollama & LLM  
Install Ollama and pull the TinyLLaMA model:

ollama pull tinyllama:1.1b  

### 5. Run the App  
streamlit run main.py  
Then, open http://localhost:8501 in your browser.  

---

📁 Project Structure  
KnowledgeBot/  
├── main.py  
├── state.py  
├── ui.py  
├── requirements.txt  
└── README.md  

---

📃 License  
This project is licensed under the MIT License.

---

🙋‍♂️ Author  
Hemanth Yarra  
🔗 [LinkedIn](https://www.linkedin.com/in/hemanth-yarra-5a1775305/)  
📫 yarrahemanth5@gmail.com
