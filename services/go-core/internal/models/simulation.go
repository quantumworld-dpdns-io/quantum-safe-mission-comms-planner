package models

type SimulationRequest struct {
	MissionID string                 `json:"mission_id"`
	Type      string                 `json:"type"`
	Params    map[string]interface{} `json:"params"`
}

type SimulationResponse struct {
	Result interface{} `json:"result"`
	Status string      `json:"status"`
}
