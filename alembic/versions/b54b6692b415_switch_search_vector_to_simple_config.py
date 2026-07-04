"""switch search_vector to simple config

Revision ID: b54b6692b415
Revises: 757db25054a5
Create Date: 2026-07-04 07:02:35.815475

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b54b6692b415'
down_revision: Union[str, None] = '757db25054a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION yarns_search_vector_update() RETURNS trigger AS $$
        BEGIN
            NEW.search_vector := to_tsvector(
                'simple',
                coalesce(NEW.name, '') || ' ' ||
                coalesce(NEW.description, '') || ' ' ||
                array_to_string(coalesce(NEW.tags, '{}'), ' ')
            );
            RETURN NEW;
        END
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE OR REPLACE FUNCTION patterns_search_vector_update() RETURNS trigger AS $$
        BEGIN
            NEW.search_vector := to_tsvector(
                'simple',
                coalesce(NEW.name, '') || ' ' ||
                coalesce(NEW.description, '') || ' ' ||
                array_to_string(coalesce(NEW.tags, '{}'), ' ')
            );
            RETURN NEW;
        END
        $$ LANGUAGE plpgsql;
        """
    )
    # Recompute search_vector for existing rows — the trigger only fires on future insert/update.
    op.execute("UPDATE yarns SET name = name")
    op.execute("UPDATE patterns SET name = name")


def downgrade() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION yarns_search_vector_update() RETURNS trigger AS $$
        BEGIN
            NEW.search_vector := to_tsvector(
                'english',
                coalesce(NEW.name, '') || ' ' ||
                coalesce(NEW.description, '') || ' ' ||
                array_to_string(coalesce(NEW.tags, '{}'), ' ')
            );
            RETURN NEW;
        END
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE OR REPLACE FUNCTION patterns_search_vector_update() RETURNS trigger AS $$
        BEGIN
            NEW.search_vector := to_tsvector(
                'english',
                coalesce(NEW.name, '') || ' ' ||
                coalesce(NEW.description, '') || ' ' ||
                array_to_string(coalesce(NEW.tags, '{}'), ' ')
            );
            RETURN NEW;
        END
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute("UPDATE yarns SET name = name")
    op.execute("UPDATE patterns SET name = name")
