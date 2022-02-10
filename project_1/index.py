# this is our root file, when we execute this we will start our app
# webpage for fastapi framework https://fastapi.tiangolo.com/tutorial/,
# also https://realpython.com/fastapi-python-web-apis/

# uvicorn index:app --reload --port 7777
# uvicorn is the server which will start
# index:app, index -> the file name, app -> the FastAPI object name
# --reload -> the server will restart when we modify the code
# --port <port_number> -> select on which port to start


from fastapi import FastAPI
from stock import Stock
from stock_repo import StockRepository

app = FastAPI(
    title="Name of our app",  # TODO for homework, name your application
    # <major_version>.<minor_version>.<patch_version>
    version="0.2.0",  # increase version after finishing homework
    description="",  # TODO add a description
)


@app.get(
    "/health",
    summary="This will be visible at start",
    description="We can describe this API call",
    response_description="We can describe the response",
)
def health() -> dict:
    return {
        "status": "online",
        "engine": "on",
    }


stock_repo = StockRepository()


@app.post("/stocks")
def add_new_stock(stock_info: dict):
    new_stock = Stock(stock_info["ticker"], stock_info["company"], stock_info["field"])
    stock_repo.add(new_stock)


# TODO return your domain items
# example if you want to do a tasks app return the list of tasks, and rename the url /items -> /tasks
@app.get("/stocks")
def get_stocks():
    stocks = stock_repo.get_all()
    return [s.to_json() for s in stocks]


# TODO add a put method to edit your domain item
# TODO add a delete method to remove a domain item from the list
# these methods should also save the data into a file for persistence across server reboots


@app.delete("/stocks")
def remove_stock(ticker: str):
    stock_repo.remove(ticker)


@app.on_event("startup")
def load_list_of_items():
    stock_repo.load()

