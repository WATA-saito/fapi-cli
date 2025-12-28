## ADDED Requirements

### Requirement: Streaming Response Support
The CLI tool SHALL support streaming responses using the `--stream` or `-s` option, enabling real-time output of chunked data.

#### Scenario: Basic streaming output
- **WHEN** user executes `fapi-cli request app.py -P /stream --stream`
- **AND** the endpoint returns a `StreamingResponse`
- **THEN** the tool outputs each chunk to stdout as it is received
- **AND** the status code is printed to stderr

#### Scenario: Streaming with short option
- **WHEN** user executes `fapi-cli request app.py -P /stream -s`
- **THEN** the tool behaves identically to `--stream`

#### Scenario: Streaming with headers
- **WHEN** user executes `fapi-cli request app.py -P /stream --stream --include-headers`
- **THEN** response headers are printed to stderr
- **AND** streaming body data is printed to stdout

#### Scenario: Non-streaming endpoint with stream option
- **WHEN** user executes `fapi-cli request app.py -P /normal --stream`
- **AND** the endpoint returns a normal (non-streaming) response
- **THEN** the tool outputs the response body to stdout
- **AND** the status code is printed to stderr

#### Scenario: Default behavior without stream option
- **WHEN** user executes `fapi-cli request app.py -P /stream` (without `--stream`)
- **AND** the endpoint returns a `StreamingResponse`
- **THEN** the tool waits for the complete response
- **AND** outputs the result in JSON format (existing behavior)

## MODIFIED Requirements

### Requirement: Command Line Interface
The CLI tool SHALL provide a command-line interface with the following options.

#### Scenario: Help command
- **WHEN** user executes `fapi-cli --help` or `fapi-cli request --help`
- **THEN** the tool displays usage information and available options

#### Scenario: HTTP method specification
- **WHEN** user executes `fapi-cli request src/main.py -X POST` or `fapi-cli request src/main.py --method PUT`
- **THEN** the tool uses the specified HTTP method for the request

#### Scenario: Path specification
- **WHEN** user executes `fapi-cli request src/main.py -P /api/users` or `fapi-cli request src/main.py --path /api/users`
- **THEN** the tool sends the request to the specified path (default: `/`)

#### Scenario: Request body specification
- **WHEN** user executes `fapi-cli request src/main.py -d '{"key":"value"}'` or `fapi-cli request src/main.py --data '{"key":"value"}'`
- **THEN** the tool includes the specified JSON body in the request

#### Scenario: Header specification
- **WHEN** user executes `fapi-cli request src/main.py -H "Key: Value"` or `fapi-cli request src/main.py --header "Key: Value"`
- **THEN** the tool includes the specified header in the request (can be specified multiple times)

#### Scenario: Query parameter specification
- **WHEN** user executes `fapi-cli request src/main.py -q "key=value"` or `fapi-cli request src/main.py --query "key=value"`
- **THEN** the tool appends the query parameters to the request URL

#### Scenario: Form data specification
- **WHEN** user executes `fapi-cli request src/main.py -F "key=value"` or `fapi-cli request src/main.py --form "key=value"`
- **THEN** the tool includes the form field in a multipart/form-data request (can be specified multiple times)

#### Scenario: File upload specification
- **WHEN** user executes `fapi-cli request src/main.py -F "file=@path/to/file"`
- **THEN** the tool uploads the file as part of a multipart/form-data request

#### Scenario: Streaming output specification
- **WHEN** user executes `fapi-cli request src/main.py -s` or `fapi-cli request src/main.py --stream`
- **THEN** the tool outputs streaming response data in real-time to stdout
