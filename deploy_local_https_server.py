import datetime
import http.server
import os
import ssl
import socket
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509 import CertificateBuilder, DNSName, Name, NameAttribute, SubjectAlternativeName
from cryptography.x509.oid import NameOID

# ===== CONFIGURATION ======
CERT_FILE = 'server.crt'
KEY_FILE = 'server.key'

HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 1234


def get_local_ip():
    """Gets the local IP address of the machine on the local network."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)  # Don't wait on connection
    try:
        s.connect(('8.8.8.8', 80))  # Using Google's DNS (8.8.8.8)
        ip = s.getsockname()[0]  # Get local IP associated with the network interface
    except (socket.error, OSError) as e:
        ip = '0.0.0.0'
        print(f'Error while determining local IP: {e}')
    finally:
        s.close()
    return ip


def generate_private_key():
    """Generates and saves the RSA private key."""
    priv_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)  # Standard values
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(priv_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    return priv_key


def generate_self_signed_cert(priv_key):
    """Generates and saves the self-signed certificate."""
    subject = issuer = Name([NameAttribute(NameOID.COMMON_NAME, 'localhost')])
    not_valid_before = datetime.datetime.now(datetime.timezone.utc)
    not_valid_after = not_valid_before + datetime.timedelta(days=365)

    cert = CertificateBuilder().subject_name(subject).issuer_name(issuer).not_valid_before(
        not_valid_before).not_valid_after(not_valid_after).serial_number(1000).public_key(
        priv_key.public_key()).add_extension(
        SubjectAlternativeName([DNSName('localhost')]),
        critical=False,
    ).sign(priv_key, hashes.SHA256())

    with open(CERT_FILE, 'wb') as cert_file:
        cert_file.write(cert.public_bytes(serialization.Encoding.PEM))

    return cert


def create_https_server(handler_class):
    """Creates and configures the HTTPS server."""
    server_address = (HOST, PORT)
    server = http.server.HTTPServer(server_address, handler_class)
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    server.socket = context.wrap_socket(server.socket, server_side=True)
    return server


# Create the personalized HTTP Handler
class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    pass


# Generate the private key and certificate
private_key = generate_private_key()
generate_self_signed_cert(private_key)

# Create and configure the HTTPS server
httpd_server = create_https_server(MyHTTPRequestHandler)

# Get the local IP address of the machine
local_ip = get_local_ip()

# Start the HTTPS server
print(f'HTTPS server running at --> https://{local_ip}:{PORT}')

try:
    httpd_server.serve_forever()
except KeyboardInterrupt:
    print('===== Server stopped =====')
finally:
    # Remove the certificate and private key after stopping the server
    if os.path.exists(CERT_FILE):
        os.remove(CERT_FILE)
        print(f'Certificate "{CERT_FILE}" has been deleted')
    if os.path.exists(KEY_FILE):
        os.remove(KEY_FILE)
        print(f'Private key "{KEY_FILE}" has been deleted')
