#!/usr/bin/env python3

from lime.application import RouteGroup
from app import app

api_group_v2 = RouteGroup(app, base_rule='/api/v2')

# 让Python加载模块，否则app.route装饰器不会运行，无法添加路由
from . import search
