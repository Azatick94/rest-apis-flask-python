from flask import Flask, request, Response

app = Flask(__name__)


class Item:
    def __init__(self, name: str, price: float, amount: int):
        self.name = name
        self.price = price
        self.amount = amount

    def to_json(self):
        return {
            'name': self.name,
            'price': self.price,
            'amount': self.amount
        }


class Store:

    def __init__(self, store_name):
        self.__items: list[Item] = []
        self.store_name = store_name

    def add_item(self, item: Item):
        self.__items.append(Item(item.name, item.price, item.amount))

    def to_json(self):
        items_json = [item.to_json() for item in self.__items]
        return {
            'store_name': self.store_name,
            'items': items_json
        }


item1 = Item('item1', 100, 1)
item2 = Item('item2', 200, 2)
item3 = Item('item3', 300, 3)
item4 = Item('item4', 300, 3)
item5 = Item('item5', 300, 3)

store1 = Store('mystore')
store1.add_item(item1)
store1.add_item(item2)
store1.add_item(item3)

store2 = Store('mystore2')
store2.add_item(item2)
store2.add_item(item4)
store2.add_item(item5)

stores = [store1, store2]


@app.get("/stores")
def get_stores():
    return {"stores": [x.to_json() for x in stores]}


@app.get("/stores/<string:store_name>")
def get_items_from_store(store_name):
    for store in stores:
        if store.store_name == store_name:
            return store.to_json(), 200
    return {'message': "Store not found"}, 404


@app.post("/stores/")
def create_new_store():
    request_data = request.get_json()

    name = request_data['name']
    new_store = Store(name)
    stores.append(new_store)
    return Response(status=201)


if __name__ == '__main__':
    app.run(debug=True)
