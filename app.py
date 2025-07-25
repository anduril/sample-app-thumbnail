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

def save_object(data, file_path):
    # If file_path is None, use a default name
    if file_path is None:
        file_path = "downloaded_file"
    
    # Use the provided file path or extract filename from object path
    if os.path.isdir(os.path.dirname(file_path)) or os.path.dirname(file_path) == "":
        output_path = file_path
    else:
        output_path = os.path.basename(file_path)
        
    with open(output_path, 'wb') as file:
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
                if not object_path:
                    logging.error("Object path is required for download")
                    sys.exit(1)
                    
                result = await download_object(object_path, client)
                if result:
                    save_object(result, file_path if file_path else object_path)
                    logging.info(f"Object downloaded successfully")
                else:
                    logging.error("Failed to download object")

            case "list":
                items = await list_objects(prefix, client)

            case "delete":
                result = await delete_object(object_path, client)
                await override_entity(operation, object_path, entity_id, client)

            case _:
                logging.error("Operation not supported")

    except (asyncio.CancelledError, KeyboardInterrupt):
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
                        help='The path of the file you want to download or delete.')
    parser.add_argument('--entity', type=str, required=False,
                        help='The unique entity ID of the entity associated with the object. \
                            This option applies to upload and delete operations.')
    parser.add_argument('--prefix', type=str, required=False,
                        help='The prefix of the relative path or file name used to list objects.')
    args = parser.parse_args()

    asyncio.run(main(args))