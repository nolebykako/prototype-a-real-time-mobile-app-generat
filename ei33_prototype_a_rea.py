import os
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app_generator.db"
db = SQLAlchemy(app)

class App(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    template = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/generate', methods=['POST'])
def generate_app():
    data = request.get_json()
    app_name = data.get('name')
    app_description = data.get('description')
    template_id = data.get('template_id')

    if not app_name or not app_description or not template_id:
        return jsonify({'error': 'missing required fields'}), 400

    template = Template.query.get(template_id)
    if not template:
        return jsonify({'error': 'template not found'}), 404

    app = App(name=app_name, description=app_description, template=template.name)
    db.session.add(app)
    db.session.commit()

    generated_code = generate_code(template.code, app_name)
    return jsonify({'app_id': app.id, 'generated_code': generated_code})

def generate_code(template_code, app_name):
    # todo: implement code generation logic
    return template_code.replace('{{app_name}}', app_name)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)