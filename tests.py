# encoding=utf-8

import twitter_text, sys, os, json, argparse
from twitter_text.unicode import force_unicode

narrow_build = True
try:
    unichr(0x20000)
    narrow_build = False
except:
    pass

parser = argparse.ArgumentParser(description = u'Run the integration tests for twitter_text')
parser.add_argument('--ignore-narrow-errors', '-i', help = u'Ignore errors caused by narrow builds', default = False, type = bool)
args = parser.parse_args()

try:
    import yaml
except ImportError:
    raise Exception('You need to install pyaml to run the tests')

try:
    from bs4 import BeautifulSoup
except ImportError:
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        raise Exception('You need to install BeautifulSoup to run the tests')

def success(text):
    return (u'\033[92m%s\033[0m\n' % text)

def error(text):
    return (u'\033[91m%s\033[0m\n' % text)

attempted = 0

def assert_equal_without_attribute_order(result, test, failure_message = None):
    # Beautiful Soup sorts the attributes for us so we can skip all the hoops the ruby version jumps through
    assert BeautifulSoup(result) == BeautifulSoup(test.get('expected')), error(u'Test %d Failed: %s' % (attempted, test.get('description')))


def assert_equal(result, test):
    global attempted
    attempted += 1
    assert result == test.get('expected'), error(u'\nTest %d Failed: %s' % (attempted, test.get('description')))

# extractor section
extractor_file = open(os.path.join('twitter-text-conformance', 'extract.yml'), 'r')
extractor_tests = yaml.load(extractor_file.read())
extractor_file.close()

sys.stdout.write('Testing Extractor\n')
sys.stdout.flush()

for section in extractor_tests.get('tests'):
    sys.stdout.write('\nTesting Extractor: %s\n' % section)
    sys.stdout.flush()
    for test in extractor_tests.get('tests').get(section):
        if args.ignore_narrow_errors and section in ['hashtags'] and test.get('description') in ['Hashtag with ideographic iteration mark']:
            continue
        extractor = twitter_text.extractor.Extractor(test.get('text'))
        if section == 'mentions':
            assert_equal(extractor.extract_mentioned_screen_names(), test)
        elif section == 'mentions_with_indices':
            assert_equal(extractor.extract_mentioned_screen_names_with_indices(), test)
        elif section == 'mentions_or_lists_with_indices':
            assert_equal(extractor.extract_mentions_or_lists_with_indices(), test)
        elif section == 'replies':
            assert_equal(extractor.extract_reply_screen_name(), test)
        elif section == 'urls':
            assert_equal(extractor.extract_urls(), test)
        elif section == 'urls_with_indices':
            assert_equal(extractor.extract_urls_with_indices(), test)
        elif section == 'hashtags':
            assert_equal(extractor.extract_hashtags(), test)
        elif section == 'cashtags':
            assert_equal(extractor.extract_cashtags(), test)
        elif section == 'hashtags_with_indices':
            assert_equal(extractor.extract_hashtags_with_indices(), test)
        elif section == 'cashtags_with_indices':
            assert_equal(extractor.extract_cashtags_with_indices(), test)

# autolink section
autolink_file = open(os.path.join('twitter-text-conformance', 'autolink.yml'), 'r')
autolink_tests = yaml.load(autolink_file.read())
autolink_file.close()

sys.stdout.write('\nTesting Autolink\n')
sys.stdout.flush()

autolink_options = {'suppress_no_follow': True}

for section in autolink_tests.get('tests'):
    sys.stdout.write('\nTesting Autolink: %s\n' % section)
    for test in autolink_tests.get('tests').get(section):
        if args.ignore_narrow_errors and section in ['hashtags'] and test.get('description') in ['Autolink a hashtag containing ideographic iteration mark']:
            continue
        autolink = twitter_text.autolink.Autolink(test.get('text'))
        if section == 'usernames':
            assert_equal_without_attribute_order(autolink.auto_link_usernames_or_lists(autolink_options), test)
        elif section == 'cashtags':
            assert_equal_without_attribute_order(autolink.auto_link_cashtags(autolink_options), test)
        elif section == 'urls':
            assert_equal_without_attribute_order(autolink.auto_link_urls(autolink_options), test)
        elif section == 'hashtags':
            assert_equal_without_attribute_order(autolink.auto_link_hashtags(autolink_options), test)
        elif section == 'all':
            assert_equal_without_attribute_order(autolink.auto_link(autolink_options), test)
        elif section == 'lists':
            assert_equal_without_attribute_order(autolink.auto_link_usernames_or_lists(autolink_options), test)
        elif section == 'json':
            assert_equal_without_attribute_order(autolink.auto_link_with_json(json.loads(test.get('json')), autolink_options), test)

sys.stdout.write(u'\033[0m-------\n\033[92m%d tests passed.\033[0m\n' % attempted)
sys.stdout.flush()
sys.exit(os.EX_OK)