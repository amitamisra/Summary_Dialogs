Steps forWSD
1) Follow IMS Readme
2)Download(unzip) all the packages in one ms folder( models, examples lib)
4) For Coarse grained task
    execute 
./testPlain.bash /Users/amita/software/IMS/ims/models /Users/amita/Desktop/test_disc.txt outputfile.xml /Users/amita/software/IMS/ims/lib/dict/index.sense 0 0 0 0 

from ins folder.

This gives an xml file containing probabilities of each word in form index.sense.

5) we need to map these sense values obtained using a word net readable program to read actual text form of synsets.
     a) download word net 1.7 as  ims uses that.
      b) since we do not have write permission and its an older version
           use tar zxf wn17.unix.tar.gz -C wordnet , this extracts  word net to word net directory.
c)Go through MakeFile
do changes as per platform, For me it was linux.
since we downloaded it to different directory
set the path for variables
export WNHOME=/home/amita/software/wordnet/wordnet1.7

export WNSEARCHDIR=/home/amita/software/wordnet/wordnet1.7/dict

d) I used perl for mapping
http://wordnet.princeton.edu/wordnet/related-projects/
Download module from
https://metacpan.org/pod/Wordnet::SenseSearch

Follow read me
change the path of word net dict in all the folders.
Also since wornet not extracted to standard location
perl Makefile.PL INSTALL_BASE=/home/amita/software/perl
# changes the instal module directory since we do not have write permission
go to /home/amita/software/perl/lib/perl5

write your test per script here as test.pl
this calls the word net::sense search module as shown at
https://metacpan.org/pod/Wordnet::SenseSearch

