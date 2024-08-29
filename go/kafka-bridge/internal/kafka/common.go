package kafka

import (
	"crypto/tls"
	"crypto/x509"
	"fmt"
	"os"
)

func CreateTLSConfig(enableTLS bool, insecureSkipVerify bool, caFile, certFile, keyFile string) (*tls.Config, error) {
	if !enableTLS {
		return nil, nil
	}

	tlsConfig := &tls.Config{
		InsecureSkipVerify: insecureSkipVerify,
	}

	if caFile != "" {
		caCert, err := os.ReadFile(caFile)
		if err != nil {
			return nil, fmt.Errorf("failed to read CA file: %w", err)
		}
		caCertPool := x509.NewCertPool()
		caCertPool.AppendCertsFromPEM(caCert)
		tlsConfig.RootCAs = caCertPool
	}

	if certFile != "" && keyFile != "" {
		cert, err := tls.LoadX509KeyPair(certFile, keyFile)
		if err != nil {
			return nil, fmt.Errorf("failed to load client certificate: %w", err)
		}
		tlsConfig.Certificates = []tls.Certificate{cert}
	}

	tlsConfig.BuildNameToCertificate()
	return tlsConfig, nil
}
