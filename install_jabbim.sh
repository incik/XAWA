sudo apt-get install subversion pyqt4-dev-tools python-configobj python-twisted-words python-twisted-names python-twisted-web
svn co svn://dev.jabbim.cz/jabbim/trunk jabbim
wget https://github.com/incik/XAWA/zipball/master --no-check-certificate -O xawa.zip
unzip xawa.zip
mkdir jabbim/src/plugins/xawa
cp -r incik-XAWA-*/plugins/jabbim/xawa/ jabbim/src/plugins/
