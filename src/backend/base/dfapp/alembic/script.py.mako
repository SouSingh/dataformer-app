"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.engine.reflection import Inspector
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)  # type: ignore
    table_names = inspector.get_table_names()
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)  # type: ignore
    table_names = inspector.get_table_names()
    ${downgrades if downgrades else "pass"}
