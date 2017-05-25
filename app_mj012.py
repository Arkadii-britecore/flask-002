# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~
    A microblog example application written as Flask tutorial with
    Flask and sqlite3.
    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, request, json


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'base_mj012.db'),
    DEBUG=True,
    # SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
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


# # show all companies
@app.route('/')
def show_entries():
    db = get_db()
    # cur = db.execute('select title, text from entries order by id desc')
    cur = db.execute('select id, title from company order by id desc')
    entries = cur.fetchall()
    return render_template('index_c_mj012.html', entries=entries)

# code from example
@app.route('/signUp', methods=['POST'])
def signUp():
    try:
        # read the posted values from the UI
        _new_company_title = request.form['inputCompany']
        # _email = request.form['inputEmail']
        # _password = request.form['inputPassword']

        print('DBG receiving form data _new_company_title:{}, request.method'.format(_new_company_title, request.method))

        # validate the received values
        if _new_company_title:

            # add company into db if not empty

            db = get_db()
            db.execute('insert into company (title) values (?)',
                       [_new_company_title])
            db.commit()

            return json.dumps({'html': '<span>All fields good !!</span>'})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        print('ERR :', str(e))
        # return json.dumps({'error': str(e)})
        return redirect('/')


# # retrieve data for list of companies
# @app.route('/getBlog')
# def getBlog():
#     try:
#         # if session.get('user'):
#         # _user = session.get('user')
#         #
#         # con = mysql.connect()
#         # cursor = con.cursor()
#         # cursor.callproc('sp_GetBlogByUser', (_user,))
#         # blogs = cursor.fetchall()
#
#         db = get_db()
#         # cur = db.execute('select title, text from entries order by id desc')
#         cur = db.execute('select id, title from company order by id desc')
#         companies = cur.fetchall()
#
#         comp_dict = []
#
#         for company in companies:
#             blog_dict = {
#                 'id': company[0],
#                 'title': company[1]
#             }
#             comp_dict.append(blog_dict)
#
#         print('DBG blog_dict:', blog_dict)
#
#         return json.dumps(comp_dict)
#
#
#         # else:
#         #     return render_template('error.html', error='Unauthorized Access')
#     except Exception as e:
#         return render_template('error.html', error=str(e))
#
#
# # show list of companies with ajax
# @app.route('/show_companies', methods=['GET'])
# def show_companies():
#     print('DBG called show_companies')
#
#     # return redirect('/index_c_mj013')
#     return render_template('index_e_mj013.html')



#
#
# ## ...
# # show all companies and add another one
# @app.route('/company_add', methods=['GET','POST'])
# def company_add():
#
#     print('DBG company_add', request.method)
#
#     error = None
#     if request.method == 'POST':
#         # if request.form['username'] != app.config['USERNAME']:
#         #     error = 'Invalid username'
#         # elif request.form['password'] != app.config['PASSWORD']:
#         #     error = 'Invalid password'
#
#         #
#         print('DBG: company_add, PST', request.form['title'])
#
#         new_company_title = request.form['title']
#
#
#         # db = get_db()
#         # db.execute('insert into entries (title, text) values (?, ?)',
#         #            [request.form['title'], request.form['text']])
#         # db.commit()
#
#         db = get_db()
#         db.execute('insert into company (title) values (?)',
#                    [new_company_title])
#
#
#         db.commit()
#         flash('New entry was successfully posted')
#
#         # return redirect(url_for('company_add'))
#
#
#         # cur = db.execute('select title, text from entries order by id desc')
#         cur = db.execute('select id, title from company order by id desc')
#         entries = cur.fetchall()
#
#
#
#         return render_template('index_c_mj012.html', entries=entries)
#         # return redirect(url_for('/'))
#
#
#     else:
#         print('DBG show_and_add_company ...else... ', request.method)
#         db = get_db()
#         # cur = db.execute('select title, text from entries order by id desc')
#         cur = db.execute('select id, title from company order by id desc')
#         entries = cur.fetchall()
#         print('DBG show_and_add_company ...b4 return... ', request.method)
#         try:
#             # return render_template('index_companies.html', entries=entries)
#             return render_template('index_c_mj012.html', entries=entries)
#         except:
#             print('DBG show_and_add_company ...render error... ')
#
#
#
# def show_and_add_company():
#     # if not session.get('logged_in'):
#     #     abort(401)
#
#     print('DBG: company_add, PST', request.form['title'])
#
#     db = get_db()
#     db.execute('insert into company (title) values (?,)',
#                [request.form['title'],])
#
#
#     db.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))
#
#
# # trash ...
# def show_and_add_company():
#     db = get_db()
#     # cur = db.execute('select title, text from entries order by id desc')
#     cur = db.execute('select id, title from company order by id desc')
#     entries = cur.fetchall()
#     return render_template('index_companies.html', entries=entries)


# show all employees
@app.route('/employee', methods=['GET','POST'])
def show_employee():
    db = get_db()
    if request.method == 'POST':
        print('DBG show_employee', request.method)
        print('DBG show_employee',type(request.form['name']), type(request.form['salary']), type(request.form['company_id']))

        # add new employee

        # db = get_db()
        db.execute('insert into employee (name, salary, company_id) values (?, ?, ?)',
                   [request.form['name'], request.form['salary'], request.form['company_id']])
        db.commit()

    # db = get_db()

    # cur = db.execute('select title, text from entries order by id desc')
    cur = db.execute('select id, name, salary from employee order by id desc')
    entries = cur.fetchall()
    return render_template('index_e_mj012.html', entries=entries)


# show employee details
@app.route('/employee/<employee_id>')
def show_employee_details(employee_id):
    db = get_db()
    cur = db.execute("""select employee.id,
     employee.name, 
     employee.salary, 
     company.title,
     company.id
    from company inner join employee 
    where employee.company_id=company.id
    and employee.id = ?""", [employee_id])




    values = cur.fetchone()
    entries = []

    print('DBG values', values)
    for val in values:
        print('val=', val)
        entries.append(val)

    # cur = db.execute('select id, name, salary from employee where id = ?', [employee_id])
    # entries = cur.fetchall()
    return render_template('employee_d_mj012.html', entries=entries)


# show company details
@app.route('/company/<company_id>')
def show_company_details(company_id):
    db = get_db()
    # add here request for company.title
    # ...
    # cur = db.execute('select title from company where id = ?', [company_id])
    # company_title = cur.fetchone()

    # try:

    cur = db.execute("""select employee.id, employee.name, employee.salary, company.title 
    from company 
    inner join employee 
    where employee.company_id=company.id 
    and company.id = ?
    """, [company_id])

    entries = cur.fetchall()

    return render_template('company_d_mj012.html', entries=entries )

# -- old templates -- #

# @app.route('/add', methods=['POST'])
# def add_entry():
#     if not session.get('logged_in'):
#         abort(401)
#     db = get_db()
#     db.execute('insert into entries (title, text) values (?, ?)',
#                [request.form['title'], request.form['text']])
#     db.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != app.config['USERNAME']:
#             error = 'Invalid username'
#         elif request.form['password'] != app.config['PASSWORD']:
#             error = 'Invalid password'
#         else:
#             session['logged_in'] = True
#             flash('You were logged in')
#             return redirect(url_for('show_entries'))
#     return render_template('login.html', error=error)
#
#
# @app.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     flash('You were logged out')
#     return redirect(url_for('show_entries'))




