// Parse structure for YAML files.
package main

import (
	"gopkg.in/yaml.v3"
)

// TODO(truty): figure out how to avoid stripping comments from the yaml.

// QwiklabsQuestYaml course templates parsed by Qwiklabs.
// The root node includes lists of resources and modules which reference the
// resources.
// Initial struct from: https://yaml.to-go.online/.
type QwiklabsQuestYaml struct {
	EntityType             string          `yaml:"entity_type"`
	SchemaVersion          int             `yaml:"schema_version"`
	DefaultLocale          string          `yaml:"default_locale"`
	Badge                  string          `yaml:"badge"`
	LearningPathCollection string          `yaml:"learning_path_collection"`
	Title                  string          `yaml:"title"`
	Description            string          `yaml:"description"`
	Objectives             string          `yaml:"objectives"`
	Level                  int             `yaml:"level"`
	Tags                   []string        `yaml:"tags"`
	ProductTags            []string        `yaml:"product_tags"`
	RoleTags               []string        `yaml:"role_tags"`
	DomainTags             []string        `yaml:"domain_tags"`
	Modules                []QuestModule   `yaml:"modules"`
	Resources              []QuestResource `yaml:"resources"`
}

// QuestStep references individual, ordered tasks with an id and activity.
type QuestStep struct {
	ID              string           `yaml:"id"`
	Optional        bool             `yaml:"optional"`
	ActivityOptions []ActivityOption `yaml:"activity_options"`
}

// QuestModule is the module of the quest
type QuestModule struct {
	ID          string      `yaml:"id"`
	Title       string      `yaml:"title"`
	Description string      `yaml:"description"`
	Objectives  string      `yaml:"objectives"`
	Steps       []QuestStep `yaml:"steps"`
}

// QuestResource includes the videos and files referenced by Labs.
type QuestResource struct {
	Type          string `yaml:"type"`
	ID            string `yaml:"id"`
	Title         string `yaml:"title"`
	VideoProvider string `yaml:"video_provider,omitempty"`
	VideoID       string `yaml:"video_id,omitempty"`
	Duration      int    `yaml:"duration,omitempty"`
}

// parseQuestYaml deserializes a yaml file into an object.
func parseQuestYaml(yamlContent []byte) *QwiklabsQuestYaml {
	var qlconfig QwiklabsQuestYaml
	err := yaml.Unmarshal(yamlContent, &qlconfig)
	if err != nil {
		panic(err)
	}
	return &qlconfig
}
