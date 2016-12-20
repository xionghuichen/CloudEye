    from tornado.httpserver import HTTPServer  
    from tornado.ioloop import IOLoop  
    from tornado.web import Application, RequestHandler, asynchronous  
      
    class MainHandler(RequestHandler):  
        @asynchronous  
        def get(self):  
            self.finish("Hello, world")  
      
    if __name__ == "__main__":  
        http_server = HTTPServer(Application([(r"/", MainHandler),]))  
        http_server.listen(8888)  
        # HTTPServer继承TCPServer，它只负责处理将接收到的新连接的socket添加到IOLoop中。
        IOLoop.instance().start()  



    def listen(self, port, address=""):  
        sockets = bind_sockets(port, address=address)  
        self.add_sockets(sockets)  
      
    def add_sockets(self, sockets):  
        # 获取当前的ioloop
        if self.io_loop is None:  
            self.io_loop = IOLoop.current()  
      
        for sock in sockets:  
            self._sockets[sock.fileno()] = sock  # 这行代码干嘛的？
            add_accept_handler(sock, self._handle_connection, io_loop=self.io_loop)  

    def add_accept_handler(sock, callback, io_loop=None):  
        # 这里重新获取了一次ioloop 为何呢？ioloop干嘛的呢？
        if io_loop is None:  
            io_loop = IOLoop.current()  
       # 2. 添加完成后在accept_handler接受新连接，接受到新连接后调用self._handle_connection      
        def accept_handler(fd, events):  
            while True:  
                try:  
                    # 接受新连接
                    connection, address = sock.accept()  
                except socket.error as e:  
                    if e.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN):  
                        return  
                    if e.args[0] == errno.ECONNABORTED:  
                        continue  
                    raise  
                # 在这里调用了self._handle_connection,用来处理连接
                callback(connection, address)  
                
        #　首先将HTTPServer这个监听型socket添加到IOLoop中，
        # 添加完成后在accept_handler接受新连接，
        # 接受到新连接后调用self._handle_connection。
        # fileno()用来取得参数stream指定的文件流所使用的文件描述符
        io_loop.add_handler(
            sock.fileno(), 
            accept_handler, 
            IOLoop.READ)  

    # 在_handle_connection中创建一个IOStream对象，
    # 传给handle_stream，
    # 并且在handle_stream中初始化一个HTTPConnection对象。
    def _handle_connection(self, connection, address):  
        if self.ssl_options is not None:  
            assert ssl, "Python 2.6+ and OpenSSL required for SSL"  
            try:  
                connection = ssl_wrap_socket(connection,  
                                             self.ssl_options,  
                                             server_side=True,  
                                             do_handshake_on_connect=False)  
            except ssl.SSLError as err:  
                if err.args[0] == ssl.SSL_ERROR_EOF:  
                    return connection.close()  
                else:  
                    raise  
            except socket.error as err:  
                if err.args[0] in (errno.ECONNABORTED, errno.EINVAL):  
                    return connection.close()  
                else:  
                    raise  
        try:  
            if self.ssl_options is not None:  
                # 创建一个IOStream对象，
                # 第一个参数是connection 来自accept 的 socket。
                stream = SSLIOStream(connection, io_loop=self.io_loop, max_buffer_size=self.max_buffer_size)  
            else:  
                stream = IOStream(connection, io_loop=self.io_loop, max_buffer_size=self.max_buffer_size)  
            # 将iostream传入 handle_stream中初始化一个HTTPConnection对象
            self.handle_stream(stream, address)  
        except Exception:  
            app_log.error("Error in connection callback", exc_info=True)  
    # 并且在handle_stream中初始化一个HTTPConnection对象
    # 到HTTPConnection初始化时，新的连接已经接受，
    # 并初始化了IOStream对象，就可以开始读请求过来的数据了，
    # 读完之后交给_header_callback，
    #　实际是交给_on_headers解析数据。
    def handle_stream(self, stream, address):  
        # 并将该对象作为参数传给最初的那个request_callback
        # （即在main方法中传给HttpServer的Application）的__call__方法，
        HTTPConnection(stream, address, self.request_callback, self.no_keep_alive, self.xheaders, self.protocol)  

# 在_on_handlers解析完请求数据后创建HTTPRequest对象，
# 并将该对象作为参数传给最初的那个request_callback
# （即在main方法中传给HttpServer的Application）的__call__方法，
# 到此整个请求流程就很清晰了。
# HTTPConnection 的初始化函数：
    def __init__(self, stream, address, request_callback, no_keep_alive=False,  
                     xheaders=False, protocol=None):  
        self.stream = stream  
        self.address = address  
        self.address_family = stream.socket.family  
        self.request_callback = request_callback  
        self.no_keep_alive = no_keep_alive  
        self.xheaders = xheaders  
        self.protocol = protocol  
        self._clear_request_state()  
        # 并将该对象作为参数传给最初的那个request_callback
        # （即在main方法中传给HttpServer的Application）的__call__方法，
        self._header_callback = stack_context.wrap(self._on_headers)  
        self.stream.set_close_callback(self._on_connection_close)  
        self.stream.read_until(b"\r\n\r\n", self._header_callback)  

# 以下是__call__方法的调用逻辑：
# 这里还啰嗦几句，
# Application的__call__方法首先会调用该请求对应Handler的父类RequestHandler的_execute方法，
    # 这里的几个逻辑解释一下。
    # 首先执行self._when_complete(self.prepare(), self._execute_method)，
    # 会执行self.prepare()，即正式处理请求之前的逻辑，
        # 基类中是空实现，开发者可根据需要在自己的Handler中实现，该方法正常返回一个Future对象。
    # 如果未实现self.prepare()则直接调用self._execute_method，
    #　反之则通过IOLoop循环执行完self.prepare()后再调用self._execute_method，
    # self._execute_method，即调用开发者写的Handler里面的get或post等请求逻辑。
    # 开发者逻辑执行完成后执行self.finish()。

    def _execute(self, transforms, *args, **kwargs):  
        """Executes this request with the given output transforms."""  
        self._transforms = transforms  
        try:  
            if self.request.method not in self.SUPPORTED_METHODS:  
                raise HTTPError(405)  
            self.path_args = [self.decode_argument(arg) for arg in args]  
            self.path_kwargs = dict((k, self.decode_argument(v, name=k))  
                                    for (k, v) in kwargs.items())  
            # If XSRF cookies are turned on, reject form submissions without  
            # the proper cookie  
            if self.request.method not in ("GET", "HEAD", "OPTIONS") and \  
                    self.application.settings.get("xsrf_cookies"):  
                self.check_xsrf_cookie() 
            #  首先执行self._when_complete(self.prepare(), self._execute_method)，
            self._when_complete(self.prepare(), self._execute_method)  
        except Exception as e:  
            self._handle_request_exception(e)  
      
    def _when_complete(self, result, callback):  
        try:  
            # result = self.prepare
            # callback = self.execute_method
            # 执行self.prepare()[也就是这里的result]，即正式处理请求之前的逻辑，
                # 基类中是空实现，开发者可根据需要在自己的Handler中实现，该方法正常返回一个Future对象。
            if result is None:  
                # 如果未实现self.prepare()则直接调用self._execute_method，[也就是这里的callback()]
                # self._execute_method，即调用开发者写的Handler里面的get或post等请求逻辑。
                callback()  
            elif isinstance(result, Future):  
                #　反之则通过IOLoop循环执行完self.prepare()后再调用self._execute_method，
                if result.done():  
                    if result.result() is not None:  
                        raise ValueError('Expected None, got %r' % result)  
                    # self._execute_method，即调用开发者写的Handler里面的get或post等请求逻辑。
                    callback()  
                else:  
                    # Delayed import of IOLoop because it's not available  
                    # on app engine  
                    # 这段代码干嘛的？？？？
                    from tornado.ioloop import IOLoop  
                    IOLoop.current().add_future(  
                        result, functools.partial(self._when_complete,  
                                                  callback=callback))  
            else:  
                raise ValueError("Expected Future or None, got %r" % result)  
        except Exception as e:  
            self._handle_request_exception(e)  
      
    def _execute_method(self):  
        if not self._finished:  
            method = getattr(self, self.request.method.lower())  
            # 这里重新调用了when complete 干嘛的
            # 这个 method是干嘛的呢？
            # self._execute_method，即调用开发者写的Handler里面的get或post等请求逻辑。
            self._when_complete(method(*self.path_args, **self.path_kwargs),  
                                self._execute_finish)  
      
    def _execute_finish(self):  
        if self._auto_finish and not self._finished:  
            self.finish()  

# 再看IOLoop，这个模块是异步机制的核心，
#　它包含了一系列已经打开的文件描述符和每个描述符的处理器（handlers）。
# 针对不同的平台，tornado提供了多种IOLoop实现方式，
    # 包括select、epoll、kqueue，其实就是IO多路复用的实现，
    # 这些都继承PollIOLoop，PollIOLoop是对IOLoop的一个基本封装。

# IOLoop的功能是选择那些已经准备好读写的文件描述符，然后调用它们各自的处理器。

# 可以通过调用add_handler()方法将一个socket加入IOLoop中，
# 上面的HTTPServer监听socket就是通过add_handler添加到IOLoop中去的：
# io_loop.add_handler(sock.fileno(), accept_handler, IOLoop.READ)
# 来具体看下add_handler这个方法，
    # 为fd注册handler来接收event，
    # 事件包括READ、WRITE、ERROR三种，默认为ERROR，
    # 当注册的事件触发时，将会调用handler(fd, events)函数。

# self._impl是前面说的select、epoll、kqueue其中一种的实例，

# register函数只是根据事件类型将fd放到不同的事件集合中去。


# 回顾：这是之前调用 add_handler 的代码

    # def add_accept_handler(sock, callback, io_loop=None):  
    #     # 这里重新获取了一次ioloop 为何呢？ioloop干嘛的呢？
    #     if io_loop is None:  
    #         io_loop = IOLoop.current()  
    #    # 2. 添加完成后在accept_handler接受新连接，接受到新连接后调用self._handle_connection      
    #     def accept_handler(fd, events):  
    #         while True:  
    #             try:  
    #                 # 接受新连接
    #                 connection, address = sock.accept()  
    #             except socket.error as e:  
    #                 if e.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN):  
    #                     return  
    #                 if e.args[0] == errno.ECONNABORTED:  
    #                     continue  
    #                 raise  
    #             # 在这里调用了self._handle_connection,用来处理连接
    #             callback(connection, address)  
                
    #     #　首先将HTTPServer这个监听型socket添加到IOLoop中，
    #     # 添加完成后在accept_handler接受新连接，
    #     # 接受到新连接后调用self._handle_connection。
    #       
    #　　　fileno()用来取得参数stream指定的文件流所使用的文件描述符
    #     io_loop.add_handler(
    #         sock.fileno(), 
    #         accept_handler, 
    #         IOLoop.READ)  

# io_loop.add_handler(sock.fileno(), accept_handler, IOLoop.READ)
# 来具体看下add_handler这个方法，
    # 为fd注册handler来接收event，[fd 是一个文件描述符]

    # 事件event包括READ、WRITE、ERROR三种，默认为ERROR，
    
    # 当注册的事件触发时，将会调用handler(fd, events)函数。[事件什么时候触发？]
    
    # self._impl是前面说的select、epoll、kqueue其中一种的实例，
    # register函数只是根据事件类型将fd放到不同的事件集合中去。

        #　它包含了一系列已经打开的文件描述符和每个描述符的处理器（handlers）。
            # 针对不同的平台，tornado提供了多种IOLoop实现方式，
            # 包括select、epoll、kqueue，其实就是IO多路复用的实现，
            # 这些都继承PollIOLoop，PollIOLoop是对IOLoop的一个基本封装。
    def add_handler(self, fd, handler, events):  
        self._handlers[fd] = stack_context.wrap(handler)  
        self._impl.register(fd, events | self.ERROR)  

# 接下来IOLoop就要开始工作了，看start()方法（代码比较长，只保留了主要部分）：
    
# 回顾一下之前我们调用 start()的地方，在app.py的主函数里面，
# instance() 是ioloop的不同实现中的一种     
    # if __name__ == "__main__":  
    #     http_server = HTTPServer(Application([(r"/", MainHandler),]))  
    #     http_server.listen(8888)  
    #     # HTTPServer继承TCPServer，它只负责处理将接收到的新连接的socket添加到IOLoop中。
    #     IOLoop.instance().start()  

    
    def start(self):  
        [...]  
        self._running = True  
        [...]  
        while True:  
            poll_timeout = 3600.0  
            with self._callback_lock:  
                callbacks = self._callbacks  
                self._callbacks = []  
            for callback in callbacks:  
                self._run_callback(callback)  
      
            [...通过_timeouts来优化poll_timeout...]  
      
            if self._callbacks:  
                poll_timeout = 0.0  
      
            if not self._running:  
                break  
      
            [...]  
      
            try:  
                event_pairs = self._impl.poll(poll_timeout)#取出数据已准备好的事件，当poll有结果时才会返回，否则一直阻塞，直到poll_timeout  
            except Exception as e:  
                if (getattr(e, 'errno', None) == errno.EINTR or  
                    (isinstance(getattr(e, 'args', None), tuple) and  
                     len(e.args) == 2 and e.args[0] == errno.EINTR)):  
                    continue  
                else:  
                    raise  
      
            [...]  
      
            # Pop one fd at a time from the set of pending fds and run  
            # its handler. Since that handler may perform actions on  
            # other file descriptors, there may be reentrant calls to  
            # this IOLoop that update self._events  
            self._events.update(event_pairs)  
            while self._events:  
                fd, events = self._events.popitem()  
                try:  
                    self._handlers[fd](fd, events)#执行handler，即执行netutil中的accept_handler方法，接着会接受socket，调用TCPServer中的_handle_connection方法，该方法会创建一个IOStream实例进行异步读写  
                except (OSError, IOError) as e:  
                    if e.args[0] == errno.EPIPE:  
                        # Happens when the client closes the connection  
                        pass  
                    else:  
                        app_log.error("Exception in I/O handler for fd %s",  
                                      fd, exc_info=True)  
                except Exception:  
                    app_log.error("Exception in I/O handler for fd %s",  
                                  fd, exc_info=True)  
        [...]  