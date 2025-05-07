from flask_restx import Api, Resource, Namespace, fields
from flask import request  

frutas_ns = Namespace('frutas', description='Operaciones con frutas',path="/api/v1/")

frutas =["manzana", "banana", "naranja"]

fruta_model = frutas_ns.model("Fruta", {
    "nombre": fields.String(required=True, description="Nombre de la fruta")
})

@frutas_ns.route('/GetFrutas')
class GetFrutas(Resource):
    def get(self):
         return frutas
    


@frutas_ns.route('/agregar')
class GetFrutas(Resource):
    @frutas_ns.expect(fruta_model)
    def post(self):
        data = request.get_json()
        nombre = data.get('nombre')
        frutas.append(nombre)
        return {"mensaje": "Fruta agregada", "frutas": frutas}, 201
 