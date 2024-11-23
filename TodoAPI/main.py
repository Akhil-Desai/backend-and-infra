from fastapi import FastAPI

app = FastAPI()

# Define a route
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
