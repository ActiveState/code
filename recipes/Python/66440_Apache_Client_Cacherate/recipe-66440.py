def ClientCachePercentage(logfile_pathname):
        Contents = open(logfile_pathname, "r").readlines()
        TotalRequests = len(Contents)
        CachedRequests = 0

        for line in Contents:
                if line.split(" ")[8] == "304":  # if server returned "not modified"
                        CachedRequests += 1

        return TotalRequests / CachedRequests

# example usage
log_path = "/usr/local/nusphere/apache/logs/access_log"
print "Percentage of requests that are client-cached: " + str(ClientCachePercentage(log_path)) + "%"
