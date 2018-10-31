AGORA - Another Generator Of REST API

# What is AGORA

AGORA is a python library to generate client-side accessors for HTTP REST (or REST-like) API.

The goal is to hide every HTTP and formatting stuff to only focus on the use of the API.
Furthermore the library may enforce some checks input and output data to catch errors more easily.

The REST API may be defined in a number of way, including [Swagger](https://swagger.io/) or [RAML](https://raml.org) files.

### Simple Usage
```py
import agora
from agora.SwaggerParser import SwaggerParser


api = agora.create_api("https://petstore.swagger.io/v2/swagger.json", parser=SwaggerParser)


api.set_base_url("https://petstore.swagger.io/v2")

all_available_pets = api.pet.findByStatus.get(status="available")
if all_available_pets:
    first_pet = all_available_pets[0]

    print("now ordering ", first_pet["name"])
    order = api.store.order.post(petId=first_pet["id"], quantity=1)
    order_id = order["id"]

    print("Actually, it was impulse buy, cancel my order...")
    api.store.order(order_id).delete()
else:
    print("no pet available :(")
```
