package database

import (
	"database/sql"
	_ "github.com/marcboeker/go-duckdb"
	"log"
)

var DuckDB *sql.DB

func InitDuckDB(dbPath string) {
	var err error
	DuckDB, err = sql.Open("duckdb", dbPath)
	if err != nil {
		log.Fatalf("Failed to connect to DuckDB: %v", err)
	}

	// Create tables if they don't exist
	_, err = DuckDB.Exec(`
		CREATE TABLE IF NOT EXISTS missions (
			id VARCHAR PRIMARY KEY,
			name VARCHAR,
			status VARCHAR,
			description TEXT,
			created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
	`)
	if err != nil {
		log.Fatalf("Failed to create missions table: %v", err)
	}
}
