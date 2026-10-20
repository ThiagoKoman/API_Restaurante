from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

# Modelos para o DB

class ClienteModel(Base):
    __tablename__ ="clientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    endereco = Column(String, nullable=False)

class ProdutoModel(Base):
    __tablename__="produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    preco = Column(Float, nullable=False)

class PedidoModel(Base):
    __tablename__="pedidos"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"),nullable=False)
    status = Column(String, nullable=False, default="RECEBIDO" )
    itens = relationship("ItemPedidoModel",backref="pedido",cascade="all, delete-orphan")

class ItemPedidoModel(Base):
    __tablename__="itens_pedido"
    id = Column(Integer, primary_key=True,index=True)
    pedido_id = Column(Integer,ForeignKey("pedido.id"),nullable=False)
    produto_id = Column(Integer,ForeignKey("produto.id"),nullable=False)
    nome_produto = Column(String, nullable=False)
    preco = Column(Float,nullable=False)
    quantidade = Column(Integer,nullable=False)