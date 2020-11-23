// validate subcommand.
package main

import (
	"fmt"

	"github.com/ghodss/yaml"
	"github.com/xeipuuv/gojsonschema"
)

// coursemapValidate checks the coursemap template file against the schema.
//	import "github.com/xeipuuv/gojsonschema"
func coursemapValidate(s string, y string) int {
	var schema = `{"$schema":"http://json-schema.org/draft-07/schema#",` +
		`"$ref":"file://` + s + `"}`

	schemaLoader := gojsonschema.NewStringLoader(schema)

	j, err := yaml.YAMLToJSON(readFile(y))
	if err != nil {
		panic(err)
	}
	documentLoader := gojsonschema.NewStringLoader(string(j))

	result, err := gojsonschema.Validate(schemaLoader, documentLoader)
	if err != nil {
		panic(err.Error())
	}

	if result.Valid() {
		fmt.Printf("Document %s is valid.\n", y)
		for _, desc := range result.Errors() {
			fmt.Printf("- %s\n", desc)
		}
	} else {
		fmt.Printf("ERROR: document %s is not valid. See errors.\n", y)
		for _, desc := range result.Errors() {
			fmt.Printf("- %s\n", desc)
		}
	}

	return 0
}
