from _setup_test import *


class TestUtil(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestUtil, self).__init__(*args, **kwargs)

    def test_generate_id(self):
        log_info()
        for _ in range(10):
            log_info(generate_id())


@log_test(__file__)
def run():
    switch_log(1)
    testcase_classes = [
        TestUtil
    ]
    for tc in testcase_classes:
        testcase = unittest.TestLoader().loadTestsFromTestCase(tc)
        unittest.TextTestRunner(verbosity=2).run(testcase)


if __name__ == '__main__':
    run()
