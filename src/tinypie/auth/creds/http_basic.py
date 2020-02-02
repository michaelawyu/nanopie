class HTTPBasicUserCredential():
    """
    """
    __slots__ = ('user_id', 'password')

    def __init__(self,
                 user_id: str,
                 password: str):
        """
        """
        self.user_id = user_id
        self.password = password
