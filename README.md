# Install
`pip3 install flask-simple-csrf`
or if installing from source
```python3 setup.py install```

# How to use
This package is intended to assign a unique CSRF string per each form submit per user session, without requiring any backend session tracking. First, you'll want to set a variable `SECRET_CSRF_KEY` in your app config to a random, complex string. Example: `SECRET_CSRF_KEY = 'wMmeltW4mhwidorQRli6Oxx9VPXldz'`

Second, you probably want to add somthing like this to the top of your code:

```
from flask_simple_csrf import CSRF

#app.config should have an attribute that looks something like this
#CSRF_CONFIG = {
#    'SECRET_CSRF_KEY': 'changeme-40-50-characters-long',
#}

CSRF = CSRF(config=config.CSRF_CONFIG)
app = CSRF.init_app(app)

@app.before_request
def before_request():
        if 'CSRF_TOKEN' not in session or 'USER_CSRF' not in session:
            session['USER_CSRF'] = random_string(64)
            session['CSRF_TOKEN'] = CSRF.create(session['USER_CSRF'])
```

Each user session should have a unique CSRF string which changes on form submit.

In the HTML templates you want to protect, add: `{{ csrf_html(session['USER_CSRF'])|safe }}`

This will create something like this: `<input type="hidden" value="9D..." name="simplecsrf">`

I'd reccommend creating a wrapper to avoid code duplciation when checking for this value. Something like:
```
def require_csrf(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'POST':
            user_csrf = request.form.get('simplecsrf')

            if CSRF.verify(user_csrf, session['CSRF_TOKEN']) is False:
                flash('submitted csrf does not match combined server & user keys')
                return logout()

            clear_csrf_tokens()
            flash('csrf user token and server token match', 'success')

            return f(*args, **kwargs)
        else:
            return f(*args, **kwargs)
    return decorated
```

Then use the @require_csrf decorator before each flask view you'd like to require the check.


