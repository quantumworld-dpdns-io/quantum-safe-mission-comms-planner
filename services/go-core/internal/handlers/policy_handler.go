package handlers

import (
	"context"
	"net/http"
	"quantum-safe-mission-comms-planner/go-core/internal/database"
	"quantum-safe-mission-comms-planner/go-core/internal/models"

	"github.com/gin-gonic/gin"
)

func AddPolicy(c *gin.Context) {
	var p models.Policy
	if err := c.ShouldBindJSON(&p); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	collectionName := "mission_policies"
	// Using a simple context for the request
	ctx := context.Background()

	// In szirtesitidom/chroma-go, GetOrCreateCollection is common
	collection, err := database.ChromaClient.GetOrCreateCollection(ctx, collectionName, nil, nil, nil)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to access ChromaDB collection: " + err.Error()})
		return
	}

	// Prepare data for Chroma
	metadatas := []map[string]interface{}{p.Metadata}
	documents := []string{p.Content}
	ids := []string{p.ID}

	_, err = collection.Add(ctx, nil, metadatas, documents, ids)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to add policy to vector store: " + err.Error()})
		return
	}

	c.JSON(http.StatusCreated, gin.H{"message": "Policy added successfully", "id": p.ID})
}

func SearchPolicies(c *gin.Context) {
	var req models.PolicySearchRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	collectionName := "mission_policies"
	ctx := context.Background()

	collection, err := database.ChromaClient.GetCollection(ctx, collectionName, nil)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to access ChromaDB collection: " + err.Error()})
		return
	}

	// Query for similar policies
	nResults := 3
	results, err := collection.Query(ctx, []string{req.Query}, int32(nResults), nil, nil, nil)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to search policies: " + err.Error()})
		return
	}

	c.JSON(http.StatusOK, results)
}
