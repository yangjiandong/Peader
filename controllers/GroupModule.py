from models.user_feed import UserFeed

class GroupModule(tornado.web.UIModule):



    def render(self, group):
        
        return render_string("modules/group.html", )
        