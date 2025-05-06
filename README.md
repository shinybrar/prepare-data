# prepare-data
SRCNet Prepare Data Validation

## Installation

```bash
git clone https://github.com/shinybrar/prepare-data.git
cd prepare-data
```

## How to Run Prepare Data

### Locally via `uv`

uv is a fast Python package installer and resolver. For more information, visit the [official uv documentation](https://docs.astral.sh/uv/getting-started/installation/).

#### Installation on Linux/macOS:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, verify uv is installed correctly:
```bash
uv --version
```

### Usage
```
uv tool run marimo run --sandbox e2e.py
```


### Locally via `docker`

```bash
cd prepare-data/
docker run -p 2718:2718 --rm -it -v $(pwd):/prepare-data ghcr.io/astral-sh/uv:debian uv tool run marimo run --sandbox --no-token --host 0.0.0.0 /prepare-data/e2e.py
```

and then in your local browser visit,

```
http://localhost:2718
```

## Group Permissions Needed


The magic conservative group recipe list as of 11/03/25 is below. Note the `data/namespaces/chocolate/owner` can be replaced with the namespace group of the data that you are testing with.

```
data
data/namespaces
data/namespaces/cansrc
data/namespaces/cansrc/owner
monitoring
monitoring/grafana
prototyping-groups
prototyping-groups/mini-src
prototyping-groups/mini-src/platform-users
services
services/data-management-api
services/data-management-api/roles
services/data-management-api/roles/developer
services/gateway-backend-api
services/rucio
services/rucio/roles
services/rucio/roles/user
services/site-capabilities-api
services/site-capabilities-api/roles
services/site-capabilities-api/roles/viewer
```


