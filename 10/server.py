import bottle
import datetime
import functools
import hashlib
import json
import os
import sqlite3
import time
from HTMLParser import HTMLParser


root_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(root_dir, 'db.sqlite3')
static_dir = os.path.join(root_dir, 'static')

app = bottle.Bottle()
bottle.TEMPLATE_PATH.append(os.path.join(root_dir, 'views'))


allowed_tags = set([
    'b', 'a', 'i', 'u', 'img'
])


def create_db(conn):
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            user_id  INTEGER PRIMARY KEY,
            username  TEXT,
            password  TEXT,
            full_name TEXT
        );
        CREATE TABLE IF NOT EXISTS channels (
            channel_id  INTEGER PRIMARY KEY,
            channel     TEXT UNIQUE
        );
        CREATE TABLE IF NOT EXISTS messages (
            message_id INTEGER PRIMARY KEY,
            user_id    INTEGER REFERENCES users (user_id),
            channel_id INTEGER REFERENCES channels (channel_id),
            timestamp  INTEGER,
            text       TEXT
        );
        INSERT OR IGNORE INTO users VALUES (1, 'boss', sha1('Dancing in the dark'), 'Bruce Summersteen');
        INSERT OR IGNORE INTO users VALUES (2, 'edward', '', 'Edward Hailden');
        INSERT OR IGNORE INTO users VALUES (3, 'alice', sha1('Into the flood again.'), 'Alice InRopes');
        INSERT OR IGNORE INTO users VALUES (4, 'bob', sha1('Is this love'), 'Bob Marmite');
        INSERT OR IGNORE INTO users VALUES (5, 'system', '', 'Grape Galili');
        INSERT OR IGNORE INTO users VALUES (6, 'test', sha1('1234'), 'Testy McTestFace');
        INSERT OR IGNORE INTO channels VALUES (1, '#nsk-home');
        INSERT OR IGNORE INTO channels VALUES (2, '#announcements');
        INSERT OR IGNORE INTO channels VALUES (3, '#general-spam');
        INSERT OR IGNORE INTO messages VALUES (1, 3, 3, 1496311872, 'Hey, Bob!');
        INSERT OR IGNORE INTO messages VALUES (2, 4, 3, 1496311872, 'Hi Alice!');
    ''')


def sha1(val):
    s = hashlib.sha1()
    s.update(val)
    return s.hexdigest()


def db_required(function):
    """
    Make the database connection available to the function as its first
    parameter.
    """
    @functools.wraps(function)
    def decorated(*args, **kwargs):
        with sqlite3.connect(db_path) as conn:
            conn.create_function('sha1', 1, sha1)
            create_db(conn)
            return function(conn, *args, **kwargs)

    return decorated


def login_required(function):
    """
    Verify the login and return a login page if failed.
    Additionally, make the username and database connection available to the
    function as its first two parameters.
    """
    @db_required
    @functools.wraps(function)
    def decorated(conn, *args, **kwargs):
        login_cookie = bottle.request.get_cookie('login')
        login = None
        if login_cookie:
            try:
                login = login_cookie.decode('base64')
            except:
                pass
        if not login or not conn.execute(
            "SELECT * FROM users WHERE username = ?",
                (login,)).fetchall():
            return bottle.template('login')

        return function(login, conn, *args, **kwargs)

    return decorated


def select_scalar(conn, *args, **kwargs):
    """Utility to return a scalar value from a query."""
    row = conn.execute(*args, **kwargs).fetchone()
    return None if row is None else row[0]


@app.post('/login')
@db_required
def login(conn):
    if not conn.execute(
        "SELECT * FROM users WHERE username = ? AND password = sha1(?)", (
            bottle.request.POST.get('username'),
            bottle.request.POST.get('password'),
            )).fetchone():
        return bottle.template('login')

    bottle.response.set_cookie(
        'login',
        bottle.request.POST.get('username').encode('base64')
    )

    return bottle.redirect('/')


@app.get('/logout')
def logout():
    bottle.response.delete_cookie('login')
    return bottle.redirect('/')


def format_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%d.%m.%Y %H:%M:%S')


@app.get('/list_messages')
@login_required
def list_messages(username, conn):
    channel = bottle.request.GET['channel']
    channel_id = select_scalar(conn, "SELECT channel_id FROM channels WHERE channel = ?", (channel,))
    if channel_id is None:  # Channel not found
        return json.dumps([])
    last_id = int(bottle.request.GET['last_id'])
    return json.dumps([{
        'author': username_,
        'id': message_id,
        'date': format_timestamp(timestamp),
        'text': message,
        } for message_id, username_, timestamp, message in conn.execute("""
        SELECT message_id, username, timestamp, text
        FROM users NATURAL JOIN messages
        WHERE message_id > ? AND channel_id = ?""", (last_id, channel_id)
        ).fetchall()])


@app.get('/list_channels')
@login_required
def list_channels(username, conn):
    result = [channel for channel, in conn.execute("SELECT channel FROM channels").fetchall()]
    return json.dumps(result)


@app.get('/')
@login_required
def index(username, conn):
    name = select_scalar(conn, "SELECT full_name FROM users WHERE username = ?", (username,))
    return bottle.template('index', name=name, username=username)


class MyHTMLValidator(HTMLParser):
    def validate_link(self, link):
        if not link.startswith('http://') and not link.startswith('https://'):
            raise ValueError('Disallowed href ' + link)

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs = dict((key.lower(), val) for key, val in dict(attrs).items())

        if tag not in allowed_tags:
            raise ValueError('Disallowed HTML tag ' + tag)

        for attr in ['src', 'href']:
            if attr in attrs:
                self.validate_link(attrs[attr])


def add_channel(conn, channel):
    max_id = select_scalar(conn, 'SELECT MAX(channel_id) FROM channels')
    conn.execute('INSERT INTO channels (channel_id, channel) VALUES (?, ?)', (max_id + 1, channel))


def add_message(conn, username, message, channel):
    user_id = select_scalar(conn, "SELECT user_id FROM users WHERE username = ?", (username,))
    channel_id = select_scalar(conn, "SELECT channel_id FROM channels WHERE channel = ?", (channel,))
    conn.execute('INSERT INTO messages (user_id, channel_id, timestamp, text) VALUES (?, ?, ?, ?)', (
        user_id, channel_id, int(time.time()), message))


def validate_html(html):
    try:
        validator = MyHTMLValidator()
        validator.feed(html)
        return "OK"
    except Exception as e:
        return 'Error: %s' % str(e)


def handle_message(conn, username, message, channel):
    if channel == '#system':
        return 'Why? We really asked you not to post here :('

    if message.startswith('/'):
        action = message.split(' ', 1)[0][1:]
        rest = message[len(action) + 2:]
        result = None
        if action == 'join':
            new_channel = rest
            if not new_channel.startswith('#'):
                result = 'Channel names should start with "#"'
            elif new_channel == '#system':
                result = 'All your base are belong to us (really, stop trying)'
            else:
                add_channel(conn, new_channel)
                return new_channel
        elif action == 'math':
            equation = rest
            legal_chars = set(' \t\n\r0123456789+-*/()')
            result = 'Illegal exercise'
            if set(equation).issubset(legal_chars):
                try:
                    result = '%s = %s' % (equation, eval(equation))
                except:
                    pass
        elif action == 'whois':
            username = rest
            name = select_scalar(conn, "SELECT full_name FROM users WHERE username = ?", (username,))
            result = '%s is %s' % (username, name) if name else 'Not sure who is %s, ask Siri' % username
        elif action == 'joke':
            result = 'Funny is not yet implemented'
        elif action == 'rename':
            if not ' ' in rest:
                result = 'Bad rename format'
            else:
                user, name = tuple(rest.split(' ', 1))
                user_id = select_scalar(conn, "SELECT user_id FROM users WHERE username = ?", (user,))
                if user_id is None:
                    result = 'Invalid user'
                else:
                    conn.executescript("UPDATE users SET full_name = '%s' WHERE username = '%s'" % (name, user))
                    result = 'Renamed %s' % user
        elif action == '?' or action == 'help':
            result = '<pre>%s</pre>' % '\n'.join([
                '/join [channel]',
                '/math [expression]',
                '/whois [username]',
                '/rename [username] [new_fullname]',
                '/joke',
                '/?',
            ])
        else:
            result = 'Unknown action'
        if result:
            add_message(conn, 'system', result, channel)
        return "OK"
    else:
        validation_status = validate_html(message)
        if validation_status == 'OK':
            add_message(conn, username, message, channel)
        return validation_status


@app.post('/post')
@login_required
def post(username, conn):
    message = bottle.request.POST['message']
    channel = bottle.request.POST['channel']
    return json.dumps(handle_message(conn, username, message, channel))


@app.get('/static/<filename:path>')
def static_resources(filename):
    return bottle.static_file(filename, root=static_dir)


@app.get('/reset')
def reset():
    if os.path.exists(db_path):
        os.remove(db_path)
    bottle.response.delete_cookie('login')
    return bottle.redirect('/')


def run():
    app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
    run()
