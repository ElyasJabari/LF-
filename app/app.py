from flask import Flask, request, jsonify, render_template

import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta

app = Flask(__name__)


class Connection:
    db_params = {
        'host': 'localhost',
        'database': 'dev',
        'user': 'postgres',
        'password': 'postgres',
        'port': '5432',
    }

    def __init__(self, host, database, user, password):
        try:
            self.connection = psycopg2.connect(**Connection.db_params)
        except psycopg2.Error as e:
            print(f'Error connecting to {database}')

    @staticmethod
    def get():
        return Connection('localhost', 'dev', 'postgres', 'postgres')

    @staticmethod
    # Function to query data from the table
    def query_data(select_query):
        connection = Connection.get()
        with connection.connection.cursor() as cursor:
            cursor.execute(select_query)
            rows = cursor.fetchall()
            return rows

    @staticmethod
    # Function to insert or update data in the table
    def execute_query(query, values=None):
        connection = Connection.get()
        with connection.connection.cursor() as cursor:
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
        connection.connection.commit()

    @staticmethod
    # Function to select ref values by id
    def get_ref_by_id(table, column, id__):
        # SQL query to get the device name by ID
        select_query = f'SELECT {column} FROM {table} WHERE id = {id__};'

        # Use the Connection class to query the device name
        result = Connection.query_data(select_query)

        # Check if the result is not empty
        if result:
            # Assuming the result is a single device name (change if needed)
            name = result[0][0]
            return name
        else:
            raise ValueError(f'Could not find {table}.{column} for id {id__}')

    @staticmethod
    def get_id(table, column, value):
        select_query = f'SELECT id FROM {table} WHERE {column} = %s;'

        values = (value,)

        result = Connection.query_data(select_query, values)

        # Check if the result is not empty
        if result:
            # Assuming the result is a single device name (change if needed)
            id__ = result[0][0]
            return id__
        else:
            raise ValueError(f'Could not find {table}.{column} for value {value}')


class User:
    class Password:
        @staticmethod
        def hash(password):
            return password[::-1]
    class Role:
        @staticmethod
        def get_role_name(role_id):
            return Connection.get_ref_by_id('ref_role', 'name', role_id)

    def __init__(self, username, password, role_id):
        self.username = username
        self.password = password
        self.role_id = role_id

    def __eq__(self, other):
        return self.username == other.username and self.password == other.password

    @staticmethod
    def get_by_username(username):
        # SQL query to get a user by username
        select_user_query = "SELECT * FROM tbl_user WHERE username = %s;"

        # Values to be used in the query
        values = (username,)

        # Use the Connection class to query the user
        result = Connection.query_data(select_user_query, values)

        # Check if the result is not empty
        if result:
            # Assuming the result is a single user (change if needed)
            user_data = result[0]
            user = User(
                user_id=user_data[0],
                username=user_data[1],
                password=user_data[2],
                role=user_data[3]
            )
            return user
        else:
            raise ValueError(f'No user for username {username} could be found.')

    @staticmethod
    def create_user(username, password, role_id):
        # Hash the password using a secure hashing algorithm (e.g., bcrypt)
        hashed_password = User.Password.hash(password)

        # SQL query to insert a new user
        insert_user_query = "INSERT INTO tbl_user (username, password, role_id) VALUES (%s, %s, %s);"

        # Values to be inserted into the user table
        values = (username, hashed_password, role_id)

        # Use the Connection class to insert the new user
        Connection.execute_query(insert_user_query, values)

class Ticket:
    class Device:
        @staticmethod
        def get_device_name(device_id):
            return Connection.get_ref_by_id('ref_device', 'name', device_id)

    class Status:
        @staticmethod
        def get_status_name(status_id):
            return Connection.get_ref_by_id('ref_status', 'name', status_id)

    class Category:
        @staticmethod
        def get_category_name(category_id):
            return Connection.get_ref_by_id('ref_category', 'name', category_id)

    def __init__(self, title, description, ticket_id, creation_date, due_date, device_id, category_id, status_id):
        self.title = title
        self.description = description
        self.id = ticket_id
        self.creation_date = creation_date
        self.due_date = due_date
        self.device_id = device_id
        self.category_id = category_id
        self.status_id = status_id

    def serialize(self):
        return {
            'title': self.title,
            'id': self.id,
            'description': self.description,
            'status': self.status_id,
            'category': self.category_id,
            'device': self.device_id,
            'creation_date': self.creation_date,
            'due_date': self.due_date
        }

    @staticmethod
    def create(title, description, device, category, status):
        # Get the current date and a second date two weeks later
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        due_date = (datetime.now() + timedelta(weeks=2)).strftime('%Y-%m-%d %H:%M:%S')

        # SQL query to insert a new ticket
        insert_query = "INSERT INTO tbl_ticket (title, description, creation_date, due_date, device_id, category_id, status_id) VALUES (%s, %s, %s, %s, %s, %s, %s);"

        # Values to be inserted into the ticket table
        values = (title, description, current_date, due_date, device, category, status)

        # Use the Connection class to insert the new ticket
        Connection.execute_query(insert_query, values)

    @staticmethod
    def get_ticket_by_id(ticket_id):
        # SQL query to get a ticket by ID
        select_query = f'SELECT * FROM tbl_ticket WHERE id = {ticket_id};'

        # Values to be used in the query
        values = (ticket_id,)

        # Use the Connection class to query the ticket
        result = Connection.query_data(select_query)

        # Check if the result is not empty
        if result:
            # Assuming the result is a single ticket (change if needed)
            row = result[0]

            ticket = Ticket(
                ticket_id=row[0],
                title=row[1],
                description=row[2],
                creation_date=row[3],
                due_date=row[4],
                device_id=row[5],
                category_id=row[6],
                status_id=row[7]
            )

            return ticket
        else:
            # Ticket not found
            raise ValueError(f'Could not find ticket with id {ticket_id}')

    def save_ticket_to_db(self):
        # SQL query to update a ticket by ID
        update_query = "UPDATE tbl_ticket SET title = %s, description = %s, device_id = %s, category_id = %s, status_id = %s WHERE id = %s;"

        # Values to be used in the update query
        values = (self.title, self.description, self.device_id, self.category_id, self.status_id, self.ticket_id)

        # Use the Connection class to update the ticket
        Connection.execute_query(update_query, values)

    @staticmethod
    def get_all_tickets_serialized():
        # SQL query to get all tickets
        select_all_query = "SELECT * FROM tbl_ticket;"

        # Use the Connection class to query all tickets
        result = Connection.query_data(select_all_query)

        # Create a list of Ticket objects from the query result
        tickets = []
        for row in result:
            ticket = Ticket(
                ticket_id=row[0],
                title=row[1],
                description=row[2],
                creation_date=row[3],
                due_date=row[4],
                device_id=row[5],
                category_id=row[6],
                status_id=row[7]
            )
            tickets.append(ticket.serialize())

        return tickets


# Endpoint for posting Ticket objects
@app.route('/ticket', methods=['POST'])
def post_ticket():
    try:
        data = request.get_json()

        # Deserialize the JSON payload into a Ticket object
        Ticket.create(data['title'], data['description'], data['device'], data['category'], data['status'])

        return jsonify({'message': 'Ticket created successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Endpoint for getting all tickets as JSON
@app.route('/tickets', methods=['GET'])
def get_all_tickets():
    # Serialize all tickets to JSON
    serialized_tickets = Ticket.get_all_tickets_serialized()
    return jsonify(serialized_tickets)


# Endpoint for getting a single ticket by ID
@app.route('/ticket/<int:ticket_id>', methods=['GET'])
def get_ticket_by_id(ticket_id):
    # Find the ticket with the specified ID
    ticket = Ticket.get_ticket_by_id(ticket_id)
    if ticket:
        # Serialize the ticket to JSON
        serialized_ticket = ticket.serialize()
        return jsonify(serialized_ticket)
    else:
        return jsonify({'error': 'Ticket not found'}), 404


# Endpoint for getting the status name
@app.route('/ticket/status/<int:status_id>', methods=['GET'])
def get_status_name(status_id):
    status_name = Ticket.Status.get_status_name(status_id)
    if status_name is not None:
        return jsonify({'status_name': status_name})
    else:
        return jsonify({'error': 'Status not found'}), 404


# Example endpoint for getting the category name
@app.route('/ticket/category/<int:category_id>', methods=['GET'])
def get_category_name(category_id):
    category_name = Ticket.Category.get_category_name(category_id)
    if category_name is not None:
        return jsonify({'category_name': category_name})
    else:
        return jsonify({'error': 'Category not found'}), 404


# Example endpoint for getting the device name
@app.route('/ticket/device/<int:device_id>', methods=['GET'])
def get_device_name(device_id):
    device_name = Ticket.Device.get_device_name(device_id)
    if device_name is not None:
        return jsonify({'device_name': device_name})
    else:
        return jsonify({'error': 'Device not found'}), 404


# Example endpoint for getting the role name
@app.route('/user/role/<int:role_id>', methods=['GET'])
def get_role_name(role_id):
    role_name = User.Role.get_role_name(role_id)
    if role_name is not None:
        return jsonify({'role_name': role_name})
    else:
        return jsonify({'error': 'Device not found'}), 404


@app.route('/user/verify', methods=['POST'])
def login():
    data = request.get_json()

    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required'}), 400

    username = data['username']
    password = data['password']

    try:
        user = User.get_by_username(username)
    except Exception as e:
        return jsonify({'error': e}), 400


    # Check if the provided credentials are valid
    if user.username == username and user.password == password:
        # Replace the following URL with the actual URL for the designated account
        account_url = User.Role.get_role_name(user.role_id)
        return jsonify({'status': 200, 'account_url': account_url})
    else:
        return jsonify({'error': 'Invalid credentials'}), 400


# Endpoint to render login.html
@app.route('/login')
def render_login():
    return render_template('login.html')


# Endpoint to render ticket.html
@app.route('/ticket')
def render_ticket():
    return render_template('ticket.html')


# Endpoint to render ticketlist.html
@app.route('/ticketlist')
def render_ticketlist():
    return render_template('ticketlist.html')


# Endpoint to render technician.html
@app.route('/technician')
def render_technician():
    return render_template('technician.html')


if __name__ == '__main__':
    app.run(debug=True)
