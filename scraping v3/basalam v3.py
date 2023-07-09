import requests
import json

url = "https://search.basalam.com/ai-engine/api/v2.0/product/search?productAds=true&adsImpressionDisable=false&q=%D9%85%D8%A7%D8%B4%DB%8C%D9%86%20%D8%A7%D8%B5%D9%84%D8%A7&literal=false&from=0&size=48&facets=namedTags,categories,prices,essences,provinces&filters.hasDiscount=false&filters.isReady=false&filters.isExists=true&filters.hasDelivery=false&filters.vendorScore=false&filters.hasVideo=false&filters.queryNamedTags=false&operators=or"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

# with open("output basalam.json", "w") as file:
#     json.dump(data, file, ensure_ascii=False, indent=4)
# print("JSON data saved to output.json")

# result = json.dumps(result.json())
# result = json.loads(result)

# with open("output basalam.json", 'w', encoding="utf-8") as file:
#     json.dump(result.json(), file, indent=4)


data = json.loads(response.text)
with open("output basalam.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
print("JSON data saved to output.json")

# print(result)

# print(response.text)