# ofcourses - CLI for working with Qwiklabs course YAML.

## Creating the Cobra CLI application

I used the go
[Cobra library](https://github.com/spf13/cobra/blob/master/cobra/README.md)
to create the CLI code scaffold.

```
go get -u github.com/spf13/cobra/cobra
cobra init --pkg-name github.com/miketruty/spas/go/ofcourses
cobra add describe
cobra add validate
cobra add simplify
```

## Experimenting

To try commands.

```
go run main.go
go run main.go describe
go run main.go help describe
```

