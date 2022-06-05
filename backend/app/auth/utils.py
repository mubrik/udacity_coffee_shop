import json
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from os import environ as env
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
from app import app

# loadenv .env
load_dotenv()
# get env variables
AUTH0_DOMAIN = env.get("AUTH0_DOMAIN")
API_AUDIENCE = env.get("API_AUDIENCE")
CLIENT_ID=env.get("AUTH0_CLIENT_ID")
CLIENT_SECRET=env.get("AUTH0_CLIENT_SECRET")
ALGORITHMS = env.get("ALGORITHMS", ['RS256'])


class AuthError(Exception):
  '''
    AuthError Exception
    A standardized way to communicate auth failure modes
  '''
  def __init__(self, code=401, error='Unauthorized', description='Unable to authenticate.'):
    self.code = code
    self.error = error
    self.description = description


def get_token_auth_header():
  '''
    gets the token from the header
  '''
  if 'Authorization' not in request.headers:
    raise AuthError(description='Authorization header is expected.')
  # get Auth header  
  auth_header = request.headers['Authorization']
  # split header
  split_auth_header = auth_header.split(' ')
  # checks validity of header
  if len(split_auth_header) != 2:
    raise AuthError(description='Invalid authorization header.')
  elif split_auth_header[0] != 'Bearer':
    raise AuthError(description='Invalid bearer header.')
  return split_auth_header[1]


def verify_decode_jwt(token: str):
  """
    checks Access Token for validity
    Args:
      token (str): The token string to be verified
  """
  # get public key
  jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
  jwks = json.loads(jsonurl.read())
  # get unverified header
  unverified_header = jwt.get_unverified_header(token)
  # get rsa key from jwks & unverified header
  rsa_key = {}
  for key in jwks["keys"]:
    if key["kid"] == unverified_header["kid"]:
      rsa_key = {
        "kty": key["kty"],
        "kid": key["kid"],
        "use": key["use"],
        "n": key["n"],
        "e": key["e"]
      }
  # decode token using rsa_key
  if rsa_key:
    try:
      payload = jwt.decode(
        token,
        rsa_key,
        algorithms=ALGORITHMS,
        audience=API_AUDIENCE,
        issuer="https://"+AUTH0_DOMAIN+"/"
      )
    except jwt.ExpiredSignatureError:
      raise AuthError(description='Expired Token', error='token_expired')
    except jwt.JWTClaimsError:
      raise AuthError(description='incorrect claims, please check the audience and issuer',
        error='invalid_claims')
    except Exception:
      raise AuthError(description='Authentication token parse error',
        error='invalid_header')
    return payload
  raise AuthError(description='Unable to find RSA key', error='invalid_header')
  

def check_permissions(required_perm, payload):
  """
    Determines if the required scope is present in the Access Token
    Args:
      required_perm (str): The required permission to access the resource
  """
  if payload.get("permissions"):
    token_permissions = payload["permissions"]
    for token_perm in token_permissions:
      if token_perm == required_perm:
        return True
  raise AuthError(description='You are not authorized to access this resource.')


def requires_authentication(func):
  '''
    requires auth, user has to be authenticated
  '''
  def wrapper(*args, **kwargs):
    token = get_token_auth_header()
    # no need for result checks, error raise in function
    verify_decode_jwt(token)
    return func(*args, **kwargs)
  return wrapper


def requires_authorization(permission=''):
  '''
    requires auth, user has to be authenticated and has to have the permission
    Args:
      permission (str): The required permission to access the resource
  '''
  def requires_auth_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      token = get_token_auth_header()
      payload = verify_decode_jwt(token)
      print(payload)
      check_permissions(permission, payload)
      return func(*args, **kwargs)
    return wrapper
  return requires_auth_decorator

# oauth instance
oauth = OAuth(app)

oauth.register(
  "coffee_auth",
  client_id=CLIENT_ID,
  client_secret=CLIENT_SECRET,
  client_kwargs={
    "scope": "openid profile email",
  },
  server_metadata_url=f'https://{AUTH0_DOMAIN}/.well-known/openid-configuration'
)

# oauth implementation later