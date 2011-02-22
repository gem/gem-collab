import unittest
import doctest

from zope.testing import doctestunit
from zope.component import testing

from Testing import ZopeTestCase as ztc

from gem.community.tests import base


def test_suite():
    return unittest.TestSuite([

        # Demonstrate the main content types
        ztc.ZopeDocFileSuite(
            'README.txt', package='gem.community',
            test_class=base.FunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE |
                doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
#        doctestunit.DocTestSuite(
#            module='gem.community.validators',
#            setUp=testing.setUp, tearDown=testing.tearDown),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
