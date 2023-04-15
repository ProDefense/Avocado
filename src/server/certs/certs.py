#This Python module allows for X509 certificate generation and manipulation
#Currently only supports RSA based certificates
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
import datetime
import os
from util.util import AVOCADO_ROOT

class cert_generator(object):
    def __init__(self, name: str, client: bool):
        self.name = name
        #create an RSA private key
        self.key = rsa.generate_private_key(
                    public_exponent=65537,
                    key_size=2048,
                    )
        self.cert_dir = os.path.join(AVOCADO_ROOT, "certs", self.name) 
        
        if client == False:
            self.CA, self.CA_Key, self.CA_Path = self.generate_CA() 
        else:
            self.CA, self.CA_Key, self.CA_Path = self.load_CA('root')

    def save_private_key(self):
        key_path = os.path.join(self.cert_dir, f"{self.name}-key.pem")
        try:
            os.makedirs(self.cert_dir, mode=0o750)
        except FileExistsError:
            pass
        with open(key_path, "wb") as f:
            f.write(self.key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            #encryption_algorithm=serialization.BestAvailableEncryption(b"A"), #THIS IS DANGEROUS?????
            encryption_algorithm=serialization.NoEncryption(),
            ))
        return key_path  

    def load_private_key(self, name: str):
        with open(name, "rb") as f:
            data = f.read()
            CA_Key = serialization.load_pem_private_key(data, password=None)
        return CA_Key

    def generate_csr(self):
        csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
            # Provide various details about who we are.
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"mysite.com"),
        ])).add_extension(
        x509.SubjectAlternativeName([
            # Describe what sites we want this certificate for.
            x509.DNSName(u"mysite.com"),
            x509.DNSName(u"www.mysite.com"),
            x509.DNSName(u"subdomain.mysite.com"),
        ]),
            critical=False,
        # Sign the CSR with our private key.
        ).sign(self.key, hashes.SHA256())
    

        # Write our CSR out to disk.
        with open("csr.pem", "wb") as f:
            f.write(csr.public_bytes(serialization.Encoding.PEM))

    def build_x509_cert(self):
        one_day = datetime.timedelta(1, 0, 0)  #get date
        private_key = self.key #get key
        public_key = private_key.public_key() #pubkey
        builder = x509.CertificateBuilder() #instantiate builder object
        
        builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, f'{self.name}'),
        ]))

        builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'root'),
        ]))

        builder = builder.not_valid_before(datetime.datetime.today() - one_day) 
        
        builder = builder.not_valid_after(datetime.datetime.today() + (one_day * 30)) 
        
        builder = builder.serial_number(x509.random_serial_number())
        
        builder = builder.public_key(public_key)
        
        builder = builder.add_extension(
        x509.SubjectAlternativeName(
        [x509.DNSName(f'{self.name}')]
        ),
        critical=False
        )

        builder = builder.add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True,
        )
    
        certificate = builder.sign(
        private_key=self.CA_Key, algorithm=hashes.SHA256(),
        )
        assert isinstance(certificate, x509.Certificate)

        cert_path = self.save_cert(certificate)
        key_path =self.save_private_key()

        #print(cert_path, key_path) debug purposes
        return cert_path, key_path
    
    def generate_CA(self):
        one_day = datetime.timedelta(1, 0, 0)  #get date
        private_key = rsa.generate_private_key(
                    public_exponent=65537,
                    key_size=2048,
                    )
        public_key = private_key.public_key() #pubkey
        builder = x509.CertificateBuilder() #instantiate builder object
        
        builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'root'),
        ]))

        builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'root'),
        ]))

        builder = builder.not_valid_before(datetime.datetime.today() - one_day) 
        
        builder = builder.not_valid_after(datetime.datetime.today() + (one_day * 30)) 
        
        builder = builder.serial_number(x509.random_serial_number())
        
        builder = builder.public_key(public_key)
        
        builder = builder.add_extension(
        x509.SubjectAlternativeName(
        [x509.DNSName(u'root')]
        ),
        critical=False
        )

        builder = builder.add_extension(
        x509.BasicConstraints(ca=True, path_length=None), critical=True,
        )
    
        certificate = builder.sign(
        private_key=private_key, algorithm=hashes.SHA256(),
        )
        assert isinstance(certificate, x509.Certificate)

        rootCA_dir = os.path.join(AVOCADO_ROOT, "certs", "root") #.avocado/certs/root
        rootCA_key = os.path.join(rootCA_dir, "root-key.pem")
        rootCA_cert = os.path.join(rootCA_dir, "root.pem")

        try:
            os.makedirs(rootCA_dir, mode=0o750)
        except FileExistsError:
            pass

        with open(rootCA_key, "wb") as f:
            f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            #encryption_algorithm=serialization.BestAvailableEncryption(b"A"), #THIS IS DANGEROUS?????
            encryption_algorithm=serialization.NoEncryption(),
            ))

        with open(rootCA_cert, "wb") as f:
            f.write(certificate.public_bytes(serialization.Encoding.PEM))
        
        return certificate, private_key, rootCA_cert

    def load_csr(self, csr_name: str):
        with open(csr_name, "rb") as f:
            pem_req_data = f.read()
        csr = x509.load_pem_x509_csr(pem_req_data)
        assert isinstance(csr.signature_hash_algorithm, hashes.SHA256)
        return csr

    def save_csr(self):
        with open("csr.pem", "wb") as f:
            f.write(csr.public_bytes(serialization.Encoding.PEM))
        return True

    def sign_csr(self):
        pass #Not implemented yet

    def load_cert(self, cert_name: str):
        with open(cert_name, "rb") as f:
            pem_data = f.read()
        cert = x509.load_pem_x509_certificate(pem_data)
        return cert

    def save_cert(self, cert):
        cert_path = os.path.join(self.cert_dir, f"{self.name}.pem")
        try:
            os.makedirs(self.cert_dir, mode=0o750)
        except FileExistsError:
            pass
        with open(cert_path, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        return cert_path

    def load_CA(self, name):
        #This is required so that the implant can sign their cert for mtls, this is probably bad
        #TODO Make it so the CA can be in any location
        rootCA_dir = os.path.join(AVOCADO_ROOT, "certs", "root") #.avocado/certs/root
        rootCA_key = os.path.join(rootCA_dir, "root-key.pem")
        rootCA_cert = os.path.join(rootCA_dir, "root.pem")
        
        CA_key = self.load_private_key(rootCA_key)
        CA_cert = self.load_cert(rootCA_cert)    
        return CA_cert, CA_key, rootCA_cert



#### FOR TESTING PURPOSES#######
def main():
    generator = cert_generator('test_hostname', client=False)
    cert_path, key_path = generator.build_x509_cert()
    
    print(cert_path, key_path)


if __name__ == "__main__":
    main()


## TODO 
#ECDSA 
#public_key = cert.public_key()
#if isinstance(public_key, rsa.RSAPublicKey):
#    # Do something RSA specific
#elif isinstance(public_key, ec.EllipticCurvePublicKey):
#    # Do something EC specific
#else:
#    # Remember to handle this case
