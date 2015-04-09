:: If pyrcc complain of "No resources in resource description", remove from
:: qt_resources.qrc any tag besides the <RCC> tree, including comments.
pyrcc4 ../qt/qt_resources.qrc -o ../animetorr/manager/qt/qt_resources_rc.py
::pyuic is a .bat file, therefore must use 'call'
call pyuic4 ../qt/qt_main.ui -o ../animetorr/manager/qt/main.py
call pyuic4 ../qt/qt_about.ui -o ../animetorr/manager/qt/about.py
call pyuic4 ../qt/qt_log.ui -o ../animetorr/manager/qt/log.py
call pyuic4 ../qt/qt_options.ui -o ../animetorr/manager/qt/options.py
call pyuic4 ../qt/qt_add.ui -o ../animetorr/manager/qt/add.py