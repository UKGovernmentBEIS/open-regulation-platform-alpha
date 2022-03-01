<!---
2021 Alastair McKinley (a.mckinley@analyticsengines.com)
-->

# ORP Alpha Repository Layout

## Top Level

At the top level for the project the ```.env``` files contain the environment variables used during Docker stack creation by each service.
The ```deploy.sh``` and ```redeploy.sh``` scripts boot a new stack or tear down an old one and boot a new stack respectively.
In practice, only ```redeploy.sh``` is required.

## ```api_demo```

The ```api_demo``` folder contains the source for the Streamlit app and the script to deploy the demo.

## ```ddl```

The ```ddl``` folder contains the SQL scripts that initialise the ORP Alpha Database and backend data processing logic.  These are executed in numeric prefix sequence by the ```init.sh``` script in the PostgreSQL container.

## ```demo_data```

The ```demo_data``` folder contains the demo data set that is downloaded and extracted before the test system is deployed.

## ```docs```

The ```docs``` folder contains several documents about the technical architecture developed during the Alpha phase.

## ```editorial-ui```

The ```editorial-ui``` folder contains React app and Docker container definition that deploys it for the Editorial UI component.

## ```event_consumer```

The ```event_consumer``` folder contains a service definition that listens to events from the RabbitMQ queue and a dummy "email" consumer that could be extended to notify users via email of events.

## ```external-apis```

The ```external-apis``` folder contains the implementation of the public-facing Django based REST API.

## ```init```

This folder contains the init script that is launched on the PostgreSQL instance when the Docker stack is created.

## ```legislation_connector```

The ```legislation_connector``` folder contains the python based tool that was used to build the test data set from legislation.gov.uk.

## ```python```

The ```python``` folder contains the python tools that are utilised by the backend data processing logic. Named Entity Extraction, Deontic Language and common XML processing functions are implemented here.

## ```setup```

The setup directory are scripts that are executed after the data platform is deployed to intialise it in a known state for testing.  This mostly references scripts in the ```tests/test_support/``` folder.

## ```tests```

The ```tests``` folder contains all tests executed when the ```./redeploy_and_test.sh``` script is executed.  The top level of ```tests``` contain the TAP tests executed inside the database.  The ```tests/api_tests/pytests``` folder contains the python pytest scripts that run many tests against the internal API.  The ```tests/pytests``` folder contains pytest scripts that test the API and internal database operations in conjunction.  The ```tests/test_support/``` folder contains a set of standard scripts that set up the platform for both testing and demo purposes.


