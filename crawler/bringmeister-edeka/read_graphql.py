import json
import pandas as pd
simplified_list = []
for j in [0,1]:
    with open(f"while_graphql_response{j}.txt", "r", encoding="utf-8") as file:
        file_content = file.read()

    j = json.loads(file_content)
    data = j.get("data")
    products = data["products"]["edges"]
    for i in products:
        # print(i['node'].keys())
        data = (i['node'])
        simplified_data = {
            'productId': data['productId'],
            'name': data['name'],
            'categories': data['rootCategory']['name'],
            'price': data['prices']['price']
        }
        simplified_list.append(simplified_data)
    print(len(simplified_list))
df = pd.DataFrame(simplified_list)
df.set_index(df.columns[0],inplace=True)
print(df.head())
df.to_csv("simplified_data.csv")
    # print(simplified_data)
    # k = json.dumps(simplified_data,indent=3)
    # with open(f"simplified_bringmeister_product_example.json", "w", encoding="utf-8") as file:
    #     file.write(k)
    # break
# print(data["data"]["products"]["edges"][-1]["cursor"])
# print(len(json["data"]["products"]["edges"]))