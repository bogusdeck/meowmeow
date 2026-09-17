package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
)

var (
	preferredProvider = getEnvOrDefault("OVERLAY_PROVIDER", "ollama")
	ollamaURL         = getEnvOrDefault("OLLAMA_URL", "http://localhost:11434/api/generate")
	ollamaTagsURL     = getEnvOrDefault("OLLAMA_TAGS_URL", "http://localhost:11434/api/tags")
	ollamaModel       = getEnvOrDefault("OLLAMA_MODEL", "gemini-3.1-pro-high")
	ollamaAPIKey      = os.Getenv("OLLAMA_API_KEY")

	agyModel  = getEnvOrDefault("AGY_MODEL", "gemini-3.1-pro-high")
	agyEffort = getEnvOrDefault("AGY_EFFORT", "high")
	agyPath   = resolveAgyPath()
)

const translateTextPrompt = `Here is my coding challenge problem. Act like a candidate in a technical interview.

Provide:
1. A simple, clean, and easy-to-understand solution (nothing fancy, use basic code).
2. A short, clear, and user-friendly explanation as you would explain to an interviewer.

Problem:
%s`

func getEnvOrDefault(key, fallback string) string {
	if val := os.Getenv(key); val != "" {
		return val
	}
	return fallback
}

func resolveAgyPath() string {
	if p, err := exec.LookPath("agy"); err == nil {
		return p
	}
	homeAgy := filepath.Join(os.Getenv("HOME"), ".local", "bin", "agy")
	if _, err := os.Stat(homeAgy); err == nil {
		return homeAgy
	}
	return "agy"
}

type OllamaTagsResponse struct {
	Models []struct {
		Name string `json: "name"`
	} `json:"models"`
}

type OllamaGenerateRequest struct {
	Model  string `json:"model"`
	Prompt string `json:"prompt"`
	Stream bool   `json:"stream"`
}

type OllamaGenerateResponse struct {
	Response string `json:"response"`
}

func getAvailableOllamaModel() string {
	client := http.Client{Timeout: 5 * time.Second}
	resp, err := client.Get(ollamaTagsURL)
	if err == nil && resp.StatusCode == 200 {
		defer resp.Body.Close()
		var tags OllamaTagsResponse
		if err := json.NewDecoder(resp.Body).Decode(&tags); err == nil {
			var names []string
			for _, m := range tags.Models {
				if m.Name != "" {
					names = append(names, m.Name)
					if m.Name == ollamaModel || m.Name == ollamaModel+":latest" {
						return ollamaModel
					}
				}
			}
			for _, name := range names {
				if !strings.Contains(strings.ToLower(name), "embed") {
					log.Printf("Model '%s' not found on Ollama. Using available model '%s'", ollamaModel, name)
					return name
				}
			}
			if len(names) > 0 {
				return names[0]
			}
		}
	}
	return ollamaModel
}

func translateWithOllama(prompt string) (string, error) {
	modelName := getAvailableOllamaModel()
	log.Printf("Starting translation request to %s with model '%s'", ollamaURL, modelName)

	reqBody, err := json.Marshal(OllamaGenerateRequest{
		Model:  modelName,
		Prompt: prompt,
		Stream: false,
	})
	if err != nil {
		return "", err
	}

	req, err := http.NewRequest("POST", ollamaURL, bytes.NewBuffer(reqBody))
	if err != nil {
		return "", err
	}
	req.Header.Set("Content-Type", "application/json")
	if ollamaAPIKey != "" {
		req.Header.Set("Authorization", "Bearer "+ollamaAPIKey)
	}

	client := http.Client{Timeout: 120 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		body, _ := io.ReadAll(resp.Body)
		return "", fmt.Errorf("Ollama returned HTTP %d: %s", resp.StatusCode, string(body))
	}

	var genResp OllamaGenerateResponse
	if err := json.NewDecoder(resp.Body).Decode(&genResp); err != nil {
		return "", err
	}

	result := strings.TrimSpace(genResp.Response)
	if result == "" {
		return "", fmt.Errorf("Ollama returned an empty response")
	}
	return result, nil
}

func translateWithAntigravity(prompt string) (string, error) {
	args := []string{}
	if agyModel != "" {
		args = append(args, "--model", agyModel)
	}
	if agyEffort != "" {
		args = append(args, "--effort", agyEffort)
	}
	args = append(args, "-p", prompt)

	cmd := exec.Command(agyPath, args...)
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	log.Printf("Executing prompt via Antigravity CLI (%s)...", agyPath)
	err := cmd.Run()
	if err == nil && strings.TrimSpace(stdout.String()) != "" {
		return strings.TrimSpace(stdout.String()), nil
	}

	errMsg := strings.TrimSpace(stderr.String())
	if errMsg == "" && err != nil {
		errMsg = err.Error()
	}
	return "", fmt.Errorf("Antigravity error: %s", errMsg)
}

func translateText(text string, isRawPrompt bool) string {
	prompt := text
	if !isRawPrompt {
		prompt = fmt.Sprintf(translateTextPrompt, text)
	}

	type provider struct {
		name string
		fn   func(string) (string, error)
	}

	var providers []provider
	if preferredProvider == "ollama" {
		providers = []provider{
			{"Ollama", translateWithOllama},
			{"Antigravity", translateWithAntigravity},
		}
	} else {
		providers = []provider{
			{"Antigravity", translateWithAntigravity},
			{"Ollama", translateWithOllama},
		}
	}

	var lastErr error
	for _, p := range providers {
		log.Printf("Attempting request using %s...", p.name)
		result, err := p.fn(prompt)
		if err == nil {
			return result
		}
		log.Printf("%s failed: %v. Trying fallback...", p.name, err)
		lastErr = err
	}

	return fmt.Sprintf("Execution failed on all available providers. Error: %v", lastErr)
}

func askAntigravity(question string) string {
	result, err := translateWithAntigravity(question)
	if err != nil {
		return fmt.Sprintf("Antigravity error: %v", err)
	}
	return result
}
