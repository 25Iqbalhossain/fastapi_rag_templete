from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.db.models.document import DocumentStatus


class DocumentBase(BaseModel):
    filename: str
    content_type: str
    status: DocumentStatus


class DocumentCreate(DocumentBase):
    storage_path: str


class DocumentRead(DocumentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    error_message: str | None = None

    model_config = ConfigDict(from_attributes=True)