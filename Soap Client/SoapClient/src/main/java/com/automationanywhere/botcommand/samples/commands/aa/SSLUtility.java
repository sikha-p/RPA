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
import java.net.MalformedURLException;
import java.net.URL;
import java.security.*;
import java.security.cert.CertificateException;
import java.security.cert.CertificateFactory;
import java.security.cert.X509Certificate;



public class SSLUtility {

    private static final String CERT_TYPE = "X.509", TLS_VER = "TLSv1.2";
    private static final Logger LOGGER = LogManager.getLogger(SSLUtility.class);

    public SSLSocketFactory configureSSL(final String keystorePath) {
        LOGGER.traceEntry();

        try {
            KeyStore keyStore = KeyStore.getInstance(KeyStore.getDefaultType());
            FileInputStream keystoreFile = new FileInputStream(keystorePath);
            keyStore.load(keystoreFile, "".toCharArray());

            KeyManagerFactory kmf = KeyManagerFactory.getInstance(KeyManagerFactory.getDefaultAlgorithm());
            kmf.init(keyStore, null);

            TrustManagerFactory tmf = TrustManagerFactory.getInstance("SUNX509");
            tmf.init((KeyStore) null);
            SSLContext ssl = SSLContext.getInstance("TLS");
            ssl.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);
            System.out.println(ssl.getSocketFactory());
            return LOGGER.traceExit(ssl.getSocketFactory());
        } catch (KeyStoreException | NoSuchAlgorithmException | KeyManagementException e) {
            if (e instanceof KeyStoreException) {
                LOGGER.warn("Couldn't load the Default Key Store.");
            } else {
                LOGGER.warn("Couldn't load the Default Key Store or SSL Context.");
            }
        } catch (UnrecoverableKeyException e) {
            throw new RuntimeException(e);
        } catch (CertificateException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        LOGGER.trace("Returning null");
        return null;
    }

}



