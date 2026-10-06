from fastapi import APIRouter

import service

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


# ----- Clientes -----
@clientes_router.post("", response_model=ClienteResponse, status_code=201)
def cadastrar_cliente(dados: ClienteCreate):
    return service.cadastrar_cliente(dados)


@clientes_router.get("", response_model=list[ClienteResponse])
def listar_clientes():
    return service.listar_clientes()


@clientes_router.get("/{cliente_id}", response_model=ClienteResponse)
def buscar_cliente(cliente_id: int):
    return service.buscar_cliente(cliente_id)


# ----- Produtos -----
@produtos_router.post("", response_model=ProdutoResponse, status_code=201)
def cadastrar_produto(dados: ProdutoCreate):
    return service.cadastrar_produto(dados)


@produtos_router.get("", response_model=list[ProdutoResponse])
def listar_produtos():
    return service.listar_produtos()


# ----- Pedidos -----
@pedidos_router.post("", response_model=PedidoResponse, status_code=201)
def registrar_pedido(dados: PedidoCreate):
    return service.criar_pedido(dados.cliente_id)


@pedidos_router.get("/{pedido_id}", response_model=PedidoResponse)
def buscar_pedido(pedido_id: int):
    return service.buscar_pedido(pedido_id)


@pedidos_router.post("/{pedido_id}/itens", response_model=PedidoResponse, status_code=201)
def incluir_item(pedido_id: int, dados: ItemCreate):
    return service.adicionar_item(pedido_id, dados)


@pedidos_router.get("/{pedido_id}/status")
def consultar_status(pedido_id: int):
    pedido = service.buscar_pedido(pedido_id)
    return {"pedido_id": pedido["id"], "status": pedido["status"]}


@pedidos_router.patch("/{pedido_id}/status")
def atualizar_status(pedido_id: int, dados: StatusUpdate):
    pedido = service.atualizar_status(pedido_id, dados.status)
    return {"pedido_id": pedido["id"], "status": pedido["status"]}