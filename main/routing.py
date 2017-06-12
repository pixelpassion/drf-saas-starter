# In routing.py
from channels.routing import route

from apps.users.consumers import users_ws_connect, users_ws_disconnect, \
    users_ws_message, ws_add, ws_disconnect, ws_message

channel_routing = [
    route("users.websocket.connect", users_ws_connect),
    route("users.websocket.receive", users_ws_message),
    route("users.websocket.disconnect", users_ws_disconnect),

    # # Called when incoming WebSockets connect
    # route("websocket.connect", connect_blog, path=r'^/liveblog/(?P<slug>[^/]+)/stream/$'),
    #
    # # Called when the client closes the socket
    # route("websocket.disconnect", disconnect_blog, path=r'^/liveblog/(?P<slug>[^/]+)/stream/$'),
    #
    # # Called when the client sends message on the WebSocket
    # route("websocket.receive", save_post, path=r'^/liveblog/(?P<slug>[^/]+)/stream/$'),

    # A default "http.request" route is always inserted by Django at the end of the routing list
    # that routes all unmatched HTTP requests to the Django view system. If you want lower-level
    # HTTP handling - e.g. long-polling - you can do it here and route by path, and let the rest
    # fall through to normal views.

    route("websocket.connect", ws_add),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),


]
