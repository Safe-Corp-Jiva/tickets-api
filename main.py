# Fast API API for Safe Corp Jiva with PostgreSQL database
# Rodrigo Nunez, Apr 2024
from pydantic import BaseModel
from fastapi import FastAPI
from sqlalchemy import MetaData
from databases import Database
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse

DATABASE_URL = "postgres://tickets_2b4c_user:keoKLVv5kduVrJx3vQRjOKdesn3KImYA@dpg-cokqe320si5c73dvgi20-a.oregon-postgres.render.com/tickets_2b4c"

database = Database(DATABASE_URL)
metadata = MetaData()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()
 
app = FastAPI(lifespan=lifespan)

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>SCJ Tickets API</title>
        </head>
        <body>
            <h1>Welcome to the tickets API for Safe Corp Jiva's Amazon Connect Supervisor Insights project</h1>
            <p>To GET all tickets in the database, go to <code>/tickets</code>.</p>
            <p>To POST a new ticket, go to <code>/tickets</code>.</p>
            <p>A ticket has the following fields: <code>title</code>, <code>description</code>, and <code>priority</code>.</p>
            <p>The title and description are strings, and the priority is an integer.</p>
        </body>
    </html>
"""

class Ticket(BaseModel):
    title: str
    description: str
    priority: int

@app.get("/tickets")
async def return_all_tickets():
    query = "SELECT * FROM tickets"
    result = await database.fetch_all(query)
    return result

@app.post("/tickets")
async def create_sample_ticket(ticket: Ticket):
    query = "INSERT INTO tickets (title, description, priority) VALUES (:title, :description, :priority)"
    await database.execute(query, values={"title": ticket.title, "description": ticket.description, "priority": ticket.priority})
    return {"title": ticket.title, "description": ticket.description, "priority": ticket.priority}
























# Sample code from fastapi get started tutorial
# 
# 
# 
# from typing import Union
# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}