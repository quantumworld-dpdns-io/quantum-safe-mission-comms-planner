package handlers

import (
	"bytes"
	"encoding/json"
	"io"
	"net/http"
	"quantum-safe-mission-comms-planner/go-core/internal/models"

	"github.com/gin-gonic/gin"
)

func Simulate(c *gin.Context) {
	var req models.SimulationRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request: " + err.Error()})
		return
	}

	// Forward to Python microservice
	// Assuming Python service runs at http://localhost:8082
	// Depending on req.Type, we might want to map to different endpoints
	// For now, let's assume a generic /simulate or map BB84
	pythonURL := "http://localhost:8082/simulate"
	if req.Type == "bb84" {
		pythonURL = "http://localhost:8082/simulate/bb84"
	}

	jsonData, err := json.Marshal(req.Params)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to marshal parameters: " + err.Error()})
		return
	}

	resp, err := http.Post(pythonURL, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		c.JSON(http.StatusServiceUnavailable, gin.H{"error": "Python simulation service unavailable: " + err.Error()})
		return
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to read response from simulation service: " + err.Error()})
		return
	}

	var simResult interface{}
	if err := json.Unmarshal(body, &simResult); err != nil {
		// If it's not JSON, just return the body as string
		c.JSON(resp.StatusCode, gin.H{
			"status": "completed",
			"result": string(body),
		})
		return
	}

	c.JSON(resp.StatusCode, models.SimulationResponse{
		Status: "completed",
		Result: simResult,
	})
}
