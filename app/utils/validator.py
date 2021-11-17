from dataclasses import asdict


class Validator:

    def validate(self, dto, schema):
        schema().load(asdict(dto))
