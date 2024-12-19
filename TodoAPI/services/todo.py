def verifyToken(auth_token: str) -> bool:
    token = auth_token.split('#')
    return token[0] == "TestToken123"
