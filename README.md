# 🎯 GPT-Based Slide Generator API

A FastAPI-powered backend to generate customizable PowerPoint presentations using LLMs (via OpenRouter). Supports themes, LLM selection, image-enhanced slides, and download via Swagger or REST clients.

---

## 🚀 Features

- ✅ Generate and configure style of `.pptx` files from a topic
- 🎨 Custom font, and slide count
- 🧠 Dynamic LLM selection (e.g., Mistral, LLaMA 3, GPT-4)
- 🔐 API key-based authentication
- 📊 Rate limiting per user
- 📎 Swagger UI for testing

---

## 📂 Project Structure
```
.
├── api/
│   └── routes_presentation.py        # All API routes
├── config/
│   └── llm_registry.py               # LLM aliases (mistral, llama3, etc.)
├── models/
│   └── models.py                     # Pydantic schemas
├── stores/
│   ├── presentation_store.py         # Slide metadata store
│   └── user_store.py                 # API key → user ID store
├── utils/
│   ├── auth.py                       # API key verification
│   ├── limiter.py                    # Rate limiting logic
│   ├── slide_generator.py            # LLM-based slide content + .pptx creation
│   └── slide_styler.py               # Re-theming existing .pptx files (configure endpoint)
├── samples/                          # Generated .pptx files
├── main.py                           # FastAPI entrypoint
├── requirements.txt
└── render.yaml                       # Render.com deployment config
```

---

## 🛠️ Setup Locally

### 1. Clone the repository

```bash
git clone https://github.com/arnald999/customizable-presentation.git
cd customizable-presentation
```

### 2. Setup environment and install dependencies

Run setup_venv.bat file (work for Windows)

```bash
setup_venv.bat
```

### 3. Configure .env

```env
OPENROUTER_API_KEY=sk-xxxxxxx
```

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

### 5. Access the API

The APIs can be accessed via Swagger:
- http://localhost:8000/docs

---

## 🔐 Authentication and Rate Limiting 

- All endpoints require an API key header.
- Authorize user via Swagger 
- Each user gets rate-limited based on this key.

---

## 📤 Sample Payload

```json
{
  "topic": "Impact of AI in Education",
  "config": {
    "num_slides": 4,
    "font": "Calibri",
    "color_theme": "#0D47A1",
    "llm_model": "mistral"
  }
}
```
---

## 📥 Output
- A downloadable `.pptx` file
- Available via `/api/v1/presentations/{id}/download`

---

## 🌐 Deploy to Render
Already set up with `render.yaml`. Steps:
- Push to GitHub
- Go to https://render.com
- "New Web Service" → Connect repo
- Set environment variable `OPENROUTER_API_KEY`
- Deploy 🎉

---

## 🧠 Supported LLMs
Short names mapped in llm_registry.py:

| Alias   | Model ID                               |
|---------|----------------------------------------|
| mistral | mistralai/mixtral-8x7b-instruct        |
| llama3  | meta-llama/llama-3-8b-instruct         |
| gpt4    | openai/gpt-4                           |
| gemma   | google/gemma-7b-it                     |

---

## 🧪 API Endpoints Summary
| Method | Endpoint                                 | Description                      |
|--------|------------------------------------------|----------------------------------|
| POST   | `/api/v1/presentations`                  | Generate new presentation        |
| GET    | `/api/v1/presentations/{id}`             | Get presentation metadata        |
| GET    | `/api/v1/presentations/{id}/download`    | Download `.pptx`                 |
| POST   | `/api/v1/presentations/{id}/configure`   | Change style and color of `.pptx`|

---

## ⚙️ Live Code Deployment

⚠️ **Please be patient!**

This API is hosted on a **free-tier service (Render)** which may take **10–30 seconds to wake up** after inactivity.

If the first request seems delayed or the Swagger UI doesn't load instantly, give it a few moments and try refreshing.

```Swagger API
https://customizable-presentation.onrender.com/docs
```