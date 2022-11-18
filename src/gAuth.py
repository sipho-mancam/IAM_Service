from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from utility import *
from googleapiclient.discovery import build


def google_authentication_url(scopes=['openid',
                                      "https://www.googleapis.com/auth/userinfo.profile",
                                      "https://www.googleapis.com/auth/userinfo.email"])->str:

    flow = Flow.from_client_secrets_file(
        DATA_DIR+'/creds.json',
        scopes=scopes
    )
    url_t = flow.authorization_url()

    return url_t[0]+'&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Fgoogle_auth%2F'


def google_fetch_access_code(code: str, scopes=['openid',
                                         "https://www.googleapis.com/auth/userinfo.profile",
                                         "https://www.googleapis.com/auth/userinfo.email"]) -> dict:
            
    flow = Flow.from_client_secrets_file(
        DATA_DIR+'/creds.json',
        scopes=scopes
    )

    flow.fetch_token(code=code)

    creds = flow.credentials
    return creds.to_json()


def google_user_data(creds)->dict:

    service = build('oauth2', 'v2', credentials=creds)

    user_info = service.userinfo().get().execute()

    return user_info

