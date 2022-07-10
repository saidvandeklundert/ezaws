from ezaws.models.common import ResponseMetadata
from pydantic import BaseModel
from typing import List, Any, Dict, Optional
from enum import Enum


class DBInstanceType(Enum):
    db_t2_micro = "db.t2.micro"


class DBEngine(Enum):
    MYSQL = "mysql"
    POSTGRES = "postgress"
    MARIA_DB = "mariadb"
    AURORA = "aurora"


class DBInstanceNotFoundResponse(BaseModel):
    error_message: str = "DBInstanceNotFound"


class Endpoint(BaseModel):
    Address: str
    HostedZoneId: str
    Port: int


class DBInstance(BaseModel):
    DBInstanceIdentifier: str
    DBInstanceClass: str
    Engine: str
    DBInstanceStatus: str
    MasterUsername: str
    AllocatedStorage: int
    PreferredBackupWindow: str
    BackupRetentionPeriod: int
    DBSecurityGroups: List[Any]
    VpcSecurityGroups: Dict[Any, Any]
    DBParameterGroups: List[Any]
    DBSubnetGroup: Dict[Any, Any]
    PreferredMaintenanceWindow: str
    PendingModifiedValues: Dict[Any, Any]
    MultiAZ: bool
    EngineVersion: str
    AutoMinorVersionUpgrade: bool
    ReadReplicaDBInstanceIdentifiers: List[Any]
    LicenseModel: str
    OptionGroupMemberships: List[Any]
    PubliclyAccessible: bool
    StorageType: str
    DbInstancePort: int
    StorageEncrypted: bool
    DbiResourceId: str
    CACertificateIdentifier: str
    DomainMemberships: List[Any]
    Endpoint: Optional[Endpoint]
    CopyTagsToSnapshot: bool
    MonitoringInterval: int
    DBInstanceArn: str
    IAMDatabaseAuthenticationEnabled: bool
    PerformanceInsightsEnabled: bool
    DeletionProtection: bool
    AssociatedRoles: List[Any]
    TagList: List[Any]
    CustomerOwnedIpEnabled: bool
    ActivityStreamStatus: Optional[str]
    BackupTarget: str


class DescribeDBResponse(BaseModel):
    ResponseMetadata: ResponseMetadata
    DBInstances: List[DBInstance]


class CreateDBResponse(BaseModel):
    ResponseMetadata: ResponseMetadata
    DBInstance: DBInstance


class DeleteDBResponse(BaseModel):
    DBInstance: DBInstance
    ResponseMetadata: ResponseMetadata


class StartRDSResponse(BaseModel):
    DBInstance: DBInstance
    ResponseMetadata: ResponseMetadata


class StopRDSResponse(BaseModel):
    DBInstance: DBInstance
    ResponseMetadata: ResponseMetadata
