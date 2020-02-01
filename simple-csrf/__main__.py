import config
import sys
from werkzeug.security import generate_password_hash, check_password_hash
from argparse import ArgumentParser


def create_csrf_token(client_key, server_key=config.SECRET_CSRF_KEY):
    token = generate_password_hash(client_key + server_key,
                                   method='pbkdf2:sha256:10000',
                                   salt_length=8)
    return token


def verify_csrf_token(client_key, csrf_token, server_key=config.SECRET_CSRF_KEY):
    return check_password_hash(csrf_token,
                               client_key + server_key)


def html_input(client_key, elem_name=config.HTML_ELEM_NAME):
    return '<input type="hidden" value="%s" name="%s"' % (client_key,
                                                          elem_name)


if __name__ == '__main__':
    parser = ArgumentParser(description='Simple CSRF tokens')

    parser.add_argument('--client_key', type=str,
                        help='The client CSRF key. ' +
                             'This, combined with the server ' +
                             'key and hashed, creates the final ' +
                             'csrf token included in html input.')

    parser.add_argument('--token-only', help='Only return the final token ' +
                                             'wihtout the html input.')

    parser.add_argument('create', type=str, nargs='+',
                        help='Example: create --client-key="a8Uma8U2ox"')

    parser.add_argument('verify', type=str, nargs='+',
                        help='Example: create --client-key="a8Uma8U2ox" ' +
                             '--csrf-token="Ay0pVKrOsEKVqVjtrXZT"')

    args = parser.parse_args()
    print(args)
    print(str(vars(args)))


