
# RisparmioSmart Backend + Database + OCR Pipeline (FastAPI)

Backend FastAPI con:
- OCR (Tesseract) via `pytesseract` con pre-processing (Pillow/OpenCV opzionale)
- API REST per salvare e leggere offerte
- Database SQLite di default (oppure PostgreSQL se imposti `DATABASE_URL`)
- Dockerfile pronto per Render/Railway (installa `tesseract-ocr` + lingua italiana)
- CORS abilitato per chiamate dal frontend su Vercel

## Avvio rapido (senza Docker)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Installa tesseract sul sistema:
# Ubuntu/Debian: sudo apt-get update && sudo apt-get install -y tesseract-ocr tesseract-ocr-ita
# macOS (brew): brew install tesseract && sudo cp -R /usr/local/Cellar/tesseract/*/share/tessdata/ita.traineddata /usr/local/share/tessdata/ (se serve)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Apri: http://localhost:8000/docs

## Variabili ambiente
Copia `.env.example` in `.env` e personalizza:
```env
DATABASE_URL=sqlite:///./risparmiosmart.db
ALLOWED_ORIGINS=http://localhost:3000,https://<tuo-frontend>.vercel.app
```

## Deploy con Docker (consigliato per OCR)
```bash
docker build -t risparmiosmart-backend .
docker run -p 8000:8000 --env-file .env risparmiosmart-backend
```

Su Render:
- Crea un servizio Web "Docker"
- Seleziona il repository
- Porta: 8000
- Comando di avvio: (vuoto, usa CMD dal Dockerfile)
