from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

class Ticket:
    def __init__(self, title, description, id, creation_date, due_date, device, category, status):
        self.title = title
        self.description = description
        self.id = id
        self.creation_date = creation_date
        self.due_date = due_date
        self.device = device
        self.category = category
        self.status = status

# In-memory storage for tickets (replace with a database in a real application)
tickets = []

# Endpoint for posting Ticket objects
@app.route('/tickets', methods=['POST'])
def post_ticket():
    try:
        data = request.get_json()

        # Deserialize the JSON payload into a Ticket object
        ticket = Ticket(
            title=data['title'],
            description=data['description'],
            id=data['id'],
            creation_date=data['creationDate'],
            due_date=data['dueDate'],
            device=data['device'],
            category=data['category'],
            status=data['status']
        )

        # Add the ticket to the in-memory storage
        tickets.append(ticket)

        return jsonify({'message': 'Ticket created successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Endpoint for getting all tickets as JSON
@app.route('/tickets', methods=['GET'])
def get_all_tickets():
    # Serialize all tickets to JSON
    serialized_tickets = [
        {
            'title': ticket.title,
            'id': ticket.id,
            'status': ticket.status,
            'category': ticket.category,
            'device': ticket.device,
            'creation_date': ticket.creation_date,
            'due_date': ticket.due_date
        }
        for ticket in tickets
    ]
    return jsonify(serialized_tickets)

# Endpoint for getting a single ticket by ID
@app.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket_by_id(ticket_id):
    # Find the ticket with the specified ID
    ticket = next((t for t in tickets if t.id == ticket_id), None)

    if ticket:
        # Serialize the ticket to JSON
        serialized_ticket = {
            'title': ticket.title,
            'description': ticket.description,
            'id': ticket.id,
            'creation_date': ticket.creation_date,
            'due_date': ticket.due_date,
            'device': ticket.device,
            'category': ticket.category,
            'status': ticket.status
        }
        return jsonify(serialized_ticket)
    else:
        return jsonify({'error': 'Ticket not found'}), 404

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
