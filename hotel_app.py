from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)  # ← You’re missing this line

BOOKINGS_FILE = 'bookings.json'

def load_bookings():
    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_bookings(bookings):
    with open(BOOKINGS_FILE, 'w') as f:
        json.dump(bookings, f, indent=2)

@app.route('/')
def dashboard():
    bookings = load_bookings()
    stats = {
        'total_rooms': 120,
        'occupied': len([b for b in bookings if b['status'] == 'checked-in']),
        'available': 120 - len([b for b in bookings if b['status'] == 'checked-in']),
        'revenue': sum(b['total'] for b in bookings)
    }
    return render_template('Dashboard.html', stats=stats)  # Use your filename

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/staff')
def staff():
    staff_data = [
        {'name': 'Sarah Johnson', 'role': 'General Manager', 'exp': '12 years', 'img': 'https://i.pravatar.cc/150?img=1'},
        {'name': 'Michael Chen', 'role': 'Head Chef', 'exp': '15 years', 'img': 'https://i.pravatar.cc/150?img=2'},
        {'name': 'Emma Rodriguez', 'role': 'Front Desk Manager', 'exp': '8 years', 'img': 'https://i.pravatar.cc/150?img=3'},
        {'name': 'James Wilson', 'role': 'Concierge', 'exp': '10 years', 'img': 'https://i.pravatar.cc/150?img=4'}
    ]
    return render_template('staff_page.html', staff=staff_data)  # Use your filename

@app.route('/bookings')
def bookings():
    return render_template('book_now.html')  # Use your filename

@app.route('/api/bookings', methods=['GET', 'POST'])
def api_bookings():
    if request.method == 'POST':
        data = request.json
        bookings = load_bookings()
        data['id'] = len(bookings) + 1
        data['booked_at'] = datetime.now().isoformat()
        data['status'] = 'confirmed'
        bookings.append(data)
        save_bookings(bookings)
        return jsonify({'success': True, 'booking': data})
    
    return jsonify(load_bookings())

@app.route('/api/checkin/<int:booking_id>', methods=['POST'])
def checkin(booking_id):
    bookings = load_bookings()
    for b in bookings:
        if b['id'] == booking_id:
            b['status'] = 'checked-in'
            save_bookings(bookings)
            return jsonify({'success': True})
    return jsonify({'success': False}), 404

if __name__ == '__main__':
    app.run(debug=True)