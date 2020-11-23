// Test ProblemName
package main

import (
	"reflect"
	"testing"
)

var tests = []struct {
	inName string
	in1    []int
	in2    []int
	out    []int
	outerr bool
}{
	{"simple 0", []int{}, []int{}, []int{}, false},
	{"simple 2a", []int{1, 2}, []int{}, []int{1, 2}, false},
	{"simple 3a", []int{}, []int{3, 4, 5}, []int{3, 4, 5}, false},
	{"simple 6a", []int{1, 2}, []int{4, 5, 6, 7}, []int{1, 2, 4, 5, 6, 7}, false},
	{"simple 6b", []int{1, 2, 3, 4, 5}, []int{-1}, []int{-1, 1, 2, 3, 4, 5}, false},
	{"simple 8a", []int{1, 3, 4, 5}, []int{2, 4, 6, 8}, []int{1, 2, 3, 4, 4, 5, 6, 8}, false},
}

func TestExampleProblem(t *testing.T) {
	for _, tt := range tests {
		t.Run(tt.inName, func(t *testing.T) {
			m, err := mergeTwoArrays(tt.in1, tt.in2)
			if !reflect.DeepEqual(m, tt.out) {
				t.Errorf("got %v, want %v", m, tt.out)
			} else if (err != nil) != tt.outerr {
				t.Errorf("got %v, want %v", err, tt.outerr)
			}
		})
	}
}

// Example functions are documentation.
// They demonstrate proper output of execution.
// They're run just like Tests as well, and printed with godoc package docs.
func ExamplePrint() {
	printTry()
	// Output: merge two arrays in go: try 'go test'.
}
