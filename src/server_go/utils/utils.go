package utils

import (
	"encoding/json"
	"fmt"
)

func PrettyPrint(v interface{}) {
	b, err := json.MarshalIndent(v, "", "  ")
	if err != nil {
		fmt.Println(err.Error())
	} else {
		fmt.Println(string(b))
	}
}
