from anduril import Lattice

from objects import upload_object, download_object, delete_object, list_objects
from entities import override_entity
import os, sys, asyncio, logging, argparse

lattice_endpoint = os.getenv('LATTICE_ENDPOINT')
environment_token = os.getenv('ENVIRONMENT_TOKEN')
# Remove sandboxes_token from the following statements if you are not developing on Sandboxes.
sandboxes_token = os.getenv('SANDBOXES_TOKEN')
if not environment_token or not lattice_endpoint or not sandboxes_token:
    logging.warning("Missing environment variables.")
    sys.exit(1)

def save_object(data, object_path):
    file_name = os.path.basename(object_path)
    with open(file_name, 'wb') as file:
        file.write(data)

client = Lattice(
    base_url=f"https://{lattice_endpoint}",
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
                # Get the name of the file.
                upload_response = await upload_object(file_path, client)
                if (upload_response):
                    object_path = f"/api/v1/objects/{upload_response.content_identifier.path}"
                    logging.info(f"Object path: {object_path}")
                else:
                    logging.error("Failed to upload object.")
                    sys.exit(1)

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
    parser = argparse.ArgumentParser(description="Track Thumbnails Sample App")

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