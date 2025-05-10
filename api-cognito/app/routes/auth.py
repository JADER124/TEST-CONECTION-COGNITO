from flask_restx import Api, Resource, Namespace, fields
from flask import request,make_response,render_template
import boto3
import hmac
import hashlib
import base64

auth_ns = Namespace('Auth', description='Apis para la autenticacion con cognito y google',path="/api/auth/")

auth_model = auth_ns.model("Auth", {
    "Usuario" : fields.String(required=True, description="User"),
    "Password": fields.String(required=True, description="Password")

})

# Configuración base 
COGNITO_CLIENT_ID = "5rlup4jm31f1nfjg27jephpjr1"
COGNITO_USER_POOL_ID = "us-east-1_DSlegZc6q"
REGION = "us-east-1"  
COGNITO_CLIENT_SECRET = "r65lru7g4hgenm0p2q6e7t7880pncb0qapne1u73i03128eruuh"  # copia tu client secret real aquí


client = boto3.client('cognito-idp', region_name = REGION)

def get_secret_hash(username, client_id, client_secret):
    message = username + client_id
    dig = hmac.new(
        client_secret.encode('utf-8'),
        msg=message.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode()

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(auth_model)
    def post(self):
        data = request.get_json()
        username = data.get("Usuario")
        password = data.get("Password")
        print(username)
        print(password)
        secret_hash = get_secret_hash(username, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET)
        try:
            response = client.initiate_auth(
                ClientId=COGNITO_CLIENT_ID,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password,
                    'SECRET_HASH': secret_hash
                }
            )
            return {
                "message": "Login exitoso",
                "tokens": response['AuthenticationResult']
            }, 200
        except client.exceptions.NotAuthorizedException:
            return {"error": "Credenciales incorrectas"}, 401
        except Exception as e:
            return {"error": str(e)}, 500

@auth_ns.route('/form')
class LoginFormView(Resource):
    def get(self):
        return make_response(render_template('login.html'), 200, {"Content-Type": "text/html"})