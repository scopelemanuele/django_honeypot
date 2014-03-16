from __future__ import unicode_literals

from django.http import HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils.translation import ugettext, ugettext_lazy as _

import socket


from django_honeypot import settings
from django_honeypot.models import *

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class HoneypotMiddleware(object):
    """
    Process the request and return the IP
    """

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def dns_request(self, ip, request):
        """
        Perform request to honeypot server and process the response
        """
        req = settings.HoneyKey + '.' + self.revers_ip(ip) + '.' + settings.DNSUrl
        logger.info('***Honeypot: request: %s' % req)
        try:
            res = socket.gethostbyname(req)
            response = res.split('.')
            if int(response[0]) == 127 and int(response[3]) >= 1:
                logger.info('***Honeypot: Bad visitor! Ip: %s response: %s' % (ip, res))
                self.save_log(ip, response, request)
                #Suspicious permitted andThreatRating unset permit visitor
                if settings.Suspicious and not settings.ThreatRating and int(response[3]) == 1:
                    logger.info('***Honeypot: Bad visitor allowed')
                    return None
                #Suspicious permitted and ThreatRating set permit
                elif settings.Suspicious and settings.ThreatRating and int(response[3]) == 1:
                    #control visitor rating
                    if int(response[2]) > settings.ThreatRating:
                        logger.info('***Honeypot: Bad visitor denyed')
                        return True
                    else:
                        logger.info('***Honeypot: Bad visitor allowed')
                        return None
                elif not settings.Suspicious and not settings.ThreatRating and int(response[3]) > 1:
                    logger.info('***Honeypot: Bad visitor denyed')
                    return True
                elif not settings.Suspicious and settings.ThreatRating and int(response[3]) > 1:
                    #control visitor rating
                    if int(response[2]) > settings.ThreatRating:
                        logger.info('***Honeypot: Bad visitor denyed')
                        return True
                    else:
                        logger.info('***Honeypot: Bad visitor allowed')
                        return None
                logger.info('***Honeypot: Bad visitor denyed')
                return True
            else:
                logger.info('***Honeypot: Visitor allowed')
                return None
        except:
            logger.info('***Honeypot: Visitor not in db allowed!')
            return None

    def save_log(self, ip, response, request):
        """
        If visitor is scheduled write it into the log
        """

        TYPE = {
            '0': _('Search Engine'),
            '1': _('Suspicious'),
            '2': _('Harvester'),
            '4': _('Comment Spammer'),
        }

        log = HoneypotLog(ip=ip)
        log.last_activity = int(response[1])
        log.rating = int(response[2])
        try:
            log.type = TYPE[response[3]]
        except:
            logger.error('***Honeypot: Type wrong!')
            log.type = TYPE['2']
        log.from_url = request.META.get('HTTP_REFERER')
        log.request_url = request.get_full_path()
        log.save()

    def revers_ip(self, ip):
        """
        inverse the ip
        """
        t = ip.split('.')
        return t[3] + '.' + t[2] + '.' + t[1] + '.' + t[0]

    def process_request(self, request):
        if self.dns_request(self.get_client_ip(request), request):
            return HttpResponseRedirect(settings.HoneyPotUrl)
