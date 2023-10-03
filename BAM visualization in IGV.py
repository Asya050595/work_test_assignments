#Работа была выполнена в Google Colab

pip install igv-notebook
import os
os.system('wget -O first_sample.bam https://www.dropbox.com/scl/fi/kwiv5pcp7bly7fwvdl9kg/sample.bam?rlkey=b0wovxuf9oabc1d7x17g10e30&dl=0')
os.system('wget -O first_sample.bai https://www.dropbox.com/scl/fi/4zpnrk23yd9d0ftlooxpr/sample.bai?rlkey=4s10bfwn05pse298tt9odh3nt&dl=0')

#BAM (от Binary Alignment Map) - двоичный эквивалент формата SAM, в котором данные хранятся в сжатом двоичном представлении. 
#В свою очередь SAM (от Sequence Alignment Map) - текстовый формат файла, содержит биологические последовательности, 
#выровненные по референсу, состоит из заголовка и выравнивания. BAI файл содержит индексы файла BAM.

import igv_notebook
igv_notebook.init()

b = igv_notebook.Browser(
    {
        "genome": "hg38",
         "locus": "chr20"
    }
)


b.load_track(
    {
        "name": "Local BAM",
        "path": "/content/first_sample.bam",
        "indexPath": "/content/first_sample.bai",
        "format": "bam",
        "type": "alignment"
    })


b.zoom_in()
