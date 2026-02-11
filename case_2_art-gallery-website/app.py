from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'

db = SQLAlchemy(app)
class Concact(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100), nullable=False)
  submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
  def __repr__(self):
    return f'<Concact: {self.name} - {self.email} >'

with app.app_context():
  db.create_all()

@app.route('/')
def homepage():
  return render_template('index.html')

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
  try:
    name = request.form.get('name')
    email = request.form.get('email')
    if not name or not email:
      return jsonify({
        'success': False,
        'error': 'Name and email are required'
      }), 400
    
    new_contact = Concact(name=name, email=email)

    db.session.add(new_contact)
    db.session.commit()
    return jsonify({
      'success': True,
      'message': 'Submitted successfully',
      'data': {
        'name': name,
        'email': email
      }
    }), 200
  except Exception as e:
    return jsonify({
      'success': False,
      'error': str(e)
    }), 500

@app.route('/admin')
def view_contacts():
  contacts = Concact.query.all()
  concacts_list = []
  for contact in contacts:
    concacts_list.append(
      {
        'id': contact.id,
        'name': contact.name,
        'email': contact.email,
        'submitted_at': contact.submitted_at.strftime('%Y-%m-%d %H:%M:%S')
      }
    )
  return jsonify({
      'success': True,
      'contacts': concacts_list
    })

if __name__ == '__main__':
  app.run(debug=True)