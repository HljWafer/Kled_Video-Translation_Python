# from googletrans import Translator
#
# translate = Translator()
# result = translate.translate('hello', dest='zh-CN')
# print(result.text)
import json

from requests import get

text = "in hope i'm scott pagano and welcome to up and running with houdini houdini is a really powerful through the application that particular unique you it's all procedural work flow and that we build been using some crucial three techniques but we're also building networks of notes to build more complex systems the law for a tremendous amount power and flexibility will sort of taking a look at how to deal with geometry and eugenie moma von to admit animation and then we'll move on to dealing with shading the mining and renderings we can figure out how these materials and have lights and cameras were seen as woes and how to do with monterey houdini's internal render to write files out to desk and they will take a look at it is simple particles the simpson houdini had a particles are moving off of an object and had a minute with the forces that are driving those particles historically houdini is been intimidating three application for his show you all the basic steps you need just to get up and running club start"
getBatchImageUrl = "http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i=" + text
getBatchImageUrl = "http://fy.iciba.com/ajax.php?a=fy&f=auto&t=auto&w="+text
headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
results = get(getBatchImageUrl, headers=headers)
con = json.loads(results.content)
print(con)
