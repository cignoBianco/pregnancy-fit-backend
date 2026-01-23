"""add is_active and exercisecategory safely

Revision ID: 3e9015daf3c4
Revises: c3f7aad95529
Create Date: 2026-01-23 00:19:26.683361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '3e9015daf3c4'
down_revision: Union[str, Sequence[str], None] = 'c3f7aad95529'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Создаём ENUM тип (обязательно ДО использования!)
    exercisecategory_enum = sa.Enum('strength', 'cardio', 'mobility', 'breathing', name='exercisecategory')
    exercisecategory_enum.create(op.get_bind())

    # 2. Добавляем is_active как nullable=True (без значения по умолчанию)
    op.add_column('exercise', sa.Column('is_active', sa.Boolean(), nullable=True))

    # 3. Заполняем все существующие строки значением TRUE (или FALSE, если нужно)
    op.execute("UPDATE exercise SET is_active = TRUE WHERE is_active IS NULL;")

    # 4. Теперь делаем is_active NOT NULL — уже безопасно!
    op.alter_column('exercise', 'is_active', nullable=False)

    # 5. Меняем тип category на ENUM — с явным преобразованием
    # PostgreSQL требует USING, потому что VARCHAR → ENUM — неавтоматическое
    op.alter_column('exercise', 'category',
               existing_type=sa.VARCHAR(),
               type_=exercisecategory_enum,
               existing_nullable=True,
               postgresql_using='category::exercisecategory')

    # 6. Создаём индекс (если нужен)
    op.create_index(op.f('ix_exercise_name'), 'exercise', ['name'], unique=False)


def downgrade() -> None:
    # 1. Удаляем индекс
    op.drop_index(op.f('ix_exercise_name'), table_name='exercise')

    # 2. Меняем category обратно на VARCHAR
    op.alter_column('exercise', 'category',
               existing_type=sa.Enum('strength', 'cardio', 'mobility', 'breathing', name='exercisecategory'),
               type_=sa.VARCHAR(),
               existing_nullable=True)

    # 3. Удаляем столбец is_active
    op.drop_column('exercise', 'is_active')

    # 4. Удаляем ENUM тип
    sa.Enum('strength', 'cardio', 'mobility', 'breathing', name='exercisecategory').drop(op.get_bind())