import boto3
import botocore
from ezaws import Region
from dataclasses import dataclass
from botocore.exceptions import ClientError
from ezaws.models.rds import (
    DescribeDBResponse,
    DBInstanceNotFoundResponse,
    CreateDBResponse,
    DeleteDBResponse,
    Endpoint,
    DBInstance,
    DBEngine,
)
from typing import Union, Optional
from ezaws.exceptions import RDSException


@dataclass
class RDS:
    """
    Interface to the SSM Parameter store.
    """

    region: str
    master_user_password: str
    master_username: str
    db_name: str
    db_engine: DBEngine
    db_instance: DBInstance
    storage: int  # GiB
    arn: Optional[str] = None
    endpoint: Optional[Endpoint] = None
    rds_client: botocore.client = boto3.client("rds")

    def create_database(self) -> Union[DescribeDBResponse, CreateDBResponse]:
        """Create the database for this RDS instance"""
        resp = self.describe_db()
        if isinstance(resp, DescribeDBResponse):
            return resp
        elif isinstance(resp, DBInstanceNotFoundResponse):
            response = self.rds_client.create_db_instance(
                AllocatedStorage=self.storage,
                DBInstanceClass=self.db_instance,
                DBInstanceIdentifier=self.db_name,
                Engine=self.db_engine,
                MasterUserPassword=self.master_user_password,
                MasterUsername=self.master_username,
            )
            db_response = CreateDBResponse(**response)
            self.arn = db_response.DBInstance.DBInstanceArn
            return CreateDBResponse(**response)
        else:
            raise RDSException("Runtime error executing 'RDS.create_database'")

    def delete_database(self) -> Union[DeleteDBResponse, None]:
        """Delete this RDS instance"""
        resp = self.describe_db()
        if isinstance(resp, DescribeDBResponse):
            response = self.rds_client.delete_db_instance(
                DBInstanceIdentifier=self.db_name,
                SkipFinalSnapshot=True,
            )
            return DeleteDBResponse(**response)
        else:
            return None

    def describe_db(self) -> Union[DescribeDBResponse, DBInstanceNotFoundResponse]:
        """Have AWS describe the RDS instance, returns
        DBInstanceNotFoundResponse in case the instance does not exist."""

        try:
            response = self.rds_client.describe_db_instances(
                DBInstanceIdentifier=self.db_name,
                MaxRecords=100,
                Filters=[
                    {
                        "Name": "engine",
                        "Values": [
                            self.db_engine,
                        ],
                    }
                ],
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "DBInstanceNotFound":
                # this means the DB does not exist
                e.response
                return DBInstanceNotFoundResponse()
            raise e
        # pprint(response, width=2)
        response = DescribeDBResponse(**response)
        self.arn = response.DBInstances[0].DBInstanceArn
        if response.DBInstances[0].Endpoint:
            self.endpoint = response.DBInstances[0].Endpoint
        return response


if __name__ == "__main__":
    from pprint import pprint

    rds = RDS(
        region=Region.eu_central_1,
        master_user_password="U2sbF~q~%!Lrp^vq",
        master_username="admin01",
        storage=5,
        db_name="pipeline01",
        db_engine=DBEngine.MYSQL.value,
        db_instance=DBInstance.db_t2_micro.value,
    )
    resp = rds.create_database()
    pprint(resp)
    # resp = rds.delete_database()
    # pprint(resp)
    resp = rds.describe_db()
    pprint(resp)
    # sql querry:
    import mysql.connector

    mydb = mysql.connector.connect(
        host=rds.endpoint.Address,
        user=rds.master_username,
        password=rds.master_user_password,
        database="pipeline01",
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM Orders")

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)
