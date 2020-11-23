// Test ProblemName
package main

import (
	"testing"
)

// TODO(truty): replace test data.
var tests = []struct {
	inName string
	in     string
	out    int
}{
	{"simple 1a", "aaa", 0},
}

func TestExampleProblem(t *testing.T) {
	for _, tt := range tests {
		t.Run(tt.inName, func(t *testing.T) {
			// TODO(truty): replace exampleProblem
			result := exampleProblem(tt.in)
			if result != tt.out {
				t.Errorf("got %v, want %v", result, tt.out)
			}
		})
	}
}

// Example functions are documentation.
// They demonstrate proper output of execution.
// They're run just like Tests as well, and printed with godoc package docs.
func ExamplePrint() {
	printTry()
	// Output: [replace me] in go: try 'go test'.
}
