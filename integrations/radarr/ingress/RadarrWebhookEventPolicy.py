from integrations.radarr.ingress.requests import RadarrWebhookPayload

class RadarrWebhookEventPolicy:
    @staticmethod
    def is_download(payload: RadarrWebhookPayload) -> bool:
        return payload.eventType == "Download"