/* Copyright (c) 2022 Automation Anywhere. All rights reserved.
 *
 * This software is the proprietary information of Automation Anywhere. You shall use it only in
 * accordance with the terms of the license agreement you entered into with Automation Anywhere.
 */
package com.automationanywhere.botcommand.samples.commands.aa;

import com.automationanywhere.botcommand.exception.BotCommandException;
import org.apache.commons.lang3.StringUtils;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import javax.net.ssl.*;
import java.io.*;
import java.net.URL;
import java.security.*;
import java.security.cert.CertificateException;


public class SSLUtilityExp {

    private static final String CERT_TYPE = "X.509", TLS_VER = "TLSv1.2";
    private static final Logger LOGGER = LogManager.getLogger(SSLUtilityExp.class);

    public SSLSocketFactory configureSSL(final String keystorePath) {
        LOGGER.traceEntry();

        try {
            KeyStore keyStore = KeyStore.getInstance("Windows-MY");
            FileInputStream keystoreFile = new FileInputStream(keystorePath);
            keyStore.load(keystoreFile, "".toCharArray());

            // Load the Windows-ROOT keystore (trusted root certificates)
            KeyStore trustStore = KeyStore.getInstance("Windows-Root");
            trustStore.load(null, null);

            // Initialize KeyManagerFactory with Windows-MY keystore
            KeyManagerFactory kmf = KeyManagerFactory.getInstance(KeyManagerFactory.getDefaultAlgorithm());
            kmf.init(keyStore, null);

            // Initialize TrustManagerFactory with Windows-ROOT truststore
            TrustManagerFactory tmf = TrustManagerFactory.getInstance("SUNX509");
            tmf.init(trustStore);
            SSLContext ssl = SSLContext.getInstance("TLS");
            ssl.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);
//            System.out.println(ssl.getSocketFactory());
            return LOGGER.traceExit(ssl.getSocketFactory());

        } catch (KeyStoreException | NoSuchAlgorithmException | KeyManagementException e) {
            if (e instanceof KeyStoreException) {
                LOGGER.warn("Couldn't load the Default Key Store.");
            } else {
                LOGGER.warn("Couldn't load the Default Key Store or SSL Context.");
            }
        } catch (CertificateException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        } catch (UnrecoverableKeyException e) {
            throw new RuntimeException(e);
        }

        LOGGER.trace("Returning null");
        return null;
    }
}
