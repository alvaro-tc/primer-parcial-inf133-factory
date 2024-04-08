import requests
url="http://localhost:8000/orders"
headers= {"Content-Type":"application/json"}


data ={
    "client":"Juan Perez",
    "status":"Pendiente",
    "payment":"Tarjeta de Credito",
    "shipping": 10.0,
    "products": ["Camiseta","Pantalon","Zapatos"],
    "order_type":"Fisica"
}

response = requests.post(url=url,json=data,headers=headers)
print("Mostrar primer post: ",response.text)


data ={
    "client":"Maria Rodriguez",
    "status":"Pendiente",
    "payment":"PayPal",
    "code": "ABC123",
    "expiration": "2022-12-31",
    "order_type":"Digital"
}

response = requests.post(url=url,json=data,headers=headers)
print("Mostrar segundo post: ",response.text)

response = requests.get(url)
print("Mostrar GET: ",response.text)

response = requests.get(url+"/?status=Pendiente")
print("Mostrar GET por status: ",response.text)

data2 ={
    "client":"Juan Perez",
    "status":"En Proceso",
    "payment":"Tarjeta de Credito",
    "shipping": 10.0,
    "products": ["Camiseta"],
    "order_type":"Fisica"
}

response = requests.put(url=url+"/1",json=data2,headers=headers)
print ("Mostrar PUT: ",response.text)

response = requests.delete(url=url+"/1",json=data2,headers=headers)
print ("Mostrar DELETE: ",response.text)

data3 ={
    "client":"Ana Gutierrez",
    "status":"Pendiente",
    "payment":"Tarjeta de Debito",
    "shipping": 20.0,
    "products": ["Licuadora","Refrigeradora","Lavadora"],
    "order_type":"Fisica"
}

response = requests.post(url=url,json=data3,headers=headers)
print("Mostrar tercer post: ",response.text)

response = requests.get(url)
print("Mostrar GET: ",response.text)
