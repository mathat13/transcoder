import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from tests.factories.JobModelFactory import JobModelFactory
from tests.bootstrap.bootstrap_test_system import (
    bootstrap_application_test_system,
    bootstrap_job_service_test_system,
    bootstrap_workflow_test_system,
)
from tests.bootstrap.Types import (
    ApplicationTestSystem,
    JobServiceTestSystem,
    WorkflowTestSystem,
)

from infrastructure import (
    Base,
    SQLiteJobRepository,
)

# --- Test systems ---
@pytest.fixture()
def application_test_system() -> ApplicationTestSystem:
    system = bootstrap_application_test_system()
    return system

@pytest.fixture()
def job_service_test_system() -> JobServiceTestSystem:
    system = bootstrap_job_service_test_system()
    return system

@pytest.fixture()
def workflow_test_system() -> WorkflowTestSystem:
    system = bootstrap_workflow_test_system()
    return system

# --- Database ---
TEST_DATABASE_URL = "sqlite://"

@pytest.fixture()
def db_session():
    """Creates a brand new in-memory DB for each test."""

    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # forces all connections to use same in-memory DB
    )

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    # Recreate all tables for a fresh DB
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    yield session

    session.close()

@pytest.fixture()
def job_repository(db_session) -> SQLiteJobRepository:
    return SQLiteJobRepository(db_session)

@pytest.fixture()
def job_model_factory(db_session) -> JobModelFactory:
    JobModelFactory._meta.sqlalchemy_session = db_session
    return JobModelFactory