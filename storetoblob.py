from azure.storage.blob import BlobServiceClient


def main(file_path):
    container_name  = "input"

    # file_name = file_path.split('/')
    # file_name = file_name[len(file_name) - 1]
    file_name = "image1"
    account_name = "mockupcode"
    account_name = account_name.strip()
    account_key = "Hbfdp0tL6MHdbNXlCGbx5+IN9n1RRkPiG2lde+rz38rqJd/PLmdYSKroh0A99iyQoNyIiji5azySKr0+B4GYwA=="
    account_key = account_key.strip()

    connect_str = "DefaultEndpointsProtocol=https;AccountName=mockupcode;AccountKey=Hbfdp0tL6MHdbNXlCGbx5+IN9n1RRkPiG2lde+rz38rqJd/PLmdYSKroh0A99iyQoNyIiji5azySKr0+B4GYwA==;EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)
    return "done"

main()