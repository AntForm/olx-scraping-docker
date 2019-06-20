from celery import shared_task
from django.core.mail import EmailMessage
from grab import Grab
import re
from django.utils import timezone
from django.core.mail import send_mail
from olx.models import OlxRequest

@shared_task
def send_email(mail_subject, message, to_email):
    email = EmailMessage(mail_subject, message, 'noreply@medlogic.online', [to_email])
    email.send()
    return 1

@shared_task
def get_request(request_id):
    model = OlxRequest.objects.get(pk = request_id)
    dic = {'января' : '1', 'февраля' : '2', 'марта': '3', 'апреля' : '4', 'мая' : '5', 'июня' : '6', 'июля' : '7', 'августа' : '8', 'сентября' : '9', 'октября' : '10', 'ноября' : '11', 'декабря': '12'}

    g = Grab(timeout=50, connect_timeout=50)
    g.go(model.url)

    if g.doc.text_search(u'page-link-last'):
        page_num = int(g.doc.select('//a[contains(@data-cy, "page-link-last")]').text())
    else:
        page_num = 1

    while page_num > 0:
        page = Grab(timeout=50, connect_timeout=50)
        if '?' in model.url:
            page.go(model.url + '&page=' + str(page_num))
        else:
            page.go(model.url + '?page=' + str(page_num))
        links_list = page.xpath_list('//a[contains(@class, "detailsLink")][contains(@class, "thumb")]')
        for item in links_list:
            lnk = item.get('href')
            ann = Grab(timeout=50, connect_timeout=50)
            ann.go(lnk)
            strng = ann.doc.select('//div[contains(@class, "offer-titlebox__details")]').text()
            dt_o = re.search('(?<=в )\d\d:\d\d, .* 20\d\d(?=, )', strng).group(0)
            month = re.search('[а-я].*[а-я]', dt_o).group(0)
            dt = dt_o.replace(month, dic[month])
            dt_obj = timezone.datetime.strptime(dt, "%H:%M, %d %m %Y")
            model.olxlinks_set.create(link=lnk, datetime=dt_obj)
        page_num -= 1

    message = 'Popular time: /olx/p_time/' + str(model.pk) + '\n' + 'Popular day: /olx/p_day/' + str(model.pk)
    send_mail('Report', message, 'nekidaemtestblog@gmail.com', [model.email], fail_silently=False,)
    return 1
