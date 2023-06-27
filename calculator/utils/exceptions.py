class BaseCustomException(Exception):

    status_code = None
    developer_message = None
    user_message = "Some error occurred. Please try again later."
    is_an_error_response = True

    def __init__(
        self,
        developer_message: str = None,
        user_message: str = None,
    ):
        super(BaseCustomException, self).__init__(
            developer_message if developer_message else self.developer_message
        )
        if developer_message:
            self.developer_message = developer_message

        if user_message:
            self.user_message = user_message

    def to_dict(self):
        if not self.developer_message:
            self.developer_message = self.__class__.__name__

        return {
            "status": self.status_code,
            "developer_message": self.developer_message,
            "user_message": self.user_message,
        }



class NotFound(BaseCustomException):
    """
    Should be thrown whenever there is a bad API call that doesn't fit a more
    specific error message.
    """
    status_code = 404
    user_message = "The record that you are searching for do not exist"

class BadRequest(BaseCustomException):
    """
    Should be thrown whenever an object was not found
    specific error message.
    """
    status_code = 400
    user_message = "Invalid payload, please check the API doc and try again"


class Unauthorized(BaseCustomException):
    """
    The class represents an exception for unauthorized access with a status code of 401 and a user
    message.
    """
    status_code = 401
    user_message = "The user doesn't have the credentials to access the api"



class OutOfMoney(BaseCustomException):
    """
    The class defines a custom exception for when a user doesn't have enough money in their account to
    perform an operation.
    """
    status_code = 402
    user_message = "The user doesn't have enough money in their account to perform the operation"
