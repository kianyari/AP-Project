import requests
import json

url = "https://api.digikala.com/v1/search/?q=ایفون%2013&seo_url=&page=1"

payload = {}
headers = {'Cookie': 'TS01c77ebf=0102310591b0544921e66e6ad4f4ac7402dc892d9c2d4a7e8b3861c9a7cf5644ae54594d02fb3a4d3617e861f52950ce2b7d6151b93fd453f32fe70157aaf76e93dd129ebfaaf1e163ce12a8a43e417deaab477415; tracker_glob_new=efd1e1P; tracker_session=7teOUB1'}

response = requests.request("GET", url, headers=headers, data=payload)
# data = json.loads(response.text)
# print(data)



data = json.loads(response.text)
with open("output digikala.json", "w", encoding="utf-8") as file:
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