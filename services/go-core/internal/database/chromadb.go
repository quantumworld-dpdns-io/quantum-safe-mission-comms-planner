package database

import (
	"context"
	chroma "github.com/szirtesitidom/chroma-go"
	"log"
)

var ChromaClient *chroma.Client

func InitChroma(host, port string) {
	var err error
	ChromaClient, err = chroma.NewClient("http://" + host + ":" + port)
	if err != nil {
		log.Fatalf("Failed to initialize ChromaDB client: %v", err)
	}
	
	// Check connection
	_, err = ChromaClient.Heartbeat(context.Background())
	if err != nil {
		log.Printf("Warning: ChromaDB heartbeat failed: %v. Ensure ChromaDB server is running.", err)
	}
}
