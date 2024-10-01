from drf_yasg.inspectors import SwaggerAutoSchema

class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        tags = super().get_tags(operation_keys)
        if operation_keys:
            if operation_keys[0] == 'v1':
                tags = ['Login API']
            else:
                tags = [operation_keys[0]]
        return tags

    def get_operation(self, operation_keys=None):
        operation = super().get_operation(operation_keys)
        # Customizando a ordem dos grupos
        if 'tags' in operation:
            if operation['tags'] == ['Login API']:
                operation['x-order'] = 1  # Define o valor de ordem para "Login API"
            elif operation['tags'] == ['items']:
                operation['x-order'] = 2
            elif operation['tags'] == ['robots']:
                operation['x-order'] = 3
            elif operation['tags'] == ['tasks']:
                operation['x-order'] = 4
        return operation
