#!/bin/bash

docs_dir=docs/coverage
pwd
cd src/newenv/horseshow-proj
coverage run --source='.' manage.py test show
coverage report > $docs_dir/coverage_report
coverage html 
rm -rf $docs_dir/htmlcov
mv htmlcov $docs_dir