from fastapi import FastAPI, APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

import json

load_dotenv()

app = FastAPI()
router = APIRouter()

class Question(BaseModel):
    text_input: str
    text_history: Optional[str] = None
    context: Optional[str] = None
    way_respond: Optional[str] = None
    filters: Optional[dict] = None
    
    
def load_client_api_keys():
    if not hasattr(load_client_api_keys, "cache"):
        try:
            with open('client_api_keys.json', 'r') as file:
                load_client_api_keys.cache = json.load(file)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al cargar las claves de API: {str(e)}")
    return load_client_api_keys.cache

@router.post("/ia-fenalco/consultar-gpt")
async def consultar_gpt(request: Question, Authorization: str = Header(...), nameModel: str = Header(...)):
    try:
        if not Authorization or not nameModel:
            raise HTTPException(status_code=400, detail="Missing required headers")

       
        client_api_keys = load_client_api_keys()  
        openai_api_key = client_api_keys.get(Authorization)

        if not openai_api_key:
            raise HTTPException(status_code=403, detail="Invalid API Key")

        llm = ChatOpenAI(model_name=nameModel, openai_api_key=openai_api_key)
        chain = load_qa_chain(llm, chain_type="stuff")

        respuesta = chain.run(input_documents=[], question=request.text_input)

        return {"respuesta": respuesta, "detail": "Success"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hubo un problema al procesar tu solicitud: {str(e)}")


app.include_router(router)
