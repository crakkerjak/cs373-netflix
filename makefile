EID := cat3263

FILES :=                   							 \
    .travis.yml                      		 \
    netflix-tests/$(EID)-RunNetflix.in   \
    netflix-tests/$(EID)-RunNetflix.out  \
    netflix-tests/$(EID)-TestNetflix.out \
    netflix-tests/$(EID)-TestNetflix.py  \
    Netflix.html                      	 \
    Netflix.log                      		 \
    Netflix.py                        	 \
    RunNetflix.in                     	 \
    RunNetflix.out                    	 \
    RunNetflix.py                     	 \
    TestNetflix.out                   	 \
    TestNetflix.py

check:
	@not_found=0;                                 	\
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -f  RunNetflix.tmp
	rm -f  TestNetflix.tmp
	rm -rf __pycache__

config:
	git config -l

scrub:
	make clean
	rm -f  Netflix.html
	rm -f  Netflix.log
	rm -rf netflix-tests

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

test: RunNetflix.tmp TestNetflix.tmp

netflix-tests:
	git clone https://github.com/cs373-spring-2016/netflix-tests.git

Netflix.html: Netflix.py
	pydoc3 -w Netflix

Netflix.log:
	git log > Netflix.log

RunNetflix.tmp: RunNetflix.in RunNetflix.out RunNetflix.py
	./RunNetflix.py < RunNetflix.in > RunNetflix.tmp
	# diff RunNetflix.tmp RunNetflix.out

TestNetflix.tmp: TestNetflix.py
	coverage3 run    --branch TestNetflix.py >  TestNetflix.tmp 2>&1
	coverage3 report -m --omit='/lusr/lib/python3.4/site-packages/*' >> TestNetflix.tmp
	cat TestNetflix.tmp
