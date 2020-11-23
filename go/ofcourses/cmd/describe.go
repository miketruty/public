/*
Copyright © 2020 NAME HERE <EMAIL ADDRESS>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
package cmd

import (
	"fmt"
	"os"
	"path/filepath"

    "github.com/miketruty/spas/go/ofcourses/util"
	"github.com/spf13/cobra"
)

// describeCmd represents the describe command
var describeCmd = &cobra.Command{
	Use:     "describe",
	Aliases: []string{"de", "desc"},
	Short:   "Show details about parsed course yaml",
	Long: `A longer description that spans multiple lines and likely contains examples
and usage of using your command. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	Args: func(cmd *cobra.Command, args []string) error {
		return validateArgs(cmd, args)
	},
	RunE: func(cmd *cobra.Command, args []string) error {
		return describeInternal(args[0])
	},
}

func init() {
	rootCmd.AddCommand(describeCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// describeCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// describeCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}

func describeInternal(yf string) error {
	fmt.Printf("describe called with %s\n", yf)
	// TODO(truty): let's do some REAL YAML parsing now!!
	//              problably need a struct def for the base course bundle yaml
	//              schema.
	qlconfig := parseYaml(readFile(yf))

	fmt.Printf("entity_type: %s\n", qlconfig.EntityType)
	fmt.Printf("schema_version: %d\n", qlconfig.SchemaVersion)
	fmt.Printf("default_locale: %s\n", qlconfig.DefaultLocale)
	fmt.Printf("badge: %s\n", qlconfig.Badge)
	fmt.Printf("title: %s\n", qlconfig.Title)
	fmt.Printf("description: %s\n", qlconfig.Description)
	fmt.Printf("level: %d\n", qlconfig.Level)
	fmt.Printf("objectives: %s\n", qlconfig.Objectives)
	fmt.Printf("resources: %v\n", qlconfig.Resources)
	fmt.Printf("modules: %v\n", qlconfig.Modules)
	return nil
}
