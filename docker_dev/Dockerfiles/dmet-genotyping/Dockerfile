FROM ubuntu:16.04

USER root

# Set up Environment
ENV http_proxy http://proxy-server.pri.bms.com:8080
ENV https_proxy http://proxy-server.pri.bms.com:8080
ENV ftp_proxy http://proxy-server.pri.bms.com:8080
ENV no_proxy bms.com,localhost
#ENV no_proxy s3.amazonaws.com,bms.com,localhost,169.254.169.254 ###this causes some wget ops to fail, go into endless redirect loop

#### Utilities ####

RUN \
    # Create a domino user and give sudoer privs
    groupadd -g 12574 domino && \
    useradd -u 12574 -g 12574 -m -N -s /bin/bash domino && \
    #echo "domino ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    adduser domino sudo && \

    # UPDATE, UPGRADE, ADD repositories
    apt-get update -y && \
    apt-get -y install python-software-properties software-properties-common && \
    add-apt-repository -y ppa:git-core/ppa && \
    apt-get update -y && \
    apt-get -y install git && \
    add-apt-repository -y ppa:webupd8team/java && \
    apt-get -y upgrade && \
    add-apt-repository -y ppa:linuxuprising/java && \
    apt-get -y -q update && \
    #apt-get -y -q install oracle-java10-installer && \
    #apt install oracle-java10-set-default && \

    # CONFIGURE locales
    apt-get install -y locales && \
    locale-gen en_US.UTF-8 && \
    dpkg-reconfigure locales

RUN \
    # INSTALL common
    apt-get -y install build-essential cmake python3-dev wget sudo curl apt-utils net-tools libzmq3-dev ed git openssh-server  && \
    apt-get -y install openjdk-8-jdk && \
    #echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections && \
    apt-get -y -q install libaio1 && \
    apt-get -y install vim nano

RUN \  
    apt-get -y install htop bmon slurm tcptrack iftop nethogs qpdf && \
    apt-get -y install alien screen tmux sshfs libpoppler-cpp-dev && \
    apt-get -y install emacs24-nox ess libv8-3.14-dev texlive-xetex 

RUN apt-get -y install libpng12-dev

RUN \
    apt-get -y -f install imagemagick libmagick++-dev libmagickcore-6.q16-dev libmagickwand-6.q16-dev libmagick++-6.q16-dev libfreetype6-dev librsvg2-dev libwmf-dev libgdk-pixbuf2.0-dev libcairo2-dev

RUN apt-get -y install libpng16-devtools
RUN apt-get -y install libpng16-dev


RUN \
    apt-get -y install dos2unix && \
    apt-get -y install libnlopt0 libnlopt-dev && \
    apt-get -y install manpages manpages-dev freebsd-manpages funny-manpages man2html asr-manpages && \
    apt-get -y install cifs-utils  && \
    apt-get -y install libfontconfig1-dev libfreetype6-dev libpng-dev  && \
    apt-get -y install libhdf5-dev && \
    apt-get -y install libpq-dev && \
    apt-get -y install libmysqlclient-dev libgdal-dev libgdal1-dev libgdal1i libproj-dev nano #&& \
    #gpasswd -a domino fuse

    #RUN \
    #  DEBIAN_FRONTEND=noninteractive apt-get -y install heirloom-mailx postfix && \
    #  sed 's/^relayhost/\# relayhost/' /etc/postfix/main.cf >> /tmp/main.cf && \
    #  echo 'myorigin = $myhostname' >> /tmp/main.cf && \
    #  echo 'relayhost = mailhost.bms.com' >> /tmp/main.cf && \
    #  mv /etc/postfix/main.cf /etc/postfix/main.cf.sav && \
    #  mv /tmp/main.cf /etc/postfix/main.cf

    RUN \
    # ADD SSH start script
    mkdir -p /scripts && \
    printf "#!/bin/bash\\nservice ssh start\\n" > /scripts/start-ssh && \
    chmod +x /scripts/start-ssh && \
    echo 'export PYTHONIOENCODING=utf-8' >> /home/domino/.domino-defaults && \
    echo 'export LANG=en_US.UTF-8' >> /home/domino/.domino-defaults && \
    echo 'export JOBLIB_TEMP_FOLDER=/tmp' >> /home/domino/.domino-defaults && \
    echo 'export LC_ALL=en_US.UTF-8' >> /home/domino/.domino-defaults

# Set locale
RUN \
    echo "EST" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    echo 'LANG="en_US.UTF-8"'>/etc/default/locale && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8

# Oracle client
RUN \
    wget --quiet -O /tmp/oracle-instantclient.rpm https://s3-us-west-2.amazonaws.com/domino-operations/mirror/oracle-instantclient12.1-basic-12.1.0.2.0-1.x86_64.rpm && \
    wget --quiet -O /tmp/oracle-instantclient-devel.rpm https://s3-us-west-2.amazonaws.com/domino-operations/mirror/oracle-instantclient12.1-devel-12.1.0.2.0-1.x86_64.rpm && \
    alien -i /tmp/oracle-instantclient.rpm && \
    alien -i /tmp/oracle-instantclient-devel.rpm && \
    rm -rf /tmp/oracle-instantclient.rpm && \
    rm -rf /tmp/oracle-instantclient-devel.rpm && \
    echo "/usr/lib/oracle/12.1/client64/lib" > /etc/ld.so.conf.d/oracle.conf && \
    ldconfig

#Install R
RUN \
    gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys E084DAB9 && \
    gpg -a --export E084DAB9 | sudo apt-key add - && \
    echo "deb http://cran.rstudio.com/bin/linux/ubuntu xenial-cran35/" | sudo tee -a /etc/apt/sources.list && \
    apt-get update -y && \
    apt-get install r-base-core=3.5* --force-yes -y && \
    # INSTALL R packages dependencies
    apt-get -y install libssl-dev libxml2-dev libxt-dev libssh2-1-dev libcurl4-openssl-dev libsasl2-dev libssl-dev && \
    # INSTALL R packages required by Domino
    R -e 'options(repos=structure(c(CRAN="http://cran.us.r-project.org"))); install.packages(c( "devtools","jsonlite","lubridate","Rcpp"))' && \
    #dependencies of various R packages
    apt-get update && \
    apt-get install -y libcairo2-dev  libxt-dev libgmp3-dev jags libgsl0-dev libx11-dev mesa-common-dev libglu1-mesa-dev libmpfr-dev libfftw3-dev libtiff5-dev libiodbc2-dev && \
    #required for rJava
    export LD_LIBRARY_PATH=/usr/lib/jvm/java-8-oracle/jre/lib/amd64/server && \
    R CMD javareconf && \
    echo 'export LD_LIBRARY_PATH=/usr/lib/jvm/java-8-oracle/jre/lib/amd64/server:${LD_LIBRARY_PATH:-}' >> /home/domino/.domino-defaults

#install R dplyr
RUN \
    R -e 'install.packages(c("dplyr", "tidyr", "openxlsx"), repos=c("http://bran.pri.bms.com", "http://cran.us.r-project.org"))'

# ROracle
RUN \
    wget --quiet -O /tmp/ROracle_1.3-1.tar.gz https://cran.r-project.org/src/contrib/ROracle_1.3-1.tar.gz && \
    wget --quiet -O /tmp/DBI_1.0.0.tar.gz https://cran.r-project.org/src/contrib/DBI_1.0.0.tar.gz && \
    export OCI_LIB=/usr/lib/oracle/12.1/client64/lib && \
    export OCI_INC=/usr/include/oracle/12.1/client64 && \
    #export PATH=/opt/oracle/instantclient_12_1:${PATH:-} && \
    #export LD_LIBRARY_PATH=/opt/oracle/instantclient_12_1:${LD_LIBRARY_PATH:-} && \
    R CMD INSTALL /tmp/DBI_1.0.0.tar.gz && \
    R CMD INSTALL --configure-args='--with-oci-lib=/usr/lib/oracle/12.1/client64/lib --with-oci-inc=/usr/include/oracle/12.1/client64' /tmp/ROracle_1.3-1.tar.gz && \
    rm -rf /tmp/DBI_1.0.0.tar.gz && \
    rm -rf /tmp/ROracle_1.3-1.tar.gz && \
    R -e 'install.packages(c("ROracle"), repos="http://cran.us.r-project.org")'

# Update Bioconductor Packages
# RUN \
#     R -e 'if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager"); BiocManager::install(c("affy","AnnotationDbi","Biobase","biobroom","BiocGenerics","biomaRt","Biostrings","bumphunter","ComplexHeatmap","DECIPHER","edgeR","EGSEA","EGSEAdata","EnsDb.Hsapiens.v86","EnsDb.Hsapiens.v75","GenomicRanges","GenomicFeatures","GenomicAlignments","GEOquery","GSEABase","GSVA","hgu95av2.db","hgu133plus2.db","IHW","IlluminaHumanMethylation450kanno.ilmn12.hg19","IRanges","JunctionSeq","KEGGREST","limma","lpsymphony","lumi","oligo","org.Hs.eg.db","org.Mm.eg.db","org.Rn.eg.db","OSAT","pathview","piano","plotROC","preprocessCore","pvca","qvalue","readat","Rgraphviz","RNASeqPower","rtracklayer","S4Vectors","survcomp","sva","scde","splatter","scater","singscore","SummarizedExperiment","TCGAbiolinks","variancePartition","XVector"), version = "3.8")'

# # Individual GitHub Packages
# RUN \
#     R -e 'options(repos = setNames(c("http://bran.pri.bms.com", "http://cran.cnr.berkeley.edu"), c("BRAN", "CRAN"))); devtools::install_github("ronammar/zFPKM"); devtools::install_github("stephenturner/annotables"); remotes::install_github("r-lib/remotes"); devtools::install_github("yihui/printr"); devtools::install_github("dgJacks0n/envDocument/envDocument");' && \
#     chown -R domino:domino /home/domino

# # The following R packages depend on BioConductor packages, so they must wait to be installed until after BioConductor packages
# RUN \
#     R -e 'source("http://bran.pri.bms.com/resources/configureRepo.R"); install.packages(c("WGCNA"), quiet=TRUE)' && \
#     chown -R domino:domino /usr/lib/R/library

# # BRAN packages
# RUN \
#     R -e 'source("http://bran.pri.bms.com/resources/configureRepo.R"); install.packages(c("AnnotatedMatrix","ArrayServer","bmsgsa","bmsTbioTemplate","DGEobj","DGE.Tools2","JRTutil","metabaser","purrPull","pvcaMod","rXpress","SiteMinderBMS","TBioTemplate","Xpress2R")); install.packages(c("BMS.PathwayTools","dynamictable","edgeRun","estimate","imputeLCMD","jackstraw","myRepository","periscope.bms","setfisher","VAN","Xpress2RSE"))' && \
#     chown -R domino:domino /usr/lib/R/library

# RUN \
#     R -e 'source("http://bran.pri.bms.com/resources/configureRepo.R"); install.packages(c("CompQuadForm","CBDD","CBDDnetworks","ndexr")); install.packages("CBDDbenchmarks", repos="http://bran.pri.bms.com/XRAN"); devtools::install_github(repo = "sahirbhatnagar/sail")'

# RUN \
#     R -e 'install.packages(c("mixtools","rlang","table1","ModelGood","simr","ggsci","glmnetcr","pathwaze","ggsignif","janitor","visdat","MVN","pacman","fastDummies","fuzzyjoin","coop","ggforce","poibin","lmerTest","dbscan","PropCIs","Rmagic","pdist","densityClust","egg","forestplot","beeswarm","kableExtra","dunn.test","mcr","BMS.PathwayTools","tumgr","cubature","directlabels","gghighlight","venneuler","poweRlaw","rcompanion","coxphw","reticulate","umap","brms","cowplot","gmodels","survMisc","simPH","ggExtra","ggcorrplot","plot3D","samplesizeCMH","descr","randomizr","pspline","kader","rstan","bmsgsa2","iheatmapr","arsenal","sjmisc","ggeffects","mRMRe","clinfun","gginnards","Greg","AlgDesign","MatchIt","ggvis","tableone","conflicted","shinyjs","phia","effects","powerMediation","simpleboot","colorRamps","poisbinom","ggpmisc","sjPlot","truncdist","useful","epiR","sjlabelled","vcfR","glue","gcookbook","gganimate","ggpubr"), quiet=TRUE, repos=c("http://bran.pri.bms.com", "http://cran.us.r-project.org"));'

RUN \
    chown -R domino:domino /home/domino && \
    chown -R domino:domino /usr/local/lib/R/site-library

# Install WuXi NextCode tools
# RUN \
#   cd /opt && \
#   wget --quiet -O /opt/sm-clients-dist-5.24.7.zip https://s3.amazonaws.com/bmsrd-ngs-61534/outgoing/resources/sm-clients-dist-5.24.7.zip && \
#   unzip -o -q sm-clients-dist-5.24.7.zip && \
#   echo 'export PATH=${PATH:-}:/opt/sm-clients-dist-5.24.7/bin' >> /home/domino/.domino-defaults && \
#   rm -f sm-clients-dist-5.24.7.zip

# RUN \
#   add-apt-repository -y ppa:jonathonf/gcc-7.1 && \
#   apt-get update -y && \
#   apt-get -y install gcc-7 g++-7 && \
#   apt-get -y install gfortran-7 && \
#   R -e 'install.packages(c("igraph","huge"), quiet=TRUE, repos="http://cran.us.r-project.org")' && \
#   chown -R domino:domino /usr/lib/R/library

#RUN cd /tmp/ && wget https://s3.amazonaws.com/hdf-wordpress-1/wp-content/uploads/manual/HDF5/HDF5_1_10_4/hdf5-1.10.4.tar.gz && tar xvfz hdf5-1.10.4.tar.gz && cd hdf5-1.10.4 && ./configure && make && make check && make install 
# RUN \
#     R -e 'devtools::install_github(repo = "dviraran/SingleR")' 
# # && R -e 'install.packages("bmsshinyfw.report", repos="http://bran.pri.bms.com")'

RUN mkdir -p /home/domino/.ssh && ssh-keyscan -H biogit.pri.bms.com >> /home/domino/.ssh/known_hosts && chown -R domino:domino /home/domino/.ssh

#### Install drivers for common data source connections #####

#Database drivers
#SQL 
RUN \
    # apt-get -y -q install vpnc && \
    apt-get update -y && apt-get install tdsodbc -y && \
    apt-get -y remove libodbc1 unixodbc unixodbc-dev freetds-common freetds-dev

# RUN \
#   cd /tmp && \
#   wget http://ftp.osuosl.org/pub/blfs/conglomeration/unixODBC/unixODBC-2.3.4.tar.gz && \
#   tar -xf unixODBC-2.3.4.tar.gz && \
#   cd unixODBC-2.3.4 && \
#   ./configure --enable-gui=no --enable-drivers=no --enable-iconv --with-iconv-char-enc=UTF8 --with-iconv-ucode-enc=UTF16LE --libdir=/usr/lib/x86_64-linux-gnu --prefix=/usr --sysconfdir=/etc --enable-stats=no && \
#   make && \
#   make install && \
#   ln -s /lib/x86_64-linux-gnu/libssl.so.1.0.0 /lib/x86_64-linux-gnu/libssl.so.10 && \
#   ln -s /lib/x86_64-linux-gnu/libcrypto.so.1.0.0 /lib/x86_64-linux-gnu/libcrypto.so.10 && \
#   ldconfig
# #  rm -rf /tmp/*

# Python
RUN \
    apt-get update && \
    apt-get -y install python-pip && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get -y install python3.6 && \
    apt-get -y install python3-pip

#Oracle instantclient
RUN \
    mkdir -p /opt/oracle && \
    wget https://s3-us-west-2.amazonaws.com/domino-deployment/2016/02/22/instantclient-basic-linux.x64-12.1.0.2.0.zip -O /opt/oracle/instantclient-basic-linux.x64-12.1.0.2.0.zip && \
    wget https://s3-us-west-2.amazonaws.com/domino-deployment/2016/02/22/instantclient-sdk-linux.x64-12.1.0.2.0.zip -O /opt/oracle/instantclient-sdk-linux.x64-12.1.0.2.0.zip && \
    mkdir -p /opt/oracle/instantclient_12_1 && \
    cd /opt/oracle && \
    unzip instantclient-basic-linux.x64-12.1.0.2.0.zip && \
    unzip instantclient-sdk-linux.x64-12.1.0.2.0.zip && \
    cd /opt/oracle/instantclient_12_1 && \
    ln -s libclntsh.so.12.1 libclntsh.so && \
    ln -s libocci.so.12.1 libocci.so && \
    echo "export LD_LIBRARY_PATH=/opt/oracle/instantclient_12_1:\${LD_LIBRARY_PATH:-}" >> /home/domino/.domino-defaults && \
    echo "export PATH=/opt/oracle/instantclient_12_1:\${PATH:-}" >> /home/domino/.domino-defaults && \
    export PATH=/opt/oracle/instantclient_12_1:${PATH:-} && \
    export LD_LIBRARY_PATH=/opt/oracle/instantclient_12_1:${LD_LIBRARY_PATH:-}

RUN \
    chown -R domino:domino /home/domino

#Install PostgreSQL client
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN apt-get update && apt-get -y -q install python-software-properties software-properties-common && apt-get -y -q install postgresql-9.3 postgresql-client-9.3 postgresql-contrib-9.3

#### Julia ####
# #install Julia
# RUN \
#     cd /home/domino && \
#     wget https://julialang-s3.julialang.org/bin/linux/x64/0.6/julia-0.6.2-linux-x86_64.tar.gz && \
#     tar xzf julia-0.6.2-linux-x86_64.tar.gz && \
#     chmod +x julia-d386e40c17 && \
#     chown -R domino:domino julia-d386e40c17/ && \
#     ln -s /home/domino/julia-d386e40c17/bin/julia /usr/bin/julia && \
#     rm -rf julia-0.6.2-linux-x86_64.tar.gz

# #add Julia to Jupyter
# User domino 
# RUN julia -e 'Pkg.update(); Pkg.add("IJulia")'
# USER root

# # Install Node.js
# RUN \
# apt-get update && \
# apt-get install nodejs -y

#### Installing Notebooks,Workspaces,IDEs,etc ####

#Clone in workspaces install scripts
RUN mkdir /var/opt/workspaces

RUN \
    cd /tmp && wget https://github.com/dominodatalab/workspace-configs/archive/2019q1-v1.1.zip && \
    unzip 2019q1-v1.1.zip  && \
    find /tmp/workspace-configs-2019q1-v1.1 -type f | xargs perl -p -i -e 's/ubuntu/domino/g' && \
    cp -Rf /tmp/workspace-configs-2019q1-v1.1/. /var/opt/workspaces && \
    rm -rf /var/opt/workspaces/workspace-logos && rm -rf /tmp/workspace-configs-2019q1-v1.1

# Add RProfile including BRAN and update to .libPaths to include /home/domino/rLibrary
ADD https://biogit.pri.bms.com/raw/russom/domino_support/master/Genomics%202019-03/Rprofile.txt /home/domino/.Rprofile
RUN chown domino:domino /home/domino/.Rprofile

# # # #Install Rstudio from workspaces
RUN chmod +x /var/opt/workspaces/rstudio/install
RUN /var/opt/workspaces/rstudio/install

# # #Install Jupyter and Jupyterlab from workspaces
RUN \
    mv /usr/bin/pip /usr/bin/pip2 && \
    ln -s /usr/bin/pip3 /usr/bin/pip && \
    chmod +x /var/opt/workspaces/jupyter/install && \
    /var/opt/workspaces/jupyter/install && \
    /var/opt/workspaces/Jupyterlab/install && \
    rm /usr/bin/pip && \
    ln -s /usr/bin/pip2 /usr/bin/pip

# Add BMS-specific utilities
RUN \
    wget --quiet -O /usr/local/bin/smount https://biogit.pri.bms.com/raw/russom/domino_support/master/smount/smount.py && \
    wget --quiet -O /usr/local/bin/sumount https://biogit.pri.bms.com/raw/russom/domino_support/master/smount/sumount.py && \
    wget --quiet -O /usr/local/bin/dmount https://biogit.pri.bms.com/raw/russom/domino_support/master/smount/dmount.py && \
    wget --quiet -O /usr/local/bin/dumount https://biogit.pri.bms.com/raw/russom/domino_support/master/smount/dumount.py && \
    wget --quiet -O /usr/local/bin/load-settings https://biogit.pri.bms.com/raw/russom/domino_support/master/Genomics%202019-03/load-settings.py && \
    wget --quiet -O /usr/local/bin/save-settings https://biogit.pri.bms.com/raw/russom/domino_support/master/Genomics%202019-03/save-settings.py && \
    wget --quiet -O /usr/local/bin/stash https://biogit.pri.bms.com/raw/russom/stash-cli/master/stash.py && \
    chmod 755 /usr/local/bin/load-settings && \
    chmod 755 /usr/local/bin/save-settings && \
    chmod 755 /usr/local/bin/smount && \
    chmod 755 /usr/local/bin/sumount && \
    chmod 755 /usr/local/bin/dmount && \
    chmod 755 /usr/local/bin/dumount && \
    chmod 755 /usr/local/bin/stash && \
    chown -R domino:domino /usr/lib/R/library

# Give sudo to domino
RUN   echo "domino ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Set some environment variables
RUN \
    echo "export R_ZIPCMD=/usr/bin/zip" >> /home/domino/.domino-defaults && \
    echo "export https_proxy=https://proxy-server.bms.com:8080" >> /home/domino/.domino-defaults && \
    echo "export http_proxy=http://proxy-server.bms.com:8080" >> /home/domino/.domino-defaults && \
    echo "export NO_PROXY=s3.amazonaws.com,bms.com,localhost,169.254.169.254" >> /home/domino/.domino-defaults

RUN groupadd -g 9500 bioinfo

RUN \
    apt-get -y install passwd supervisor && \
    mkdir -p /var/log/supervisor && mkdir -p /etc/supervisor/conf.d && mkdir -p /var/run/sshd

ADD ./start.sh /start.sh
ADD ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN yes y | ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N '' 
RUN chmod 755 /start.sh
EXPOSE 80 22 8787
RUN ./start.sh

###id_rsa.pub should be the apache (or whatever user is running Apache) user's public ssh key (e.g. generated by ssh-keygen -t rsa)
###Below enables apache user to run commands inside the running Docker container without entering
###a password (i.e. just using ssh keys). E.g. to mount /stash and user home dir with sshfs.
###See these 2 links for how to enable passwordless ssh via ssh-keygen:
###https://www.tecmint.com/ssh-passwordless-login-using-ssh-keygen-in-5-easy-steps/
###http://www.linuxproblem.org/art_9.html
RUN mkdir -p /home/rr_user/.ssh
ADD id_rsa.pub /home/rr_user/.ssh/id_rsa.pub
RUN cat /home/rr_user/.ssh/id_rsa.pub >> /home/rr_user/.ssh/authorized_keys && chown -R rr_user /home/rr_user/.ssh && chgrp -R rr_user /home/rr_user/.ssh && chmod 700 /home/rr_user/.ssh && chmod 640 /home/rr_user/.ssh/authorized_keys

###Same as above, but for domino user
RUN mkdir -p /home/domino/.ssh
ADD id_rsa.pub /home/domino/.ssh/id_rsa.pub
RUN cat /home/domino/.ssh/id_rsa.pub >> /home/domino/.ssh/authorized_keys && chown -R domino /home/domino/.ssh && chgrp -R domino /home/domino/.ssh && chmod 700 /home/domino/.ssh && chmod 640 /home/domino/.ssh/authorized_keys

#Create /stash directory
RUN mkdir /stash && chown rr_user /stash && chgrp bioinfo /stash && chmod g+r /stash && chmod g+w /stash && chmod g+x /stash

###for some strange reason, rm -Rf /tmp/* fails, says "directory not empty", so I just took it out
# Clean up temporary files
RUN \
    rm -Rf /var/lib/apt/lists/* && \
    #  rm -Rf /tmp/* && chown -R domino:domino /tmp
    chown -R domino:domino /tmp

RUN chown -R rr_user:bioinfo /home/rr_user

## mount specific files 
ADD ./affymetrixpowertools /dmet/affymetrixpowertools
ADD ./results /dmet/results 
ADD ./data /dmet/data

RUN chmod 755 /dmet/affymetrixpowertools/apt-2.10.2.2-x86_64-intel-linux/bin/apt-dmet-genotype
RUN chmod 755 /dmet/affymetrixpowertools/apt-2.10.2.2-x86_64-intel-linux/bin/apt-dmet-translation

ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

