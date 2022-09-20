import boto3
import botocore

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
    StartRDSResponse,
    StopRDSResponse,
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
        return_value = DescribeDBResponse(**response)
        self.arn = return_value.DBInstances[0].DBInstanceArn
        if return_value.DBInstances[0].Endpoint:
            self.endpoint = return_value.DBInstances[0].Endpoint
        return return_value

    def start_db(self) -> StartRDSResponse:
        """Start the database instance"""
        response = self.rds_client.start_db_instance(DBInstanceIdentifier=self.db_name)

        return StartRDSResponse(**response)

    def stop_db(self, snap_shot_identifier: Optional[str] = None) -> StopRDSResponse:
        """Stop the database instance"""
        arg = {"DBInstanceIdentifier": self.db_name}
        if snap_shot_identifier:
            arg["DBSnapshotIdentifier"] = snap_shot_identifier
        response = self.rds_client.stop_db_instance(**arg)
        return StopRDSResponse(**response)
