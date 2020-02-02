#!/usr/bin/env python3
from flask_simple_csrf.config import config
import sys
from werkzeug.security import generate_password_hash, check_password_hash
from argparse import ArgumentParser


class CSRF:
    def __init__(self, default_config=config, config=config):
        self.config = default_config
        for key in config.keys():
            self.config[key] = config[key]

    def create(self, client_key, server_key=None):
        server_key = self.config['SECRET_CSRF_KEY'] if server_key is None else server_key
        token = generate_password_hash(client_key + server_key,
                                       method=config['METHOD'],
                                       salt_length=config['SALT_LENGTH'])
        token = token.replace(config['METHOD'] + '$', '')
        return token


    def verify(self, client_key, csrf_token, server_key=None):
        server_key = self.config['SECRET_CSRF_KEY'] if server_key is None else server_key
        return check_password_hash(config['METHOD'] + '$' + csrf_token,
                                   client_key + server_key)


    def csrf_html(self, csrf_token, elem_name=None):
        elem_name = self.config['HTML_ELEM_NAME'] if elem_name is None else elem_name
        return '<input type="hidden" value="%s" name="%s">' % (csrf_token,
                                                               elem_name)


    def init_app(self, app):
        app.jinja_env.globals.update(csrf_html=self.csrf_html)

        return app

def init_CSRF():
    return CSRF()

if __name__ == '__main__':
    parser = ArgumentParser(description='Simple CSRF tokens')

    parser.add_argument('-c', '--client-key', type=str,
                        help='The client CSRF key. ' +
                             'This, combined with the server ' +
                             'key and hashed, creates the final ' +
                             'csrf token included in html input.')

    parser.add_argument('-t', '--csrf-token', type=str,
                        help='The generated csrf token.')

    parser.add_argument('-o', '--token-only', action='store_true',
                        help='Only return the final token ' +
                             'wihtout the html input.')

    parser.add_argument('action', type=str, nargs='+',
                        help='"create" or "verify". ' +
                             'Examples: (TO CREATE: ' +
                             'create --client-key="a8Uma8U2ox" ' +
                             ') | (TO VERIFY: ' +
                             'verify --client-key="a8Uma8U2ox" ' +
                             '--csrf-token="Ay0pVKrOsEKVqVjtrXZT")')

    args = parser.parse_args()

    if len(args.action) != 1:
        raise Exception('Invalid amount of positional aguments. ' +
                        'Must be "create" or "verify".')
    elif args.action[0] not in ['create', 'verify']:
        raise Exception('Invalid acion. ' +
                        'Valid actions are "create" and verify"')

    if args.client_key is None:
        raise Exception('Every action requires a client key.')
    else:
        client_key = args.client_key

    CSRF = CSRF()

    if args.action[0] == 'create':
        csrf_token = CSRF.create(client_key=client_key)
        if args.token_only:
            print(csrf_token)
            sys.exit()
        else:
            print(CSRF.csrf_html(csrf_token))
    else:
        if args.csrf_token is None:
            raise Exception('Must include csrf token.')
        else:
            print(CSRF.verify(client_key, args.csrf_token))
