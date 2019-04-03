from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from . import models as m
from .extensions import starchart
from . import utils


class Cat(HTTPEndpoint):
    async def get(self, req: Request):
        """
        summary: Get single cat
        tags:
        - cat
        parameters:
        - name: id
          in: query
          required: True
          schema:
            type: integer
        responses:
          "200":
            description: OK
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Cat'
          "404":
            description: Not found
       """
        cat = await m.Cat.get(utils.parse_id(req.query_params.get("id")))
        return JSONResponse(cat.dict())

    async def put(self, req: Request):
        """
        summary: Update single cat
        tags:
        - cat
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                - id
                properties:
                  name:
                    type: string
                    maxLength: 32
                    description: naming cat
                  age:
                    type: integer
                  id:
                    type: integer
                    minimum: 1
        responses:
          "201":
            description: OK
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Cat'
          "404":
            description: Not found
       """
        data = await utils.get_json(req)

        cat = await m.Cat.get(utils.parse_id(data.get("id")))
        cat.name = data.get("name", cat.name)
        cat.age = data.get("age", cat.age)
        await cat.save()
        return JSONResponse(cat.dict())

    async def delete(self, req: Request):
        """
        summary: Delete single cat
        tags:
        - cat
        parameters:
        - name: id
          in: query
          required: True
          schema:
            type: integer
        responses:
          "204":
            description: OK
          "404":
            description: Not found
        """
        await m.Cat.delete(int(req.query_params.get("id")))
        return Response(status_code=204)


class Cats(HTTPEndpoint):
    async def get(self, req: Request):
        """
        summary: Get all cats
        tags:
        - cats
        parameters:
        - name: page
          in: query
          required: False
          schema:
            type: integer
            default: 1
            minimum: 1
        - name: count
          in: query
          required: False
          schema:
            type: integer
            default: 20
            maximum: 40
            minimum: 1
        responses:
          "200":
            description: OK
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Cats'
        """
        page, count = utils.parse_paginate(req)
        cats = await m.Cat.list(page=page, count=count)

        return JSONResponse(
            {"objects": [cat.dict() for cat in cats], "page": page, "count": count}
        )

    @starchart.schema_generator.schema_from("./docs/cats_post.yml")
    async def post(self, req: Request):
        data = await utils.get_json(req)

        cat = m.Cat(**data)
        cat.id = 0
        await cat.save()
        return JSONResponse(cat.dict())
