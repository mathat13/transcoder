from application.events.EventEnvelope import EventEnvelope
from application.events.ApplicationEvents import TranscodeSuccess

class JobCompletionProcessManager:
    def __init__(self, event_publisher, radarr_api, jellyfin_api, filesystem):
        self.publisher = event_publisher
        self.filesystem = filesystem
        self.radarr_api = radarr_api
        self.jellyfin_api = jellyfin_api

    # Takes a JobCompleted Event
    def __call__(self, envelope: EventEnvelope):
        self.handle(envelope)
        
    def handle(self, envelope: EventEnvelope):
        event = envelope.event
        media_ids = event.media_ids
        source_file = event.source_file
        transcode_file = event.transcode_file
        context = envelope.context

        # Hardlink file
        self.filesystem.hardlink(source_file=transcode_file.path, destination=source_file.parent)

        # Ask radarr to update file
        self.radarr_api.rescan_movie(media_identifiers=media_ids, context=context)

        # Get info for movie
        self.radarr_api.get_moviefile(media_identifiers=media_ids, context=context)

        # Add logic for checking if file is correctly updated

        # On failure

        # On success:
        # Delete file from filesystem
        self.filesystem.delete(file=source_file.path)

        # Update jellyfin library on success
        self.jellyfin_api.refresh_library(context=context)

        self.publisher.publish(event=TranscodeSuccess(job_id=event.job_id), operation_context=envelope.context)



        
        
        