import flask # type: ignore
import flask_cors # type: ignore
import flask_sqlalchemy # type: ignore
from datetime import datetime

app = flask.Flask(__name__)
flask_cors.CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campusflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask_sqlalchemy.SQLAlchemy(app)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='OPEN')
    priority = db.Column(db.String(20), default='MEDIUM')
    assigned_to = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    data = flask.request.json
    ticket = Ticket(
        title=data['title'],
        description=data.get('description', ''),
        category=data['category'],
        priority=data.get('priority', 'MEDIUM')
    )
    db.session.add(ticket)
    db.session.commit()
    return flask.jsonify({'message': 'Ticket created successfully', 'ticket_id': ticket.id}), 201

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    return flask.jsonify([{
        'id': t.id,
        'title': t.title,
        'description': t.description,
        'category': t.category,
        'status': t.status,
        'priority': t.priority,
        'assigned_to': t.assigned_to,
        'created_at': t.created_at.strftime('%Y-%m-%d %H:%M')
    } for t in tickets]), 200

@app.route('/api/tickets/<int:ticket_id>', methods=['PATCH'])
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    data = flask.request.json
    if 'status' in data:
        ticket.status = data['status']
    if 'assigned_to' in data:
        ticket.assigned_to = data['assigned_to']
    db.session.commit()
    return flask.jsonify({'message': 'Ticket updated successfully'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)