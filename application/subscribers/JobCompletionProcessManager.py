from application.events.EventEnvelope import EventEnvelope
from application.events.ApplicationEvents import TranscodeSuccessful

class JobVerifyingProcessManager:
    def __init__(self, event_publisher, radarr_api, jellyfin_api, filesystem):
        self.publisher = event_publisher
        self.filesystem = filesystem
        self.radarr_api = radarr_api
        self.jellyfin_api = jellyfin_api

    # Takes a JobCompleted Event
    def __call__(self, envelope: EventEnvelope):
        self.handle(envelope)
        
    def handle(self, envelope: EventEnvelope):
        idempotency_key = envelope.context.operation_id
        media_ids = envelope.event.media_ids
        source_file = envelope.event.source_file
        transcode_file = envelope.event.transcode_file

        # Hardlink file
        self.filesystem.hardlink(source_file=transcode_file.path, destination=source_file.parent)

        # Ask radarr to update file
        self.radarr_api.rescan_movie(media_identifiers=media_ids, idempotency_key=idempotency_key)

        # Check file is updated
        response = self.radarr_api.get_movie(media_identifiers=media_ids, idempotency_key=idempotency_key)

        if response.movie_path != transcode_file.path:
            self.radarr_api.rescan_movie(media_identifiers=media_ids, idempotency_key=idempotency_key)
            response = self.radarr_api.get_movie(media_identifiers=media_ids, idempotency_key=idempotency_key)

        # Update jellyfin library
        self.jellyfin_api.refresh_library(idempotency_key=idempotency_key)

        # Delete old file from filesystem on success
        self.filesystem.delete(file=source_file.path)

        self.publisher.publish(event=TranscodeSuccessful(), operation_context=envelope.context)



        
        
        