from fastapi import FastAPI

app = FastAPI(title="GateFlow Downstream Service")


#This gives us two fake backend services conceptually

@app.get("/users")
def get_users():
    return {
        "service": "User Service",
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]
    }


@app.get("/orders")
def get_orders():
    return {
        "service": "Order Service",
        "orders": [
            {"id": 101, "status": "processing"},
            {"id": 102, "status": "completed"}
        ]
    }