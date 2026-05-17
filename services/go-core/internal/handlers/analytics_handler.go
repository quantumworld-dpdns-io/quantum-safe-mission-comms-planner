package handlers

import (
	"net/http"
	"quantum-safe-mission-comms-planner/go-core/internal/database"

	"github.com/gin-gonic/gin"
)

func GetAnalytics(c *gin.Context) {
	// Analytical SQL via DuckDB
	// Count missions by status
	rows, err := database.DuckDB.Query("SELECT status, COUNT(*) as count FROM missions GROUP BY status")
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to run analytics: " + err.Error()})
		return
	}
	defer rows.Close()

	analytics := make(map[string]interface{})
	statusCounts := make(map[string]int)
	
	total := 0
	for rows.Next() {
		var status string
		var count int
		if err := rows.Scan(&status, &count); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to scan analytics result: " + err.Error()})
			return
		}
		statusCounts[status] = count
		total += count
	}

	analytics["status_distribution"] = statusCounts
	analytics["total_missions"] = total

	c.JSON(http.StatusOK, analytics)
}
