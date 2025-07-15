from object_store_client import upload_object, download_object, delete_object, list_objects
from entity_manager_client import override_entity

from modules.src.anduril import anduril

import os, sys, asyncio, logging, argparse

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')


# Get your Lattice URL and environment bearer token from your environment variables.
lattice_endpoint = os.getenv('LATTICE_ENDPOINT')
environment_token = os.getenv('ENVIRONMENT_TOKEN')

# Get the sandboxes token from your environment variables.
# The following only applies to environments created in Lattice Sandboxes.
# Remove if you are developing on a different deployment of Lattice.
sandboxes_token = os.getenv('SANDBOXES_TOKEN')

if not environment_token or not lattice_endpoint:
    logging.warning("Make sure your Lattice URL and bearer token have been set as system environment variables.")
    sys.exit(1)

# The following only applies to environments created in Lattice Sandboxes.
# Remove, if you are developing on a different deployment of Lattice.
if not sandboxes_token:
    logging.warning("Make sure your sandboxes token has been set as system environment variables.")
    sys.exit(1)
def save_object(data, object_path):
    file_name = os.path.basename(object_path)
    with open(file_name, 'wb') as file:
        file.write(data)

client = anduril(
    base_url=f"https://{lattice_endpoint}/api/v1",
    token=environment_token,
    headers={ "Anduril-Sandbox-Authorization": f"Bearer {sandboxes_token}" }
)
async def main(args):
    try:
        operation = args.operation
        file_path = args.file
        object_path = args.path
        entity_id = args.entity
        prefix = args.prefix

        match operation:
            case "upload":
                # Get the name of the file. This is used, along with your integration name,
                # to define a unique object path in Lattice for the image.
                file_name = os.path.basename(file_path)

                upload_response = await upload_object(file_path, file_name, entity_id, client)

                object_path = f"/api/v1/objects/{upload_response.content_identifier.path}"
                logging.info(f"Object path: {object_path}")

                await override_entity(operation, object_path, entity_id, client)

            case "download":
                result = await download_object(object_path, client)
                save_object(result, file_path)

            case "list":
                await list_objects(prefix, client)

            case "delete":
                result = await delete_object(object_path, client)
                await override_entity(operation, object_path, entity_id, client)

            case _:
                logging.error("Operation not supported")

    except asyncio.CancelledError or KeyboardInterrupt:
        logging.error(">>>Exiting...")
    except Exception as error:
        logging.error(f"Exception: {error}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Object Store API")

    parser.add_argument('--operation', type=str, required=True,
                        help='The API service operation you want to execute. \
                            Possible values: upload | download | list | delete')
    parser.add_argument('--file', type=str, required=False,
                        help='The file you want to upload.')
    parser.add_argument('--path', type=str, required=False,
                        help='The path of the file you want to donwload, or delete.')
    parser.add_argument('--entity', type=str, required=False,
                        help='The unique entity ID of the entity associated with the object. \
                            This option applies to upload and delete operations.')
    parser.add_argument('--prefix', type=str, required=False,
                        help='The prefix of the relative path used to list objects.')
    args = parser.parse_args()

    asyncio.run(main(args))