from fastapi import FastAPI
from database import Base, engine
from routers import clientes_router, pedidos_router, produtos_router

Base.metadata.create_all(bind=engine)
app = FastAPI(title="API do Restaurante")

app.include_router(clientes_router)
app.include_router(pedidos_router)
app.include_router(produtos_router)