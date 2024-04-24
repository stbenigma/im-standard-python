import yaml
import requests
from requests.exceptions import HTTPError


class ConfluenceApi():
    """ api for confluence. expecting a yaml file
        #template configuration for accessing a confluence space
        # copy this file to your local environment and add the proper path's and credenttials
        confluence:
          apiurl: 'https://<yourconfluence>.atlassian.net/wiki/rest/api'
          space: '<yourspace>'
          rootpage: '<yourrootpage>'        
        
          cooldown: 0.01
          credentials:
            user: <yourusername>
            token: '<yourtoken>'
        
        # Abort processing if pages with same title exist outside of the specified document root
        cautious: true
        
        #<yourconfluence> = informationskartografie      foryouandyourcustomers
        #<youacpace>     =  IF                           FYYCYIM
        #<yourrootpoge =    Informationsmodell           Information Model of foryouandyourcustomers
        #<yourusername> =   stb@foryouandyourcustomers.com
        #<yourtoken> =      ATATT3xFE...=47AA2015

    """
    def __init__(self,yamlfile):
        self.username=None
        self.apiurl=None
        self.space=None
        self.rootpagename=None
        self.headers = dict()
        self.auth=(())
        self.proxies = None

        self.verify = None

        self.connect2api(yamlfile=yamlfile)
        self.params=self.conflparams(spacekey=self.space)
        return

    @property
    def searchurl(self):
        return self.apiurl + "/content/search"

    def pageurl(self,pageid):
        return self.apiurl + f"/content/{pageid}"

    def conflparams(self,spacekey):
        params = {}
        # safeguard: don't touch other spaces
        params['cql'] = f'label="generated" and space={spacekey}'
        params['cqlcontext'] = f'{{ "spaceKey": "{spacekey}" }}'
        params['limit'] = 50
        params['max'] = 5
        params['expand'] = 'version'
        return params

    def connect2api(self,yamlfile):
        
        with open(yamlfile, 'r') as src:
            configuration = yaml.safe_load(src)

        confluence = configuration['confluence']
        assert len(confluence['apiurl']) > 0
        
        self.username=confluence['credentials']['user']
        self.apiurl=confluence.get('apiurl')
        self.space=confluence.get('space')
        self.rootpagename=confluence.get('rootpage')

        if confluence.get('proxy') is not None:
            wampassword_key = 'wampassword'
            proxypassword_key = 'proxypassword'
            if not confluence['credentials'].get(wampassword_key):
                confluence['credentials'][wampassword_key] = keyring.get_password(wampassword_key, self.username)

            if not confluence['credentials'].get(proxypassword_key):
                confluence['credentials'][proxypassword_key] = keyring.get_password(proxypassword_key, self.username)

            self.proxies = {
                "http": f"http://{username}:{configuration['credentials'][proxypassword_key]}@rb-proxy-ext.bosch.com:8080",
                "https": f"http://{username}:{configuration['credentials'][proxypassword_key]}@rb-proxy-ext.bosch.com:8080"
                }
            self.auth = (username, confluence['credentials'][wampassword_key])
        else:
            self.auth = (self.username, confluence['credentials']['token'])

        # Looks like an issue with the proxy and a self signed certificate ...
        self.verify = configuration.get('verify_ssl', True)


        if confluence.get('apikey') is not None:
            self.headers = {'KeyId': confluence['apikey']}

        return 

    def queryconfluence(self,url):
        try:
            result = requests.get(url, headers=self.headers, auth=self.auth,
                                  proxies=self.proxies, verify=self.verify)
        except HTTPError as e:
            log.exception('Failed ' + e.response.content.decode('utf-8'), e)
        return result


    def getspace(self,title):
        #title = config["page"].replace('-', ' ')
        # query_url = url + "?cql=( title ~ " + f'"{title}"' + f" )&type=page&spaceKey={config['space']}&expand=children,ancestors&"
        query_url = self.searchurl + "?cql=( title ~ " + f'"{title}"' + f" )&type=page&spaceKey={self.space}&expand=children,ancestors&"
        #print(f"Scanning for root page with cql: {params} on {query_url}")
        result= self.queryconfluence(url=query_url)
        assert result.status_code == 200, f"Failed to get root page '{title}'. {result} {result.json()}"

        results=result.json()
        root_page = None
        for page in results["results"]:
            if page["title"] == self.rootpagename:
                root_page = page
        assert root_page is not None, f"Expecting root page with name {self.rootpagename}"

        return root_page

    def getpages(self,root_page):
        query_url = self.searchurl + f"?cql=( ancestor={root_page['id']} )" + f"&type=page&spaceKey={self.space}&limit=75&expand=children,ancestors&"
        result= self.queryconfluence(url=query_url)
        envelope = dict(result.json())
        envelope.pop('results')
        next = envelope['_links'].get('next')

        child_pages = result.json()['results']
        batch_size = len(child_pages)
        all_pages=[]
        while batch_size > 0:
            for page in child_pages:
                page_id = page['id']
                ancestors = page.get('ancestors', [])
                all_pages.append( { 'id': page_id, 'title': page['title'], 'depth': len(ancestors) } )

            if next is not None:
                next_url = self.apiurl + "/" + next.replace("/rest/api", "")
                next_batch = self.queryconfluence(url=next_url)
                res = next_batch.json()
                child_pages = res.get("results")
                batch_size = len(child_pages)
                next = res['_links'].get('next')
            else:
                batch_size = 0
        return all_pages

    def deltepage(self,pageid):
        deleteurl=self.pageurl(pageid)
        try:
            res = requests.delete(deleteurl, headers=self.headers, auth=self.auth,
                                  proxies=self.proxies, verify=self.verify)
            if res.status_code not in (200,204):
                print(f"Failed to delete page {deleteurl}: {res.message}")

        except Exception as ex:
            print(f"Unable to delete page {pageid}: {ex}\n{deleteurl}\n{type(ex)}")
            raise ex
        return
