api_table = { 
    ("ip","basic"):"/_api/search/ip/basic/", 
    ("ip","whois"):"/_api/search/ip/whois/", 
    ("ip","passive_dns"):"/_api/search/ip/passive_dns/", 
    ("ip","file"):"/_api/search/ip/file/", 
    ("domain","basic"):"/api/v2/domain/basic/", 
    ("domain","whois"):"/api/v2/domain/whois/", 
    ("domain","passive_dns"):"/api/v2/domain/passive_dns/", 
    ("domain","file"):"/api/v2/domain/file/", 
    ("url","basic"):"/api/v2/url/basic?q=", 
    ("url","whois"):"/api/v2/url/whois?q=", 
    ("url","passive_dns"):"/api/v2/url/passive_dns?q=", 
    ("url","file"):"/_api/search/url/file?q=", 
    ("hash","basic"):"/_api/search/hash/basic/",
    ("hash","network"):"/_api/search/hash/network/",
    ("email","whois"):"/_api/search/email/whois/",
}


def RESTful_API(ioc,parameter):
    return api_table[(ioc,parameter)]
