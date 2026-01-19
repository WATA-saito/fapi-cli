## ADDED Requirements
### Requirement: Streaming Response Support
The CLI tool SHALL support streaming response bodies when the user specifies the `--stream` option, without buffering the entire response in memory.

#### Scenario: Stream plain text response
- **WHEN** user executes `fapi-cli request app.py -P /stream --stream`
- **THEN** the tool writes the response body bytes to stdout as they are received, preserving chunk order

#### Scenario: Stream binary response
- **WHEN** user executes `fapi-cli request app.py -P /download --stream > out.bin`
- **THEN** the tool writes the response body bytes to stdout without attempting to decode as text or JSON

#### Scenario: Invalid combination with headers output
- **WHEN** user executes `fapi-cli request app.py -P /stream --stream --include-headers`
- **THEN** the tool outputs a clear error message indicating the options cannot be used together and exits with code 1

## MODIFIED Requirements
### Requirement: Response Output Format
The CLI tool SHALL output responses in a structured JSON format to stdout, except when streaming mode is enabled.

#### Scenario: Successful response output (default mode)
- **WHEN** a request succeeds with status 200 and `--stream` is not specified
- **THEN** the tool outputs JSON containing at least `status_code` and `body` fields

#### Scenario: Error response output (default mode)
- **WHEN** a request fails with status 404 or 500 and `--stream` is not specified
- **THEN** the tool outputs JSON containing `status_code` and `body` fields with error details

#### Scenario: Response headers output (optional, default mode)
- **WHEN** user specifies `--include-headers` flag and `--stream` is not specified
- **THEN** the tool includes response headers in the output JSON

#### Scenario: Streaming response output (stream mode)
- **WHEN** user specifies `--stream`
- **THEN** the tool writes response body bytes to stdout as they are received and does not emit the structured JSON response wrapper

