import ipaddress
import os
import tempfile
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from fastapi.security import APIKeyQuery

from .net import get_local_ip


@contextmanager
def temp_tls_cert():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    local_ip = get_local_ip()
    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COMMON_NAME, local_ip),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "ShDir"),
        ]
    )

    now = datetime.now(timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + timedelta(days=7))
        .add_extension(
            x509.SubjectAlternativeName(
                [
                    x509.IPAddress(ipaddress.ip_address(local_ip)),
                    x509.DNSName("localhost"),
                ]
            ),
            critical=False,
        )
        .sign(private_key, hashes.SHA256())
    )
    cert_file = tempfile.NamedTemporaryFile(delete=False, suffix=".crt")
    key_file = tempfile.NamedTemporaryFile(delete=False, suffix=".key")

    try:
        key_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
        key_file.close()

        cert_file.write(cert.public_bytes(serialization.Encoding.PEM))
        cert_file.close()

        yield cert_file.name, key_file.name

    finally:
        for path in (cert_file.name, key_file.name):
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass
