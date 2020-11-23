package cmd

import (
	"fmt"

	"github.com/spf13/cobra"

	"github.com/miketruty/spas/go/ofcourses/util"
)

// validateArgs used to check all commands for positional yaml file.
func validateArgs(cmd *cobra.Command, args []string) error {
	if len(args) != 1 {
		return fmt.Errorf("need the yaml file to validate")
	}
	return util.FileExists(args[0])
}
