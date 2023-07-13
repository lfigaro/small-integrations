#!/bin/bash

lambda="bgg-to-bgp"

cd /Users/lfigaro/projects/boardgameplay

mkdir build
pip3 install -r requirements.txt -t build/
cp -R src/$1/* build


echo "deploying $lambda >>>>>>>>>"
cd build
zip -qr ../src.zip *
cd ../

### Create the role for the lambda to assume
role="lambda_basic_execution"
function_name="$lambda"
handler_name="main.lambda_handler"
package_file=./src.zip

### Update the function
runtime=python2.7
aws lambda update-function-code \
  --function-name $function_name \
  --zip-file fileb://$package_file \
  --region us-east-1


rm src.zip
rm -rf build

cd html
aws s3 cp . s3://bgpweb --recursive --exclude "src/*" --exclude "*/.DS_Store" --exclude ".DS_Store"

echo 'End of the deploy >>>>>>>>>'