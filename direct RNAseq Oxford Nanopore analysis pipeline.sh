#Пайплайн анализа direct RNAseq с опорой на скрипт в bash из статьи Pai S., et al: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9394670/

mkdir -p ~/miniconda3 #Установка tombo через bioconda. Tombo - это инструмент для обработки сырых данных Nanopore
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
chmod +x Miniconda3-py37_4.8.2-Linux-x86_64.sh
import sys
sys.path.append('/usr/local/lib/python3.7/site-packages/')
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge
conda install -c bioconda ont-tombo -y
tombo resquiggle <fast5 files directory> <reference.fasta> # Выравниваем риды на референс
conda config --add channels conda-forge # Установка salmon через bioconda. Salmon - инструмент для квантификации
conda config --add channels bioconda
conda create -n salmon salmon
conda activate salmon
#Квантификация РНК (оценка уровня экспрессии). transcripts.fa cодержит выравненные транскрипты, экспрессию которых мы хотим оценить
./bin/salmon quant -t transcripts.fa -l <LIBTYPE> -a aln.bam -o salmon_quant #В результате появится директория salmon_quant, в которой лежит файл с экспрессиями quant.sf
