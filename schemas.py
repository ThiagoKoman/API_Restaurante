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