
#coding:gb2312  
from ctypes import *

class tokenizer:
   
        def __init__(self):
            self._stext=[''] 
            
            self._stopword_list=["a","b"] 


        def parse(self,text):       
            atext_list=[]
            rtext=[]
            participle = cdll.LoadLibrary("ICTCLAS50.dll")
            participle.ICTCLAS_Init(c_char_p('.'))
            num = participle.ICTCLAS_ImportUserDictFile(c_char_p("./userdict.txt"), c_int(0));
            #print num
            strlen = len(c_char_p(text).value)
            t = c_buffer(strlen*6)
            a =participle.ICTCLAS_ParagraphProcess(c_char_p(text),c_int(strlen),t,c_int(2),0)
            atext_list=t.value.split(' ')
            participle.ICTCLAS_Exit()
            rtext=[item for item in atext_list if item not in self._stext]
            result_list=[iword for iword in rtext if iword not in self._stopword_list]

            return result_list
if __name__ == '__main__':
    text = "请有育儿经验的朋友回答下，多美滋奶粉好不好"       
    wlist=tokenizer().parse(text)
    for item in wlist:
        print item
        
        
        
        
##coding:gb2312   
#from ctypes import *   
#  
#dll=cdll.LoadLibrary("ICTCLAS50.dll")   
#flag = dll.ICTCLAS_Init(c_char_p("./"))   
#print flag
#print bool(flag)
#lpText = ""  
#res = create_string_buffer('a',1000)
#print repr(res.value)
#res1 = (c_char*1000)()
#type = c_int(1)
#print res1.value
#print sizeof(res1)
#
#bSuccess = dll.ICTCLAS_ParagraphProcess(c_char_p(lpText),c_int(len(lpText)),pointer(type),0,res)   
#print bSuccess,c_char_p(bSuccess),lpText,res1,repr(res1.value),res,res.value
#dll.ICTCLAS_Exit()  
#
##enum eCodeType {
##    CODE_TYPE_UNKNOWN,        // type unktem will automatically detect
##    CODE_TYPE_ASCII,            // ASCII
##    CODE_TYPE_GB,                // GB2312,GBK, gb18030
##    CODE_TYPE_UTF8,            // UTF-8
##    CODE_TYPE_BIG5            // BIG5
##};
