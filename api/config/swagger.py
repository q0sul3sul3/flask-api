template = {
    "swagger": "2.0",
    "info": {
        "title": "Flask API",
        "description": "APIs for Senao",
        "contact": {
            "responsibleOrganization": "Me",
            "responsibleDeveloper": "Me",
            "email": "q0sul3sul3@gmail.com",
            "url": "https://github.com/q0sul3sul3",
        },
        # "termsOfService": "http://me.com/terms",
        "version": "0.0.1"
    },
    # "host": "127.0.0.1:3000",  # overrides localhost:500
    "basePath": "/api/v1",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "operationId": "getmyData"
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}