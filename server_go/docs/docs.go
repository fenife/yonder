// Package docs Code generated by swaggo/swag. DO NOT EDIT
package docs

import "github.com/swaggo/swag"

const docTemplate = `{
    "schemes": {{ marshal .Schemes }},
    "swagger": "2.0",
    "info": {
        "description": "{{escape .Description}}",
        "title": "{{.Title}}",
        "termsOfService": "http://swagger.io/terms/",
        "contact": {},
        "version": "{{.Version}}"
    },
    "host": "{{.Host}}",
    "basePath": "{{.BasePath}}",
    "paths": {
        "/api/v1/user/signup": {
            "post": {
                "description": "创建新用户",
                "consumes": [
                    "application/json"
                ],
                "produces": [
                    "application/json"
                ],
                "tags": [
                    "users"
                ],
                "summary": "用户注册",
                "parameters": [
                    {
                        "description": "查询参数",
                        "name": "object",
                        "in": "body",
                        "schema": {
                            "$ref": "#/definitions/req.CreateUserReq"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "OK",
                        "schema": {
                            "$ref": "#/definitions/renderx.Response"
                        }
                    }
                }
            }
        },
        "/ping": {
            "get": {
                "produces": [
                    "application/json"
                ],
                "tags": [
                    "ping"
                ],
                "summary": "ping,检查服务是否正常",
                "responses": {
                    "200": {
                        "description": "OK",
                        "schema": {
                            "$ref": "#/definitions/renderx.Response"
                        }
                    }
                }
            }
        }
    },
    "definitions": {
        "renderx.Response": {
            "type": "object",
            "properties": {
                "data": {},
                "result": {
                    "$ref": "#/definitions/renderx.Result"
                }
            }
        },
        "renderx.Result": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "integer"
                },
                "msg": {
                    "type": "string"
                }
            }
        },
        "req.CreateUserReq": {
            "type": "object",
            "required": [
                "name",
                "password"
            ],
            "properties": {
                "name": {
                    "type": "string"
                },
                "password": {
                    "type": "string"
                }
            }
        }
    }
}`

// SwaggerInfo holds exported Swagger Info so clients can modify it
var SwaggerInfo = &swag.Spec{
	Version:          "1.0",
	Host:             "localhost:8030",
	BasePath:         "/",
	Schemes:          []string{},
	Title:            "yonder blog api",
	Description:      "yonder博客的后端API服务",
	InfoInstanceName: "swagger",
	SwaggerTemplate:  docTemplate,
	LeftDelim:        "{{",
	RightDelim:       "}}",
}

func init() {
	swag.Register(SwaggerInfo.InstanceName(), SwaggerInfo)
}
