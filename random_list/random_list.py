import os
import random
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
             render_template, flash


app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file



#Load default config and override config from an environment variable
app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'random_list.db'),
            SECRET_KEY=SECRET_KEY,
                USERNAME=USERNAME,
                    PASSWORD=PASSWORD
                    ))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
        """Connects to the specific database."""
        rv = sqlite3.connect(app.config['DATABASE'])
        rv.row_factory = sqlite3.Row
        return rv

                
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()

@app.cli.command('initdb')
def initdb_command():
        """Initializes the database."""
        init_db()
        print('Initialized the database.')


def get_db():
        """Opens a new database connection if there is none yet for the
            current application context.
                """
        if not hasattr(g, 'sqlite_db'):
            g.sqlite_db = connect_db()
            return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
        """Closes the database again at the end of the request."""
        if hasattr(g, 'sqlite_db'):
                    g.sqlite_db.close()


@app.route('/')
def get_anime():
    db = get_db()
    cur = db.execute('select distinct searchable_anime, anime from chars')
    entries = cur.fetchall()
    print(entries)
    cur.close()
    return render_template('show_entries.html', anime=entries)


@app.route('/<anime>/',methods=['GET'])
def get_char(anime):
    anime = anime.lower()
    #anime= r"'" + anime + "'"
    db = get_db()
    cur = db.execute("select distinct name, anime from chars where searchable_anime is '%s';"  % anime )
    entries = cur.fetchall()
    print(entries)
    cur.close()
    return render_template('show_entries.html', chars=entries)

@app.route('/<anime>/<character>/',methods=['GET'])
def get_quote(anime, character):
    if character is not None:
        character = character.lower()
        #character = r"'" + character + r"'"
        print('Character retrieved is ' + character)
        anime = anime.lower()
        #anime = r"'" + anime + "'"
        print('Anime retrieved is ' + anime)
        db = get_db()
        query = "select quote, fullname, character, image from quotes where anime is '%s' and character is '%s' ORDER by RANDOM() LIMIT 1" % (anime, character)
        print('Query is ' + query)
        cur = db.execute(query)
        entries = cur.fetchall()
        cur.close()
        print(entries)
        return render_template('show_entries.html', quote=entries)
    else:
        print('Failed')
        return

