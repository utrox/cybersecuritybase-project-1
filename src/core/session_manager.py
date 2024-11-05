from django.contrib.sessions.backends.db import SessionStore as SS

# FIX FOR PROBLEM #2 - A2:2017 Broken Authentication System
# Don't use predictable session key generation, because
# it can be guessed by an attacker. 
# Instead, you can just use django's default session key generation,
# or you can use a custom session key generator with a secure way to generate sessions.
class SessionStore(SS):
    def _get_new_session_key(self):
       counter = 0
       while True:
           counter += 1
           session_key = f"session-{counter}" 
           if not self.exists(session_key):
               return session_key