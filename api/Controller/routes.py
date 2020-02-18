from .routesfunc import *

def setuproute(app, call):
    @app.route('/test/',            ['OPTIONS', 'POST', 'GET'], lambda x = None: call([])                                            )
    @app.route('/login/',    	    ['OPTIONS', 'POST'],        lambda x = None: call([getauth])                                     )
    @app.route('/signup/',    	    ['OPTIONS', 'POST'],        lambda x = None: call([myauth, signup, signin, gettoken])            )
    @app.route('/signin/',    	    ['OPTIONS', 'POST'],        lambda x = None: call([myauth, signin, gettoken])                    )
    @app.route('/renew/',    	    ['OPTIONS', 'GET'],         lambda x = None: call([myauth, authuser, gettoken])                  )
    @app.route('/wp/new/',    	    ['OPTIONS', 'POST'],        lambda x = None: call([myauth, wordpressb, wp_new])                  )
    @app.route('/wp/save/',    	    ['OPTIONS', 'POST'],        lambda x = None: call([myauth, wordpressb, wp_save])                 )
    @app.route('/wp/deploy/',    	['OPTIONS', 'POST'],        lambda x = None: call([myauth, wordpressb, wp_deploy])               )
    def base():
        return
