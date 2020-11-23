// Parse (and reformat) Course Template YAML files.
//
// INPUT FORMAT
//   Course Template YAML file (qwiklabs.yaml) path.
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
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

const cmdDescribeCourse = "describecourse"
const cmdDescribeLab = "describelab"
const cmdExportCourse = "xcourse"
const cmdExportLab = "xlab"
const cmdExportQuest = "xquest"
const cmdSimplify = "simplify"
const cmdValidateCourse = "validatecourse"
const cmdYAMLToJSON = "yamltojson"

type subCommand struct {
	description string
}

var subCommands map[string]subCommand
var subCommandKeys []string

// init up a map of the subcommands to make it easier to document them.
func init() {
	subCommands = make(map[string]subCommand)
	subCommands[cmdDescribeCourse] = subCommand{
		"Show details about parsed course yaml"}
	subCommands[cmdDescribeLab] = subCommand{
		"Show details about parsed lab yaml"}
	subCommands[cmdExportCourse] = subCommand{
		"Export details from parsed course yaml to csv"}
	subCommands[cmdExportLab] = subCommand{
		"Export details from parsed lab yaml to csv"}
	subCommands[cmdExportQuest] = subCommand{
		"Export details from parsed quest yaml to csv"}
	subCommands[cmdSimplify] = subCommand{
		"Translate QL course yaml to simple yaml"}
	subCommands[cmdValidateCourse] = subCommand{
		"Check course yaml against schema"}
	subCommands[cmdYAMLToJSON] = subCommand{
		"Convert yaml file to json"}

	subCommandKeys = make([]string, 0, len(subCommands))
	for k := range subCommands {
		subCommandKeys = append(subCommandKeys, k)
	}
}

// usage prints the general syntax of the command.
func usage() {
	fmt.Printf("Usage: %s SUBCOMMAND yamlfile\n\n", filepath.Base(os.Args[0]))
	fmt.Printf("  SUBCOMMAND is one of:\n\n")
	for k, v := range subCommands {
		fmt.Printf("  %s: %s.\n", k, v.description)
	}
	flag.PrintDefaults()
}

// fileExists does the work of looking for a file.
func fileExists(fn string) string {
	y, err := filepath.Abs(fn)
	if err != nil {
		fmt.Printf("Error: cannot parse file path %s (%v).\n", fn, err)
		return ""
	}

	info, err := os.Stat(y)
	if os.IsNotExist(err) || info.IsDir() {
		fmt.Printf("Error: cannot find YAML file %s (%v).\n", y, err)
		return ""
	}
	return y
}

// checkYAMLExists checks for a yaml file argument, which should be an existing
// file, not a directory.
func checkYAMLExists(args []string) string {
	if len(args) != 1 {
		fmt.Println("Error: expected YAML file path.")
		flag.Usage()
		os.Exit(1)
	}

	fileYAML := fileExists(args[0])
	if fileYAML == "" {
		os.Exit(1)
	}
	return fileYAML
}

// main parses subcommand, flags, and args then invokes subcommand.
func main() {
	flag.Usage = usage

	describeCourseSet := flag.NewFlagSet(cmdDescribeCourse, flag.ExitOnError)
	describeLabSet := flag.NewFlagSet(cmdDescribeLab, flag.ExitOnError)
	exportCourseSet := flag.NewFlagSet(cmdExportCourse, flag.ExitOnError)
	exportLabSet := flag.NewFlagSet(cmdExportLab, flag.ExitOnError)
	exportQuestSet := flag.NewFlagSet(cmdExportQuest, flag.ExitOnError)
	simplifySet := flag.NewFlagSet(cmdSimplify, flag.ExitOnError)
	validateCourseSet := flag.NewFlagSet(cmdValidateCourse, flag.ExitOnError)
	validateSchema := validateCourseSet.String("schema", "schema/content_bundle.json",
		"Schema file to validate against")

	convertYAMLToJSONSet := flag.NewFlagSet(cmdYAMLToJSON, flag.ExitOnError)

	if len(os.Args) < 2 {
		fmt.Printf("Error: expected subcommand one of: %s.\n",
			strings.Join(subCommandKeys, ", "))
		os.Exit(1)
	}

	switch os.Args[1] {

	case cmdDescribeCourse:
		if err := describeCourseSet.Parse(os.Args[2:]); err != nil {
			panic(err)
		}
		fileYAML := checkYAMLExists(describeCourseSet.Args())
		coursemapDescribeCourse(fileYAML)

	case cmdDescribeLab:
		if err := describeLabSet.Parse(os.Args[2:]); err != nil {
			panic(err)
		}
		fileYAML := checkYAMLExists(describeLabSet.Args())
		coursemapDescribeLab(fileYAML)

	case cmdExportCourse:
		if err := exportCourseSet.Parse(os.Args[2:]); err != nil {
			panic(err)
		}
		fileYAML := checkYAMLExists(exportCourseSet.Args())
		coursemapExportCourse(fileYAML)

	case cmdExportLab:
		if err := exportLabSet.Parse(os.Args[2:]); err != nil {
			panic(err)
		}
		fileYAML := checkYAMLExists(exportLabSet.Args())
		coursemapExportLab(fileYAML)

	case cmdExportQuest:
		if err := exportQuestSet.Parse(os.Args[2:]); err != nil {
			panic(err)
		}
		fileYAML := checkYAMLExists(exportQuestSet.Args())
		coursemapExportQuest(fileYAML)

	case cmdSimplify:
		if err := simplifySet.Parse(os.Args[2:]); err != nil {
			panic(err)
		}
		fileYAML := checkYAMLExists(simplifySet.Args())
		coursemapSimplify(fileYAML)

	case cmdValidateCourse:
		if err := validateCourseSet.Parse(os.Args[2:]); err != nil {
			panic(err)
		}
		fileSchema := fileExists(*validateSchema)
		fileYAML := checkYAMLExists(validateCourseSet.Args())
		coursemapValidate(fileSchema, fileYAML)

	case cmdYAMLToJSON:
		if err := convertYAMLToJSONSet.Parse(os.Args[2:]); err != nil {
			panic(err)
		}
		fileYAML := checkYAMLExists(convertYAMLToJSONSet.Args())
		convertYAMLToJSON(fileYAML)

	default:
		flag.Usage()
	}
}
