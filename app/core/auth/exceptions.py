from fastapi import HTTPException, status


class TooLargeTokenExpiryException(Exception):
    def __init__(self, expiry, max_expiry):
        super().__init__(
            f"Token expiry is too large. Max is {max_expiry}, received {expiry}"
        )


class BaseTokenException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        error_code: str = None,
        message: str = "",
    ):
        self.error_code = error_code
        self.message = message
        super().__init__(
            status_code=status_code,
            detail={"error_code": error_code, "message": message},
        )

    def __str__(self):
        return str({"error_code": self.error_code, "message": self.message})


class TokenExceptionByErrorCode(BaseTokenException):
    # TODO: Replace with actual error code
    def __init__(self, error_code: str):
        config = error_code.get_config()
        super().__init__(
            status_code=config.status_code,
            error_code=error_code,
            message=config.display_msg,
        )
