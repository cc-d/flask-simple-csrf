#!/usr/bin/env python3
import config
import sys
from werkzeug.security import generate_password_hash, check_password_hash
from argparse import ArgumentParser


def create_csrf_token(client_key, server_key=config.SECRET_CSRF_KEY):
    token = generate_password_hash(client_key + server_key,
                                   method=config.METHOD,
                                   salt_length=config.SALT_LENGTH)
    token = token.replace(config.METHOD + '$', '')
    return token


def verify_csrf_token(client_key, csrf_token,
                      server_key=config.SECRET_CSRF_KEY):
    return check_password_hash(config.METHOD + '$' + csrf_token,
                               client_key + server_key)


def html_input(csrf_token, elem_name=config.HTML_ELEM_NAME):
    return '<input type="hidden" value="%s" name="%s">' % (csrf_token,
                                                           elem_name)


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
    elif args.action[0] not in ['create','verify']:
        raise Exception('Invalid acion. ' +
                        'Valid actions are "create" and verify"')

    if args.client_key is None:
        raise Exception('Every action requires a client key.')
    else:
        client_key = args.client_key

    if args.action[0] == 'create':
        csrf_token = create_csrf_token(client_key=client_key)
        if args.token_only:
            print(csrf_token)
            sys.exit()
        else:
            print(html_input(csrf_token))
    else:
        if args.csrf_token is None:
            raise Exception('Must include csrf token.')
        else:
            print(verify_csrf_token(client_key, args.csrf_token))