# CAMADA DE SERVIÇO (Aula 6: Regras de Negócio)
#
# O que muda da aula passada: toda função agora recebe "db: Session" e repassa
# para o repository. As REGRAS continuam exatamente as mesmas de antes —
# é só o jeito de guardar o dado que mudou, não a regra em si.
from fastapi import HTTPException
from sqlalchemy.orm import Session

import repository
from models import ClienteModel, ItemPedidoModel, PedidoModel, ProdutoModel
from schemas import ClienteCreate, ItemCreate, ProdutoCreate, StatusPedido

# A ordem da lista define o fluxo permitido do pedido
ORDEM_STATUS = [
    StatusPedido.RECEBIDO,
    StatusPedido.EM_PREPARO,
    StatusPedido.SAIU_PARA_ENTREGA,
    StatusPedido.ENTREGUE,
]


# ----- Clientes -----
def cadastrar_cliente(db: Session, dados: ClienteCreate) -> ClienteModel:
    cliente = ClienteModel(**dados.model_dump())
    return repository.salvar_cliente(db, cliente)


def listar_clientes(db: Session) -> list[ClienteModel]:
    return repository.listar_clientes(db)


def buscar_cliente(db: Session, cliente_id: int) -> ClienteModel:
    cliente = repository.buscar_cliente(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


# ----- Produtos -----
def cadastrar_produto(db: Session, dados: ProdutoCreate) -> ProdutoModel:
    produto = ProdutoModel(
        nome=dados.nome,
        categoria=dados.categoria.value,
        preco=dados.preco,
    )
    return repository.salvar_produto(db, produto)


def listar_produtos(db: Session) -> list[ProdutoModel]:
    return repository.listar_produtos(db)


def buscar_produto(db: Session, produto_id: int) -> ProdutoModel:
    produto = repository.buscar_produto(db, produto_id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


# ----- Pedidos -----
def criar_pedido(db: Session, cliente_id: int) -> PedidoModel:
    buscar_cliente(db, cliente_id)  # se o cliente não existir, já dá erro 404
    pedido = PedidoModel(cliente_id=cliente_id, status=StatusPedido.RECEBIDO.value)
    return repository.salvar_pedido(db, pedido)


def buscar_pedido(db: Session, pedido_id: int) -> PedidoModel:
    pedido = repository.buscar_pedido(db, pedido_id)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido


def adicionar_item(db: Session, pedido_id: int, dados: ItemCreate) -> PedidoModel:
    pedido = buscar_pedido(db, pedido_id)

    # Regra 1: só pode incluir itens enquanto o pedido está RECEBIDO
    if pedido.status != StatusPedido.RECEBIDO.value:
        raise HTTPException(status_code=400, detail="Pedido não aceita mais itens")

    produto = buscar_produto(db, dados.produto_id)

    item = ItemPedidoModel(
        pedido_id=pedido.id,
        produto_id=produto.id,
        nome_produto=produto.nome,
        preco=produto.preco,  # guarda o preço do momento da compra
        quantidade=dados.quantidade,
    )
    repository.adicionar_item(db, item)
    db.refresh(pedido)  # recarrega o pedido para já vir com o item novo em pedido.itens
    return pedido


def atualizar_status(db: Session, pedido_id: int, novo_status: StatusPedido) -> PedidoModel:
    pedido = buscar_pedido(db, pedido_id)

    posicao_atual = ORDEM_STATUS.index(StatusPedido(pedido.status))
    posicao_nova = ORDEM_STATUS.index(novo_status)

    # Regra 2: o status só pode avançar para o próximo da lista
    if posicao_nova != posicao_atual + 1:
        raise HTTPException(status_code=400, detail="Transição de status inválida")

    # Regra 3: não pode preparar um pedido vazio
    if pedido.status == StatusPedido.RECEBIDO.value and len(pedido.itens) == 0:
        raise HTTPException(status_code=400, detail="Pedido sem itens")

    return repository.atualizar_status_pedido(db, pedido, novo_status.value)


def calcular_total(pedido: PedidoModel) -> float:
    """Função auxiliar: soma os itens. Fica aqui (service) porque é uma regra,
    não um acesso a dado."""
    return round(sum(item.preco * item.quantidade for item in pedido.itens), 2)