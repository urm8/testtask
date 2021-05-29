from decimal import Decimal, InvalidOperation

from flask import current_app, g, jsonify, request


def get_tax():
    """
    Return tax amount for given annual_rate
    This is using docstrings for specifications.
    ---
    parameters:
      - name: rate
        in: query
        type: number
        required: true
      - name: detailed
        in: query
        type: boolean
        required: false
    definitions:
      TaxDetail:
        type: object
        properties:
            amount:
              type: number
            range:
              type: string
      Tax:
        type: object
        properties:
            amount:
              type: number
            rate:
              type: string, null
            details:
                $ref: '#/definitions/TaxDetail'
    responses:
      200:
        description: current rate
        schema:
            $ref: '#/definitions/Tax'
      400:
        description: in case rate request param is missing or given rate is not a valid number
    """
    try:
        rate = Decimal(request.args["rate"])
        return (
            jsonify(
                g.service.get_tax_amount(
                    rate, request.args.get("detailed") in [1, "true", True]
                )
            ),
            200,
        )
    except KeyError:
        current_app.logger.warning("rate was not given")
        return '"rate" query parameter is required', 400
    except InvalidOperation:
        current_app.logger.warning(f"invalid rate was given: {rate}")
        return '"rate" is not valid decimal', 400
