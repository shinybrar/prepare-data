# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx==0.28.1",
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.13.2"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import httpx
    import asyncio
    from typing import Dict, List, Any
    from uuid import uuid4
    from time import sleep
    from random import randint
    return Dict, List, asyncio, httpx, randint, uuid4


@app.cell
def _(mo, randint, uuid4):
    md = mo.md(
        r"""
        # Welcome to the CANSRC Prepare Data Test.

        ## Before you begin,
        - Login into [_`keel-dev`_](https://rc-src.canfar.net/science-portal) or [_`keel-prod`_](https://src.canfar.net/science-portal)
        - Start a Notebook Session **_(Required)_**
        - Install SKA IAM OIDC Agents following [_these instructions_](https://indigo-dc.gitbook.io/oidc-agent/intro/install)
        - Generate a SKA OIDC Token with these instructions,
            ```
            eval `oidc-agent`
            oidc-gen ska
            ```
            Select the following options,
            - Issuer: `https://ska-iam.stfc.ac.uk/`
            - Scope: `max`
            - Encryption Password: _any local password of your choice_

            Generate a token with the following command,
            ```
            oidc-token ska -f
            ```
        - **Note:** For _`keel-dev`_ you are required to be within the CADC Network


        ## Test Scenario

         The goal of prepare data is to stage science data in the for users.


        ### To begin, please provide a valid SKA token.

        - SKA Token: {SKA_IAM_TOKEN}

        ### Choose Test Paramaters
        - Dataset ID: {DID}
        - Filename: {FILENAME}
        - Gatekeeper URL: {GATEKEEPER_URL}
            - `https://rc-src.canfar.net` is _`keel-dev`_
            - `https://src.canfar.net` is _`keel-prod`_
        - Data Destination: {DESTINATION}

        ### Assumptions
        - The Rucio Storage Element is configured properly
        - The Dataset ID and filename exist on the RSE
        -`preparedata` operates under `gatekeeper/preparedata` url prefix
        - Your user the the proper ska iam groups to run prepare data
        - Data is staged at _`/cavern/home/<username>/<destination>`_

        ### Click Submit to Configure Tests...
        """
    )
    servers = [
        "https://rc-src.canfar.net",
        "https://src.canfar.net"
    ]
    datasets = [
        "purple:random_CASRC_XRD_50_1GiB_a3d5d740"
    ]
    filenames = [
        "purple/77/ad/random_1GiB_050119fc",
        "purple/c3/73/random_1GiB_0710ac51",
        "purple/1f/12/random_1GiB_08888761",
        "purple/5a/e5/random_1GiB_118d6722",
        "purple/2f/03/random_1GiB_13ff9a62",
        "purple/ed/53/random_1GiB_161dddb1",
        "purple/d0/3f/random_1GiB_1762f804",
        "purple/8e/72/random_1GiB_1c9b66e0",
        "purple/23/4c/random_1GiB_26e00259",
        "purple/c8/f1/random_1GiB_2f0eaa1f",
    ]
    form = md.batch(
        SKA_IAM_TOKEN=mo.ui.text(),
        DID=mo.ui.dropdown(options=datasets, value=datasets[0]),
        FILENAME=mo.ui.dropdown(options=filenames, value=filenames[randint(1,10)]),
        GATEKEEPER_URL=mo.ui.dropdown(options=servers, value=servers[0]),
        DESTINATION=mo.ui.text(value=f"./preparedata-test-{str(uuid4())[:8]}"),
    ).form()
    form
    return (form,)


@app.cell
def _(form, mo):
    mo.stop(form.value is None, mo.md("**Submit the form to continue.**"))
    mo.stop(form.value.get("SKA_IAM_TOKEN") is None, mo.md("**Provide SKA IAM Token to continue.**"))
    return


@app.cell
def _(form):
    form.value
    return


@app.cell
def _(mo):
    run = mo.ui.button(label="Prepare Data", kind="success", full_width=True)
    run
    return (run,)


@app.cell
async def _(Dict, List, asyncio, form, httpx, mo, run):
    run
    with mo.status.spinner(title="Sending Prepare Data Request to Gatekeeper") as _spinner:
        with mo.redirect_stdout():
            try:
                baseurl = form.value.get("GATEKEEPER_URL")
                prepare_data_url: str = f'{baseurl}/preparedata'
                headers: Dict[str, str] = {}
                headers['accept'] ='application/json'
                headers['Content-Type']='application/json'
                headers['Authorization'] = f"Bearer {form.value.get("SKA_IAM_TOKEN")}"
                did: str = form.value.get("DID")
                source: str = form.value.get("FILENAME")
                destination: str = form.value.get("DESTINATION")
                data: List[List[str]] = [] 
                data.append([did, source, destination])
                print("Request Payload:")
                print(data)
                async with httpx.AsyncClient() as client:
                    response = await client.post(url=prepare_data_url, headers=headers, json=data)
                    response.raise_for_status()
                print("Successfully submitted prepare data request")
                print(f"Response: {response.json()}")
                task_id = response.json().get("task_id")
                _spinner.update(f"Tracking Task ID: {task_id}")
                done: bool = False
                attempts: int = 0
                status_url: str = f"{baseurl}/preparedata/{task_id}"

                while (not done) and (attempts < 10):
                    print(f"Attempt: {attempts}")
                    await asyncio.sleep(1)
                    async with httpx.AsyncClient() as client:
                        status = await client.get(url=status_url, headers=headers)
                    status.raise_for_status()
                    response = status.json()
                    attempts += 1
                    if response.get("status") == "SUCCESS":
                        done = True
                    print(response)
            except Exception as error:
                print(error)

    return


if __name__ == "__main__":
    app.run()
