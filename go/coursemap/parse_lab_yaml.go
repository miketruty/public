// Parse structure for YAML files.
package main

import (
	"gopkg.in/yaml.v3"
)

// TODO(truty): figure out how to avoid stripping comments from the yaml.

// QwiklabsLabYaml course templates parsed by Qwiklabs.
// The root node includes lists of resources and modules which reference the
// resources.
// Initial struct from: https://yaml.to-go.online/.
type QwiklabsLabYaml struct {
	SchemaVersion        int                   `yaml:"schema_version"`
	Title                string                `yaml:"title"`
	Description          string                `yaml:"description"`
	DefaultLocale        string                `yaml:"default_locale"`
	Duration             int                   `yaml:"duration"`
	MaxDuration          int                   `yaml:"max_duration"`
	Level                string                `yaml:"level"`
	Tags                 []string              `yaml:"tags"`
	Credits              int                   `yaml:"credits"`
	Tagline              string                `yaml:"tagline"`
	Resources            []LabResource         `yaml:"resources"`
	EnvironmentResources []EnvironmentResource `yaml:"environment_resources"`
	Assessment           string                `yaml:"assessment"`
}

// LabResource includes the videos and files referenced by Labs.
type LabResource struct {
	ID          string      `yaml:"id"`
	Title       string      `yaml:"title"`
	Description interface{} `yaml:"description"`
	Type        string      `yaml:"type"`
	URI         string      `yaml:"uri"`
}

// EnvironmentResource describes runtime setup.
type EnvironmentResource struct {
	Type           string       `yaml:"type"`
	ID             string       `yaml:"id"`
	Permissions    []Permission `yaml:"permissions,omitempty"`
	DefaultRegion  string       `yaml:"default_region,omitempty"`
	DefaultZone    string       `yaml:"default_zone,omitempty"`
	AvailableZones []string     `yaml:"available_zones,omitempty"`
	DmTemplate     DmTemplate   `yaml:"dm_template,omitempty"`
}

// Permission is used to set runtime roles.
type Permission struct {
	Project string   `yaml:"project"`
	Roles   []string `yaml:"roles"`
}

// DmTemplate is used to identify an automation template file.
type DmTemplate struct {
	Script string `yaml:"script"`
}

// parseLabYaml deserializes a yaml file into an object.
func parseLabYaml(yamlContent []byte) *QwiklabsLabYaml {
	var qlconfig QwiklabsLabYaml
	err := yaml.Unmarshal(yamlContent, &qlconfig)
	if err != nil {
		panic(err)
	}
	return &qlconfig
}
