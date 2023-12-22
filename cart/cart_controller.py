from flask import jsonify, request
from flask_restful import Resource
from models.ShoppingItem import ShoppingItem
from models.ShoppingList import ShoppingList

'''
Shopping List Management Endpoints
'''

'''
A Endpoint to create a new Shopping List
TODO add status codes as response

@:param: item1 (json)   : First item of the shopping list (send as json)
@:param: item2 (json)   : Second item of the shopping list (send as json)
@:param: item3 (json)   : Third item of the shopping list (send as json) 
@:param: status (string)    : Current status of the shopping list (e.g open, closed)
@:param: created_by (integer)  : creator of the shopping list
@:param: allow_multiple_shoppers (boolean)  : Allow multiple shoppers to participate in finishing the list

@:return 201 : TODO
'''


class CreateShoppingList(Resource):
    def post(self):
        status = 400
        required_params = {"item1", "item2", "item3", "status", "created_by", "allow_multiple_shoppers"}
        request_data = request.get_json()

        if (request_data is not None):
            items = getShoppingItems(request_data)
            status = request_data.get("status")
            created_by = request_data.get("created_by")
            allow_multiple_shoppers = request_data.get("allow_multiple_shoppers")

            item_ids = {
                "item1": None,
                "item2": None,
                "item3": None
            }

            # Create single shopping items
            for item in items.keys():
                new_shopping_item = ShoppingItem(
                    product=request_data[item]["product"],
                    count=request_data[item]["count"],
                    shopper=request_data[item]["shopper"],
                    status=request_data[item]["status"]
                )
                session.add(new_shopping_item)
                session.commit()
                item_ids[item] = new_shopping_item.id

            # Create shopping list
            new_shopping_list = ShoppingList(
                item1=item_ids["item1"],
                item2=item_ids["item2"],
                item3=item_ids["item3"],
                status=status,
                created_by=created_by,
                allow_multiple_shoppers=allow_multiple_shoppers
            )

            session.add(new_shopping_list)
            session.commit()
            status = 201
        else:
            status = 409

        return jsonify({
            "status": status
        })


'''
A Class to change Shopping List´s Status
Data is given using post Method
it checks if all the parameters exist and request is not empty
then changes the status of Shopping List

@:param: id (integer)     : id of the Shopping List
@:param: status (string)  : new status of the Shopping List (open, closed)

@:return 200 : if Status Changed Successfully 
@:return 404 : if Shopping List does not exist
@:return 400 : if data is not in a correct form or has missing parameters
'''


class ChangeShoppingListStatus(Resource):
    def post(self):
        request_data = request.get_json()
        required_params = {"id", "status"}
        status = 400
        if (request_data is not None and validateParameters(request_data, required_params, request_data.keys(),
                                                            required_params)):
            shoppinglist_id = request_data.get("id")
            new_status = request_data.get("status")
            if (shopping_list_exists(shoppinglist_id)):
                shoppinglist = session.query(ShoppingList).filter((ShoppingList.id == shoppinglist_id))
                shoppinglist.status = new_status
                status = 200
                session.commit()
                session.close()

            else:
                status = 404

        return jsonify({
            "status": status
        })


'''
A Class to change Shopping Item´s Status

@:param: id (integer)     : id of the Shopping List
@:param: status (string)  : new status of the Shopping Item (open, shopping, closed)

@:return 200 : if Status Changed Successfully 
@:return 404 : if Shopping Item does not exist
@:return 400 : if data is not in a correct form or has missing parameters
'''


class ChangeShoppingItemStatus(Resource):
    def post(self):
        request_data = request.get_json()
        required_params = {"id", "status"}
        status = 400
        if (request_data is not None and validateParameters(request_data, required_params, request_data.keys(),
                                                            required_params)):
            shoppingitem_id = request_data.get("id")
            new_status = request_data.get("status")
            if (shopping_item_exists(shoppingitem_id)):
                shoppingitem = session.query(ShoppingItem).filter(ShoppingItem.id == shoppingitem_id)
                shoppingitem.status = new_status
                status = 200
                session.commit()
                session.close()
            else:
                status = 404

        return jsonify({
            "status": status
        })
