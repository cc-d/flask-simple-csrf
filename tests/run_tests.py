#!/usr/bin/env python3
import os
import sys

LIB = os.path.join(os.path.dirname(os.path.realpath(__file__)))
LIB = os.path.join(LIB, '../flask_simple_csrf/')

sys.path.append(LIB)

from flask_simple_csrf import CSRF

CSRF = CSRF()

import re


def main():
    client_key = 'hello'
    csrf_token = CSRF.create(client_key)

    assert csrf_token != CSRF.create('other'), 'duplicate token gen'

    html = CSRF.csrf_html(csrf_token)
    reg = re.findall(r'<input type="hidden" (value=".*") (name=".*")>', html)

    assert len(reg) == 1, 'invalid html element'
    assert 'value="%s"' % csrf_token in reg[0], 'html element value error'

    assert CSRF.verify(client_key, csrf_token) is True, 'correct token returned False'
    assert CSRF.verify(client_key + '1', csrf_token) is False, 'Incorrect Token returned True'

    print('Tests complete.')

if __name__ == '__main__':
    main()
