from dataclasses import dataclass


@dataclass(frozen=True)
class Region:
    """All the AWS regions"""

    us_east_2: str = "us-east-2"  # US East (Ohio)
    us_east_1: str = "us-east-1"  # US East (N. Virginia)
    us_west_1: str = "us-west-1"  # US West (N. California)
    us_west_2: str = "us-west-2"  # US West (Oregon)
    af_south_1: str = "af-south-1"  # Africa (Cape Town)
    ap_east_1: str = "ap-east-1"  # Asia Pacific (Hong Kong)
    ap_southeast_3: str = "ap-southeast-3"  # Asia Pacific (Jakarta)
    ap_south_1: str = "ap-south-1"  # Asia Pacific (Mumbai)
    ap_northeast_3: str = "ap-northeast-3"  # Asia Pacific (Osaka)
    ap_northeast_2: str = "ap-northeast-2"  # Asia Pacific (Seoul)
    ap_southeast_1: str = "ap-southeast-1"  # Asia Pacific (Singapore)
    ap_southeast_2: str = "ap-southeast-2"  # Asia Pacific (Sydney)
    ap_north_east_1: str = "ap-northeast-1"  # Asia Pacific (Tokyo)
    ca_central_1: str = "ca-central-1"  # Canada (Central)
    cn_north_1: str = "cn-north-1"  # China (Beijing)
    cn_north_west: str = "cn-northwest-1"  # China (Ningxia)
    eu_central_1: str = "eu-central-1"  # Europe (Frankfurt)
    eu_west_1: str = "eu-west-1"  # Europe (Ireland)
    eu_west_2: str = "eu-west-2"  # Europe (London)
    eu_south_1: str = "eu-south-1"  # Europe (Milan)
    eu_west_3: str = "eu-west-3"  # Europe (Paris)
    eu_north_1: str = "eu-north-1"  # Europe (Stockholm)
    me_south_1: str = "me-south-1"  # Middle East (Bahrain)
    sa_east_1: str = "sa-east-1"  # South America (São Paulo)
