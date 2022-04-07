from rozlink import app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8443, ssl_context=(app.config["WEBHOOK_SSL_CERT"], app.config["WEBHOOK_SSL_PRIV"]),debug=True)
