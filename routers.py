from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import service
from database import get_db
from models import PedidoModel

from schemas import (
    ClienteCreate,
    ClienteResponse,
    ItemCreate,
    ItemResponse,
    PedidoCreate,
    PedidoResponse,
    ProdutoCreate,
    ProdutoResponse,
    StatusPedido,
    StatusUpdate
)

clientes_router = APIRouter(prefix="/clientes", tags=["Clientes"])
produtos_router = APIRouter(prefix="/produtos", tags=["Produtos"])
pedidos_router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

def _pedido_para_response(pedido: PedidoModel) -> PedidoResponse:
    return PedidoResponse(
        id=pedido.id,
        cliente_id=pedido.cliente_id,
        status=pedido.status,
        itens=[
            {
                "produto_id": item.produto_id,
                "nome": item.nome_produto,
                "preco": item.preco,
                "quantidade": item.quantidade
            }
            for item in pedido.itens
        ],
        total=service.calcular_total(pedido)
    )


# ----- Clientes -----
@clientes_router.post("", response_model=ClienteResponse, status_code=201)
def cadastrar_cliente(dados: ClienteCreate, db: Session = Depends(get_db)):
    return service.cadastrar_cliente(db, dados)


@clientes_router.get("", response_model=list[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db) ):
    return service.listar_clientes(db)


@clientes_router.get("/{cliente_id}", response_model=ClienteResponse)
def buscar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return service.buscar_cliente(db, cliente_id)


# ----- Produtos -----
@produtos_router.post("", response_model=ProdutoResponse, status_code=201)
def cadastrar_produto(dados: ProdutoCreate, db: Session = Depends(get_db)):
    return service.cadastrar_produto(db,dados)


@produtos_router.get("", response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return service.listar_produtos(db)


# ----- Pedidos -----
@pedidos_router.post("", response_model=PedidoResponse, status_code=201)
def registrar_pedido(dados: PedidoCreate, db: Session = Depends(get_db)):
    pedido = service.criar_pedido(db,dados.cliente_id)
    return _pedido_para_response(pedido)

@pedidos_router.get("/{pedido_id}", response_model=PedidoResponse)
def buscar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = service.buscar_pedido(db,pedido_id)
    return _pedido_para_response(pedido)


@pedidos_router.post("/{pedido_id}/itens", response_model=PedidoResponse, status_code=201)
def incluir_item(pedido_id: int, dados: ItemCreate,  db: Session = Depends(get_db)):
    pedido = service.adicionar_item(db, pedido_id, dados) 
    return _pedido_para_response(pedido)


@pedidos_router.get("/{pedido_id}/status")
def consultar_status(pedido_id: int, db: Session = Depends(get_db)):
    pedido = service.buscar_pedido(db,pedido_id)
    return {"pedido_id": pedido["id"], "status": pedido["status"]}


@pedidos_router.patch("/{pedido_id}/status")
def atualizar_status(pedido_id: int, dados: StatusUpdate, db: Session = Depends(get_db)):
    pedido = service.atualizar_status(db, pedido_id, dados.status)
    return {"pedido_id": pedido["id"], "status": pedido["status"]}