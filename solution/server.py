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
        self.order_type = order_type
        self.client = client
        self.status = status
        self.payment = payment
    
        
        

class Fisico(Orden):
    def __init__(self,client,status,payment,shipping,products):
        self.shipping = shipping
        self.products = products
        super().__init__("Física",client,status,payment)
class Digital(Orden):
    def __init__(self,client,status,payment,code,expiration):
        self.code = code
        self.expiration = expiration
        super().__init__("Digital",client,status,payment)
        



class OrdenFactory():
    @staticmethod
    def crearOrden(order_type,client,status,payment,shipping,products,code,expiration):
        if order_type == "Física":
            return Fisico(client,status,payment,shipping,products)
        elif order_type == "Digital":
            return Digital(client,status,payment,code,expiration)
        else:
            return "Tipo de orden no valido"

class OrdenService():
    def __init__(self):
        self.factory = OrdenFactory()
    
    def readOrdenes(self):
        return {id: orden.__dict__ for id, orden in ordenes.keys()}
    
    def createOrden(self,data):
        order_type = data.get("order_type",None)
        client = data.get("client",None)
        status = data.get("status",None)
        payment = data.get("payment",None)
        shipping = data.get("shipping",None)
        products = data.get("products",None)
        code = data.get("code",None)
        expiration = data.get("expiration",None)

        if order_type == "Física":
            orden = self.factory.crearOrden(order_type,client,status,payment,shipping,products, code =None, expiration=None)
        elif order_type == "Digital":
            orden = self.factory.crearOrden(order_type,client,status,payment,code,expiration,shipping=None,products=None )
 
 
        if ordenes:
            new_id = max(ordenes.keys())+1
        else:
            new_id = 1
        ordenes[new_id]=orden
        if orden:
            return orden.__dict__
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
        else:
            HTTPDataHandler.handle_response(self,404,{"error":"Ruta no existente"})
    def do_POST(self):
        if self.path == "/orders":
            data = HTTPDataHandler.handle_reader(self)
            post_data = self.controller.createOrden(data)
            HTTPDataHandler.handle_response(self,201,post_data)
        else:
            HTTPDataHandler.handle_response(self,404,{"error":"Ruta no existente"})
            
def run(server_class=HTTPServer, handler_class =OrdenDataHandler,port =8000):
    server_address=("",port)
    httpd = server_class(server_address, handler_class)
    print("Iniciando server web")
    httpd.serve_forever()
    
if __name__=="__main__":
    run()