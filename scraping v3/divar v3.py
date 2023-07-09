import requests
import json

url = "https://api.divar.ir/v8/web-search/tehran?goods-business-type=all&q=iphone%2013"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
# data = json.loads(response.text)
# print(data)



data = json.loads(response.text)
with open("output.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
print("JSON data saved to output.json")



# content = response.content.decode("utf-8")
# with open("output.txt", "w", encoding="utf-8") as file:
#     file.write(content)
# print("done")
# out_file = open("myfile.json", "w")
  
# json.dump(response.content, out_file, indent = 2)
  
# out_file.close()
# print(response.text)
# serch_res = json.dump