import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on theb given port", type=int)

import tornado.ioloop
import tornado.web
import tornado.autoreload


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_cookie('cookie_1', '123456')
        self.set_secure_cookie('s_cookie_1', 's_1234')
        self.render('test.html')
        #self.write("Hello, world")


class SubHandler(tornado.web.RequestHandler):
    def get(self):
        cookie = self.get_cookie('cookie_1')
        s_cookie = self.get_secure_cookie('s_cookie_1')
        if not cookie:
            cookie = 'none cookie'
        if not s_cookie:
            s_cookie = 'none secure cookie'

        print 'cookie : ', cookie
        print 's_cookie: ', s_cookie
        self.write(cookie + s_cookie)


class SubPost1(tornado.web.RequestHandler):
    def post(self):
        cookie = self.get_cookie('cookie_1')
        s_cookie = self.get_secure_cookie('s_cookie_1')

        print '/subpost1 post'
        print 'cookie: ', cookie
        print 's_cookie: ', s_cookie


class FormHandler(tornado.web.RequestHandler):
    def get(self):
        print 'form get'
        self.render('form.html')

    def post(self):
        t_1 = self.get_argument('t_1', None)
        print 't_1: ', t_1
        print 'form post'
        self.redirect('/')


settings = {'cookie_secret': '32143232'}
application = tornado.web.Application([
    (r"/", MainHandler),
    (r'/1', SubHandler),
    (r'/s/1', SubPost1),
    (r'/form', FormHandler),
],
    **settings)

if __name__ == "__main__":
    print '**********web start***************'
    application.listen(options.port)

    def fn():
        print '********** restart **********'
    tornado.autoreload.add_reload_hook(fn)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()
