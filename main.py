import traceback
import pymysql
import random
from flask_toastr import Toastr
from flask import flash, render_template, request, redirect, jsonify
from flask_table import Col, create_table, ButtonCol
from werkzeug.security import generate_password_hash
from app import app
from db_config import mysql

global choice, current_choice, load_startup, pk_value_dict, columns_dict_keys, where_condition, table_desc, column_names, columns_desc
choice = ''
current_choice = ''
load_startup = ''
# id8813320_flutter

# Activities to be completed
# 1. Hash password
# 2. Primary keys with drop down / with running serial numbers
# 3. Add and Edit screens on the same page
# 4. Ajax
# 5. Code review and clean up

@app.route('/add_record_view', methods=['GET', 'POST'])
def add_record_view():
    global choice, current_choice, load_startup, pk_value_dict, columns_dict_keys, where_condition, table_desc, column_names, columns_desc
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        params = request.values
        choice = params.get('table_menu')
        current_choice = choice
        cursor.execute('DESC ' + choice)
        columns_desc = cursor.fetchall()

        # _hashed_password = generate_password_hash(_password)
        editfields = "<div><dl><p>"
        column_names = []
        column_types = []
        for column_name in columns_desc:
            editfields = editfields + "<p><input name=\"" + column_name['Field'] + \
                           "\" type=\"text\" placeholder=\"" + column_name['Field'] + "\" autocomplete=\"off\" " \
                           + ("required" if column_name['Null'] == "Yes" else "") + "></p>"
            column_names.append(column_name['Field'])
            column_types.append(column_name['Type'])

        editfields = editfields + "</p></dl><p> </p></div>"
            # <button id=\"save_new_record\" class =\"btn btn-primary align-right\" style=\"margin:5px\" >Save</button></p></div>"
        if columns_desc:
            return jsonify(editfields)
        else:
            return 'Error loading page for adding record'
    except Exception as e:
        print(e)
        err_lineno = str(traceback.format_exc()).split(",")[1]
        print(err_lineno)
    finally:
        cursor.close()
        conn.close()


@app.route('/add_generic', methods=['GET', 'POST'])
def add_generic():
    global choice, current_choice, load_startup, pk_value_dict, columns_dict_keys, where_condition, table_desc, column_names, columns_desc
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        params = request.values
        insert_column_names = ''
        insert_column_values = ''
        i = 0
        for record_item in columns_desc:
            insert_column_names = insert_column_names + record_item['Field'] + ", "
            insert_column_values = insert_column_values + \
                                   ("\'" if record_item['Type'][0:3] == "var" else "") + \
                                   params.get(record_item['Field']) + \
                                   ("\'" if record_item['Type'][0:3] == "var" else "") + ", "
            i = i + 1
        insert_column_names = insert_column_names[:-2]
        insert_column_values = insert_column_values[:-2]

        # validate the received values
        # if _name and _email and _password and request.method == 'POST':
        if request.method == 'GET' or request.method == 'POST':
            # do not save password as a plain text
            # _hashed_password = generate_password_hash(_password)
            # save edits
            sql = "INSERT INTO " + choice + "(" + insert_column_names + ") VALUES(" + insert_column_values + ")"
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            flash('Record added successfully!', 'success')
            load_startup = "yes"
            return jsonify("Success")
        else:
            return 'Error adding record with conditions: ' + where_condition
    except Exception as e:
        print(e)
        err_lineno = str(traceback.format_exc()).split(",")[1]
        print(err_lineno)
    finally:
        cursor.close()
        conn.close()

@app.route('/get_word')
def languages():
    '''Return data in json format'''
    lst = ["Python", 'HTML', 'JavaScript', 'CSS']
    words = {}
    words['choice'] = random.choice(lst)
    return jsonify(words)

@app.route('/update_tables_list', methods=['GET', 'POST'])
def update_tables_list():
    global choice, current_choice, load_startup, pk_value_dict, columns_dict_keys, where_condition, table_desc, column_names, columns_desc
    conn = None
    cursor = None
    try:
        params = request.values
        choice = params.get('db_name')
        app.config['MYSQL_DATABASE_DB'] = (
            choice if choice else app.config['MYSQL_DATABASE_DB'])

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        choice = ''
        table_list = []

        cursor.execute('SHOW TABLES')
        rows = cursor.fetchall()
        table_name_dict = {}
        i = 0
        for table_name in rows:
            table_name_dict['table_name' + str(i)] = table_name['Tables_in_' + app.config['MYSQL_DATABASE_DB']]
            i = i + 1

        responses = {}
        responses['response'] = table_name_dict

        if table_name_dict:
            return jsonify(table_name_dict)
        else:
            return 'Error loading tables list'
    except Exception as e:
        print(e)
        err_lineno = str(traceback.format_exc()).split(",")[1]
        print(err_lineno)
    finally:
        cursor.close()
        conn.close()

@app.route('/', methods=['GET', 'POST'])
def main():
    global choice, current_choice, load_startup, pk_value_dict, columns_dict_keys, where_condition, table_desc, column_names, columns_desc
    conn = None
    cursor = None
    try:

        params = request.values
        db_name = params.get('db_name')
        app.config['MYSQL_DATABASE_DB'] = (
            db_name if db_name else app.config['MYSQL_DATABASE_DB'])
        if params.get('table_menu'):
            choice = params.get('table_menu')

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        table_list = []

        cursor.execute('SHOW TABLES')
        rows = cursor.fetchall()
        for (table_name) in rows:
            table_list.append(table_name['Tables_in_' + app.config['MYSQL_DATABASE_DB']])
        if params.get('table_menu'):
            cursor.execute('SELECT * FROM ' + choice)
            rows = cursor.fetchall()
            if not rows:
                return jsonify("No records found")
            tablecls = create_table('tablecls')

            columns_dict_keys = rows[0].keys()
            for header in rows[0].keys():
                tablecls.add_column(header, Col(header))
            cursor.execute("select sta.column_name as pk_name from information_schema.statistics " + \
                           "as sta WHERE sta.table_name = '" + choice + "' AND sta.index_name = 'PRIMARY';")
            pkey_rows = cursor.fetchall()

            cursor.execute('DESC ' + choice)
            columns_desc = cursor.fetchall()

            pk_value_dict = {}
            for pkvalue in pkey_rows:
                pk_value_dict[pkvalue['pk_name']] = pkvalue['pk_name']

            if pk_value_dict == {}:
                for header in rows[0].keys():
                    tablecls.add_column(header, Col(header))
                    pk_value_dict[header] = header

            table_desc = [None] * 7
            for i in range(len(cursor.description)):
                table_desc[i] = cursor.description[i]

            tablecls.add_column('Edit', ButtonCol('Edit', 'edit_view_generic', url_kwargs=pk_value_dict))
            tablecls.add_column('Delete', ButtonCol('Delete', 'delete_user', url_kwargs=pk_value_dict))
            tablecls.border = True
            table = tablecls(rows)
            if load_startup == "yes":
                load_startup = ''
                return render_template("index.html", table=table)
            else:
                return jsonify(table)
        else:
            table = "<table></table>"
            return render_template("index.html", table=table)
    except Exception as e:
        print(e)
        err_lineno = str(traceback.format_exc()).split(",")[1]
        print(err_lineno)
    finally:
        cursor.close()
        conn.close()


@app.route('/edit_generic', methods=['POST'])
def edit_view_generic():
    global choice, current_choice, load_startup, pk_value_dict, columns_dict_keys, where_condition, table_desc, column_names, columns_desc
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        params = request.values
        where_condition = ''
        for k in pk_value_dict.keys():
            where_condition = where_condition + k + ' = ' + params.get(k) + ' AND '
        where_condition = where_condition[:-5]
        cursor.execute("SELECT * FROM " + choice + " WHERE " + where_condition)
        rows = cursor.fetchone()
        form_content = "<form method=\"post\" action=\"/update\"><dl><p>"
        table_desc = [None] * 7
        for i in range(len(cursor.description)):
            table_desc[i] = cursor.description[i]
        i = 0
        for header in rows:
            form_content = form_content + "<p><input name=\"" + header + "\" value=\" " + str(rows[header]) + \
                           "\" type=\"text\" placeholder=\"Name\" autocomplete=\"off\" " \
                           + ("required" if table_desc[i][6] else "") + "></p>"
            i = i + 1

        form_content = form_content + "</p></dl><p>\
            <input name=\"where_condition\" value=\"" + where_condition + "\" type=\"hidden\">\
            <input type=\"submit\" value=\"Submit\"></p></form>"
        if rows:
            return render_template('edit.html', form_content=form_content)
        else:
            return 'Error loading for record with conditions: ' + where_condition
    except Exception as e:
        print(e)
        err_lineno = str(traceback.format_exc()).split(",")[1]
        print(err_lineno)
    finally:
        cursor.close()
        conn.close()


@app.route('/update', methods=['POST'])
def update_user():
    global choice, current_choice, load_startup, pk_value_dict, columns_dict_keys, where_condition, table_desc, column_names, columns_desc
    conn = None
    cursor = None
    params = request.values

    try:
        # validate the received values

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        params = request.values
        update_string = ''
        i = 0
        for record_item in columns_desc:
            update_string = update_string + record_item['Field'] + " =" + \
                   ("\'" if record_item['Type'][0:3] == "var" else "") + \
                   params.get(record_item['Field']) + \
                   ("\'" if record_item['Type'][0:3] == "var" else "") + ", "
            i = i + 1
        update_string = update_string[:-2]


        # Do data validations - if _name and _email and _password and _id and request.method == 'POST':
        if request.method == 'POST':
            # do not save password as a plain text
            # _hashed_password = generate_password_hash(request.form['user_password'])
            # save edits
            sql = "UPDATE " + choice + " SET " + update_string + " WHERE " + where_condition
            current_choice = choice
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            flash('Record updated successfully!', 'success')
            load_startup = "yes"
            return redirect('/')
        else:
            return 'Error while updating the record with conditions: ' + where_condition
    except Exception as e:
        print(e)
        err_lineno = str(traceback.format_exc()).split(",")[1]
        print(err_lineno)
    finally:
        cursor.close()
        conn.close()


@app.route('/delete', methods=['POST'])
def delete_user():
    global choice, current_choice, load_startup, pk_value_dict, columns_dict_keys, where_condition, table_desc, column_names, columns_desc
    conn = None
    cursor = None
    params = request.values
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        if request.method == 'POST':
            where_condition = ''
            i = 0
            for k in pk_value_dict:
                column_type = next((item['Type'] for item in columns_desc if item["Field"] == k), None)
                where_condition = where_condition + k + " = " + \
                                  ("\'" if column_type[0:3] == 'var' else "") + params.get(k) \
                                  + ("\'" if column_type[0:3] == 'var' else "") + ' AND '
                i = i + 1
            where_condition = where_condition[:-5]
            sql = "DELETE FROM " + choice + " WHERE " + where_condition
            cursor.execute(sql)
            conn.commit()
            flash('Record deleted successfully!', 'success')
            load_startup = "yes"
            return redirect('/')
    except Exception as e:
        print(e)
        err_lineno = str(traceback.format_exc()).split(",")[1]
        print(err_lineno)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run()
