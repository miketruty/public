// Given an array of integers, return indices of the two numbers such that they
// add up to a specific target.
// https://leetcode.com/problems/two-sum/
//
// You may assume that each input would have exactly one solution, and you may
// not use the same element twice.
//
// Example:
//
// Given nums = [2, 7, 11, 15], target = 9,
//
// Because nums[0] + nums[1] = 2 + 7 = 9,
// return [0, 1].
package main

import "fmt"

// twoSum returns the 2 indices of the numbers that sum to target.
func twoSum(nums []int, target int) []int {
	result := []int{-1, -1}

	for i := 0; i < len(nums)-1; i++ {
		for j := i + 1; j < len(nums); j++ {
			if nums[i]+nums[j] == target {
				return []int{i, j}
			}
		}
	}

	return result
}

func main() {
	fmt.Println("twoSum: try 'go test -test.v'")
}
