// Test ProblemName
package main

import (
	"testing"
)

var tests = []struct {
	inName     string
	inYamlPath string
	out        int
}{
	{"Example Starter",
		"/home/truty/src/github.com/CloudVLab/gcp-ondemand-content/course_templates/EXAMPLE-STARTER-COURSE/qwiklabs.yaml",
		0},
}

func TestExampleProblem(t *testing.T) {
	for _, tt := range tests {
		t.Run(tt.inName, func(t *testing.T) {
			result := coursemapDescribe(tt.inYamlPath)
			if result != tt.out {
				t.Errorf("got %v, want %v", result, tt.out)
			}
		})
	}
}

// ExampleValidate runs a simple check of the validator.
func ExampleValidate() {
	coursemapValidate("schematest/schema1.json", "schematest/doc1.json")
	coursemapValidate("schematest/schema2.json", "schematest/doc2.json")
	coursemapValidate("schematest/schema3.json", "schematest/doc3.json")
	// Output:
	// Document schematest/doc1.json is valid.
	// Document schematest/doc2.json is valid.
	// Document schematest/doc3.json is valid.
}
