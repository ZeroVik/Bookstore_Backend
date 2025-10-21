from fastapi import FastAPI
from app.routes import users, books, ai, uploads, categories, admin_users
from app.database import Base, engine
from fastapi.staticfiles import StaticFiles
from app.routes import admin_products
import os


app = FastAPI(title="Bookstore Backend")
# Serve uploaded files (public/)
if not os.path.exists("public/uploads/books"):
    os.makedirs("public/uploads/books")

app.mount("/public", StaticFiles(directory="public"), name="public")

app.include_router(users.router)
app.include_router(books.router)
app.include_router(ai.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(ai.router)
app.include_router(uploads.router)
app.include_router(categories.router)
app.include_router(admin_users.router)
app.include_router(admin_products.router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
