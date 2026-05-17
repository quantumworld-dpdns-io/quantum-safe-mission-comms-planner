package models

type Policy struct {
	ID       string                 `json:"id"`
	Content  string                 `json:"content"`
	Metadata map[string]interface{} `json:"metadata"`
}

type PolicySearchRequest struct {
	Query string `json:"query"`
}
