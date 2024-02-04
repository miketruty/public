// Determine whether an integer is a palindrome. An integer is a palindrome when it reads the same backward as forward.
//
// Example 1:
//
// Input: 121
// Output: true
// Example 2:
//
// Input: -121
// Output: false
// Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.
// Example 3:
//
// Input: 10
// Output: false
// Explanation: Reads 01 from right to left. Therefore it is not a palindrome.
// Follow up:
//
// Coud you solve it without converting the integer to a string?
// Problem statement here, with example problems.
package main

import (
	"fmt"
)

// This version simple, but inefficient.
// func isPalindrome(x int) bool {
// 	fmt.Printf("%d.\n", x)
// 	if x < 0 {
// 		return false
// 	}
//
// 	s := strconv.Itoa(x)
// 	for i, j := 0, len(s)-1; i < j; i, j = i+1, j-1 {
// 		if s[i] != s[j] {
// 			return false
// 		}
// 	}
//
// 	return true
// }

// isPalindrome
func isPalindrome(x int) bool {
	// Negative numbers and any non-zero number ending in zero: not a palindrome.
	if x < 0 || (x > 9 && x%10 == 0) {
		return false
	}
	if x <= 9 {
		return true
	}

	var y int

	for x > y {
		y = (y * 10) + (x % 10)
		x /= 10
	}

	// Handle odd length numbers like 323, 50100
	if x != y {
		y /= 10
	}

	return y == x
}

func main() {
	fmt.Println("exampleProblem: try 'go test'")
}
