from fastapi import FastAPI
import json 
app = FastAPI()

data = json.load(open('data.json'))
@app.get("/")
async def root():
    return {"message": "Hello World2"}
tickets = {ticket["id"]: ticket for ticket in data}

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str):
    if ticket_id in tickets:
        return tickets[ticket_id]
    else:
        return {"error": "Ticket not found"}