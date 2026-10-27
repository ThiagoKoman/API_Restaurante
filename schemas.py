from enum import Enum

from pydantic import BaseModel, Field

class Categoria(str, Enum):
    LANCHE = "LANCHE"
    BEBIDA = "BEBIDA"
    SOBREMESA = "SOBREMESA"

class StatusPedido(str, Enum):
    RECEBIDO = "RECEBIDO"
    EM_PREPARO = "EM_PREPARO"
    SAIU_PARA_ENTREGA = "SAIU_PARA_ENTREGA"
    ENTREGUE = "ENTREGUE"

class Perfil(str, Enum):
    ADMIN = "ADMIN"
    CLIENTE = "CLIENTE"

# ----- Usuario -----
class UsuarioCreate(BaseModel):
    email: str
    senha: str = Field(min_length=6,description="Minimo 6 caracteres")
    perfil: Perfil = Perfil.CLIENTE 

class UsuarioResponse(BaseModel):    
    id: int
    email: str
    perfil: Perfil

class LoginRequest(BaseModel):
    email: str
    senha: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ----- Cliente -----
class ClienteCreate(BaseModel):
    nome: str = Field(min_length=2)
    telefone: str
    endereco: str


class ClienteResponse(ClienteCreate):
    id: int


# ----- Produto -----
class ProdutoCreate(BaseModel):
    nome: str = Field(min_length=2)
    categoria: Categoria
    preco: float = Field(gt=0)  # preço tem que ser maior que zero


class ProdutoResponse(ProdutoCreate):
    id: int


# ----- Pedido -----
class PedidoCreate(BaseModel):
    cliente_id: int


class ItemCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0)


class ItemResponse(BaseModel):
    produto_id: int
    nome: str
    preco: float
    quantidade: int


class PedidoResponse(BaseModel):
    id: int
    cliente_id: int
    status: StatusPedido
    itens: list[ItemResponse]
    total: float


class StatusUpdate(BaseModel):
    status: StatusPedido