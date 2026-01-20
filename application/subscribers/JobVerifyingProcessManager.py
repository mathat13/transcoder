from application.events.ApplicationEvents import TranscodeVerified, TranscodeVerificationFailed
from application.events.EventEnvelope import EventEnvelope

class JobVerifyingProcessManager:
    def __init__(self, event_publisher, filesystem):
        self.publisher = event_publisher
        self.filesystem = filesystem

    def __call__(self, envelope: EventEnvelope):
        self.handle(envelope)
        
    def handle(self, envelope: EventEnvelope):
        event = envelope.event
        if not self.filesystem.exists(event.transcode_file.path):
            self.publisher.publish(TranscodeVerificationFailed(job_id=event.job_id,
                                                               transcode_file=event.transcode_file
                                                               ),
                                                               envelope.context)
            return
        
        self.publisher.publish(TranscodeVerified(job_id=event.job_id,
                                                 transcode_file=event.transcode_file),
                                                 envelope.context)