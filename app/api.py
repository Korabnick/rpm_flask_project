from flask import jsonify
from app.models import Location
from flask_login import login_required
from app import app

@app.route('/api/locations', methods=['GET'])
@login_required
def get_locations():
    locations = Location.query.all()
    locations_list = []
    for location in locations:
        location_data = {
            'id': location.id,
            'name': location.name,
            'image': location.image,
            'location': location.location,
            'rental_price': location.rental_price,
            'description': location.description
        }
        locations_list.append(location_data)
    return jsonify({'locations': locations_list})
