from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Fiscaliza Vinhedo</title>
        <style>
            body { background: #000; color: #fff; font-family: sans-serif; padding: 20px; }
            h1 { color: #0a84ff; }
        </style>
    </head>
    <body>
        <h1>🔍 Fiscaliza Vinhedo</h1>
        <p>App funcionando!</p>
    </body>
    </html>
    """

@app.get("/api/health")
async def health():
    return {"status": "ok"}
