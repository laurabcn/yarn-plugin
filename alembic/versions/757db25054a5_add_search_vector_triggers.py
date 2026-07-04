"""add search_vector triggers

Revision ID: 757db25054a5
Revises: e910eab7e245
Create Date: 2026-07-04 05:58:01.309961

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '757db25054a5'
down_revision: Union[str, None] = 'e910eab7e245'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE FUNCTION yarns_search_vector_update() RETURNS trigger AS $$
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
        CREATE TRIGGER yarns_search_vector_trigger
        BEFORE INSERT OR UPDATE ON yarns
        FOR EACH ROW EXECUTE FUNCTION yarns_search_vector_update();
        """
    )

    op.execute(
        """
        CREATE FUNCTION patterns_search_vector_update() RETURNS trigger AS $$
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
        CREATE TRIGGER patterns_search_vector_trigger
        BEFORE INSERT OR UPDATE ON patterns
        FOR EACH ROW EXECUTE FUNCTION patterns_search_vector_update();
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS patterns_search_vector_trigger ON patterns")
    op.execute("DROP FUNCTION IF EXISTS patterns_search_vector_update()")
    op.execute("DROP TRIGGER IF EXISTS yarns_search_vector_trigger ON yarns")
    op.execute("DROP FUNCTION IF EXISTS yarns_search_vector_update()")
