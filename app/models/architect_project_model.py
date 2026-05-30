from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey
)

from database import Base


class ArchitectProject(Base):

    __tablename__ = "architect_projects"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    architect_id = Column(
        Integer,
        ForeignKey(
            "arch_register_users.id"
        ),
        nullable=False
    )

    title = Column(
        String,
        nullable=False
    )

    location = Column(
        String,
        nullable=True
    )

    description = Column(
        Text,
        nullable=True
    )

    status = Column(
        String,
        default="In Progress"
    )

    image_url = Column(
        String,
        nullable=True
    )