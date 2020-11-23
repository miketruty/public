// <Detailed question text>
//
// INPUT FORMAT
//   <add>
//
// OUTPUT FORMAT
//   <add>
//
// SAMPLE INPUT
//   <add>
//
// SAMPLE OUTPUT
//   <add>
//
package main

import (
	"fmt"
)

// ProblemName is the package-level label of the coding problem.
const ProblemName = "[replace me]"

// TODO(truty): replace any helper functions.
func helperFunc(s string) int {
	// TODO(truty): write code
	fmt.Println("helperFunc: " + s)
	return 0
}

// TODO(truty): Grab function from leetcode prototype.
func exampleProblem(in string) int {
	result := 0

	// TODO(truty): write code
	result = helperFunc(in)

	return result
}

func printTry() {
	fmt.Printf("%s in go: try 'go test'.\n", ProblemName)
}

func main() {
	printTry()
}
