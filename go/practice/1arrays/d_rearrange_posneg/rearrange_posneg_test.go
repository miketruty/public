// Test ProblemName
package main

import (
	"reflect"
	"testing"
)

var tests = []struct {
	inName string
	in     []int
	out    []int
}{
	{"simple 0", []int{}, []int{}},
	{"simple 1a", []int{-1}, []int{-1}},
	{"simple 1b", []int{9}, []int{9}},
	{"simple 2a", []int{1, -2}, []int{-2, 1}},
	{"simple 9a", []int{12, 11, -13, -5, 6, -7, 5, -3, -6}, []int{-13, -5, -7, -3, -6, 12, 11, 6, 5}},
}

func TestExampleProblem(t *testing.T) {
	for _, tt := range tests {
		t.Run(tt.inName, func(t *testing.T) {
			r := rearrangePosNeg(tt.in)
			if !reflect.DeepEqual(r, tt.out) {
				t.Errorf("got %v, want %v", r, tt.out)
			}
		})
	}
}

// Example functions are documentation.
// They demonstrate proper output of execution.
// They're run just like Tests as well, and printed with godoc package docs.
func ExamplePrint() {
	printTry()
	// Output: rearrange positive negative in go: try 'go test'.
}
