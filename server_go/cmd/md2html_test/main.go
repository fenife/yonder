package main

import (
	"fmt"
	"os"
	"server-go/pkg/md2html"
)

func readMds() []byte {
	configFile := "./test.md"
	data, err := os.ReadFile(configFile)
	if err != nil {
		panic(fmt.Sprintf("read file failed: %v", err))
	}
	return data
}

func writeHTMLs(html []byte) {
	err := os.WriteFile("test.html", html, 0666)
	if err != nil {
		fmt.Println(err)
	}
}

func main() {
	md := readMds()
	html := md2html.Parse(md)
	writeHTMLs(html)
}
