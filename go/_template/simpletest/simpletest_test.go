package main

import "testing"

func TestReturnOne(t *testing.T) {

	result := ReturnOne()
	if result != 1 {
		t.Errorf("Expected 1 but returned %d.", result)
	}
}

func TestReturnTwo(t *testing.T) {

	result := returnTwo()
	if result != 2 {
		t.Errorf("Expected 2 but returned %d.", result)
	}
}

func ExamplePrints() {
	printResults()
	// Output: One: 1. Two: 2.
}
