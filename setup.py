from setuptools import setup
 
setup(
    name='twitter-text-py',
    version='1.0.1',
    description='A library for auto-converting URLs, mentions, hashtags, lists, etc. in Twitter text. Also does tweet validation and search term highlighting.',
    author='Daniel Ryan',
    author_email='dryan@dryan.com',
    url='http://github.com/dryan/twitter-text-py',
    packages=['twitter_text'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    install_requires=['setuptools'],
    license = "BSD"
)
