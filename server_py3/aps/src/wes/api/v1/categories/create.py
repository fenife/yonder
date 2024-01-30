#!/usr/bin/env python3

from sim.exceptions import abort
from sim.context import AppRequestContext
from wes.model import Category
from wes.consts import RespCode, Permission, CATEGORY
from wes.api.decorators import permission_required
from wes.api.desc import ApiDescBase, api_desc_wrapper
from .. import api_group
from wes.api._utils import clear_cache_data


@api_group.route('/category/create', methods=('POST', ))
@permission_required(Permission.admin)
def category_create(ctx: AppRequestContext):
    """分类新建"""
    input_json = ctx.request.json()
    if not input_json or "name" not in input_json:
        abort(RespCode.error, "field `name` is required")

    name = Category.valid_name(input_json['name'])

    # check if category name existed
    if Category.find_by_name(name) is not None:
        abort(RespCode.error, f"name `{name}` existed")

    cate = Category()
    cate.name = name
    cate.status = CATEGORY.status.active

    cate.save()
    if getattr(cate, 'id', None) is None:
        abort(RespCode.error, "create new category error")

    # 创建成功后，清除分类列表的缓存
    clear_cache_data("/api/category*")
    clear_cache_data('/api/article*')

    return cate


@api_group.route('/category/create/desc', methods=('POST', ))
@api_desc_wrapper()
class ApiCateCreateDesc(ApiDescBase):
    name = "分类新建"
    desc = ""
    method = ['POST']
    rule = "/api/category/create"

    def req_headers(self):
        headers = [
            # (key, val, desc)
            ('Cookie', 'token=xxx', "用户登录token"),
        ] + self.default_req_headers
        return headers

    def req_body(self):
        # {
        # 	"name": "aabb"
        # }
        body = [
            # (key, name, type, default, required, desc)
            ('name',   '分类名称', 'string', '', 1, ''),
        ]
        return body

    @property
    def example(self):
        r = {
            "url": self.url,
            "note": "先登录，请求头部Cookie带上token",
            "request": {
                "body": {
                    "name": "aabb"
                }
            },
            "response": {
                "code": 0,
                "data": {
                    "name": "aabb",
                    "status": 1,
                    "created_at": "2020-01-12 10:02:28",
                    "updated_at": "2020-01-12 10:02:28",
                    "id": 5
                },
                "msg": "OK"
            }
        }
        return r
