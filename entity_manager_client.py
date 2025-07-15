from modules.src.anduril import Media, MediaItem, Entity, Provenance, Provenance

from datetime import datetime, timezone
import logging

async def override_entity(operation, object_path, entity_id, client):
    try:
        latest_timestamp = datetime.now(timezone.utc)
        
        provenance = Provenance(
            integration_name="your_integration_name",
            data_type="test_data",
            source_update_time=latest_timestamp
        )

        if operation == "upload":
            media = Media(
                media=[
                    MediaItem(
                        relative_path=object_path,
                        type="MEDIA_TYPE_THUMBNAIL"
                    )
                ]
            )
        elif operation == "delete":
            media = Media(
                media=[]
            )

        client.entities.override_entity(
            entity_id=entity_id,
            field_path="media.media",
            entity=Entity(
                entity_id=entity_id,
                media=media
            ),
            provenance=provenance
        )
    except Exception as error:
        logging.error(f"Exception: {error}")