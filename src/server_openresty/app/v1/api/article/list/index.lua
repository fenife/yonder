local cjson = require('cjson')

local res = {
    code = 2,
    data = "hello"
}

local res = {
    code = 0,
    data = {1, 2, 3},
    msg = "OK"
}

ngx.say(cjson.encode(res))

