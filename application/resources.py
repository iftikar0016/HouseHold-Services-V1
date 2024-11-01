from flask import jsonify, request
from flask_restful import Api, Resource, fields, marshal_with
from flask_security import auth_required, current_user, roles_required
from application.models import Professional, Service, db


api = Api(prefix='/api')

professional_fields = {
    'id' : fields.Integer,
    'fullname' : fields.String,
    'address' : fields.String,
    'user_id' : fields.Integer,
    'service_id' : fields.Integer,
}

service_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'price' : fields.Float,
    'description' : fields.String,
    'time_required' : fields.Integer,
}


# class BlogAPI(Resource):

#     @marshal_with(blog_fields)
#     @auth_required('token')
#     def get(self, blog_id):
#         blog = Blog.query.get(blog_id)

#         if not blog:
#             return {"message" : "not found"}, 404
#         return blog
    
#     @auth_required('token')
#     def delete(self, blog_id):

#         blog = Blog.query.get(blog_id)

#         if not blog:
#             return {"message" : "not found"}, 404
        
#         if blog.user_id == current_user.id:

#             db.session.delete(blog)
#             db.session.commit()
#         else:
#             return {"message" : "not valid user"}, 403
        

class ProfessionalsListAPI(Resource):

    @marshal_with(professional_fields)
    @auth_required('token')
    def get(self ):
        pofessionals = Professional.query.all()
        return pofessionals
    
    # @auth_required('token')
    # def post(self):
    #     data = request.get_json()
    #     title = data.get('title')
    #     caption = data.get('caption')
    #     image_url = data.get('image_url')

    #     blog = Blog(title = title, caption = caption, image_url = image_url, user_id = current_user.id)

    #     db.session.add(blog)
    #     db.session.commit()
    #     return jsonify({'message' : 'blog created'})

class ServiceListAPI(Resource):
    @marshal_with(service_fields)
    @auth_required('token')
    def get(self):
        services = Service.query.all()
        return services
    
    @roles_required('admin')
    @auth_required('token')
    def post(self):
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        description = data.get('description')
        new_service = Service(name=name, price=price, description=description)
        db.session.add(new_service)
        db.session.commit()
        return jsonify({'message' : 'New service added'})

api.add_resource(ServiceListAPI, '/services')
api.add_resource(ProfessionalsListAPI,'/professionals')