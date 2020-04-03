package utils

import (
	"bytes"
	"encoding/gob"
	"encoding/json"
	"fmt"
	"log"
)

func PrettyPrint(v interface{}) {
	b, err := json.MarshalIndent(v, "", "  ")
	if err != nil {
		fmt.Println(err.Error())
	} else {
		fmt.Println(string(b))
	}
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
