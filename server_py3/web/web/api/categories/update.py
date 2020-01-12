#!/usr/bin/env python3

from sim.exceptions import abort
from sim.context import AppRequestContext
from ...model import Category
from ...consts import RespCode, Permission, CATEGORY
from ...decorators import permission_required
from ...desc import ApiDescBase, api_desc_wrapper
from ... import app
from .. import api_group
from .._utils import clear_cache_data, to_int
from ._internal import get_cid_from_request


@api_group.route('/category/update', methods=('PUT', ))
@permission_required(Permission.admin)
def category_update(ctx: AppRequestContext):
    """分类更新"""
    # cid = ctx.request.get_param('cid')
    # try:
    #     cid = int(cid)
    # except Exception as e:
    #     app.logger.error(f"cid must be an integer, but get cid: {cid}")
    #     abort(RespCode.error, "cid must be an integer")
    cid = get_cid_from_request(ctx)

    input_json = ctx.request.json()
    if not input_json:
        abort(RespCode.error, "body data required")

    supported = {'name', }
    unsupported = set(input_json.keys()) - supported
    if unsupported:
        abort(RespCode.error, f"unsupported fields: {list(unsupported)}")

    cate = Category.find(cid)
    if not cate:
        abort(RespCode.error, f"category not existed")

    need_update = False
    if 'name' in input_json:
        name = input_json.get('name')

        # category name need update
        if name != cate.name:
            name = Category.valid_name(name)
            # check if category existed
            if Category.find_by_name(name) is not None:
                abort(RespCode.error, f"name `{name}` existed")

            cate.name = name
            need_update = True
        else:
            abort(RespCode.error, f"name `{name}` is the same as before")

    if need_update:
        if cate.modify() is False:
            app.logger.error("update category error")

    # 更新成功后，清除分类列表的缓存
    clear_cache_data("/api/category*")

    return cate


@api_group.route('/category/update/desc', methods=('PUT', ))
@api_desc_wrapper()
class ApiArticleUpdateDesc(ApiDescBase):
    name = "分类更新"
    desc = ""
    method = ['PUT']
    rule = "/api/category/update"

    def req_headers(self):
        headers = [
            # (key, val, desc)
            ('Cookie', 'token=xxx', "用户登录token"),
        ] + self.default_req_headers
        return headers

    def req_args(self):
        args = [
            # (key, name, type, default, required, desc)
            # (字段，字段名称，字段类型，默认值，是否必传，备注描述)
            ('cid', '分类ID', 'number', '', 1, ''),
        ]
        return args

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
            "url": self.url + "?cid=5",
            "note": "先登录，请求头部Cookie带上token",
            "request": {
                "body": {
                    "name": "fsfdsf"
                }
            },
            "response": {
                "code": 0,
                "data": {
                    "id": 5,
                    "created_at": "2020-01-12 10:02:28",
                    "updated_at": "2020-01-12 11:12:20",
                    "name": "fsfdsf",
                    "status": 1
                },
                "msg": "OK"
            }
        }
        return r
