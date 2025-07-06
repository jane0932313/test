from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required
from extensions import db
from models.device import Device

device_bp = Blueprint('device', __name__, url_prefix='/devices')

#增加设备
@device_bp.route('', methods=['POST'])
@jwt_required()
def create_device():
    data = request.json
    new_device = Device(
        name=data['name'],
        type=data['type'],
        status=data['status'],
        location=data['location']
    )
    db.session.add(new_device)
    db.session.commit()
    return jsonify({'message':'设备添加成功', 'device':new_device.to_dict()}), 201

#查询所有设备
@device_bp.route('', methods=['GET'])
def get_devices():
    devices = Device.query.all()
    return jsonify([device.to_dict() for device in devices])

#查询单个设备
@device_bp.route('/<int:device_id>', methods=['GET'])
def get_device(device_id):
    device = Device.query.get_or_404(device_id)
    return jsonify(device.to_dict())

#更新设备
@device_bp.route('/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    device = Device.query.get_or_404(device_id)
    data = request.json
    device.name = data.get('name', device.name)
    device.type = data.get('type', device.type)
    device.status = data.get('status', device.status)
    device.location = data.get('location', device.location)
    db.session.commit()
    return jsonify({'message':'设备更新成功','device':device.to_dict()})

# 删除设备
@device_bp.route('/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    device = Device.query.get_or_404(device_id)
    db.session.delete(device)
    db.session.commit()
    return jsonify({'message': '设备删除成功'})

@device_bp.route('/page', methods=['GET'])
def device_page():
    return render_template('index.html')

