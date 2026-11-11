import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = 'poder-ser-qualquer-mensgem'
ALGORITHM = 'HS256'
EXPIRA_MIN = 60

security = HTTPBearer()

# Banco de dados em memória para os usuários cadastrados
usuarios_db = []

# Criar função criar_hash
def criar_hash(senha: str) -> str:
    """Gera o hash bcrypt da senha."""
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Criar função verificar_senha
def verificar_senha(senha_informada: str, senha_hash: str) -> bool:
    """Verifica se a senha bate com o hash armazenado."""
    return bcrypt.checkpw(senha_informada.encode('utf-8'), senha_hash.encode('utf-8'))

# Criar função criar_token
def criar_token(dados: dict) -> str:
    """Cria um token JWT com tempo de expiração."""
    dados_cópia = dados.copy()
    exp = datetime.now(timezone.utc) + timedelta(minutes=EXPIRA_MIN)
    dados_cópia.update({"exp": exp})
    return jwt.encode(dados_cópia, SECRET_KEY, algorithm=ALGORITHM)

# Criar função usuario_logado
def usuario_logado(credenciais: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Valida o token JWT e retorna o email do usuário logado."""
    token = credenciais.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )