from flask import Blueprint, request, render_template
from flask import jsonify

from database.sql_alchemy_init import db

from database.models.label import Label

label = Blueprint('label', __name__)


@label.route("/get-all", methods=['GET'])
def label_get_all():
    label_list = Label.query.all()
    result = [label.serialize() for label in label_list]
    return render_template('label_management.html', label_list = enumerate(result, start=0) )
    # return jsonify(
    #     data=result,
    #     message='Lấy danh sách nhãn thành công',
    #     status=200
    # ), 200


@label.route("/save", methods=['POST'])
def label_save():
    if request.data:
        data = request.get_json()

        if 'name' not in data or data['name'] == '':
            return jsonify(
                data=None,
                message='Tên nhãn không được bỏ trống',
                status=400
            ), 400
        elif 'status' not in data or data['status'] == '':
            return jsonify(
                data=None,
                message='Trạng thái nhãn không được bỏ trống',
                status=400
            ), 400

        name = data['name']
        status = data['status']

        label = Label(name, status)

        db.session.add(label)
        db.session.commit()

        return jsonify(
            data=label.serialize(),
            message='Thêm mới thành công',
            status=200
        ), 200


@label.route("/update/<int:id>", methods=['POST'])
def label_update(id):
    label = Label.query.get(id)

    if label == None:
        return jsonify(
            data=None,
            message='Nhãn không tồn tại',
            status=400
        ), 400

    if request.data:
        data = request.get_json()

        if 'name' not in data or data['name'] == '':
            return jsonify(
                data=None,
                message='Tên nhãn không được bỏ trống',
                status=400
            ), 400
        elif 'status' not in data or data['status'] == '':
            return jsonify(
                data=None,
                message='Trạng thái nhãn không được bỏ trống',
                status=400
            ), 400

        label.name = data['name']
        label.status = data['status']

        db.session.commit()

        return jsonify(
            data=label.serialize(),
            message='Sửa mới thành công',
            status=200
        ), 200


@label.route("/detail/<int:id>", methods=['GET'])
def label_detail(id):
    label = Label.query.get(id)

    if label == None:
        return jsonify(
            data=None,
            message='Nhãn không tồn tại',
            status=400
        ), 400

    return jsonify(
            data=label.serialize(),
            message='Lấy thông tin chi tiết nhãn thành công',
            status=200
        ), 200


@label.route("/delete/<int:id>", methods=['GET'])
def label_delete(id):
    label = Label.query.get(id)

    if label == None:
        return jsonify(
            data=None,
            message='Nhãn không tồn tại',
            status=400
        ), 400

    db.session.delete(label)
    db.session.commit()

    return jsonify(
        data=None,
        message='Xóa thành công',
        status=200
    ), 200
