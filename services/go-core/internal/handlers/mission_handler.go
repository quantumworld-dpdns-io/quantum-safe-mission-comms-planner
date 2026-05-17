package handlers

import (
	"net/http"
	"quantum-safe-mission-comms-planner/go-core/internal/database"
	"quantum-safe-mission-comms-planner/go-core/internal/models"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

func GetMissions(c *gin.Context) {
	rows, err := database.DuckDB.Query("SELECT id, name, status, description, created_at FROM missions")
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch missions: " + err.Error()})
		return
	}
	defer rows.Close()

	var missions []models.Mission
	for rows.Next() {
		var m models.Mission
		err := rows.Scan(&m.ID, &m.Name, &m.Status, &m.Description, &m.CreatedAt)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to scan mission: " + err.Error()})
			return
		}
		missions = append(missions, m)
	}

	if missions == nil {
		missions = []models.Mission{}
	}

	c.JSON(http.StatusOK, missions)
}

func CreateMission(c *gin.Context) {
	var m models.Mission
	if err := c.ShouldBindJSON(&m); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if m.ID == "" {
		m.ID = uuid.New().String()
	}
	m.CreatedAt = time.Now()
	if m.Status == "" {
		m.Status = "PLANNING"
	}

	_, err := database.DuckDB.Exec("INSERT INTO missions (id, name, status, description, created_at) VALUES (?, ?, ?, ?, ?)",
		m.ID, m.Name, m.Status, m.Description, m.CreatedAt)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to save mission: " + err.Error()})
		return
	}

	c.JSON(http.StatusCreated, m)
}
