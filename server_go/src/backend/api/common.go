package api

import (
	"bytes"
	"encoding/gob"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
)

type errCode struct {
	SUCCESS int
	ERROR 	int
}

var ErrCode = errCode{
	SUCCESS: 0,
	ERROR: 	 1,
}

// 发送正确请求
func SendResp(c *gin.Context, data gin.H) {
	c.JSON(http.StatusOK, gin.H{
		"code": ErrCode.SUCCESS,
		"msg": "success",
		"data": data,
	})
}


// args: errNo, ...
// 如果服务器出错，返回错误信息和错误码
func SendErrResp(c *gin.Context, msg string, args ...interface{})  {

	var errNo = ErrCode.ERROR
	if len(args) != 0 {
		errNum, ok := args[0].(int)
		if !ok {
			panic("errNo error!")
		}
		errNo = errNum
	}

	c.JSON(http.StatusOK, gin.H{
		"code": errNo,
		"msg": msg,
		"data": gin.H{},
	})

	c.Abort()
}

// Clone deep-copies src to dst
// src, dst must be pointer
func Deepcopy(src, dst interface{}) error {

	//buff := new(bytes.Buffer)
	var buff bytes.Buffer
	enc := gob.NewEncoder(&buff)
	dec := gob.NewDecoder(&buff)
	if err := enc.Encode(src); err != nil {
		log.Print(err)
		return err
	}
	if err := dec.Decode(dst); err != nil {
		log.Print(err)
		return err
	}
	return nil
}
