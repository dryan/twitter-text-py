# encoding=utf-8

import twitter_text

text = '@foo said the funniest thing to ＠monkeybat and @bar http://dryan.net/xxxxx?param=true#hash #comedy #url'
tt = twitter_text.TwitterText(text)

def extractor_tests(tests, passed, failed):
    print u'Running Extractor tests'
    correct_mentioned_screen_names = [u'@foo', u'＠monkeybat', u'@bar']
    correct_mentioned_screen_names_with_indices = [{'indicies': (0, 4), 'screen_name': u'@foo'}, {'indicies': (32, 42), 'screen_name': u'＠monkeybat'}, {'indicies': (47, 51), 'screen_name': u'@bar'}]
    correct_reply_screen_name = '@foo'
    correct_urls = [u'http://dryan.net/xxxxx?param=true#hash']
    correct_urls_with_indices = [{'url': u'http://dryan.net/xxxxx?param=true#hash', 'indices': (52, 90)}]
    correct_hashtags = [u'comedy', u'url']
    correct_hashtags_with_indices = [{'indices': (92, 98), 'hashtag': u'comedy'}, {'indices': (100, 103), 'hashtag': u'url'}]

    extractor = twitter_text.Extractor(text)
    
    if tt.extractor.extract_mentioned_screen_names() == correct_mentioned_screen_names:
        print u'\033[92m  Attached extract_mentioned_screen_names passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Attached extract_mentioned_screen_names failed:\033[0m'
        print u'    Expected: %s' % str(correct_mentioned_screen_names)
        print u'    Returned: %s' % str(tt.extractor.extract_mentioned_screen_names())
        failed +=1
    tests +=1

    if extractor.extract_mentioned_screen_names() == correct_mentioned_screen_names:
        print u'\033[92m  Stand alone extract_mentioned_screen_names passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Stand alone extract_mentioned_screen_names failed:\033[0m'
        print u'    Expected: %s' % str(correct_mentioned_screen_names)
        print u'    Returned: %s' % str(extractor.extract_mentioned_screen_names())
        failed +=1
    tests +=1

    if tt.extractor.extract_mentioned_screen_names_with_indices() == correct_mentioned_screen_names_with_indices:
        print u'\033[92m  Attached extract_mentioned_screen_names_with_indices passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Attached extract_mentioned_screen_names_with_indices failed:\033[0m'
        print u'    Expected: %s' % str(correct_mentioned_screen_names_with_indices)
        print u'    Returned: %s' % str(tt.extractor.extract_mentioned_screen_names_with_indices())
        failed += 1
    tests += 1

    if extractor.extract_mentioned_screen_names_with_indices() == correct_mentioned_screen_names_with_indices:
        print u'\033[92m  Stand alone extract_mentioned_screen_names_with_indices passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Stand alone extract_mentioned_screen_names_with_indices failed:\033[0m'
        print u'    Expected: %s' % str(correct_mentioned_screen_names_with_indices)
        print u'    Returned: %s' % str(extractor.extract_mentioned_screen_names_with_indices())
        failed += 1
    tests += 1

    if tt.extractor.extract_reply_screen_name() == correct_reply_screen_name:
        print u'\033[92m  Attached extract_reply_screen_name passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Attached extract_reply_screen_name failed:\033[0m'
        print u'    Expected: %s' % str(correct_reply_screen_name)
        print u'    Returned: %s' % str(tt.extractor.extract_reply_screen_name())
        failed +=1
    tests +=1

    if extractor.extract_reply_screen_name() == correct_reply_screen_name:
        print u'\033[92m  Stand alone extract_reply_screen_name passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Stand alone extract_reply_screen_name failed:\033[0m'
        print u'    Expected: %s' % str(correct_reply_screen_name)
        print u'    Returned: %s' % str(extractor.extract_reply_screen_name())
        failed +=1
    tests +=1

    if tt.extractor.extract_urls() == correct_urls:
        print u'\033[92m  Attached extract_urls passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Attached extract_urls failed:\033[0m'
        print u'    Expected: %s' % str(correct_urls)
        print u'    Returned: %s' % str(tt.extractor.extract_urls())
        failed +=1
    tests +=1

    if extractor.extract_urls() == correct_urls:
        print u'\033[92m  Stand alone extract_urls passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Stand alone extract_urls failed:\033[0m'
        print u'    Expected: %s' % str(correct_urls)
        print u'    Returned: %s' % str(extractor.extract_urls())
        failed +=1
    tests +=1

    if tt.extractor.extract_urls_with_indices() == correct_urls_with_indices:
        print u'\033[92m  Attached extract_urls_with_indices passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Attached extract_urls_with_indices failed:\033[0m'
        print u'    Expected: %s' % str(correct_urls_with_indices)
        print u'    Returned: %s' % str(tt.extractor.extract_urls_with_indices())
        failed += 1
    tests += 1

    if extractor.extract_urls_with_indices() == correct_urls_with_indices:
        print u'\033[92m  Stand alone extract_urls_with_indices passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Stand alone extract_urls_with_indices failed:\033[0m'
        print u'    Expected: %s' % str(correct_urls_with_indices)
        print u'    Returned: %s' % str(extractor.extract_urls_with_indices())
        failed += 1
    tests += 1

    if tt.extractor.extract_hashtags() == correct_hashtags:
        print u'\033[92m  Attached extract_hashtags passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Attached extract_hashtags failed:\033[0m'
        print u'    Expected: %s' % str(correct_hashtags)
        print u'    Returned: %s' % str(tt.extractor.extract_hashtags())
        failed +=1
    tests +=1

    if extractor.extract_hashtags() == correct_hashtags:
        print u'\033[92m  Stand alone extract_hashtags passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Stand alone extract_hashtags failed:\033[0m'
        print u'    Expected: %s' % str(correct_hashtags)
        print u'    Returned: %s' % str(extractor.extract_hashtags())
        failed +=1
    tests +=1

    if tt.extractor.extract_hashtags_with_indices() == correct_hashtags_with_indices:
        print u'\033[92m  Attached extract_hashtags_with_indices passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Attached extract_hashtags_with_indices failed:\033[0m'
        print u'    Expected: %s' % str(correct_hashtags_with_indices)
        print u'    Returned: %s' % str(tt.extractor.extract_hashtags_with_indices())
        failed += 1
    tests += 1
        
    if extractor.extract_hashtags_with_indices() == correct_hashtags_with_indices:
        print u'\033[92m  Stand alone extract_hashtags_with_indices passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Stand alone extract_hashtags_with_indices failed:\033[0m'
        print u'    Expected: %s' % str(correct_hashtags_with_indices)
        print u'    Returned: %s' % str(tt.extractor.extract_hashtags_with_indices())
        failed += 1
    tests += 1
    
    return tests, passed, failed

def run_all():
    tests, passed, failed = 0, 0, 0
    tests, passed, failed = extractor_tests(tests, passed, failed)
    results = u'%d tests run. \033[92m%d passed.\033[0m' % (tests, passed)
    if failed > 0:
        results = u'%s \033[91m%d failed.\033[0m' % (results, failed)
    print ''
    print u'\033[1m%s\033[0;0m' % results
        
if __name__ == '__main__':
    run_all()