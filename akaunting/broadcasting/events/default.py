import secrets


def default_webhook_secret():
    return secrets.token_hex(32)
