from fastapi import HTTPException

import repository

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
    Categoria
)

ORDEM_STATUS = [
    StatusPedido.RECEBIDO,
    StatusPedido.EM_PREPARO,
    StatusPedido.SAIU_PARA_ENTREGA,
    StatusPedido.ENTREGUE,
]


# ----- Clientes -----
def cadastrar_cliente(dados: ClienteCreate) -> dict:
    return repository.salvar_cliente(dados.model_dump())


def listar_clientes() -> list:
    return repository.listar_clientes()


def buscar_cliente(cliente_id: int) -> dict:
    cliente = repository.buscar_cliente(cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


# ----- Produtos -----
def cadastrar_produto(dados: ProdutoCreate) -> dict:
    return repository.salvar_produto(dados.model_dump())


def listar_produtos() -> list:
    return repository.listar_produtos()


def buscar_produto(produto_id: int) -> dict:
    produto = repository.buscar_produto(produto_id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


# ----- Pedidos -----
def criar_pedido(cliente_id: int) -> dict:
    buscar_cliente(cliente_id)  # se o cliente não existir, já dá erro 404
    pedido = {
        "cliente_id": cliente_id,
        "status": StatusPedido.RECEBIDO,
        "itens": [],
        "total": 0,
    }
    return repository.salvar_pedido(pedido)


def buscar_pedido(pedido_id: int) -> dict:
    pedido = repository.buscar_pedido(pedido_id)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido


def adicionar_item(pedido_id: int, dados: ItemCreate) -> dict:
    pedido = buscar_pedido(pedido_id)

    # Regra 1: só pode incluir itens enquanto o pedido está RECEBIDO
    if pedido["status"] != StatusPedido.RECEBIDO:
        raise HTTPException(status_code=400, detail="Pedido não aceita mais itens")

    produto = buscar_produto(dados.produto_id)

    item = {
        "produto_id": produto["id"],
        "nome": produto["nome"],
        "preco": produto["preco"],  # guarda o preço do momento da compra
        "quantidade": dados.quantidade,
    }
    pedido["itens"].append(item)
    pedido["total"] = round(pedido["total"] + item["preco"] * item["quantidade"], 2)
    return pedido


def atualizar_status(pedido_id: int, novo_status: StatusPedido) -> dict:
    pedido = buscar_pedido(pedido_id)

    posicao_atual = ORDEM_STATUS.index(pedido["status"])
    posicao_nova = ORDEM_STATUS.index(novo_status)

    # Regra 2: o status só pode avançar para o próximo da lista
    if posicao_nova != posicao_atual + 1:
        raise HTTPException(status_code=400, detail="Transição de status inválida")

    # Regra 3: não pode preparar um pedido vazio
    if pedido["status"] == StatusPedido.RECEBIDO and len(pedido["itens"]) == 0:
        raise HTTPException(status_code=400, detail="Pedido sem itens")

    pedido["status"] = novo_status
    return pedido