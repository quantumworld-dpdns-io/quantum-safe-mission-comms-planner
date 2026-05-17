package main

import (
	"log"
	"quantum-safe-mission-comms-planner/go-core/internal/database"
	"quantum-safe-mission-comms-planner/go-core/internal/handlers"

	"github.com/gin-gonic/gin"
)

func main() {
	// Initialize DuckDB
	// Path relative to services/go-core is ../../data/mission_planner.db
	dbPath := "../../data/mission_planner.db"
	database.InitDuckDB(dbPath)
	log.Printf("DuckDB initialized at %s", dbPath)

	// Initialize ChromaDB
	// Assuming ChromaDB server is running on localhost:8000
	database.InitChroma("localhost", "8000")
	log.Println("ChromaDB client initialized")

	// Set up Gin router
	r := gin.Default()

	// Missions endpoints
	r.GET("/missions", handlers.GetMissions)
	r.POST("/missions", handlers.CreateMission)

	// Analytics endpoint
	r.GET("/analytics", handlers.GetAnalytics)

	// Policy endpoints
	r.POST("/policies", handlers.AddPolicy)
	r.POST("/policies/search", handlers.SearchPolicies)

	// Simulation endpoint
	r.POST("/simulate", handlers.Simulate)

	// Health check
	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "up"})
	})

	log.Println("Go Core Backend Service starting on :8080")
	if err := r.Run(":8080"); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
