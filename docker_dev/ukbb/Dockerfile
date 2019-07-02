FROM docker.rdcloud.bms.com:443/rr:Genomics2019-03_all

USER root

ARG AWS_ACCESS_KEY_ID
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID

ARG AWS_SECRET_ACCESS_KEY
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

RUN \
    R -e 'install.packages(c("SKAT","ukbtools","qqman","fuzzywuzzyR","rtf","AER","coloc"), repos="http://cran.us.r-project.org")'  \ 
    R -e 'install.packages(c("MASS","meta","ggrepel","DT"), dependencies=c("Depends", "Imports", "LinkingTo", "Suggests", "Enhances"))' \
    R -e 'install.packages("logistf")'

# Update Bioconductor Packages
RUN \
    R -e 'if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager"); BiocManager::install(c("GeneticsDesign","IRanges"), version = "3.8")'

RUN \
    R -e 'devtools::install_github(c("paradigm4/scidbr", "PheWAS/PheWAS")); devtools::install_github("paradigm4/curl", ref = "realloc_fix")' \
    # TEMP FIX FOR FlashPCA package see: https://github.com/gabraham/flashpca/issues/37 
    R -e 'remotes::install_version(package = "RSpectra", \
    version = "0.13-1", \
    repos = c("http://cran.us.r-project.org", "https://cran.rstudio.com/"), \
    upgrade = "never")' \ 
    R -e 'remotes::install_github( \
    repo = "gabraham/flashpca/flashpcaR", \
    upgrade = "never" \
    )'
# END TEMP FIX # 


RUN \
    R -e 'install.packages(c("data.table","Matrix","inline","base64enc","gtools"), repos="http://cran.us.r-project.org")'

#See here: https://stackoverflow.com/questions/45233113/aws-credentials-during-docker-build-process
#And here: https://vsupalov.com/docker-build-pass-environment-variables/
#for info on how to safely pass AWS credentials into the Docker build process as ARGs that set ENV vars.
#Build like this to have the build process be able to use the AWS credentials stored in the host's env vars:
#docker build --build-arg AWS_ACCESS_KEY_ID --build-arg AWS_SECRET_ACCESS_KEY -t "rr:Genomics2019-03_ukb" .
#Can similarly pass safely AWS credentials when doing docker run like this:
#docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -it --cap-add=SYS_ADMIN --device=/dev/fuse --security-opt=apparmor:unconfined --cap-add=DAC_READ_SEARCH --entrypoint /bin/bash <IMAGE_ID>
#See here: https://stackoverflow.com/questions/30494050/how-do-i-pass-environment-variables-to-docker-containers

#RUN aws s3 cp s3://bmsrd-ngs-ukbb-68039/biobank_P4_R_package/Biobank_0.2.0_March2019/package_builds/biobank_0.2.0.tar.gz /tmp/
#RUN R -e 'install.packages("/tmp/biobank_0.2.0.tar.gz", repos=NULL)'

RUN aws s3 cp s3://bmsrd-ngs-ukbb-68039/biobank_P4_R_package/Biobank_0.2.0_March2019/package_builds/biobank_0.2.4.tar.gz /tmp/
RUN R -e 'install.packages("/tmp/biobank_0.2.4.tar.gz", repos=NULL)'

#plink1.9: got from here: https://www.cog-genomics.org/plink2
RUN mkdir -p /usr/local/plink1_9 && cd /usr/local/plink1_9 && wget -q http://s3.amazonaws.com/plink1-assets/plink_linux_x86_64_20190304.zip && unzip plink_linux_x86_64_20190304.zip && ln -s /usr/local/plink1_9/plink /usr/local/bin/plink


#plink2: got from here: https://www.cog-genomics.org/plink/2.0/
RUN mkdir -p /usr/local/plink2 && cd /usr/local/plink2 && wget -q http://s3.amazonaws.com/plink2-assets/plink2_linux_x86_64_20190628.zip && unzip plink2_linux_x86_64_20190628.zip && ln -s /usr/local/plink2/plink /usr/local/bin/plink2

#bcftools: got from here: https://samtools.github.io/bcftools/, then went here: http://www.htslib.org/download/
RUN cd /tmp && wget -q https://github.com/samtools/bcftools/releases/download/1.9/bcftools-1.9.tar.bz2 && tar -vxjf bcftools-1.9.tar.bz2 && cd bcftools-1.9 && ./configure --prefix=/usr/local && make && make install

#bolt-lmm: got from here: https://data.broadinstitute.org/alkesgroup/BOLT-LMM/
RUN mkdir -p /usr/local/bolt-lmm && cd /usr/local/bolt-lmm && wget -q https://data.broadinstitute.org/alkesgroup/BOLT-LMM/downloads/BOLT-LMM_v2.3.2.tar.gz && tar -vxzf BOLT-LMM_v2.3.2.tar.gz && ln -s /usr/local/bolt-lmm/BOLT-LMM_v2.3.2/bolt /usr/local/bin/bolt

#KING: got from here: http://people.virginia.edu/~wc9c/KING/
RUN mkdir -p /usr/local/KING && cd /usr/local/KING && wget http://people.virginia.edu/~wc9c/KING/Linux-king.tar.gz && tar -vxzf Linux-king.tar.gz && mv /usr/local/KING/king /usr/local/bin/king
#ln -s /usr/local/KING/king /usr/local/bin/king
#Temp solution since KING download was blocked by BMS network:
#COPY ./Linux-king.tar.gz /tmp/Linux-king.tar.gz
#RUN cd /tmp && tar -vxzf Linux-king.tar.gz && mv /tmp/king /usr/local/bin/king

#VEP: got from here: https://useast.ensembl.org/info/docs/tools/vep/index.html
RUN mkdir -p /usr/local/VEP && cd /usr/local/VEP && git clone https://github.com/Ensembl/ensembl-vep.git && cd ensembl-vep && apt-get -y install libdbi-perl libmodule-build-perl libjson-perl && perl INSTALL.pl && ln -s /usr/local/VEP/ensembl-vep/vep /usr/local/bin/vep && ln -s /usr/local/VEP/ensembl-vep/variant_recoder /usr/local/bin/variant_recoder && ln -s /usr/local/VEP/ensembl-vep/haplo /usr/local/bin/haplo && ln -s /usr/local/VEP/ensembl-vep/filter_vep /usr/local/bin/filter_vep

#bedtools: got from here: https://bedtools.readthedocs.io/en/latest/
RUN cd /usr/local/bin && wget -q https://github.com/arq5x/bedtools2/releases/download/v2.28.0/bedtools && chmod +x /usr/local/bin/bedtools

#HTSlib/tabix: got from here: http://www.htslib.org/download/
RUN mkdir -p /usr/local/htslib && cd /usr/local/htslib && wget -q https://github.com/samtools/htslib/releases/download/1.9/htslib-1.9.tar.bz2 && tar -vxjf htslib-1.9.tar.bz2 && cd htslib-1.9 && ./configure --prefix=/usr/local && make && make install

#Beagle: got from here: http://faculty.washington.edu/browning/beagle/beagle.html
RUN mkdir -p /usr/local/Beagle && cd /usr/local/Beagle && wget -q http://faculty.washington.edu/browning/beagle/beagle.28Sep18.793.jar && wget -q http://faculty.washington.edu/browning/beagle/run.beagle.28Sep18.793.example && chmod +x run.beagle.28Sep18.793.example

RUN pip install -Iv scipy==1.2

#MetaXcan: got from here: https://github.com/hakyimlab/MetaXcan
RUN mkdir -p /usr/local/metaxcan && cd /usr/local/metaxcan && git clone https://github.com/hakyimlab/MetaXcan && cd MetaXcan/software && python setup.py install

#new-fugue (recommended prereq for locuszoom):
RUN cd /tmp/ && wget -q http://www.sph.umich.edu/csg/abecasis/downloads/generic-new_fugue-2010-06-02.tar.gz && tar -zxvf generic-new_fugue-2010-06-02.tar.gz && cd generic-new_fugue && make all && make install

#locuszoom, program only
RUN cd /usr/local && wget https://statgen.sph.umich.edu/locuszoom/download/locuszoom_1.4_srconly.tgz && tar xvfz locuszoom_1.4_srconly.tgz && cd /usr/local/bin && ln -s /usr/local/locuszoom/bin/locuszoom .

#Install s3fs, see here for what I did: http://www.whiteboardcoder.com/2017/12/how-to-mount-s3-bucket-as-hard-drive.html
#Note that you need to start the Docker container in --privileged mode in order to run s3fs (basically similar options as you need for sshfs I think)
#See here: https://github.com/s3fs-fuse/s3fs-fuse/issues/647
RUN apt-get update && apt-get install -y --fix-missing automake autotools-dev fuse g++ git libcurl4-gnutls-dev libfuse-dev libssl-dev libxml2-dev make pkg-config

RUN cd /tmp/ && git clone https://github.com/s3fs-fuse/s3fs-fuse.git && cd s3fs-fuse && \
    ./autogen.sh && ./configure && make && make install

#Setup mount point for EFS volume that stores UKB data
#Once a container is started, mount with this command:
#sudo mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport fs-352a06d5.efs.us-east-1.amazonaws.com:/ /efs/ukb-storage
#although you will have to change us-east-1 to the AWS region you are in if different
ADD mount_ukb.pl /tmp
ADD mount_ukb.sh /tmp
RUN apt-get install -y nfs-common && mkdir -p /efs/ukb-storage && chown domino:domino /efs/ukb-storage && chmod 777 /efs/ukb-storage && chmod +x /tmp/mount_ukb.pl && chmod +x /tmp/mount_ukb.sh

###Install SAIGE

RUN R -e 'install.packages(c("R.utils", "Rcpp", "RcppParallel", "RcppArmadillo", "data.table", "RcppEigen", "Matrix", "methods", "BH", "optparse", "SPAtest"), repos="http://cran.us.r-project.org")' && wget -q https://github.com/weizhouUMICH/SAIGE/releases/download/v0.29.5/SAIGE_0.29.5_R_x86_64-pc-linux-gnu.tar.gz && R CMD INSTALL SAIGE_0.29.5_R_x86_64-pc-linux-gnu.tar.gz

#RUN git clone https://github.com/weizhouUMICH/SAIGE.git && Rscript SAIGE/extdata/install_packages.R && wget -q https://github.com/weizhouUMICH/SAIGE/releases/download/v0.29.5/SAIGE_0.29.5_R_x86_64-pc-linux-gnu.tar.gz && R CMD INSTALL SAIGE_0.29.5_R_x86_64-pc-linux-gnu.tar.gz
