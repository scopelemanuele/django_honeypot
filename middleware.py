from __future__ import unicode_literals

from django.http import HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils.translation import ugettext, ugettext_lazy as _

import socket


from django_honeypot import settings
from django_honeypot.models import *


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

    def dns_request(self, ip):
        """
        Perform request to honeypot server and process the response
        """
        request = settings.HoneyKey + '.' + self.revers_ip(ip) + '.' + settings.DNSUrl
        try:
            res = socket.gethostbyname(request)
            response = res.split('.')
            if int(response[0]) == 127 and int(response[3]) >= 1:
                self.save_log(ip, response)
                #Suspicious permitted andThreatRating unset permit visitor
                if settings.Suspicious and not settings.ThreatRating and int(response[3]) == 1:
                    return None
                #Suspicious permitted and ThreatRating set permit
                elif settings.Suspicious and settings.ThreatRating and int(response[3]) == 1:
                    #control visitor rating
                    if int(response[2]) > settings.ThreatRating:
                        return True
                    else:
                        return None
                elif not settings.Suspicious and not settings.ThreatRating and int(response[3]) > 1:
                    return True
                elif not settings.Suspicious and settings.ThreatRating and int(response[3]) > 1:
                    #control visitor rating
                    if int(response[2]) > settings.ThreatRating:
                        return True
                    else:
                        return None
                return True
            else:
                return None
        except:
            return None

    def save_log(self, ip, response):
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
        log.type = TYPE[response[3]]
        log.save()

    def revers_ip(self, ip):
        """
        inverse the ip
        """
        t = ip.split('.')
        return t[3] + '.' + t[2] + '.' + t[1] + '.' + t[0]

    def process_request(self, request):
        if self.dns_request(self.get_client_ip(request)):
            return HttpResponseRedirect(settings.HoneyPotUrl)

