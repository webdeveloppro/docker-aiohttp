from marshmallow import Schema, fields, validate


class ItemSchema(Schema):
    # id = fields.Integer(load_only=True)
    text = fields.String(validate=[validate.Length(min=5, max=255)])
    date_posted = fields.DateTime(load_only=True)
