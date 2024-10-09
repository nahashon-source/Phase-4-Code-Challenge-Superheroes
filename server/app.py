from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models here
from models import Hero, Power, HeroPower

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes])

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get_or_404(id)
    return jsonify({'id': hero.id, 'name': hero.name, 'super_name': hero.super_name})

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([{'id': power.id, 'name': power.name, 'description': power.description} for power in powers])

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get_or_404(id)
    return jsonify({'id': power.id, 'name': power.name, 'description': power.description})

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    strength = data.get('strength')
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')

    if strength not in ['Strong', 'Weak', 'Average']:
        return jsonify({'errors': ["Strength must be Strong, Weak, or Average"]}), 400

    hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
    db.session.add(hero_power)
    db.session.commit()
    return jsonify({'id': hero_power.id, 'hero_id': hero_power.hero_id, 'power_id': hero_power.power_id, 'strength': hero_power.strength}), 201

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

