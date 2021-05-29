import os
import sys
from pathlib import Path

from flasgger import Swagger
from flask import Flask, g

import _orjson
import api
from storage.json_storage import JSONStorage


def get_storage() -> JSONStorage:
    import json
    import jsonschema

    if path := os.environ.get("TAX_BANDS_SRC"):
        path = Path(path).resolve()
        if not path.exists():
            print(f"could not resolve path: {path}", file=sys.stderr)
            sys.exit(1)
        with open(Path(__file__).parent / "storage" / "schema") as schema, open(
            path
        ) as fin:
            try:
                schema = json.load(schema)
                source = json.load(fin)
                jsonschema.validate(source, schema=schema)
            except jsonschema.ValidationError as err:
                print(
                    f"given json file is not valid against schema: {err}",
                    file=sys.stderr,
                )
                sys.exit(1)
            except ValueError:
                print(
                    f'given json file "{path.absolute()}" is not valid json',
                    file=sys.stderr,
                )
                sys.exit(1)
    else:
        path = Path(__file__).parent / "storage" / "tax_bands.json"
    return JSONStorage(path)


STORAGE = get_storage()


def create_app(test_config=None):
    # create and configure the app
    app = _orjson.setup(Flask(__name__, instance_relative_config=True))
    Swagger(
        app,
        config={
            **Swagger.DEFAULT_CONFIG,
            **{"swagger_ui": True, "specs_route": "/docs/"},
        },
    )
    app.config.from_mapping(SECRET_KEY=os.environ.get("SECRET_KEY", "dev"))

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    @app.before_request
    def init_service():
        from service import Service

        g.service = Service(STORAGE)

    app.get("/tax")(api.get_tax)
    return app


app = create_app()
