import logging
import json
from confluent_kafka.admin import AdminClient, ResourceType, ResourcePatternType 
from confluent_kafka.admin import AclBinding, AclBindingFilter
from confluent_kafka.admin import AclOperation, AclPermissionType

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_admin_client(bootstrap_servers):
    logger.info(f"Creating Kafka Admin Client for bootstrap servers: {bootstrap_servers}")
    return AdminClient({"bootstrap.servers": bootstrap_servers})

def add_acl(admin_client, resource_type, resource_name, principal, operation, permission_type, pattern_type=ResourcePatternType.LITERAL):
    acl = AclBinding(
        restype=resource_type,
        name=resource_name,
        resource_pattern_type=pattern_type,
        principal=f"User:{principal}",
        host="*",
        operation=operation,
        permission_type=permission_type
    )
    
    fs = admin_client.create_acls([acl])
    
    for acl, f in fs.items():
        try:
            f.result()  # Wait for the result
            logger.info(f"✅ ACL successfully added: {acl}")
        except Exception as e:
            logger.error(f"❌ Failed to add ACL {acl}: {e}")

def list_acls(admin_client):
    """List all ACLs in the Kafka cluster."""
    logger.info("Fetching all ACLs from Kafka cluster...")
    acl_filter = AclBindingFilter(
        restype=ResourceType.ANY,
        name=None,
        resource_pattern_type=ResourcePatternType.ANY,
        principal=None,
        host=None,
        operation=AclOperation.ANY,
        permission_type=AclPermissionType.ANY
    )
    
    fs = admin_client.describe_acls(acl_filter)
    
    try:
        acls = fs.result()
        if acls:
            logger.info("✅ ACLs in Kafka cluster:")
            for acl in acls:
                logger.info(acl)
        else:
            logger.info("No ACLs found.")
    except Exception as e:
        logger.error(f"❌ Failed to fetch ACLs: {e}")

def load_acls_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error loading ACLs from file {filename}: {e}")
        return []

if __name__ == "__main__":
    BOOTSTRAP_SERVERS = "localhost:9092"  # Update with your Kafka brokers
    ACL_FILE = "acls.json"  # JSON file containing ACL rules

    logger.info("Starting Kafka ACL batch processing script.")
    admin_client = create_admin_client(BOOTSTRAP_SERVERS)
    
    acls = load_acls_from_file(ACL_FILE)
    
    for acl in acls:
        add_acl(
            admin_client=admin_client,
            resource_type=getattr(ResourceType, acl["resource_type"].upper()),
            resource_name=acl["resource_name"],
            principal=acl["principal"],
            operation=getattr(AclOperation, acl["operation"].upper()),
            permission_type=getattr(AclPermissionType, acl["permission_type"].upper())
        )
    
    logger.info("Kafka ACL batch processing completed.")

    # List all ACLs after processing
    list_acls(admin_client)