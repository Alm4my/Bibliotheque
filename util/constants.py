import re

EMAIL_REGEXP = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,63})+\Z'
PHONE_REGEXP = r'^[0-9]{0,10}\Z'
USERNAME_REGEXP = r'^([a-zA-Z0-9]+)([-._]{0,2})([\w]*)\Z'
PHONE_PREFIX_REGEXP = r'^[+][\d]{1,7}'

#######

PHONE_REGEXP_CPL = re.compile(PHONE_REGEXP)
EMAIL_REGEXP_CPL = re.compile(EMAIL_REGEXP)
