from models.user_feed import UserFeed

class FeedModule(tornado.web.UIModule):

    def render(self, feed):
        return render_string("modules/feed.html", feed)
        