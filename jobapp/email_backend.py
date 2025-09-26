import ssl
import smtplib
from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend

class GmailSMTPEmailBackend(SMTPEmailBackend):
    def open(self):
        """
        Ensure an open connection to the email server. Return whether or not a
        new connection was required (True or False) or None if an exception
        occurred.
        """
        if self.connection:
            # Nothing to do if the connection is already open.
            return False
        try:
            # Create SSL context that doesn't verify certificates (for development)
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            # If local_hostname is not specified, socket.getfqdn() gets used.
            # For performance, we use the cached FQDN for local_hostname.
            local_hostname = getattr(self, 'local_hostname', None)
            if self.timeout is None:
                self.connection = self.connection_class(
                    self.host, self.port, local_hostname=local_hostname
                )
            else:
                self.connection = self.connection_class(
                    self.host, self.port, local_hostname=local_hostname, timeout=self.timeout
                )
            debug_level = getattr(self, 'debug', 0)
            self.connection.set_debuglevel(debug_level)
            if self.use_tls:
                self.connection.starttls(context=context)
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except OSError:
            if not self.fail_silently:
                raise
            return None
