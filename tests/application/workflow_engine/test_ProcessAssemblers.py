import pytest

from tests.bootstrap.TestSystem import TestSystem

from application import (ProcessRunnerInput,
                         ProcessDefinition,
                         HardlinkFile,
                         UpdateRadarrMovieFile,
                         DeleteSourceFile,
                         RefreshJellyfinLibrary,
                         CheckFileExistence,
                         JobCompletionContext,
                         JobVerificationContext,
                         FileContext,
                         MediaContext,
                         ProcessAssemblerRegistry,
                         )


from tests.factories.EventFactories import (
    JobCompletedEventFactory,
    JobMovedToVerifyingEventFactory,
    EventEnvelopeFactory,
)

def test_ProcessAssemblerRegistry_raises_KeyError_on_no_assembler(test_system: TestSystem):
    registry = ProcessAssemblerRegistry()
    envelope = EventEnvelopeFactory(event=JobCompletedEventFactory())

    # No assembler added to registry

    with pytest.raises(KeyError):
        registry.assemble(envelope=envelope)

def test_JobVerificationProcessAssembler_assembles_correct_object(test_system: TestSystem):
    envelope = EventEnvelopeFactory(event=JobMovedToVerifyingEventFactory())

    process_input = test_system.assembler_registry.assemble(envelope=envelope)

    assert isinstance(process_input, ProcessRunnerInput)
    
    # process_context:
    process_context = process_input.process_context
    assert isinstance(process_context, JobVerificationContext)
    assert process_context.operation_context is envelope.context
    assert process_context.envelope is envelope

    # process_context.files:
    assert isinstance(process_context.files, FileContext)
    assert process_context.files.source_file == None
    assert process_context.files.transcode_file == envelope.event.transcode_file

    # process_definition:
    process_definition = process_input.process_definition
    assert isinstance(process_definition, ProcessDefinition)
    processes = []

    for step in process_definition.steps:
        processes.append(type(step))
    
    assert processes == [
                CheckFileExistence,
            ]
    
def test_JobCompletionProcessAssembler_assembles_correct_object(test_system: TestSystem):
    envelope = EventEnvelopeFactory(event=JobCompletedEventFactory())

    process_input = test_system.assembler_registry.assemble(envelope=envelope)

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

