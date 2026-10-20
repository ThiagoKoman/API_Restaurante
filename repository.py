# CAMADA DE ACESSO A DADOS (Aula 6: Repository | Aula 8: agora com banco de dados)
#
# ANTES (listas em memória):
#   clientes = []
#   def salvar_cliente(cliente): clientes.append(cliente)
#
# AGORA (banco de dados via ORM):
#   toda função recebe uma "db: Session" (a conversa com o banco)
#   e manipula objetos ClienteModel/ProdutoModel/PedidoModel,
#   que o SQLAlchemy converte em SQL por baixo dos panos.
#
# Repare que NENHUMA regra de negócio mora aqui. Esta camada só sabe
# salvar e buscar. Quem decide "pode ou não pode" é o service.py.
from sqlalchemy.orm import Session

from models import ClienteModel, ItemPedidoModel, PedidoModel, ProdutoModel


# ----- Clientes -----
def salvar_cliente(db: Session, cliente: ClienteModel) -> ClienteModel:
    db.add(cliente)  # prepara o INSERT
    db.commit()  # executa de verdade no banco
    db.refresh(cliente)  # busca o id gerado pelo banco
    return cliente


def listar_clientes(db: Session) -> list[ClienteModel]:
    return db.query(ClienteModel).all()


def buscar_cliente(db: Session, cliente_id: int) -> ClienteModel | None:
    return db.query(ClienteModel).filter(ClienteModel.id == cliente_id).first()


# ----- Produtos -----
def salvar_produto(db: Session, produto: ProdutoModel) -> ProdutoModel:
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto


def listar_produtos(db: Session) -> list[ProdutoModel]:
    return db.query(ProdutoModel).all()


def buscar_produto(db: Session, produto_id: int) -> ProdutoModel | None:
    return db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()


# ----- Pedidos -----
def salvar_pedido(db: Session, pedido: PedidoModel) -> PedidoModel:
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return pedido


def buscar_pedido(db: Session, pedido_id: int) -> PedidoModel | None:
    return db.query(PedidoModel).filter(PedidoModel.id == pedido_id).first()


def adicionar_item(db: Session, item: ItemPedidoModel) -> None:
    db.add(item)
    db.commit()


def atualizar_status_pedido(db: Session, pedido: PedidoModel, novo_status: str) -> PedidoModel:
    pedido.status = novo_status
    db.commit()
    db.refresh(pedido)
    return pedido