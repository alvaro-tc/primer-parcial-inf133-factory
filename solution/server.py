from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json 

ordenes = {}


class HTTPDataHandler():
    @staticmethod
    def handle_response(handler,status,data):
        handler.send_response(status)
        handler.send_header("Content-type","application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    
    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        data = handler.rfile.read(content_length)
        return json.loads(data.decode("utf-8"))
    
class Orden():
    def __init__(self,order_type,client,status,payment):
        self.client = client
        self.status = status
        self.payment = payment
        self.order_type = order_type   

        
        
        

class Fisico(Orden):
    def __init__(self,client,status,payment,shipping,products):
        super().__init__("Fisica",client,status,payment)
        self.shipping = shipping
        self.products = products

    
class Digital(Orden):
    def __init__(self,client,status,payment,code,expiration):
        super().__init__("Digital",client,status,payment)
        self.code = code
        self.expiration = expiration
        



class OrdenFactory():
    @staticmethod
    def crearOrden(order_type,client,status,payment,shipping,products,code,expiration):
        if order_type == "Fisica":
            return Fisico(client,status,payment,shipping,products)
        elif order_type == "Digital":
            return Digital(client,status,payment,code,expiration)
        else:
            return "Tipo de orden no valido"

class OrdenService():
    def __init__(self):
        self.factory = OrdenFactory()
    
    def readOrdenes(self):
        d_Ordenes= {}
        for id in ordenes:
            orden = ordenes[id]
            d_Ordenes[id]=orden.__dict__
        return d_Ordenes
    def searchStatus(self, query_params):
        d_Ordenes= {}
        if "status" in query_params:
            status = query_params["status"][0]
            for id in ordenes:
                orden = ordenes[id]
                if orden.status == status:
                    d_Ordenes[id]=orden.__dict__
            
            if d_Ordenes :
                return d_Ordenes
            else:
                return {"message":"Status no existente"}
        else:
            return None
    
    def createOrden(self,data):
        order_type = data.get("order_type",None)
        client = data.get("client",None)
        status = data.get("status",None)
        payment = data.get("payment",None)
        shipping = data.get("shipping",None)
        products = data.get("products",None)
        code = data.get("code",None)
        expiration = data.get("expiration",None)

        if order_type == "Fisica":
            orden = self.factory.crearOrden(order_type,client,status,payment,shipping,products, code, expiration)
        elif order_type == "Digital":
            orden = self.factory.crearOrden(order_type,client,status,payment, shipping,products,code,expiration )
        else: 
            return {"message":"order_type no existente"}
 
        if ordenes:
            new_id = max(ordenes.keys())+1
        else:
            new_id = 1
        ordenes[new_id]=orden
        if orden:
            return orden.__dict__
        else:
            return None
        
    def putOrden(self,orden_id,data):
        client = data.get("client",None)
        status = data.get("status",None)
        payment = data.get("payment",None)
        shipping = data.get("shipping",None)
        products = data.get("products",None)
        code = data.get("code",None)
        expiration = data.get("expiration",None)
        if orden_id in ordenes:
            orden = ordenes[orden_id]
            if client:
                orden.client =client
            if status:
                orden.status =status
            if payment:
                orden.payment =payment
            if shipping:
                orden.shipping =shipping
            if products:
                orden.products =products
            if code:
                orden.code =code
            if expiration:
                orden.expiration =expiration
            return orden.__dict__
        else:
            return None
  
    def deleteOrden(self,orden_id):
        if orden_id in ordenes:
            orden = ordenes[orden_id]
            del ordenes[orden_id]
            return orden
        else:
            return None
            
        
                

        
    
        
class OrdenDataHandler(BaseHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        self.controller = OrdenService()
        super().__init__(*args,**kwargs)
    
    def do_GET(self):
        if self.path == "/orders":
            get_data = self.controller.readOrdenes()
            HTTPDataHandler.handle_response(self,200,get_data)
        elif self.path.startswith("/orders/"):
            parsed_url = urlparse(self.path)
            query_params= parse_qs(parsed_url.query)
            if query_params:
                data = self.controller.searchStatus(query_params)
                HTTPDataHandler.handle_response(self,200,data)
            else:
                HTTPDataHandler.handle_response(self,404,{"error":"Ruta no existente"})
        else:
            HTTPDataHandler.handle_response(self,404,{"error":"Ruta no existente"})
    def do_POST(self):
        if self.path == "/orders":
            data = HTTPDataHandler.handle_reader(self)
            post_data = self.controller.createOrden(data)
            HTTPDataHandler.handle_response(self,201,post_data)
        else:
            HTTPDataHandler.handle_response(self,404,{"error":"Ruta no existente"})
    def do_PUT(self):
        if self.path.startswith("/orders/"):
            orden_id = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            post_data = self.controller.putOrden(orden_id,data)
            if (post_data):
                HTTPDataHandler.handle_response(self,200,post_data)
            else:
                HTTPDataHandler.handle_response(self,404,{"message":"Orden no existente"})
        else:
            HTTPDataHandler.handle_response(self,404,{"error":"Ruta no existente"})
    def do_DELETE(self):
        if self.path.startswith("/orders/"):
            orden_id = int(self.path.split("/")[-1])
            post_data = self.controller.deleteOrden(orden_id)
            if (post_data):
                HTTPDataHandler.handle_response(self,200,{"message":"Orden eliminada"})
            else:
                HTTPDataHandler.handle_response(self,404,{"message":"Orden no existente"})
        else:
            HTTPDataHandler.handle_response(self,404,{"error":"Ruta no existente"})
            
def run(server_class=HTTPServer, handler_class =OrdenDataHandler,port =8000):
    try:
        server_address=("",port)
        httpd = server_class(server_address, handler_class)
        print("Iniciando server web en http://localhost:8000")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando Servidor Web")
    
if __name__=="__main__":
    run()