class FilterModule(object):
    ''' Custom filters are loaded by FilterModule objects '''

    def filters(self):
        ''' FilterModule objects return a dict mapping filter names to
            filter functions. '''
        return {
            'memcached_filter': self.memcached_filter,
        }

    def memcached_filter(self, hosts, hostvars, port):
        #return ["%s:%s" % (host, port) for host in hosts]
        return ["%s:%s" % (hostvars[host]['my_int_ip'], port)
                for host in hosts]
