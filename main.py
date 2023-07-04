from fastapi import FastAPI, HTTPException, Query
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

data = json.load(open('data.json'))
tickets = {ticket["id"]: ticket for ticket in data}
@app.get("/")
async def root():
    return {"message": "Hello World2"}

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str):
    if ticket_id in tickets:
        return tickets[ticket_id]
    else:
        return {"error": "Ticket not found"}
    

@app.get("/search")
def search_tickets(
    ticket_id: str = Query(None, title="ID"),
    title: str = Query(None, title="Title"),
    content: str = Query(None, title="Content"),
    email: str = Query(None, title="Email"),
    created_from: int = Query(None, title="Created From"),
    created_to: int = Query(None, title="Created To"),
    labels: List[str] = Query(None, title="Labels"),
):
    # Filter the tickets based on the provided parameters
    results = []
    for ticket in data:
        if (
            (title is None or title.lower() in ticket["title"].lower())
            and (ticket_id is None or ticket_id.lower() in ticket["id"].lower())
            and (content is None or content.lower() in ticket["content"].lower())
            and (email is None or email.lower() in ticket["userEmail"].lower())
            and (created_from is None or ticket["creationTime"] >= created_from)
            and (created_to is None or ticket["creationTime"] <= created_to)
            and (labels is None or ("labels" in ticket and all(label in ticket["labels"] for label in labels)))
        ):
            results.append(ticket)

    if not results:
        raise HTTPException(status_code=404, detail="No tickets found.")

    return results


@app.get("/user_search")
def user_search():
    # Load the HTML file
    with open("static/index.html") as file:
        html_content = file.read()

    return HTMLResponse(content=html_content, status_code=200)