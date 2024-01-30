#!/usr/bin/env python3

from sim.application import RouteGroup
from wes import app

api_group = RouteGroup(app, base_rule='/api')

# 让Python加载模块，否则app.route装饰器不会运行，无法添加路由
from . import users, categories, articles, about, archive, search
