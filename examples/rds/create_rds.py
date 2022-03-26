from ezaws import Region, RDS, DBEngine, DBInstanceType, ParameterStore
from pprint import pprint


if __name__ == "__main__":

    ps = ParameterStore(region="eu-central-1")
    db_pass = ps.get_parameter("/passwords/infrastructure/rds/pipeline01/password")
    db_user = ps.get_parameter("/passwords/infrastructure/rds/pipeline01/username")

    rds = RDS(
        region=Region.eu_central_1,
        master_user_password=db_pass.Parameter.Value,
        master_username=db_user.Parameter.Value,
        storage=5,
        db_name="pipeline01",
        db_engine=DBEngine.MYSQL.value,
        db_instance=DBInstanceType.db_t2_micro.value,
    )

    resp = rds.create_database()
    pprint(resp)
    # resp = rds.delete_database()
    # pprint(resp)
    resp = rds.describe_db()
    pprint(resp)
