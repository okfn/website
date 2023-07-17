from cms.test_utils.testcases import CMSTestCase

from ..models import (NetworkGroup,
                      NetworkGroupList)
from ..cms_plugins import (NetworkGroupFlagsPlugin)


class NetworkGroupPluginTest(CMSTestCase):

    def setUp(self):
        super().setUp()

        self.britain = NetworkGroup.objects.create(
            name='Open Knowledge Foundation Britain',
            group_type=0,  # local group
            description='Bisquits, tea, and open data',
            country='GB',
            mailinglist_url='http://lists.okfn.org/okfn-britain',
            homepage_url='http://gb.okfn.org/',
            twitter='OKFNgb'
        )

        self.buckingham = NetworkGroup.objects.create(
            name='Open Knowledge Buckingham',
            group_type=0,  # local group
            description='We run the Open Palace project',
            country='GB',
            region='Buckingham',
            homepage_url='http://queen.okfn.org/',
            twitter='buckingham',
            facebook_url='http://facebook.com/queenthepersonnottheband',
        )

        self.germany = NetworkGroup.objects.create(
            name='Open Knowledge Foundation Germany',
            group_type=1,  # chapter
            description='Haben Sie ein Kugelschreiber bitte?',
            country='DE',
            mailinglist_url='http://lists.okfn.org/okfn-de',
            homepage_url='http://de.okfn.org/',
            twitter='OKFNde'
        )

        self.switzerland = NetworkGroup.objects.create(
            name='Open Knowledge Foundation Switzerland',
            group_type=1,  # chapter
            description='Switzerland loves open data',
            country='CH',
            mailinglist_url='http://lists.okfn.org/okfn-ch',
            homepage_url='http://opendata.ch',
        )

        self.localgroups = NetworkGroupList(group_type=0)
        self.chapters = NetworkGroupList(group_type=1)

    def test_localgroups_plugin(self):
        plug = NetworkGroupFlagsPlugin()
        result = plug.render({}, self.localgroups, 'foo')

        self.assertSequenceEqual(sorted(result['countries'],
                                        key=lambda group: group.name),
                                 result['countries'])
        self.assertIn(self.britain, result['countries'])
        self.assertNotIn(self.germany, result['countries'])
        self.assertNotIn(self.buckingham, result['countries'])

    def test_chapters_plugin(self):
        plug = NetworkGroupFlagsPlugin()
        result = plug.render({}, self.chapters, 'foo')

        self.assertSequenceEqual(sorted(result['countries'],
                                        key=lambda chapter: chapter.name),
                                 result['countries'])
        self.assertNotIn(self.britain, result['countries'])
        self.assertIn(self.germany, result['countries'])
        self.assertNotIn(self.buckingham, result['countries'])
