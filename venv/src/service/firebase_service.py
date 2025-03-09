from firebase_admin import auth
import requests
from flask import current_app


def get_request_auth_token(request):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise ValueError("Token not provided or invalid")

        token = auth_header.split(" ")[1]
        decoded_token = auth.verify_id_token(token)
        return decoded_token["uid"]
    except Exception as e:
        raise ValueError(f"Error verifying the token: {e}")


def authenticate_user(email, password):
    try:
        FIREBASE_AUTH_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={current_app.firebase_api_key}"
        response = requests.post(
            FIREBASE_AUTH_URL,
            json={"email": email, "password": password, "returnSecureToken": True},
        )

        response_data = response.json()
        if "error" in response_data:
            raise ValueError(response_data["error"]["message"])

        id_token = response_data.get("idToken")
        user = auth.get_user_by_email(email)

        return {"idToken": id_token, "uid": user.uid}
    except Exception as e:
        raise ValueError(f"Error authenticating the user: {e}")


def register_user(name, email, password):
    try:
        FIREBASE_AUTH_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={current_app.firebase_api_key}"
        response = requests.post(
            FIREBASE_AUTH_URL,
            json={"email": email, "password": password, "returnSecureToken": True},
        )

        response_data = response.json()
        if "error" in response_data:
            raise ValueError(response_data["error"]["message"])

        id_token = response_data.get("idToken")

        user = auth.get_user_by_email(email)
        auth.update_user(user.uid, display_name=name)

        # Retorna o token e o UID
        return {"idToken": id_token, "uid": user.uid}
    except Exception as e:
        raise ValueError(f"Error registering the user: {e}")


def logoff_user(user_id):
    try:
        auth.revoke_refresh_tokens(user_id)
    except Exception as e:
        raise ValueError(f"Error revoking user tokens: {e}")
