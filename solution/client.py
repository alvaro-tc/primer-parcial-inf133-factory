import requests
url="http://localhost:8000/orders"
headers= {"Content-Type":"application/json"}


response = requests.get(url)
print("Mostrar GET: ",response.text)


data ={
    "client":"Juan Perez",
    "status":"Pendiente",
    "payment":"Tarjeta de Credito",
    "shipping": 10.0,
    "products": ["Camiseta","Pantalon","Zapatos"],
    "order_type":"Física"
}

response = requests.post(url=url,json=data,headers=headers)
print("Mostrar POST: ",response.text)

response = requests.get(url)
print("Mostrar GET: ",response.text)
