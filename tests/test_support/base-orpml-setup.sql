
-- insert into public_api.document_type (
--     name,
--     format,
--     json_schema
-- ) values (
--     'orpml',
--     'json',
--     '{
--         "$schema": "http://json-schema.org/draft-04/schema",
--         "id": "http://example.com/example.json",
--         "type": "object",
--         "title": "The root schema",
--         "description": "The root schema comprises the entire JSON document.",
--         "default": {},
--         "examples": [
--             {
--                 "guidance_identifier": "",
--                 "guidance_element": "this is some guidance",
--                 "laid_pursuant_to": [
--                     {
--                         "document_key": "upkga/2020/01",
--                         "document_extent": null
--                     }
--                 ],
--                 "created_on": "2021-08-01",
--                 "valid_from": "2021-08-01"
--             }
--         ],
--         "required": [
--             "guidance_identifier",
--             "guidance_element",
--             "laid_pursuant_to",
--             "created_on",
--             "valid_from"
--         ],
--         "properties": {
--             "guidance_identifier": {
--                 "id": "#/properties/guidance_identifier",
--                 "type": "string",
--                 "title": "The guidance_identifier schema",
--                 "description": "An explanation about the purpose of this instance.",
--                 "default": "",
--                 "examples": [
--                     ""
--                 ]
--             },
--             "guidance_element": {
--                 "id": "#/properties/guidance_element",
--                 "type": "string",
--                 "title": "The guidance_element schema",
--                 "description": "An explanation about the purpose of this instance.",
--                 "default": "",
--                 "examples": [
--                     "this is some guidance"
--                 ]
--             },
--             "laid_pursuant_to": {
--                 "id": "#/properties/laid_pursuant_to",
--                 "type": "array",
--                 "title": "The laid_pursuant_to schema",
--                 "description": "An explanation about the purpose of this instance.",
--                 "default": [],
--                 "examples": [
--                     [
--                         {
--                             "document_key": "upkga/2020/01",
--                             "document_extent": null
--                         }
--                     ]
--                 ],
--                 "additionalItems": true,
--                 "items": {
--                     "id": "#/properties/laid_pursuant_to/items",
--                     "anyOf": [
--                         {
--                             "id": "#/properties/laid_pursuant_to/items/anyOf/0",
--                             "type": "object",
--                             "title": "The first anyOf schema",
--                             "description": "An explanation about the purpose of this instance.",
--                             "default": {},
--                             "examples": [
--                                 {
--                                     "document_key": "upkga/2020/01",
--                                     "document_extent": null
--                                 }
--                             ],
--                             "required": [
--                                 "document_key",
--                                 "document_extent"
--                             ],
--                             "properties": {
--                                 "document_key": {
--                                     "id": "#/properties/laid_pursuant_to/items/anyOf/0/properties/document_key",
--                                     "type": "string",
--                                     "title": "The document_key schema",
--                                     "description": "An explanation about the purpose of this instance.",
--                                     "default": "",
--                                     "examples": [
--                                         "upkga/2020/01"
--                                     ]
--                                 },
--                                 "document_extent": {
--                                     "id": "#/properties/laid_pursuant_to/items/anyOf/0/properties/document_extent",
--                                     "type": "null",
--                                     "title": "The document_extent schema",
--                                     "description": "An explanation about the purpose of this instance.",
--                                     "default": null,
--                                     "examples": [
--                                         null
--                                     ]
--                                 }
--                             },
--                             "additionalProperties": false
--                         }
--                     ]
--                 }
--             },
--             "created_on": {
--                 "id": "#/properties/created_on",
--                 "type": "string",
--                 "title": "The created_on schema",
--                 "description": "An explanation about the purpose of this instance.",
--                 "default": "",
--                 "examples": [
--                     "2021-08-01"
--                 ]
--             },
--             "valid_from": {
--                 "id": "#/properties/valid_from",
--                 "type": "string",
--                 "title": "The valid_from schema",
--                 "description": "An explanation about the purpose of this instance.",
--                 "default": "",
--                 "examples": [
--                     "2021-08-01"
--                 ]
--             }
--         },
--         "additionalProperties": false
--     }'::jsonb
-- );
