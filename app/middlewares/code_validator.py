from flask import request, abort, current_app
import re


def validate_code(func):
    def validation(*args, **kwargs):
        return func(*args, **kwargs)

    return validation
