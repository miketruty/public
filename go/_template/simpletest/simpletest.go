// simpletest demonstrates very simple use of unit tests.
//
// INPUT FORMAT
//   None
//
// OUTPUT FORMAT
//   One line of text.
//
// SAMPLE INPUT
//   None
//
// SAMPLE OUTPUT
//   One: 1. Two: 2.
//
package main

import "fmt"

// ReturnOne is a public function that returns 1.
func ReturnOne() int {
	return 1
}

// returnTwo is a private function that returns 2.
func returnTwo() int {
	return 2
}

//
func printResults() {
	fmt.Printf("One: %d. Two: %d.\n", ReturnOne(), returnTwo())
}

// main is to execute with go run.
func main() {
	printResults()
}
