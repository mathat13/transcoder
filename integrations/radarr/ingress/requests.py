from pydantic import BaseModel, ConfigDict

class RadarrWebhookPayload(BaseModel):
    model_config = ConfigDict(extra="ignore")

    eventType: str
