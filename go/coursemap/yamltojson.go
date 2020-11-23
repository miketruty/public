// yamltojson subcommand.
package main

import (
	"fmt"

	"github.com/ghodss/yaml"
)

// convertYAMLToJSON emits JSON converted from YAML.
func convertYAMLToJSON(y string) int {
	s, err := yaml.YAMLToJSON(readFile(y))
	if err != nil {
		panic(err)
	}
	fmt.Print(string(s))

	return 0
}
