from rest_framework.schemas import AutoSchema
import coreapi


class VerifyPhoneNumbeSchemas2(AutoSchema):
    # def get_manual_fields(self, path, method):
    #     extra_fields = []
    #     print('******************')

    #     if method.lower() in ['post', 'get']:
    #         print('******************')
    #     extra_fields = [coreapi.Field('otp')]
    #     manual_fields = super().get_manual_fields(path, method)
    #     return extra_fields

    def get_schema_fields(self, view):
        return [coreapi.Field(
            name='name',
            location='query',
            required=False,
            type='string',
            description='name of recording'
        )]


class VerifyPhoneNumbeSchemas(AutoSchema):

    def get_manual_fields(self, path, method):
        return self._manual_fields

    # def get_operation(self, path, method):
    #     op = super().get_operation(path, method)
    #     op['parameters'].append({
    #         "name": "foo",
    #         "in": "query",
    #         "required": True,
    #         "description": "What foo does...",
    #         'schema': {'type': 'string'}
    #     })
    #     return op
