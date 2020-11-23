#!/usr/bin/env bash

set -x # show commands

echo ----------------------------------------
echo .
go run ./main.go 
echo ----------------------------------------
echo .
go run main.go describe
echo ----------------------------------------
echo .
go run main.go help describe
echo ----------------------------------------
echo .
go run main.go simplify
echo ----------------------------------------
echo .
go run main.go help simplify
echo ----------------------------------------
echo .
go run main.go validate
echo ----------------------------------------
echo .
go run main.go help validate
echo ----------------------------------------
echo .
echo Done.
