from mc_automation_tools import postgres

from common.config.config import Database

DATABASE_COLUMNS = """ max_resolution_deg , product_bbox , product_id"""


# ToDo: Reuse this function
def get_db_client(db_name=Database.PG_RECORD_PYCSW_DB):
    return postgres.PGClass(
        Database.PG_HOST,
        db_name,
        Database.PG_USER,
        Database.PG_PASS,
        Database.RASTER_CATALOG,
        port=int(Database.PG_PORT),
    )
