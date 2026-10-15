import io
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from rembg import remove, new_session

app = FastAPI(title="Journal Background Removal API")

# Libera o CORS estritamente para o Next.js local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Mude de ["http://localhost:3000"] para ["*"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pré-carrega a sessão do modelo de IA na inicialização do servidor
# Isso elimina o cold start de ~2s a cada requisição
print("Carregando modelo U2-Net...")
model_session = new_session("u2netp")
print("Modelo carregado. API pronta.")

@app.post("/api/remove-background")
async def remove_background(file: UploadFile = File(...)):
    # Lê os bytes da imagem enviada
    input_data = await file.read()
    
    # Processa a remoção de fundo passando a sessão em cache
    output_data = remove(input_data, session=model_session)
    
    # Retorna o resultado direto da memória como um stream PNG
    return StreamingResponse(io.BytesIO(output_data), media_type="image/png")