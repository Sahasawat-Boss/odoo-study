# from odoo import http


# class MyStudyModule(http.Controller):
#     @http.route('/my_study_module/my_study_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_study_module/my_study_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_study_module.listing', {
#             'root': '/my_study_module/my_study_module',
#             'objects': http.request.env['my_study_module.my_study_module'].search([]),
#         })

#     @http.route('/my_study_module/my_study_module/objects/<model("my_study_module.my_study_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_study_module.object', {
#             'object': obj
#         })

