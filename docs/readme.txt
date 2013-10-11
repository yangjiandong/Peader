学习
===

2013.10.11
----------

    1. 解决 UnicodeEncodeError: 'ascii' codec can't encode characters
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    --END