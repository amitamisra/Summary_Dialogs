'''
Created on Apr 15, 2015
from paraphrase import similarity
@author: amita
'''
from paraphrase import similarity
from requests import get
def sss(s1, s2, type_sim='relation', corpus='webbase'):
    sss_url = "http://swoogle.umbc.edu/SimService/GetSimilarity"
    try:
        response = get(sss_url, params={'operation':'api','phrase1':s1,'phrase2':s2,'type':type,'corpus':corpus})
        return float(response.text.strip())
    except:
        print 'Error in getting similarity for %s: %s' % ((s1,s2), response)
        return -1
    
def sss_stsnew(s1, s2, type_sim='relation', corpus='webbase'):
    sss_url = "http://swoogle.umbc.edu/StsService/GetStsSim"
    try:
        response = get(sss_url, params={'operation':'api','phrase1':s1,'phrase2':s2,'type':type,'corpus':corpus})
        return float(response.text.strip())
    except:
        print 'Error in getting similarity for %s: %s' % ((s1,s2), response)
        return -1
      
def correctErrors():
    s1a="solutions if rouge officers and military start killing people"
    s1b="A militia group in the Midwest planned to kill police."
    
    s1="offending the sensibilities of people does not constitute harm"
    s2="offending the sensibilities of people is harm"
    
    
    
    s3="harming others by offending their sensibilities "
    s4="towards the rights of gay people"
    s5="people in support of marriage equality is growing"
    s6a="heterosexual nature of the relationship that is important, not how the children are conceived within the relationship"
    s6b="marriage should be between a heterosexual couple"
    s7a="inappropriate to label disagreement on gay marriage as bigotry"
    s7b="funny how violence is used to end an argument against religion"
    s8a="gay community is the cause of the AIDs epidemic in the US."
    s8b="No one argues the point that AIDs was spread in the United States by homosexuals."
    sim1=sss(s1a,s1b)
    sim2=sss(s1,s2)
    #----------------------------------------------------------- sim3=sss(s2,s3)
    #--------------------------------------------------------- sim6=sss(s6a,s6b)
    #--------------------------------------------------------- sim7=sss(s7a,s7b)
    #--------------------------------------------------------- sim8=sss(s8a,s8b)
#------------------------------------------------------------------------------ 
    #------------------------------------------------- sim1new=sss_stsnew(s1,s2)
    #------------------------------------------------- sim2new=sss_stsnew(s1,s3)
    #------------------------------------------------- sim3new=sss_stsnew(s2,s3)
    #----------------------------------------------- sim6new=sss_stsnew(s6a,s6b)
    #----------------------------------------------- sim7new=sss_stsnew(s7a,s7b)
    #----------------------------------------------- sim8new=sss_stsnew(s8a,s8b)
#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
    print "\nsim1 = "+ str(sim1)  
    print "\nsim2 = "+ str(sim2) 
    
  
if __name__ == '__main__':
    correctErrors()
    
 #   s1 = 0.4009652

