"""Initial schema

Revision ID: 6be4b6c6a71b
Revises: 
Create Date: 2025-07-31 11:05:27.436279
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import json
import os

# revision identifiers, used by Alembic.
revision: str = '6be4b6c6a71b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# --- UPGRADE -----------------------------------------------------------------

def upgrade() -> None:
    # --- ENUMS manuell erstellen, falls sie noch nicht existieren ---
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'difficultyenum') THEN
                CREATE TYPE difficultyenum AS ENUM ('easy', 'medium', 'hard');
            END IF;
        END$$;
    """)
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'statusenum') THEN
                CREATE TYPE statusenum AS ENUM ('pending', 'accepted', 'wrong_answer', 'error');
            END IF;
        END$$;
    """)

    # --- Tabellen erstellen ---
    op.create_table(
        'problems',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('difficulty', sa.Enum('easy', 'medium', 'hard', name='difficultyenum', create_type=False), nullable=False),
        sa.Column('example_input', sa.Text(), nullable=True),
        sa.Column('example_output', sa.Text(), nullable=True)
    )

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('hashed_password', sa.String(length=256), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
    )

    op.create_table(
        'submissions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('problem_id', sa.Integer(), nullable=False),
        sa.Column('submitted_code', sa.Text(), nullable=False),
        sa.Column('language', sa.String(length=30), nullable=False),
        sa.Column('status', sa.Enum('pending', 'accepted', 'wrong_answer', 'error', name='statusenum', create_type=False), nullable=False),
        sa.Column('execution_time_ms', sa.Float(), nullable=True),
        sa.Column('memory_usage_mb', sa.Float(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['problem_id'], ['problems.id']),
    )

    op.create_table(
        'test_cases',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('problem_id', sa.Integer(), nullable=False),
        sa.Column('input', sa.Text(), nullable=False),
        sa.Column('expected_output', sa.Text(), nullable=False),
        sa.Column('is_hidden', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['problem_id'], ['problems.id']),
    )

    # --- JSON-Probleme einfügen ---
    current_dir = os.path.dirname(__file__)
    json_file_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'problems', 'initialProblems.json'))

    if not os.path.exists(json_file_path):
        print(f"Warnung: Datei '{json_file_path}' nicht gefunden. Probleme werden nicht geladen.")
        return

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            problems_data = json.load(f)

        if not isinstance(problems_data, list):
            print(f"Fehler: '{json_file_path}' enthält kein Array von Problemen.")
            return

        problems_table = sa.Table(
            'problems',
            sa.MetaData(),
            sa.Column('id', sa.Integer),
            sa.Column('title', sa.String),
            sa.Column('description', sa.Text),
            sa.Column('difficulty', sa.Enum('easy', 'medium', 'hard', name='difficultyenum', create_type=False)),
            sa.Column('example_input', sa.Text),
            sa.Column('example_output', sa.Text),
        )

        op.bulk_insert(problems_table, problems_data)
        print(f"{len(problems_data)} Probleme erfolgreich eingefügt.")

    except Exception as e:
        print(f"Fehler beim Einfügen der Problem-Daten: {e}")

# --- DOWNGRADE ---------------------------------------------------------------

def downgrade() -> None:
    op.drop_table('test_cases')
    op.drop_table('submissions')
    op.drop_table('users')
    op.drop_table('problems')

    # ENUMs löschen
    op.execute("DROP TYPE IF EXISTS difficultyenum")
    op.execute("DROP TYPE IF EXISTS statusenum")