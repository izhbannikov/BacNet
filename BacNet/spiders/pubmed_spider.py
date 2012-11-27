# -*- coding:utf8 -*-

import re

from pubmed.items import PubmedItem
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader.processor import Join
from scrapy.http import Request

curpnum = 1
#query_str = "iners[All Fields] OR crispatus[All Fields] OR gasseri[All Fields] OR jensenii[All Fields] OR aerococcus[All Fields] OR vaginalis[All Fields] OR gemella[All Fields] OR gardnerella[All Fields] OR anaeroglobus[All Fields] OR cryptobacterium[All Fields] OR cardnerella[All Fields] OR sneathia[All Fields] OR magasphaera[All Fields] OR anaerotruncus[All Fields] OR eggerthella[All Fields] OR atopobium[All Fields] OR parvimonas[All Fields] OR porphyromonas[All Fields] OR peptoniphilus[All Fields] OR mobiluncus[All Fields] OR dialister[All Fields] OR prevotella[All Fields]"
query_str = "iners[All Fields] OR crispatus[All Fields] OR gasseri[All Fields] OR jensenii[All Fields]"
global_start_url = "http://www.ncbi.nlm.nih.gov/pubmed?EntrezSystem2.PEntrez.DbConnector.Term="+query_str+"&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.PageSize=200"


class PubmedLoader(XPathItemLoader):
    default_input_processor = MapCompose(lambda s: re.sub('\s+', ' ', s.strip()))
    default_output_processor = Join()
    state_in = MapCompose(lambda s: not re.match(u'\s*', s))
    pass

class PubmedSpider(CrawlSpider):

    name = "pubmed"
    allowed_domains = ["ncbi.nlm.nih.gov"]
    
    #rules = [ Rule(SgmlLinkExtractor(allow=('/pubmed/*?')), callback='parse')]
    def start_requests(self):
        return [Request(global_start_url)]

    

    def parse(self, response):
      total_number = 200
      #print response.body
      hxs = HtmlXPathSelector(response)
      
      s_id = ""
      tmp = hxs.select(".//*[@id='SessionId']/@value").extract()
      for item in tmp:
	s_id += str(item)
	
      tmp = hxs.select(".//*[@id='EntrezForm']/div[2]/input[5]/@value").extract()
      #print s_id
      last_query_key = ""
      for item in tmp:
	last_query_key += str(item)
	
      #print last_query_key
      for i in xrange( total_number ) :
	s2 = hxs.select(".//*[@id='maincontent']/div/div[4]/div[" + str(i) +"]/div[2]/p/a/@href").extract()
	#print s2
	next_url = "http://www.ncbi.nlm.nih.gov"
	for item in s2:
	  next_url += str(item)
	
	
      #global_start_url2 ="http://www.ncbi.nlm.nih.gov/pubmed?EntrezSystem2.PEntrez.Pubmed.Pubmed_SearchBar.SearchResourceList=pubmed&EntrezSystem2.PEntrez.Pubmed.Pubmed_SearchBar.Term="+query_str+"&EntrezSystem2.PEntrez.Pubmed.Pubmed_SearchBar.FeedLimit=15&EntrezSystem2.PEntrez.Pubmed.Pubmed_SearchBar.FeedName="+query_str+"&EntrezSystem2.PEntrez.Pubmed.Pubmed_SearchBar.CurrDb=pubmed&EntrezSystem2.PEntrez.Pubmed.Pubmed_PageController.PreviousPageName=results&EntrezSystem2.PEntrez.Pubmed.Pubmed_Facets.FacetsUrlFrag=filters%3D&EntrezSystem2.PEntrez.Pubmed.Pubmed_Facets.FacetSubmitted=false&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.sPresentation=docsum&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.sPageSize=200&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.sSort=none&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.SendTo=File&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.FFormat=xml&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.FSort=&email_format=docsum&email_sort=&email_count=200&email_add_text=&citman_count=200&citman_start=1&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.FileFormat=xml&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.LastPresentation=docsum&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.Presentation=docsum&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.PageSize=200&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.LastPageSize=200&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.Sort=&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.LastSort=&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.FileSort=&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.Format=xml&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.LastFormat=&CitationManagerStartIndex=1&CitationManagerCustomRange=false&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Entrez_Pager.cPage=1&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Entrez_Pager.CurrPage=1&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_ResultsController.ResultCount=722&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_ResultsController.RunLastQuery=&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Entrez_Pager.cPage=1&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.sPresentation2=docsum&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.sPageSize2=200&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.sSort2=none&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.FFormat2=docsum&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.FSort2=&email_format2=docsum&email_sort2=&email_count2=200&email_start2=1&email_address2=&email_subj2=&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_MultiItemSupl.RelatedDataLinks.rdDatabase=rddbto&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_MultiItemSupl.RelatedDataLinks.DbName=pubmed&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Discovery_SearchDetails.SearchDetailsTerm="+query_str+"&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.HistoryDisplay.Cmd=file&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.EmailTab.EmailReport=&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.EmailTab.EmailFormat=&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.EmailTab.EmailCount=&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.EmailTab.EmailStart=&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.EmailTab.EmailSort=&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.EmailTab.Email=&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.EmailTab.EmailSubject=&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.EmailTab.EmailText=&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.EmailTab.EmailQueryKey=&EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.EmailTab.QueryDescription=&EntrezSystem2.PEntrez.DbConnector.Db=pubmed&EntrezSystem2.PEntrez.DbConnector.LastDb=pubmed&EntrezSystem2.PEntrez.DbConnector.Term="+query_str+"&EntrezSystem2.PEntrez.DbConnector.LastTabCmd=&EntrezSystem2.PEntrez.DbConnector.LastQueryKey="+ last_query_key +"&EntrezSystem2.PEntrez.DbConnector.IdsFromResult=&EntrezSystem2.PEntrez.DbConnector.LastIdsFromResult=&EntrezSystem2.PEntrez.DbConnector.LinkName=&EntrezSystem2.PEntrez.DbConnector.LinkReadableName=&EntrezSystem2.PEntrez.DbConnector.LinkSrcDb=&EntrezSystem2.PEntrez.DbConnector.Cmd=file&EntrezSystem2.PEntrez.DbConnector.TabCmd=&EntrezSystem2.PEntrez.DbConnector.QueryKey=&p%24a=EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DisplayBar.SendToSubmit&p%24l=EntrezSystem2&p%24st=pubmed"
      global_start_url2 ="http://www.ncbi.nlm.nih.gov/pubmed?EntrezSystem2.PEntrez.PubMed.Pubmed_SearchBar.SearchResourceList=pubmed&EntrezSystem2.PEntrez.PubMed.Pubmed_SearchBar.Term="+query_str+"&EntrezSystem2.PEntrez.PubMed.Pubmed_SearchBar.FeedLimit=15&EntrezSystem2.PEntrez.PubMed.Pubmed_SearchBar.FeedName="+query_str+"&EntrezSystem2.PEntrez.PubMed.Pubmed_SearchBar.CurrDb=pubmed&EntrezSystem2.PEntrez.PubMed.Pubmed_PageController.PreviousPageName=results&EntrezSystem2.PEntrez.PubMed.Pubmed_Facets.FacetsUrlFrag=filters%3D&EntrezSystem2.PEntrez.PubMed.Pubmed_Facets.FacetSubmitted=false&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.sPresentation=docsum&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.sPageSize=20&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.sSort=none&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.SendTo=File&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.FFormat=xml&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.FSort=&email_format=docsum&email_sort=&email_count=20&email_start=1&email_address=&email_subj=iners%5BAll+Fields%5D+OR+crispatus%5BAll+Fields%5D+OR+gass+-+PubMed&email_add_text=&citman_count=20&citman_start=1&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.FileFormat=xml&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.LastPresentation=docsum&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.Presentation=docsum&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.PageSize=20&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.LastPageSize=20&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.Sort=&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.LastSort=&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.FileSort=&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.Format=&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.LastFormat=&CitationManagerStartIndex=1&CitationManagerCustomRange=false&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Entrez_Pager.cPage=1&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Entrez_Pager.CurrPage=1&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_ResultsController.ResultCount=724&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_ResultsController.RunLastQuery=&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Entrez_Pager.cPage=1&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.sPresentation2=docsum&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.sPageSize2=20&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.sSort2=none&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.FFormat2=docsum&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.FSort2=&email_format2=docsum&email_sort2=&email_count2=20&email_start2=1&email_address2=&email_subj2="+query_str+"&email_add_text2=&citman_count2=20&citman_start2=1&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_MultiItemSupl.RelatedDataLinks.rdDatabase=rddbto&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_MultiItemSupl.RelatedDataLinks.DbName=pubmed&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Discovery_SearchDetails.SearchDetailsTerm="+query_str+"&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.HistoryDisplay.Cmd=file&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.EmailReport=&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.EmailFormat=&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.EmailCount=&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.EmailStart=&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.EmailSort=&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.Email=&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.EmailSubject=&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.EmailText=&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.EmailQueryKey=&EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.EmailTab.QueryDescription=&EntrezSystem2.PEntrez.DbConnector.Db=pubmed&EntrezSystem2.PEntrez.DbConnector.LastDb=pubmed&EntrezSystem2.PEntrez.DbConnector.Term="+query_str+"&EntrezSystem2.PEntrez.DbConnector.LastTabCmd=&EntrezSystem2.PEntrez.DbConnector.LastQueryKey="+last_query_key+"&EntrezSystem2.PEntrez.DbConnector.IdsFromResult=&EntrezSystem2.PEntrez.DbConnector.LastIdsFromResult=&EntrezSystem2.PEntrez.DbConnector.LinkName=&EntrezSystem2.PEntrez.DbConnector.LinkReadableName=&EntrezSystem2.PEntrez.DbConnector.LinkSrcDb=&EntrezSystem2.PEntrez.DbConnector.Cmd=file&EntrezSystem2.PEntrez.DbConnector.TabCmd=&EntrezSystem2.PEntrez.DbConnector.QueryKey=&p%24a=EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.SendToSubmit&p%24l=EntrezSystem2&p%24st=pubmed"
      
      yield Request(global_start_url2, cookies={'ncbi_sid' : s_id,'WebEnv':""}, callback=self.save_file)
      
    
    def save_file(self, response):
      with open("pubmed_result.xml", "wb") as f:
        #print response.body
        f.write(response.body)

    
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
	#s2 = hxs.select(".//*[@id='maincontent']/div/div[4]/div[1]/div[2]/p/a/text()")
	#print "!!!"
	l = PubmedLoader(PubmedItem(), hxs)
		
	#s1 = hxs.select(".//*[@id='maincontent']/div/div[4]/div/h1")
	l.add_xpath('Title', ".//*[@id='maincontent']/div/div[4]/div/h1/text()")
	#s2 = hxs.select(".//*[@id='maincontent']/div/div[4]/div/div[2]/a")
	#for ss2 in s2:
	#  autors = ss2.select('text()').extract()
	  #l.add_value('Autors', autors)
        s3 = hxs.select(".//*[@id='maincontent']/div/div[4]/div/div[4]/p[1]")
	for ss3 in s3:
           abstract = ss3.select('text()').extract()
	   l.add_value('Abstract', abstract)
	
	s2 = hxs.select(".//*[@id='maincontent']/div/div[4]/div[1]/div[2]/p/a/text()")
	
	#print s2
	return l.load_item()
	
	
def parse_query_file(query_filename):
    file = open(query_filename)
    global query_str
    query_str = ""
    while 1:
      line = file.readline()
      if not line:
        break
      if line[len(line)-1] == "\n" :
        line = line[:-1]

      query_str +=line

    query_str.strip()


    print "Given query string: ", query_str
  