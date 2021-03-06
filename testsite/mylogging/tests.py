# -*- coding: utf-8 -*-
from testsite.mylogging.models import Request, Modellog
from testsite.profiles.models import Profile
from testsite.extra_common.testcases import MyHttpTestCase, MyTestCase
import datetime
from django.contrib.contenttypes.models import ContentType


class TestLogger(MyHttpTestCase):
    def test_counts(self):
        self.go200('/')
        count_cur = Request.objects.count()
        self.go200('/')
        self.assert_count(Request, (count_cur + 1))

        count_cur = Request.objects.count()
        self.go200('/requests/')
        self.assert_count(Request, (count_cur + 1))
        self.go200('/requests/')
        self.find(r"\bGET(\s)+/requests/ ")
        self.find(r"\bGET(\s)+/")


class testDBLogging(MyTestCase):
    def test_it(self):
        logs_count = Modellog.objects.count()

        #test creation log
        prof = Profile(name="TestName",
                       surname="TestSur",
                       bio='no bio',
                       birth=datetime.datetime(1987, 12, 11, 0, 0)
                       )
        prof.save()
        latest = Modellog.objects.latest()
        prof_type = ContentType.objects.get_for_model(prof)
        self.assertEqual(logs_count + 1, Modellog.objects.count())
        self.assertEqual(latest.action, 'C')
        self.assertEqual(latest.inst_pk, prof.pk)
        self.assertEqual(latest.app, prof_type.app_label)
        self.assertEqual(latest.model, prof_type.model)

        #test modification log
        prof.name = "NewName"
        prof.save()
        self.assertEqual(logs_count + 2, Modellog.objects.count())
        self.assertEqual(Modellog.objects.latest().action, 'E')

        #test deletion log
        prof.delete()
        self.assertEqual(Modellog.objects.latest().action, 'D')
        self.assertEqual(logs_count + 3, Modellog.objects.count())

        #test another creation log
        self.go('/')  # let pk be greater than 1
        req = Request(method='GET', path='/', get='', post='')
        req.save()
        self.assertEqual(logs_count + 5, Modellog.objects.count())
        latest = Modellog.objects.latest()
        req_type = ContentType.objects.get_for_model(req)
        self.assertEqual(latest.inst_pk, req.pk)
        self.assertEqual(latest.app, req_type.app_label)
        self.assertEqual(latest.model, req_type.model)

class TestPrioritizedLogs(MyHttpTestCase):
    def test_counts(self):
        prioritized_url = self.build_url('mylogging:listed',
                                         kwargs={'sortby': 'priority'})
        prioritized_url_r = self.build_url('mylogging:listed',
                                           kwargs={'sortby': '-priority'})
#        dated_url = self.build_url('mylogging:list',
#                                   kwargs={'sortby': 'date'})
        self.go('/')
        self.go('/')
        last_req = Request.objects.latest()
        last_req.priority = 0
        last_req.save()

        self.go(prioritized_url)
        self.find(r'/(\n|.)*1(\n|.)*<tr>(\n|.)*'
                  r'/(\n|.)*0')

        self.go('/')
        self.go('/')
        last_req = Request.objects.latest()
        last_req.priority = 0
        last_req.save()
        self.go(prioritized_url_r)
        self.find(r'/(\n|.)*0(\n|.)*<tr>(\n|.)*'
                  r'/(\n|.)*1')
