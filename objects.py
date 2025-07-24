import logging, os

async def upload_object(file_path, client):
    try:
        # Get the file name.
        file_name = os.path.basename(file_path)
        # Define a unique path for the object using the file name.
        object_path = f"{file_name}"
        # Open the file in binary mode.
        with open(f"{file_path}", "rb") as file:
            print(file)
            response = client.objects.upload_object(
                object_path=object_path,
                request=file
            )
        return response
    except Exception as error:
        logging.error(f"Exception: {error}")

async def download_object(object_path, client):
    try:
        response = client.objects.get_object(
            object_path=object_path
        )
        chunks = [chunk for chunk in response]
        return b''.join(chunks)
    except Exception as error:
        logging.error(f"Exception: {error}")

async def delete_object(object_path, client):
    try:
        response = client.objects.delete_object(
            object_path=object_path
        )
        return response
    except Exception as error:
        logging.error(f"Exception: {error}")

async def list_objects(prefix, client):
    try:
        response = client.list_objects(
            prefix=prefix
        )
        for item in response:
            yield item
            
    except Exception as error:
        logging.error(f"Exception: {error}")