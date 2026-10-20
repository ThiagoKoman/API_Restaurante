# CAMADA DE MODELOS DO BANCO (Aula 8: ORM)
#
# Diferença para o schemas.py:
#   - schemas.py  -> formato dos dados na API (Pydantic)
#   - models.py   -> formato das TABELAS no banco (SQLAlchemy)
#
# Cada classe aqui = uma tabela. Cada atributo = uma coluna.
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class ClienteModel(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    endereco = Column(String, nullable=False)


class ProdutoModel(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    preco = Column(Float, nullable=False)


class PedidoModel(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    status = Column(String, nullable=False, default="RECEBIDO")

    # "itens" não é uma coluna: é o ORM buscando automaticamente
    # todas as linhas de ItemPedidoModel que apontam para este pedido.
    itens = relationship("ItemPedidoModel", backref="pedido", cascade="all, delete-orphan")


class ItemPedidoModel(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    nome_produto = Column(String, nullable=False)  # guardamos o nome e o preço
    preco = Column(Float, nullable=False)  # do momento da compra (histórico)
    quantidade = Column(Integer, nullable=False)