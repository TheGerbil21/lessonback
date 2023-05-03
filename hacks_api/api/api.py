from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse
from .. import db
from ..model.model import Computer

computer_bp = Blueprint("computers", __name__)
computer_api = Api(computer_bp)

def get_name_list():
    names_list = [[name._name] for name in Computer.query.all()]
    return names_list

def find_by_name(name):
    names = Computer.query.filter_by(_name=name).all()
    return names[0]


class ComputerAPI(Resource):
    def get(self):
        name = request.get_json().get("name")
        print(name, "name")
        name = find_by_name(name)
        if name:
            return name.to_dict()
        return {"message": name}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True, type=str)
        parser.add_argument("year", required=True, type=int)
        parser.add_argument("age", required=True, type=int)
        args = parser.parse_args()

        computer = Computer(args["name"], args["year"],
                                  args["age"])
        try:
            db.session.add(computer)
            db.session.commit()
            return computer.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def put(self):
        name = request.get_json().get("name")
        print(name, "name")

        try:
            name = find_by_name(name)
            if name:
                name.year = int(request.get_json().get("year"))
                name.age = int(request.get_json().get("age"))
                db.session.commit()
                return name.to_dict(), 201
            else:
                return {"message": "computer not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def delete(self):
        name = request.get_json().get("name")
        print(name, "name")

        try:
            name = find_by_name(name)
            if name:
                db.session.delete(name)
                db.session.commit()
                return name.to_dict()
            else:
                return {"message": "computer not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500


class ComputerListAPI(Resource):
    def get(self):
        try:
            computers = db.session.query(Computer).all()
            return [computer.to_dict() for computer in computers]
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def delete(self):
        try:
            db.session.query(Computer).delete()
            db.session.commit()
            return []
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500
        


computer_api.add_resource(ComputerAPI, "/computer")
computer_api.add_resource(ComputerListAPI, "/computerList")