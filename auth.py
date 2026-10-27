from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorozationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
from models import UsuarioModel

SECRET_KEY = "Sennacabulos54321"
ALGORITH = "HS256"
EXPIRACAO_TOKEN_MINUTOS = 60

pwd_context = CryptContext(schemas=["bcrypt"], deprecated=auto)

security = HTTPBearer()

# 1. Hash de senha
def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)

def verificar_senha(senha: str, hash_senha: str) -> bool:
    return pwd_context.verify(senha,hash_senha)

# 2. Token JWT
def criar_token(email: str) -> str:
    payload = {
        "sub": email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRACAO_TOKEN_MINUTOS)
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITH)

def decodificar_token(token: str) -> str:
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITH])
        return payload["sub"] #devolvendo oo email do usuário
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401 , detail="Token expirado")
    except jwt.InvalidaTokenError:
        raise HTTPException(status_code=401 , detail="Token inválido")

# 3. Dependêcias de acesso

def get_usuario_atual(credentials: HTTPAuthorozationCredentials = Depends(security), db: Session = Depends(get_db)) -> UsuarioModel:
    email = decodificar_token(credentials.credentials)

    usuario = db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuário do token não existe mais")
    
    return usuario

def exige_admin(usuario: UsuarioModel = Depends(get_usuario_atual)) -> UsuarioModel:
    if usuario.perfil != "ADMIN":
        raise HTTPException(status_code=403, detail="Apenas usuários administradores podem realizar essa ação")
    return usuario