#!/bin/bash

npm config set strict-ssl false  
npm config set registry https://registry.npm.taobao.org 
npm install
# npm run build
# 开发时，可以自动加载变化的程序文件
npm run dev

