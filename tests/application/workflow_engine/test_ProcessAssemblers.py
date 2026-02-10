from domain import (
    OperationContext,
)

from application import (JobCompletionProcessAssembler,
                         EventEnvelope,
                         ProcessRunnerInput,
                         JobCompletionContext,
                         ProcessDefinition,
                         HardlinkFile,
                         UpdateRadarrMovieFile,
                         DeleteSourceFile,
                         RefreshJellyfinLibrary,
                         FileContext,
                         MediaContext,
                         )


from tests import (FakeFileSystem,
                   FakeJellyfinAPIAdapter,
                   FakeRadarrAPIAdapter,
                   JobCompletedEventFactory,
                   )


def test_JobCompletionProcessAssembler_assembles_correct_object():
    fs = FakeFileSystem()
    jellyfin = FakeJellyfinAPIAdapter()
    radarr = FakeRadarrAPIAdapter()
    assembler = JobCompletionProcessAssembler(filesystem=fs, radarr=radarr, jellyfin=jellyfin)

    event = JobCompletedEventFactory()
    envelope = EventEnvelope.create(event=event, context=OperationContext.create())

    process_input = assembler.assemble(envelope=envelope)

    assert isinstance(process_input, ProcessRunnerInput)
    
    # process_context:
    process_context = process_input.process_context
    assert isinstance(process_context, JobCompletionContext)
    assert process_context.operation_context is envelope.context
    assert process_context.envelope is envelope

    # process_context.files:
    assert isinstance(process_context.files, FileContext)
    assert process_context.files.source_file == envelope.event.source_file
    assert process_context.files.transcode_file == envelope.event.transcode_file

    # process_context.media:
    assert isinstance(process_context.media, MediaContext)
    assert process_context.media.media_ids == envelope.event.media_ids

    # process_definition:
    process_definition = process_input.process_definition
    assert isinstance(process_definition, ProcessDefinition)
    processes = []

    for step in process_definition.steps:
        processes.append(type(step))
    
    assert processes == [
                HardlinkFile,
                UpdateRadarrMovieFile,
                DeleteSourceFile,
                RefreshJellyfinLibrary,
            ]

