# encoding=utf-8

import twitter_text
from twitter_text.unicode import force_unicode

text = '@foo said the funniest thing to ＠monkeybat and @bar http://dryan.net/xxxxx?param=true#hash #comedy #url'
tt = twitter_text.TwitterText(text)

def autolink_tests(tests, passed, failed):
    print u'Running Autolink tests'

    correct_auto_link = u'<a class="tweet-url username" href="http://twitter.com/foo" rel="nofollow">@foo</a> said the funniest thing to <a class="tweet-url username" href="http://twitter.com/monkeybat" rel="nofollow">＠monkeybat</a> and <a class="tweet-url username" href="http://twitter.com/bar" rel="nofollow">@bar</a> <a href="http://dryan.net/xxxxx?param=true#hash" rel="nofollow">http://dryan.net/xxxxx?param=t…</a> <a href="http://twitter.com/search?q=%23comedy" title="#comedy" class="tweet-url hashtag" rel="nofollow">#comedy</a> <a href="http://twitter.com/search?q=%23url" title="#url" class="tweet-url hashtag" rel="nofollow">#url</a>'
    correct_auto_link_with_hit_highlight = u'<a class="tweet-url username" href="http://twitter.com/foo" rel="nofollow">@foo</a> said the <em class="search-hit">funniest</em> thing to <a class="tweet-url username" href="http://twitter.com/monkeybat" rel="nofollow">＠monkeybat</a> and <a class="tweet-url username" href="http://twitter.com/bar" rel="nofollow">@bar</a> <a href="http://dryan.net/xxxxx?param=true#hash" rel="nofollow">http://dryan.net/xxxxx?param=t…</a> <a href="http://twitter.com/search?q=%23comedy" title="#comedy" class="tweet-url hashtag" rel="nofollow">#comedy</a> <a href="http://twitter.com/search?q=%23url" title="#url" class="tweet-url hashtag" rel="nofollow">#url</a>'
    correct_auto_link_usernames_or_lists = u'<a class="tweet-url username" href="http://twitter.com/foo" rel="nofollow">@foo</a> said the funniest thing to <a class="tweet-url username" href="http://twitter.com/monkeybat" rel="nofollow">＠monkeybat</a> and <a class="tweet-url username" href="http://twitter.com/bar" rel="nofollow">@bar</a> http://dryan.net/xxxxx?param=true#hash #comedy #url'
    correct_auto_link_hashtags = u'@foo said the funniest thing to ＠monkeybat and @bar http://dryan.net/xxxxx?param=true#hash <a href="http://twitter.com/search?q=%23comedy" title="#comedy" class="tweet-url hashtag" rel="nofollow">#comedy</a> <a href="http://twitter.com/search?q=%23url" title="#url" class="tweet-url hashtag" rel="nofollow">#url</a>'
    correct_auto_link_urls_custom = u'@foo said the funniest thing to ＠monkeybat and @bar <a href="http://dryan.net/xxxxx?param=true#hash" rel="nofollow">http://dryan.net/xxxxx?param=t…</a> #comedy #url'
    correct_auto_link_urls_custom_with_kwargs = u'@foo said the funniest thing to ＠monkeybat and @bar <a href="http://dryan.net/xxxxx?param=true#hash" class="boosh" rel="external nofollow" title="a link">http://dryan.net/xxxxx?param=t…</a> #comedy #url'

    autolink = twitter_text.Autolink(text)

    # test the overall auto_link method
    test_autolink = tt.autolink.auto_link()
    if test_autolink == correct_auto_link_with_hit_highlight:
        print u'\033[92m  Attached auto_link passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Attached auto_link failed:\033[0m'
        print u'    Expected: %s' % correct_auto_link_with_hit_highlight
        print u'    Returned: %s' % test_autolink
        failed +=1
    tests +=1

    test_autolink = autolink.auto_link()
    if test_autolink == correct_auto_link:
        print u'\033[92m  Stand alone auto_link passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Stand alone auto_link failed:\033[0m'
        print u'    Expected: %s' % correct_auto_link
        print u'    Returned: %s' % test_autolink
        failed +=1
    tests +=1
    
    if failed > 0: # we need to run the individual methods to determine what failed
        # test the auto_link_usernames_or_lists method
        this_tt = twitter_text.TwitterText(text)
        autolink = twitter_text.Autolink(text)
        
        test_autolink = this_tt.autolink.auto_link_usernames_or_lists()
        if test_autolink == correct_auto_link_usernames_or_lists:
            print u'\033[92m  Attached auto_link_usernames_or_lists passed\033[0m'
            passed += 1
        else:
            print u'\033[91m  Attached auto_link_usernames_or_lists failed:\033[0m'
            print u'    Expected: %s' % correct_auto_link_usernames_or_lists
            print u'    Returned: %s' % test_autolink
            failed +=1
        tests +=1

        test_autolink = autolink.auto_link_usernames_or_lists()
        if test_autolink == correct_auto_link_usernames_or_lists:
            print u'\033[92m  Stand alone auto_link_usernames_or_lists passed\033[0m'
            passed += 1
        else:
            print u'\033[91m  Stand alone auto_link_usernames_or_lists failed:\033[0m'
            print u'    Expected: %s' % correct_auto_link_usernames_or_lists
            print u'    Returned: %s' % test_autolink
            failed +=1
        tests +=1
        
        # test the auto_link_hashtags method
        this_tt = twitter_text.TwitterText(text)
        autolink = twitter_text.Autolink(text)
        
        test_autolink = this_tt.autolink.auto_link_hashtags()
        if test_autolink == correct_auto_link_hashtags:
            print u'\033[92m  Attached auto_link_hashtags passed\033[0m'
            passed += 1
        else:
            print u'\033[91m  Attached auto_link_hashtags failed:\033[0m'
            print u'    Expected: %s' % correct_auto_link_hashtags
            print u'    Returned: %s' % test_autolink
            failed +=1
        tests +=1

        test_autolink = autolink.auto_link_hashtags()
        if test_autolink == correct_auto_link_hashtags:
            print u'\033[92m  Stand alone auto_link_hashtags passed\033[0m'
            passed += 1
        else:
            print u'\033[91m  Stand alone auto_link_hashtags failed:\033[0m'
            print u'    Expected: %s' % correct_auto_link_hashtags
            print u'    Returned: %s' % test_autolink
            failed +=1
        tests +=1

        # test the auto_link_urls_custom
        this_tt = twitter_text.TwitterText(text)
        autolink = twitter_text.Autolink(text)
        
        test_autolink = this_tt.autolink.auto_link_urls_custom()
        if test_autolink == correct_auto_link_urls_custom:
            print u'\033[92m  Attached auto_link_urls_custom passed\033[0m'
            passed += 1
        else:
            print u'\033[91m  Attached auto_link_urls_custom failed:\033[0m'
            print u'    Expected: %s' % correct_auto_link_urls_custom
            print u'    Returned: %s' % test_autolink
            failed +=1
        tests +=1

        test_autolink = autolink.auto_link_urls_custom()
        if test_autolink == correct_auto_link_urls_custom:
            print u'\033[92m  Stand alone auto_link_urls_custom passed\033[0m'
            passed += 1
        else:
            print u'\033[91m  Stand alone auto_link_urls_custom failed:\033[0m'
            print u'    Expected: %s' % correct_auto_link_urls_custom
            print u'    Returned: %s' % test_autolink
            failed +=1
        tests +=1
        
    # test the auto_link_urls_custom with some kwargs for HTML attrs
    this_tt = twitter_text.TwitterText(text)
    autolink = twitter_text.Autolink(text)
    
    test_autolink = this_tt.autolink.auto_link_urls_custom(rel = 'external', class_name = 'boosh', title = 'a link')
    if test_autolink == correct_auto_link_urls_custom_with_kwargs:
        print u'\033[92m  Attached auto_link_urls_custom with kwargs passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Attached auto_link_urls_custom with kwargs failed:\033[0m'
        print u'    Expected: %s' % correct_auto_link_urls_custom_with_kwargs
        print u'    Returned: %s' % test_autolink
        failed +=1
    tests +=1

    test_autolink = autolink.auto_link_urls_custom(rel = 'external', class_name = 'boosh', title = 'a link')
    if test_autolink == correct_auto_link_urls_custom_with_kwargs:
        print u'\033[92m  Stand alone auto_link_urls_custom with kwargs passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Stand alone auto_link_urls_custom with kwargs failed:\033[0m'
        print u'    Expected: %s' % correct_auto_link_urls_custom_with_kwargs
        print u'    Returned: %s' % test_autolink
        failed +=1
    tests +=1


    return tests, passed, failed

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
        print u'    Expected: %s' % force_unicode(correct_mentioned_screen_names)
        print u'    Returned: %s' % force_unicode(tt.extractor.extract_mentioned_screen_names())
        failed +=1
    tests +=1

    if extractor.extract_mentioned_screen_names() == correct_mentioned_screen_names:
        print u'\033[92m  Stand alone extract_mentioned_screen_names passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Stand alone extract_mentioned_screen_names failed:\033[0m'
        print u'    Expected: %s' % force_unicode(correct_mentioned_screen_names)
        print u'    Returned: %s' % force_unicode(extractor.extract_mentioned_screen_names())
        failed +=1
    tests +=1

    if tt.extractor.extract_mentioned_screen_names_with_indices() == correct_mentioned_screen_names_with_indices:
        print u'\033[92m  Attached extract_mentioned_screen_names_with_indices passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Attached extract_mentioned_screen_names_with_indices failed:\033[0m'
        print u'    Expected: %s' % force_unicode(correct_mentioned_screen_names_with_indices)
        print u'    Returned: %s' % force_unicode(tt.extractor.extract_mentioned_screen_names_with_indices())
        failed += 1
    tests += 1

    if extractor.extract_mentioned_screen_names_with_indices() == correct_mentioned_screen_names_with_indices:
        print u'\033[92m  Stand alone extract_mentioned_screen_names_with_indices passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Stand alone extract_mentioned_screen_names_with_indices failed:\033[0m'
        print u'    Expected: %s' % force_unicode(correct_mentioned_screen_names_with_indices)
        print u'    Returned: %s' % force_unicode(extractor.extract_mentioned_screen_names_with_indices())
        failed += 1
    tests += 1

    if tt.extractor.extract_reply_screen_name() == correct_reply_screen_name:
        print u'\033[92m  Attached extract_reply_screen_name passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Attached extract_reply_screen_name failed:\033[0m'
        print u'    Expected: %s' % force_unicode(correct_reply_screen_name)
        print u'    Returned: %s' % force_unicode(tt.extractor.extract_reply_screen_name())
        failed +=1
    tests +=1

    if extractor.extract_reply_screen_name() == correct_reply_screen_name:
        print u'\033[92m  Stand alone extract_reply_screen_name passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Stand alone extract_reply_screen_name failed:\033[0m'
        print u'    Expected: %s' % force_unicode(correct_reply_screen_name)
        print u'    Returned: %s' % force_unicode(extractor.extract_reply_screen_name())
        failed +=1
    tests +=1

    if tt.extractor.extract_urls() == correct_urls:
        print u'\033[92m  Attached extract_urls passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Attached extract_urls failed:\033[0m'
        print u'    Expected: %s' % force_unicode(correct_urls)
        print u'    Returned: %s' % force_unicode(tt.extractor.extract_urls())
        failed +=1
    tests +=1

    if extractor.extract_urls() == correct_urls:
        print u'\033[92m  Stand alone extract_urls passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Stand alone extract_urls failed:\033[0m'
        print u'    Expected: %s' % force_unicode(correct_urls)
        print u'    Returned: %s' % force_unicode(extractor.extract_urls())
        failed +=1
    tests +=1

    if tt.extractor.extract_urls_with_indices() == correct_urls_with_indices:
        print u'\033[92m  Attached extract_urls_with_indices passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Attached extract_urls_with_indices failed:\033[0m'
        print u'    Expected: %s' % force_unicode(correct_urls_with_indices)
        print u'    Returned: %s' % force_unicode(tt.extractor.extract_urls_with_indices())
        failed += 1
    tests += 1

    if extractor.extract_urls_with_indices() == correct_urls_with_indices:
        print u'\033[92m  Stand alone extract_urls_with_indices passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Stand alone extract_urls_with_indices failed:\033[0m'
        print u'    Expected: %s' % force_unicode(correct_urls_with_indices)
        print u'    Returned: %s' % force_unicode(extractor.extract_urls_with_indices())
        failed += 1
    tests += 1

    if tt.extractor.extract_hashtags() == correct_hashtags:
        print u'\033[92m  Attached extract_hashtags passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Attached extract_hashtags failed:\033[0m'
        print u'    Expected: %s' % force_unicode(correct_hashtags)
        print u'    Returned: %s' % force_unicode(tt.extractor.extract_hashtags())
        failed +=1
    tests +=1

    if extractor.extract_hashtags() == correct_hashtags:
        print u'\033[92m  Stand alone extract_hashtags passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Stand alone extract_hashtags failed:\033[0m'
        print u'    Expected: %s' % force_unicode(correct_hashtags)
        print u'    Returned: %s' % force_unicode(extractor.extract_hashtags())
        failed +=1
    tests +=1

    if tt.extractor.extract_hashtags_with_indices() == correct_hashtags_with_indices:
        print u'\033[92m  Attached extract_hashtags_with_indices passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Attached extract_hashtags_with_indices failed:\033[0m'
        print u'    Expected: %s' % force_unicode(correct_hashtags_with_indices)
        print u'    Returned: %s' % force_unicode(tt.extractor.extract_hashtags_with_indices())
        failed += 1
    tests += 1
        
    if extractor.extract_hashtags_with_indices() == correct_hashtags_with_indices:
        print u'\033[92m  Stand alone extract_hashtags_with_indices passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Stand alone extract_hashtags_with_indices failed:\033[0m'
        print u'    Expected: %s' % force_unicode(correct_hashtags_with_indices)
        print u'    Returned: %s' % force_unicode(extractor.extract_hashtags_with_indices())
        failed += 1
    tests += 1
    
    return tests, passed, failed
    
def highlighter_tests(tests, passed, failed):
    print u'Running HitHighlighter tests'
    
    correct_hit_highlight = u'@foo said the <em class="search-hit">funniest</em> thing to ＠monkeybat and @bar http://dryan.net/xxxxx?param=true#hash #comedy #url'
    
    highlighter = twitter_text.HitHighlighter(text)

    test_highlight = tt.highlighter.hit_highlight('funniest')
    if test_highlight == correct_hit_highlight:
        print u'\033[92m  Attached hit_highlight passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Attached hit_highlight failed:\033[0m'
        print u'    Expected: %s' % correct_hit_highlight
        print u'    Returned: %s' % test_highlight
        failed += 1
    tests += 1
        
    test_highlight = highlighter.hit_highlight('funniest')
    if test_highlight == correct_hit_highlight:
        print u'\033[92m  Stand alone hit_highlight passed\033[0m'
        passed += 1
    else:
        print u'\033[91m  Stand alone hit_highlight failed:\033[0m'
        print u'    Expected: %s' % correct_hit_highlight
        print u'    Returned: %s' % test_highlight
        failed += 1
    tests += 1
    
    return tests, passed, failed

def run_all():
    tests, passed, failed = 0, 0, 0

    tests, passed, failed = extractor_tests(tests, passed, failed)

    print ''
    tests, passed, failed = highlighter_tests(tests, passed, failed)

    print ''
    tests, passed, failed = autolink_tests(tests, passed, failed)

    print ''
    print u'Checking hit_highlight assertion that text does not have HTML tags already present'
    try:
        tt.highlighter.hit_highlight('funniest')
        print u'\033[91m  hit_highlight HTML tag check failed\033[0m'
        failed += 1
    except AssertionError:
        print u'\033[92m  hit_highlight HTML tag check passed\033[0m'
        passed += 1
    tests += 1

    results = u'%d tests run. \033[92m%d passed.\033[0m' % (tests, passed)
    if failed > 0:
        results = u'%s \033[91m%d failed.\033[0m' % (results, failed)
    print ''
    print u'\033[1m%s\033[0;0m' % results
        
if __name__ == '__main__':
    run_all()