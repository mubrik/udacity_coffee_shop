import json
from typing import List
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import urllib
from os import environ as env
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
from app import app
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

# loadenv .env
load_dotenv()

# get env variables
AUTH0_DOMAIN = env.get("AUTH0_DOMAIN")
API_AUDIENCE = env.get("API_AUDIENCE")
CLIENT_ID=env.get("AUTH0_CLIENT_ID")
CLIENT_SECRET=env.get("AUTH0_CLIENT_SECRET")
ALGORITHMS = env.get("ALGORITHMS", ['RS256'])

# create a new instance of the Auth0 GetToken class
get_token = GetToken(AUTH0_DOMAIN)
token = get_token.client_credentials(CLIENT_ID,
  CLIENT_SECRET, 'https://{}/api/v2/'.format(AUTH0_DOMAIN))
# get management api token
mgmt_api_token = token['access_token']
# create a new instance of the Auth0 Management API client
auth_management = Auth0(AUTH0_DOMAIN, mgmt_api_token)

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
  try:
    jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
  except urllib.error.URLError:
    raise AuthError(description='Unable to reach Auth server, try again later.')
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
  raise AuthError(description='Unable to find RSA key', error='invalid_header', code=403)
  

def check_permissions(required_perm: str|List[str], payload):
  """
    Determines if the required scope is present in the Access Token
    Args:
      required_perm (str): The required permission to access the resource
  """
  if payload.get("permissions"):
    # get perm
    token_permissions = payload["permissions"]
    # loop through permissions
    for token_perm in token_permissions:
      # compare permissions
      if type(required_perm) is str:
        if token_perm == required_perm:
          return True
      elif type(required_perm) is list:
        if token_perm in required_perm:
          return True
    raise AuthError(description='Permission not found', error='invalid_claims')
  raise AuthError(description='You are not authorized to access this resource.')

# decorators
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
      check_permissions(permission, payload)
      return func(permission, *args, **kwargs)
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