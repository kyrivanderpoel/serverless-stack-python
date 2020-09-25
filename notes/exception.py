from flask import jsonify
from werkzeug.exceptions import InternalServerError
import attr


@attr.s
class NotFoundInDB(Exception):
    message = attr.ib()
    query = attr.ib()
    status_code = attr.ib(default=400)

    def to_dict(self):
        return dict(
            message=self.message,
            query=self.query,
            status_code=self.status_code,
        )

@attr.s
class MissingArgument(Exception):
    message = attr.ib()
    missing_arguments = attr.ib()
    status_code = attr.ib(default=400)

    def to_dict(self):
        return dict(
            message=self.message,
            missing_arguments=self.missing_arguments,
            status_code=self.status_code,
        )

def handle_not_found_in_db(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def handle_missing_argument(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def handle_500(error):
    response = jsonify(error)
    response.status_code = error.status_code
    return response

def validate_arguments(**kwargs):
    missing_arguments = [k for k,v in kwargs.items() if not v]
    if missing_arguments:
        raise MissingArgument(message="Missing required arguments", missing_arguments=missing_arguments)


# Register error handlers here. These will be registered on the application in app.py.
ERROR_HANDLERS = {
    # The default handler for any error not caught by a specific handler
    InternalServerError: handle_500,
    MissingArgument: handle_missing_argument,
    NotFoundInDB: handle_not_found_in_db,
}
