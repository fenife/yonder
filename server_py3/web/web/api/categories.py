#!/usr/bin/env python3

from sim.exceptions import abort
from .. import app, db, cache_pool
from ..model import Category
from ..consts import RespCode, Permission, RoleUser, RoleAdmin, Roles, USER, CATEGORY, ARTICLE
from ..decorators import permission_required, login_required


@app.route('/api/category', methods=('POST', ))
@permission_required(Permission.admin)
def category_create(ctx):
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
        abort(RespCode.error, "create new user error")

    return cate


@app.route('/api/category/:cid', methods=('PUT', ))
@permission_required(Permission.admin)
def category_update(ctx):
    cid = ctx.request.get_param('cid')
    try:
        cid = int(cid)
    except Exception as e:
        app.logger.error(f"cid must be an integer, but get cid: {cid}")
        abort(RespCode.error, "cid must be an integer")

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
        name = input_json.pop('name')

        # categroy name need update
        if name != cate.name:
            username = Category.valid_name(name)
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

    return cate


@app.route('/api/category/:cid', methods=('GET', ))
def category_retrieve(ctx):
    cid = ctx.request.get_param('cid')
    try:
        cid = int(cid)
    except Exception as e:
        app.logger.error(f"cid must be an integer, but get cid: {cid}")
        abort(RespCode.error, "in GET method, cid must be an integer")

    cate = Category.find(cid)
    if not cate:
        abort(RespCode.error, "category not found")

    return cate


@app.route('/api/category', methods=('GET', ))
def category_list(ctx):
    data = Category.find_all()
    return data


def category_delete(ctx):
    pass
