# Lattice SDK: Track Thumbnail

This app demonstrates the Lattice SDK Object Store API.

In Lattice, an *object* is a data model that lets you store and access files across your environment.
The Object Store API is a content-delivery network service that provides resilient data storage at the edge.
Use objects together with entities to implement use-cases like track thumbnails, and vessle manifests.

## Before you begin

1. Install the required dependencies. Navigate to `modules`, the run the following commands:

    ```bash
    $ pipenv install
    $ pipenv shell
    $ poetry install
    ```

1. Get the following authorization tokens from the [Lattice Sandboxes dashboard](/sandboxes.developer.anduril.com):
    - ```authorization``` -- This is your **environment bearer token**, which you can get by choosing your environment
        from the [dashboard list](https://sandboxes.developer.anduril.com/idee/environments).
    - ```anduril-sandbox-authorization``` -- This is your **sandboxes bearer token**, which you can obtain from the
        [Account & Security](https://sandboxes.developer.anduril.com/user-settings) page in Sandboxes.

1. Get your environment URL from the environment details page in Sandboxes.

1. Set yous sytem environment variables:

    ```bash 
    $ export LATTICE_ENDPOINT=lattice-your_env_id.env.sandboxes.developer.anduril.com
    $ export ENVIRONMENT_TOKEN=YOUR_LATTICE_ENVIRONMENT_TOKEN
    $ export SANDBOXES_TOKEN=YOUR_LATTICE_SANDBOXES_TOKEN
    ```

## Usage

You can run the app to upload and download objects from the COP using the following command line arguments:

```bash
$ python app.py [-h] --operation OPERATION \
    [--file PATH_TO_FILE] \
    [--path PATH_TO_OBJECT_IN_LATTICE] \
    [--entity ENTITIY_ID]
```

### Example

1. To upload an object to Lattice and associate it with an entity, run the following:

    ```bash
    $ python app.py --operation upload --file ./images/N113PF.jpeg --entity adsbEntity
    ```

1. To download an existing object from Lattice, run the following:

    ```bash
    $ python app.py --operation download --path test-1.tracks.N113PF.jpeg 
    ```
1. To delete an existing object from Lattice, run the following:

    ```bash
    $ python app.py --operation delete --path test-1.tracks.N113PF.jpeg --entity adsbEntity
    ```

For more information, see [the Lattice SDK documentation](https://docs.anduril.com) website.
