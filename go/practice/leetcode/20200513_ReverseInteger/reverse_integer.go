// Reverse Integer
// https://leetcode.com/problems/reverse-integer/
// Easy
//
// Given a 32-bit signed integer, reverse digits of an integer.
//
// Example 1:
//
// Input: 123
// Output: 321
//
// Example 2:
//
// Input: -123
// Output: -321
//
// Example 3:
//
// Input: 120
// Output: 21
//
// Note:
// Assume we are dealing with an environment which could only store integers
// within the 32-bit signed integer range: [−2**31,  2**31 − 1]. For the purpose
// of this problem, assume that your function returns 0 when the reversed
// integer overflows.
package main

import (
	"fmt"
	"math"
)

const maxCheck = math.MaxInt32 / 10
const minCheck = math.MinInt32 / 10

// checkOverflow determines if our result is about to overflow.
func checkOverflow(current int32, remainder int32) bool {
	// MaxInt32: 2147483647, MinInt32: -2147483648
	if (current > maxCheck) || (current == maxCheck && remainder > 7) {
		return true
	}
	if (current < minCheck) || (current == minCheck && remainder < -8) {
		return true
	}
	return false
}

func reverse(x int32) int32 {
	var result int32 = 0
	var remainder int32

	if x > -10 && x < 10 {
		return x
	}

	for x != 0 {
		remainder = x % 10

		if checkOverflow(result, remainder) {
			return 0
		}
		result = (result * 10) + remainder
		x /= 10
	}

	return result
}

func main() {
	fmt.Println("reverse: try 'go test'")
}
