// Parse structure for course YAML files.
package main

import (
	"fmt"
	"io/ioutil"
	"os"

	"gopkg.in/yaml.v3"
)

// TODO(truty): figure out how to avoid stripping comments from the yaml.

// QwiklabsCourseYaml course templates parsed by Qwiklabs.
// The root node includes lists of resources and modules which reference the
// resources.
// Initial struct from: https://yaml.to-go.online/.
type QwiklabsCourseYaml struct {
	EntityType    string     `yaml:"entity_type"`
	SchemaVersion int        `yaml:"schema_version"`
	DefaultLocale string     `yaml:"default_locale"`
	Badge         string     `yaml:"badge"`
	Title         string     `yaml:"title"`
	Description   string     `yaml:"description"`
	Level         int        `yaml:"level"`
	Objectives    string     `yaml:"objectives"`
	Resources     []Resource `yaml:"resources"`
	Modules       []Module   `yaml:"modules"`
}

// Resource includes the videos and files included in Modules.
type Resource struct {
	Type             string `yaml:"type"`
	ID               string `yaml:"id"`
	Title            string `yaml:"title"`
	DriveURI         string `yaml:"drive_uri"`
	VideoProvider    string `yaml:"video_provider,omitempty"`
	VideoID          string `yaml:"video_id,omitempty"`
	Duration         int    `yaml:"duration,omitempty"`
	DriveMd5Checksum string `yaml:"drive_md5_checksum,omitempty"`
	URI              string `yaml:"uri,omitempty"`
}

// ActivityOption references one of type: resource, lab, quiz.
type ActivityOption struct {
	Type string `yaml:"type"`
	ID   string `yaml:"id"`
}

// Step references individual, ordered tasks with an id and activity.
type Step struct {
	ID              string           `yaml:"id"`
	ActivityOptions []ActivityOption `yaml:"activity_options"`
}

// Module is embedded in Course and includes videos and labs.
type Module struct {
	ID          string `yaml:"id"`
	Title       string `yaml:"title"`
	Description string `yaml:"description"`
	Objectives  string `yaml:"objectives"`
	Steps       []Step `yaml:"steps"`
}

// SimpleYamlConfig describes a simpler YAML course config with less metadata
// and more obvious visual readability.
type SimpleYamlConfig struct {
	EntityType    string `yaml:"entity_type"`
	SchemaVersion int    `yaml:"schema_version"`
	DefaultLocale string `yaml:"default_locale"`
	Badge         string `yaml:"badge"`
	Title         string `yaml:"title"`
	Description   string `yaml:"description"`
}

// readFile opens/reads the file in its entirety.
func readFile(filename string) []byte {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Printf("Error: cannot read file %s (%v).\n", filename, err)
		os.Exit(1)
	}

	return content
}

// parseCourseYaml deserializes a yaml file into an object.
func parseCourseYaml(yamlContent []byte) *QwiklabsCourseYaml {
	var qlconfig QwiklabsCourseYaml
	err := yaml.Unmarshal(yamlContent, &qlconfig)
	if err != nil {
		panic(err)
	}
	return &qlconfig
}
