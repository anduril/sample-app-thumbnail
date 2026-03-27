from anduril import Media, MediaItem, Entity, Provenance
from datetime import datetime, timezone
import logging
import os

INTEGRATION_NAME = os.getenv("INTEGRATION_NAME", "sample-app-thumbnail")
DATA_TYPE = os.getenv("DATA_TYPE", "test_data")

logger = logging.getLogger(__name__)


async def override_entity(
    operation: str, object_path: str, entity_id: str, client
) -> None:
    """Override an entity's media component to link or unlink a thumbnail.

    Args:
        operation: Either "upload" (link image) or "delete" (clear media).
        object_path: The object path returned by the Objects API.
        entity_id: The target entity's unique ID.
        client: An authenticated Lattice client instance.

    Raises:
        ValueError: If *operation* is not "upload" or "delete".
    """
    if operation == "upload":
        media = Media(
            media=[
                MediaItem(
                    relative_path=object_path,
                    type="MEDIA_TYPE_IMAGE",
                )
            ]
        )
    elif operation == "delete":
        media = Media(media=[])
    else:
        raise ValueError(
            f"Unsupported operation: {operation!r} (expected 'upload' or 'delete')"
        )

    provenance = Provenance(
        integration_name=INTEGRATION_NAME,
        data_type=DATA_TYPE,
        source_update_time=datetime.now(timezone.utc),
    )

    try:
        await client.entities.override_entity(
            entity_id=entity_id,
            field_path="media.media",
            entity=Entity(
                entity_id=entity_id,
                media=media,
            ),
            provenance=provenance,
        )
    except Exception:
        logger.exception("Failed to override entity %s", entity_id)
        raise
