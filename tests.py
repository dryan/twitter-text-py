# encoding=utf-8

import twitter_text, sys, os, json
from twitter_text.unicode import force_unicode

try:
    import yaml
except ImportError:
    raise Exception('You need to install pyaml to run the tests')

def success(text):
    sys.stdout.write(u'\033[92m%s\033[0m\n' % text)
    sys.stdout.flush()

def error(text):
    sys.stderr.write(u'\033[91m%s\033[0m\n' % text)
    sys.stderr.flush()

passed = 0
attempted = 0
failed = 0

def execute_test(result, test):
    global passed, attempted, failed
    attempted += 1
    if result == test.get('expected'):
        passed += 1
        success('Passed: %s' % test.get('description'))
    else:
        failed += 1
        error(u'Failed: %s' % test.get('description'))
        error(result)
        error(test.get('expected'))


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
        extractor = twitter_text.extractor.Extractor(test.get('text'))
        if section == 'mentions':
            execute_test(extractor.extract_mentioned_screen_names(), test)
        elif section == 'mentions_with_indices':
            execute_test(extractor.extract_mentioned_screen_names_with_indices(), test)
        elif section == 'mentions_or_lists_with_indices':
            execute_test(extractor.extract_mentions_or_lists_with_indices(), test)
        elif section == 'replies':
            execute_test(extractor.extract_reply_screen_name(), test)
        elif section == 'urls':
            execute_test(extractor.extract_urls(), test)
        elif section == 'urls_with_indices':
            execute_test(extractor.extract_urls_with_indices(), test)
        elif section == 'hashtags':
            execute_test(extractor.extract_hashtags(), test)
        elif section == 'cashtags':
            execute_test(extractor.extract_cashtags(), test)
        elif section == 'hashtags_with_indices':
            execute_test(extractor.extract_hashtags_with_indices(), test)
        elif section == 'cashtags_with_indices':
            execute_test(extractor.extract_cashtags_with_indices(), test)

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
        autolink = twitter_text.autolink.Autolink(test.get('text'))
        if section == 'usernames':
            execute_test(autolink.auto_link_usernames_or_lists(autolink_options), test)
        elif section == 'cashtags':
            execute_test(autolink.auto_link_cashtags(autolink_options), test)
        elif section == 'urls':
            execute_test(autolink.auto_link_urls(autolink_options), test)
        elif section == 'hashtags':
            execute_test(autolink.auto_link_hashtags(autolink_options), test)
        elif section == 'all':
            execute_test(autolink.auto_link(autolink_options), test)
        elif section == 'lists':
            execute_test(autolink.auto_link_usernames_or_lists(autolink_options), test)
        elif section == 'json':
            execute_test(autolink.auto_link_with_json(json.loads(test.get('json')), autolink_options), test)

sys.stdout.write(u'\033[0m-------\n%d tests run. \033[92m%d passed. \033[91m%s failed\033[0m\n' % (attempted, passed, failed))
sys.stdout.flush()
sys.exit(os.EX_OK if passed == attempted else os.EX_SOFTWARE)