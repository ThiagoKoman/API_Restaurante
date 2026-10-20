
clientes = []
produtos = []
pedidos = []


# ----- Clientes -----
def salvar_cliente(db: Session, cliente: ClienteModel) -> ClienteModel:
    db.add(cliente)         #Monta o insert no DB
    db.commit()             #Executa a query no DB
    db.refresh(cliente)     #Busca o id gerado no DB
    return cliente

def listar_clientes() -> list:
    return clientes


def buscar_cliente(cliente_id: int):
    for cliente in clientes:
        if cliente["id"] == cliente_id:
            return cliente
    return None


# ----- Produtos -----
def salvar_produto(produto: dict) -> dict:
    produto["id"] = len(produtos) + 1
    produtos.append(produto)
    return produto


def listar_produtos() -> list:
    return produtos


def buscar_produto(produto_id: int):
    for produto in produtos:
        if produto["id"] == produto_id:
            return produto
    return None


# ----- Pedidos -----
def salvar_pedido(pedido: dict) -> dict:
    pedido["id"] = len(pedidos) + 1
    pedidos.append(pedido)
    return pedido


def buscar_pedido(pedido_id: int):
    for pedido in pedidos:
        if pedido["id"] == pedido_id:
            return pedido
    return None