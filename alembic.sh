#!/bin/sh

if [ ! `find . -type f -name "alembic.ini"` ]; then
  alembic init -t async alembic
  sed -i "s/from alembic import context/from alembic import context\nfrom settings import ORM\nfrom utils.orm.db import Base/" alembic/env.py
  sed -i '/config = context.config/r alembic.txt' alembic/env.py
  sed -i "s/target_metadata = None/target_metadata = Base.metadata/" alembic/env.py
fi

COUNT=`find alembic/versions -name '*.py' | wc -l`
alembic revision -m "$COUNT migration" --autogenerate
alembic upgrade head