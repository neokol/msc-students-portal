"""Create database tables

Revision ID: d3d7260fadf5
Revises: 
Create Date: 2024-07-04 23:21:24.535199

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3d7260fadf5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_id', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_grades_id', table_name='grades')
    op.drop_table('grades')
    op.drop_index('ix_courses_id', table_name='courses')
    op.drop_index('ix_courses_name', table_name='courses')
    op.drop_table('courses')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('courses',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('courses_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='courses_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_courses_name', 'courses', ['name'], unique=False)
    op.create_index('ix_courses_id', 'courses', ['id'], unique=False)
    op.create_table('grades',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('course_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('grade', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('is_finalized', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], name='grades_course_id_fkey'),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], name='grades_student_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='grades_pkey')
    )
    op.create_index('ix_grades_id', 'grades', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('full_name', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('role', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    # ### end Alembic commands ###
