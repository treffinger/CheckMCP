# CheckMCP

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for [Checkmk](https://checkmk.com). CheckMCP enables AI agents to interact with a Checkmk instance to query hosts, services, downtimes, and more.
CheckMCP currently only supports read operations. This project is still in an early stage of development, changes and new features are to be expected.

![Demo](media/demo.gif)

## Tested With

- Checkmk Raw Edition 2.3.0p23

## Installation & Setup

### Option 1: Docker Compose (recommended)

**1. Create your configuration file**

Save your configuration as a YAML file, e.g. `/etc/checkmcp/config.yml`.

**2. Edit the `.env` file**

Create a `.env` file and set the path to the configuration file by providing the following content.

```
CONFIG_PATH=/path/to/config.yml
PORT=8000
```

Alternatively, the path can be specified directly within the `docker-compose.yml` file.

**3. Run the Docker Compose file using Docker or Podman**

```bash
docker compose up -d
```

The MCP server is now available at `http://localhost:8000`.

---

### Option 2: Docker

**1. Create your configuration file**

Save your configuration as a YAML file, e.g. `/etc/checkmcp/config.yml`.

**2. Build the image**

```bash
docker build -t checkmcp .
```

**3. Run the container**

```bash
docker run -d \
  -p 8000:8000 \
  -v /etc/checkmcp/config.yml:/checkmcp/config.yml \
  -e CONFIG_PATH=/checkmcp/config.yml \
  checkmcp
```

The MCP server is now available at `http://localhost:8000`.

---

### Option 3: Manual (Only for testing)

**Requirements:** Python 3.12+

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Create your configuration file**

Save your config YAML somewhere accessible, e.g. `~/checkmcp-config.yml`.

**3. Set the environment variable**

```bash
export CONFIG_PATH=~/checkmcp-config.yml
```

**4. Start the server**

```bash
python src/main.py
```

The server starts on port 8000 by default.

---

## Using self-signed certificates for Checkmk
If you use self-signed certificates for Checkmk, you must specify the CA that trusts the certificate. To do this, set the environment variable `REQUESTS_CA_BUNDLE`.

Example: `REQUESTS_CA_BUNDLE=/path/to/ca_bundle.crt`

If you don't use self-signed certificates, you can leave this variable unset.

## Configuration

CheckMCP is configured via a YAML file. The path to this file must be provided through the `CONFIG_PATH` environment variable.

### Full Example

```yaml
checkmk:
  username: "automation"
  password: "your-automation-secret"
  url: "https://checkmk.example.com"
  site: "mysite"

auth:
  mode: "none"

object_attributes:
  host:
    - alias
    - address
    - state
    - num_services
    - num_services_crit
    - num_services_warn
    - parents
    - tags
  service:
    - description
    - state
    - plugin_output
    - last_check
    - last_state_change
  downtime:
    - host_name
    - is_service
    - start_time
    - end_time
```

### Parameters

#### `checkmk` (required)

Connection settings for your Checkmk instance.

| Parameter | Type | Description |
|-----------|------|-------------|
| `username` | string | Checkmk automation user name. |
| `password` | string | Password or automation secret for the user. |
| `url` | string | Base URL of your Checkmk instance (e.g. `https://checkmk.example.com`). |
| `site` | string | Name of the Checkmk site (e.g. `mysite`). |

#### `auth` (required)

Controls how MCP clients authenticate against CheckMCP itself.

| Parameter | Type | Description |
|-----------|------|-------------|
| `mode` | string | Authentication mode. Either `"none"` or `"oauth"`. |
| `issuer_url` | string | OAuth issuer URL. Required when `mode` is `"oauth"`. |
| `jwks_url` | string | OAuth jwks URL. Required when `mode` is `"oauth"`. |
| `audience` | string | OAuth audience. Required when `mode` is `"oauth"`. |
| `resource_server_url` | string | OAuth resource server URL. Required when `mode` is `"oauth"`. |
| `required_scopes` | list of strings | OAuth scopes required for access. Required when `mode` is `"oauth"`. |

**Mode `none`:** No authentication. Any MCP client can connect without credentials. Only use this in trusted, isolated environments.

```yaml
auth:
  mode: "none"
```

**Mode `oauth`:** Enables OAuth 2.0 JWT token verification via an external identity provider.

```yaml
auth:
  mode: "oauth"
  issuer_url: "https://auth.example.com"
  jwks_url: "https://auth.example.com/certs"
  resource_server_url: "https://checkmcp.example.com"
  audience: audience
  required_scopes:
    - "checkmcp:read"
```

#### `object_attributes` (optional)

Checkmk hosts, services and other entities have a variety of attributes that can be monitored. Returning all of these attributes would fill the model's context window more quickly and would also be impractical, as not all attributes are necessarily relevant.
By default, CheckMCP returns a predefined list of attributes, which can be found in the table below.

| Parameter | Default attributes |
|-----------|--------------------|
| `host` | `alias`, `address`, `num_services`, `num_services_crit`, `num_services_warn`, `parents`, `childs`, `state`, `tags` |
| `service` | `description`, `display_name`, `downtimes`, `is_flapping`, `last_check`, `last_state`, `last_state_change`, `last_time_ok`, `plugin_output`, `state` |
| `downtime` | `comment`, `host_name`, `is_service`, `start_time`, `end_time`, `recurring` |

| Parameter | Available attributes |
|-----------|--------------------|
| `host` and `service`  | `accept_passive_checks`, `acknowledged`, `acknowledgement_type`, `active_checks_enabled`, `check_command`, `check_command_expanded`, `check_flapping_recovery_notification`, `check_freshness`, `check_interval`, `check_options`, `check_period`, `check_type`, `checks_enabled`, `comments`, `contact_groups`, `contacts`, `current_check_attempt`, `current_notification_number`, `custom_variables`, `display_name`, `downtimes`, `event_handler_command`, `event_handler_enabled`, `check_execution_time`, `first_notification_delay`, `flap_detection_enabled`, `flappiness`, `groups`, `has_been_checked`, `high_flap_threshold`, `in_check_period`, `in_notification_period`, `in_service_period`, `initial_state`, `is_executing`, `is_flapping`, `labels`, `last_check`, `last_hard_state_change`, `last_notification`, `last_state`, `last_state_change`, `check_latency`, `long_plugin_output`, `low_flap_threshold`, `max_check_attempts`, `next_check`, `next_notification`, `no_more_notifications`, `notes`, `notification_interval_minutes`, `notification_period`, `notification_postponement_reason`, `notifications_enabled`, `pending_flex_downtime`, `percent_state_change`, `performance_data`, `plugin_output`, `process_performance_data_enabled`, `check_retry_interval`, `scheduled_downtime_depth`, `service_period`, `staleness`, `state_type` |
| `host` | `address`, `alias`, `childs`, `state`, `last_time_down`, `last_time_unreachable`, `last_time_up`, `number_services`, `number_services_warn`, `number_services_critical`, `hard_state`, `last_hard_state`, `previous_hard_state` |
| `service` | `description`, `cache_interval`, `cached_at`, `state`, `in_passive_check_period`, `last_time_critical`, `last_time_ok`, `last_time_unknown`, `last_time_warning`, `obsess_over_service`, `passive_check_period`, `hard_state`, `last_hard_state`, `previous_hard_state` |

Some of the attribute names have been slightly adjusted to be more descriptive, but they still largely correspond to the standard Checkmk columns that can be retrieved for these objects.

---

## Available Tools
The following Tools are provided by the MCP server.

| Tool | Description |
|------|-------------|
| `list_hosts` | Returns all hosts. Optionally filter by folder path. |
| `search_host` | Searches hosts based on given filters. |
| `get_host` | Returns detailed information about a single host. |
| `get_host_services` | Returns all monitored services of a given host. |
| `list_downtimes` | Returns all scheduled downtimes. Optionally filter by host name. |
| `get_downtime` | Returns detailed information about a specific downtime. |
| `list_folders` | Returns all Checkmk folders (recursively). |
| `list_tags` | Returns all host tag groups and their tags. |
